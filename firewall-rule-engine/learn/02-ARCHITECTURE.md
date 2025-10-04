# Architecture

## System Overview

The tool reads a raw ruleset file (iptables-save or nft list ruleset output), converts it into an internal representation, and then does one of several things with it depending on which subcommand you ran. Here is the full picture:

```
                         ┌──────────────┐
                         │  Raw Ruleset │
                         │    (file)    │
                         └──────┬───────┘
                                │
                         ┌──────▼───────┐
                         │ detect_format│
                         └──────┬───────┘
                                │
                 ┌──────────────┼──────────────┐
                 │                             │
          ┌──────▼───────┐              ┌──────▼───────┐
          │parse_iptables│              │parse_nftables│
          └──────┬───────┘              └──────┬───────┘
                 │                             │
                 └──────────────┬──────────────┘
                                │
                         ┌──────▼───────┐
                         │   Ruleset    │
                         │ (internal)   │
                         └──────┬───────┘
                                │
          ┌─────────┬───────────┼───────────┬──────────┐
          │         │           │           │          │
   ┌──────▼──┐ ┌───▼────┐ ┌───▼────┐ ┌────▼───┐ ┌───▼────┐
   │ display │ │analyze │ │optimize│ │ export │ │  diff  │
   │  table  │ │conflict│ │suggest │ │ruleset │ │compare │
   └─────────┘ └───┬────┘ └───┬────┘ └────┬───┘ └───┬────┘
                   │           │           │         │
            ┌──────▼───────────▼──┐   ┌────▼───┐ ┌──▼─────┐
            │   print_findings    │   │ string │ │print_  │
            └─────────────────────┘   │ output │ │ diff   │
                                      └────────┘ └────────┘
```

Each CLI subcommand maps to a function in `main.v` that calls into one or more modules. No subcommand touches more than two or three modules. The `harden` command is the exception: it skips the parser entirely and goes straight to the generator.

| Command    | Modules used                       |
|------------|------------------------------------|
| `load`     | parser, display                    |
| `analyze`  | parser, analyzer, display          |
| `optimize` | parser, analyzer, display          |
| `harden`   | generator, display (banner only)   |
| `export`   | parser, generator                  |
| `diff`     | parser, display                    |


## Module Layout

In V, every directory under `src/` is a module. The module name matches the directory name. Files inside a module share the same namespace automatically, so `common.v`, `iptables.v`, and `nftables.v` all belong to `module parser` and can call each other's functions directly.

```
src/
├── main.v          (module main)
├── config/
│   └── config.v    (module config)
├── models/
│   └── models.v    (module models)
├── parser/
│   ├── common.v    (module parser)
│   ├── iptables.v  (module parser)
│   └── nftables.v  (module parser)
├── analyzer/
│   ├── conflict.v  (module analyzer)
│   └── optimizer.v (module analyzer)
├── generator/
│   └── generator.v (module generator)
└── display/
    └── display.v   (module display)
```

The dependency graph:

```
                        ┌──────┐
                        │ main │
                        └──┬───┘
                           │
          ┌────────┬───────┼────────┬──────────┐
          │        │       │        │          │
      ┌───▼──┐ ┌──▼───┐ ┌─▼──┐ ┌──▼────┐ ┌───▼───┐
      │parser│ │analyz.│ │gen.│ │display│ │config │
      └──┬───┘ └──┬───┘ └─┬──┘ └──┬────┘ └───────┘
         │        │       │       │
         │     ┌──▼───┐   │    ┌──▼───┐
         ├────►│models │◄──┘   │models│
         │     └──┬───┘        └──┬───┘
         │        │               │
         ▼        ▼               ▼
      ┌──────┐ ┌──────┐       ┌──────┐
      │config│ │config│       │config│
      └──────┘ └──────┘       └──────┘
```

Three things to notice:

- `config` and `models` are leaf modules. They import nothing from the project.
- `parser`, `analyzer`, `generator`, and `display` never import each other. Zero cross-dependencies.
- `main` is the only module that imports everything. It is the composition root.

This means you can rewrite the entire nftables parser without touching the analyzer, or overhaul the display layer without the generator knowing. V enforces no circular imports at compile time, so this structure cannot accidentally degrade.


## Data Flow

### `load` command

```
fwrule load testdata/iptables_basic.rules

  os.read_file(path)
       │
       ▼
  detect_format(content)  ──►  RuleSource.iptables
       │
       ▼
  parse_iptables(content)
       │
       ├── iterate lines
       ├── "*filter"         → set current_table = .filter
       ├── ":INPUT DROP"     → policies["INPUT"] = .drop
       ├── "-A INPUT ..."    → tokenize → parse flags → Rule
       │
       ▼
  Ruleset { rules: [...], policies: {...}, source: .iptables }
       │
       ├── display.print_banner()
       ├── display.print_summary(rs)
       └── display.print_rule_table(rs)
```

`load_ruleset` in `main.v` reads the file, auto-detects the format, and dispatches to the right parser. The resulting `Ruleset` goes to the display module for rendering.

### `analyze` command

```
fwrule analyze testdata/iptables_conflicts.rules

  load_ruleset(path)  ──►  Ruleset
       │
       ├── analyzer.analyze_conflicts(rs)
       │       │
       │       ├── rs.rules_by_chain()  →  map[string][]int
       │       │
       │       └── for each chain:
       │              find_duplicates(rules, indices)
       │              find_shadowed_rules(rules, indices)
       │              find_contradictions(rules, indices)
       │              find_redundant_rules(rules, indices)
       │       │
       │       └──►  []Finding
       │
       ├── analyzer.suggest_optimizations(rs)
       │       │
       │       └── for each chain:
       │              find_mergeable_ports(rules, indices)
       │              suggest_reordering(rules, indices)
       │              find_missing_rate_limits(rules, indices)
       │              find_missing_conntrack(rules, indices)
       │       │
       │       └── find_missing_logging(rs)  (whole-ruleset check)
       │       │
       │       └──►  []Finding
       │
       └── display.print_findings(conflicts)
           display.print_findings(optimizations)
```

Two passes: conflict detection (things that are broken) then optimization analysis (things that could be better). Both return `[]Finding` that the display module renders with severity coloring.

### `harden` command

```
fwrule harden -s ssh,http,https -f nftables

  flag.new_flag_parser(args)
       │
       ├── services = ["ssh", "http", "https"]
       ├── iface = "eth0", format = nftables
       │
       ▼
  generator.generate_hardened(services, iface, .nftables)
       │
       ├── default-deny policy → loopback accept → conntrack
       ├── anti-spoofing (RFC 1918 on public iface)
       ├── ICMP rate-limited
       ├── per-service rules from config.service_ports
       ├── drop logging → final drop
       │
       └──►  string (printed to stdout)
```

This is the only command that does not parse a file. It builds a ruleset from scratch using templates and the service-to-port mapping from `config.v`.

### `export` command

```
fwrule export testdata/iptables_basic.rules -f nftables

  load_ruleset(path)  ──►  Ruleset (source: .iptables)
       │
       ▼
  generator.export_ruleset(rs, .nftables)
       │
       ├── group rules by table
       ├── for each chain: header + policy, then rule_to_nftables per rule
       │
       └──►  string (printed to stdout)
```

Each `Rule` struct carries enough information to be serialized into either format. The `rule_to_iptables` and `rule_to_nftables` functions read fields off the struct and reconstruct the target syntax.

### `diff` command

```
fwrule diff old.rules new.rules

  load_ruleset(path1)  ──►  Ruleset (left)
  load_ruleset(path2)  ──►  Ruleset (right)
       │
       ▼
  display.print_diff(left, right)
       │
       ├── build_rule_set(rules)  →  map[string]bool  (both sides)
       ├── keys in left but not right → "only in left"
       ├── keys in right but not left → "only in right"
       └── no differences → "Rulesets are equivalent"
```

The diff normalizes every rule to a canonical string via `Rule.str()` and compares sets. It compares semantic content, not raw text, so an iptables rule and an nftables rule expressing the same policy show as equivalent.


## Core Types

All types live in `src/models/models.v`. The parser produces them, the analyzer inspects them, the generator and display modules consume them.

### Ruleset

```
Ruleset {
    rules    []Rule              ordered list of all parsed rules
    policies map[string]Action   chain name → default action ("INPUT" → .drop)
    source   RuleSource          iptables or nftables
}
```

The top-level container. `rules` is ordered by position in the original file. `policies` maps chain names to their default actions. The `rules_by_chain()` method groups rule indices by chain name so the analyzer can restrict comparisons to within a single chain.

### Rule

```
Rule {
    table       Table            filter, nat, mangle, raw, security
    chain       string           "INPUT", "FORWARD", or custom name
    chain_type  ChainType        parsed enum for known chains
    action      Action           accept, drop, reject, log, masquerade, ...
    criteria    MatchCriteria    all match conditions (see below)
    target_args string           extra args after -j (e.g., --log-prefix "...")
    line_number int              original line number in source file
    raw_text    string           unparsed original line
    source      RuleSource       which format this rule came from
}
```

Whether the input was iptables or nftables, every parsed rule becomes this same struct. `chain_type` defaults to `.custom` for user-defined chains. `line_number` and `raw_text` survive the parse so that findings can reference back to the original file.

### MatchCriteria

```
MatchCriteria {
    protocol    Protocol         default: .all (matches everything)
    source      ?NetworkAddr     optional source CIDR
    destination ?NetworkAddr     optional destination CIDR
    src_ports   []PortSpec       source port ranges
    dst_ports   []PortSpec       destination port ranges
    in_iface    ?string          input interface
    out_iface   ?string          output interface
    states      ConnState        bitmask: new|established|related|invalid
    icmp_type   ?string          ICMP type string
    limit_rate  ?string          rate limit (e.g., "3/minute")
    limit_burst ?int             burst count
    comment     ?string          rule comment
}
```

This is where V's option types (`?Type`) pay off. `source ?NetworkAddr` means "this rule might or might not constrain the source address." When `none`, the rule matches any source. When set, it matches only that network. This distinction is critical for superset/subset logic: `source = none` is a superset of `source = 10.0.0.0/8`, because "match anything" contains "match this network." Without option types you could not distinguish "no constraint" from "explicitly matches 0.0.0.0/0."

### Finding

```
Finding {
    severity     Severity        info, warning, critical
    title        string          short label ("Shadowed rule detected")
    description  string          full explanation with rule numbers
    rule_indices []int           zero-based indices into Ruleset.rules
    suggestion   string          actionable fix
}
```

The output of both conflict detection and optimization analysis. `rule_indices` contains zero-based indices into `Ruleset.rules`, so the display layer can say "Rules 7, 8" without needing to hold rule objects.

### NetworkAddr and PortSpec

```
NetworkAddr {                PortSpec {
    address string               start   int
    cidr    int = 32             end     int = -1
    negated bool                 negated bool
}                            }
```

`NetworkAddr` stores an IP and prefix length. The `cidr` field defaults to 32 (a single host). The `negated` flag handles `!` prefixes in both iptables (`! -s 10.0.0.0/8`) and nftables (`ip saddr != 10.0.0.0/8`).

`PortSpec` stores a port or port range. A single port like 22 has `end = -1`, and `effective_end()` returns `start` in that case so range math works uniformly. A range like `1024:65535` has `start = 1024, end = 65535`.

`cidr_contains` and `port_range_contains` are the two containment primitives that the analyzer's entire superset/subset logic is built on.

### ConnState as a @[flag] enum

```
@[flag]
pub enum ConnState {
    new_conn       bit 0 → value 1
    established    bit 1 → value 2
    related        bit 2 → value 4
    invalid        bit 3 → value 8
    untracked      bit 4 → value 16
}
```

The `@[flag]` attribute makes this a bitfield. Each variant is a power of two, and a single `ConnState` value can represent multiple states at once. `ESTABLISHED,RELATED` is two bits set in one integer. The `set()`, `has()`, `all()`, and `is_empty()` methods are generated automatically by V.

This mirrors how the kernel's conntrack system actually works: connection states are bitmask flags, not mutually exclusive values. A packet in state `ESTABLISHED` is not also `NEW`, but a rule can match both `ESTABLISHED` and `RELATED` simultaneously. The bitfield makes subset checks in the analyzer trivial: `outer.states.all(inner.states)` is a single bitwise AND.


## Parser Design

The parser solves a two-format problem. iptables-save and nft list ruleset express the same firewall concepts but with completely different syntax.

### iptables parser (iptables.v)

iptables-save output is line-oriented. Every rule is one line with flag-value pairs:

```
-A INPUT -p tcp -s 10.0.0.0/8 --dport 22 -m conntrack --ctstate NEW -j ACCEPT
```

The parser works in two stages. `tokenize_iptables` splits on whitespace while respecting quoted strings, then the token iterator consumes flag-value pairs:

```
["-A", "INPUT", "-p", "tcp", "-s", "10.0.0.0/8", "--dport", "22", "-j", "ACCEPT"]
  │       │       │      │     │         │            │         │     │       │
  └─chain─┘       └proto─┘    └──source──┘            └──port───┘    └action─┘
```

The `!` negation operator is handled by a `next_negated` flag that carries forward to the next address or port parsed. At the file level, `parse_iptables` iterates all lines: `*filter` sets the current table, `:INPUT DROP [0:0]` records chain policies, `COMMIT` is skipped, and lines starting with `-A`/`-I` get fed to the rule parser.

### nftables parser (nftables.v)

nftables output is block-structured with braces:

```
table inet filter {
    chain input {
        type filter hook input priority 0; policy drop;
        ct state established,related accept
        tcp dport 22 accept
    }
}
```

The parser uses line-by-line iteration with three levels of nesting:

```
parse_nftables            scans for "table" lines
    │
    └── parse_nft_table   extracts table name, scans for "chain" lines
            │
            └── parse_nft_chain   extracts chain name + policy, scans for rule lines
                    │
                    └── parse_nft_rule   tokenizes a single rule line
```

Each function takes the full `lines []string` array and a start index, returning the new index after consuming its block. A closing `}` returns control to the parent.

Inside each rule line, keyword tokens drive the parse: `tcp`/`udp` set protocol and trigger port parsing, `ip saddr`/`daddr` extract addresses, `ct state` extracts connection tracking, and terminal keywords (`accept`, `drop`, `reject`) set the action. `parse_nft_port_match` handles both single ports (`dport 22`) and brace-enclosed sets (`dport { 80, 443 }`).

### Shared parsing layer (common.v)

Both parsers share functions from `common.v`: `parse_network_addr` (CIDR + negation), `parse_port_spec` (single ports, ranges, negation), `parse_port_list` (comma-separated), `parse_protocol` (names and numbers to enum), `parse_action`, `parse_table`, `parse_chain_type`, and `parse_conn_states` (comma-separated states to bitfield).

`detect_format` looks at the first non-empty, non-comment line. `*` or `:` or `-A` means iptables. `table` means nftables.


## Analyzer Design

### Pairwise comparison

The analyzer groups rules by chain via `rs.rules_by_chain()`, then compares every pair within each chain (N*(N-1)/2 comparisons per chain). Rules in different chains are never compared because the kernel evaluates each chain independently.

### Four conflict types

```
┌────────────────┬─────────────────────────────────────────────────────┐
│ Type           │ How it is detected                                  │
├────────────────┼─────────────────────────────────────────────────────┤
│ Shadowed       │ Rule A appears before rule B in the chain. A's     │
│                │ criteria is a superset of B's. B can never fire     │
│                │ because A catches all its traffic first.            │
├────────────────┼─────────────────────────────────────────────────────┤
│ Contradiction  │ Rules A and B overlap in their match criteria but   │
│                │ have opposing actions (one accepts, one drops or    │
│                │ rejects). Not a full superset, or it would be       │
│                │ classified as shadowing instead.                    │
├────────────────┼─────────────────────────────────────────────────────┤
│ Duplicate      │ Two rules have identical criteria AND the same      │
│                │ action. The second one is dead weight.              │
├────────────────┼─────────────────────────────────────────────────────┤
│ Redundant      │ Rule A is a superset of rule B with the same       │
│                │ action, but they are not exact duplicates. B is     │
│                │ unnecessary but not harmful.                        │
└────────────────┴─────────────────────────────────────────────────────┘
```

### Superset/subset math

"Does rule A match every packet that rule B matches?" breaks down field by field.

**CIDR containment** converts IPs to 32-bit integers and compares prefixes via bit shifts:

```
outer = 10.0.0.0/8       inner = 10.1.2.0/24

ip_to_u32("10.0.0.0")  = 0x0A000000
ip_to_u32("10.1.2.0")  = 0x0A010200

shift = 32 - 8 = 24

0x0A000000 >> 24 = 0x0A
0x0A010200 >> 24 = 0x0A

Same prefix after shift → 10.0.0.0/8 contains 10.1.2.0/24
```

**Port range containment** is a simple bounds check:

```
outer = 1024:65535     inner = 8080:8443

outer.start (1024) <= inner.start (8080)  ✓
outer.end (65535)  >= inner.end (8443)    ✓

→ outer contains inner
```

**Protocol hierarchy**: protocol `.all` is a superset of every specific protocol. If the outer rule matches `.all` and the inner matches `.tcp`, the outer covers everything the inner does.

**Option type handling**: `none` (no constraint) is a superset of any specific value. `source = none` covers `source = 10.0.0.0/8` because "match anything" contains "match this network." If the outer has a specific address, the inner must also have one, and CIDR containment must hold.

### Why findings carry rule indices

Every `Finding` includes `rule_indices` pointing back to specific positions in `Ruleset.rules`. The display layer uses these to print "Rules: 7, 12" next to each finding without needing the `Rule` objects themselves.


## Generator Design

### Template-based hardened rulesets

`generate_hardened` dispatches to either `generate_iptables_hardened` or `generate_nftables_hardened`. Both build a string array line by line following the same logical template: default-deny policies, loopback accept, conntrack, anti-spoofing (RFC 1918 on public interface), rate-limited ICMP, per-service rules from `config.service_ports`, drop logging, and a final explicit DROP. SSH gets rate limiting (`3/minute` burst 5). DNS gets both TCP and UDP. NTP gets UDP only. Everything else gets TCP.

### Format export

`export_ruleset` iterates every rule and calls `rule_to_iptables` or `rule_to_nftables` to reconstruct the syntax:

```
Rule { protocol: .tcp, dst_ports: [PortSpec{22}], action: .accept }
    │
    ├── rule_to_iptables → "-A INPUT -p tcp --dport 22 -j ACCEPT"
    └── rule_to_nftables → "tcp dport 22 accept"
```

The export functions also handle structural elements: table headers, chain declarations with policies, and format-specific markers like `COMMIT` for iptables.


## Design Decisions

### Why V

V compiles to a native binary with zero runtime dependencies. You run `v .` and get a single executable. No interpreter, no VM, no shared libraries beyond libc. For a security tool that might run on locked-down servers, this matters. The `v.mod` file shows `dependencies: []`.

The syntax is deliberately simple. If you can read C, Go, or Python, you can read V immediately. Option types (`?Type`) give you null safety without Rust's ceremony. The `@[flag]` enum attribute gives you bitfield operations for free, mapping perfectly to how conntrack states work in the kernel.

### Why pairwise comparison instead of a decision tree or BDD

This is O(n^2), and there are faster approaches (decision trees, BDDs, interval trees). But at 100 rules per chain, pairwise does 4,950 checks of integer comparisons, finishing in under a millisecond. Even 1000 rules (extreme) yields roughly 500,000 comparisons, still milliseconds.

More importantly, pairwise comparison produces findings referencing exactly two rules. "Rule 7 shadows rule 12" is immediately actionable. A BDD-based approach would need extra work to trace back to the specific rules involved.

### Why no external dependencies

The V standard library provides `os` (file I/O), `flag` (argument parsing), `term` (ANSI colors), and `strings` (manipulation). That covers everything needed. External dependencies in security tools create supply chain risk. A single static binary can be dropped onto any Linux system and run immediately with no package manager involved.

### Why separate modules instead of a single file

You could put everything in one file. V would not care. But separate modules give you compiler-enforced boundaries (the parser cannot call display functions), independent test files (`v test src/parser/` runs parser tests in isolation), and navigability (conflict detection bug means look at `src/analyzer/conflict.v`).

Adding a new parser (for `ufw` rules, say) would require a new file in `src/parser/`, a new `RuleSource` variant, a new case in `detect_format`, and a new case in `load_ruleset`. No changes needed in analyzer, generator, or display. They already operate on the `Ruleset` abstraction.
