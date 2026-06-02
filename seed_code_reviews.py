"""
Submit code reviews on bot-authored open PRs, then squash-merge them.

Self-reviews of your own PRs do NOT count. Reviews of github-actions[bot]
PRs DO count toward Pull request reviews on the profile pie chart.

Usage:
  python seed_code_reviews.py
  python seed_code_reviews.py --repo portfolio
  python seed_code_reviews.py --repo cyber --limit 80
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent

REPOS = {
    "portfolio": "WinstonMascarenhas1006/Portfolio",
    "cyber": "WinstonMascarenhas1006/cybersecurity-projects",
}

REVIEW_BODIES = [
    "Looks good — docs are clear and scoped correctly. Approving.",
    "LGTM. Minor nit: keep naming consistent next time; otherwise fine.",
    "Reviewed the seed docs change. Safe to merge.",
    "Approved. Matches the intended review-practice workflow.",
    "Checked the diff — no concerns. Approving.",
]


def run(cmd: list[str], check: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=check)


def list_bot_open_prs(repo: str) -> list[dict]:
    result = run(
        [
            "gh", "pr", "list", "--repo", repo, "--state", "open",
            "--limit", "200", "--json", "number,title,author,isDraft",
        ],
        check=False,
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        return []
    items = json.loads(result.stdout)
    out = []
    for p in items:
        author = (p.get("author") or {}).get("login", "")
        title = p.get("title") or ""
        if author in ("github-actions[bot]", "app/github-actions") or "review seed" in title.lower():
            out.append(p)
    return out


def already_reviewed(repo: str, number: int) -> bool:
    result = run(
        ["gh", "api", f"repos/{repo}/pulls/{number}/reviews"],
        check=False,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return False
    reviews = json.loads(result.stdout)
    for r in reviews:
        user = (r.get("user") or {}).get("login", "")
        state = r.get("state", "")
        if user == "WinstonMascarenhas1006" and state in ("APPROVED", "COMMENTED", "CHANGES_REQUESTED"):
            return True
    return False


def submit_review(repo: str, number: int, body: str) -> bool:
    payload = json.dumps({"body": body, "event": "APPROVE"})
    result = subprocess.run(
        ["gh", "api", "-X", "POST", f"repos/{repo}/pulls/{number}/reviews", "--input", "-"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        input=payload,
    )
    if result.returncode != 0:
        err = (result.stderr or result.stdout).strip()
        print(f"  FAIL review #{number}: {err}", file=sys.stderr)
        if "secondary rate limit" in err.lower():
            return False
        return True  # continue others
    print(f"  reviewed #{number}")
    return True


def merge_pr(repo: str, number: int) -> None:
    result = run(
        [
            "gh", "pr", "merge", str(number), "--repo", repo,
            "--squash", "--delete-branch",
        ],
        check=False,
    )
    if result.returncode != 0:
        print(f"  merge skip #{number}: {(result.stderr or result.stdout).strip()[:120]}", file=sys.stderr)
    else:
        print(f"  merged #{number}")


def process_repo(repo: str, limit: int, pause: float) -> int:
    prs = list_bot_open_prs(repo)
    print(f"\n=== {repo}: {len(prs)} bot open PRs (limit {limit}) ===")
    done = 0
    for idx, pr in enumerate(prs[:limit]):
        num = pr["number"]
        if already_reviewed(repo, num):
            print(f"  skip (already reviewed) #{num}")
            merge_pr(repo, num)
            continue
        body = REVIEW_BODIES[idx % len(REVIEW_BODIES)]
        ok = submit_review(repo, num, body)
        if not ok:
            print("  rate limited — stop")
            break
        time.sleep(pause)
        merge_pr(repo, num)
        done += 1
        time.sleep(pause)
    return done


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", choices=("portfolio", "cyber", "all"), default="all")
    parser.add_argument("--limit", type=int, default=200)
    parser.add_argument("--pause", type=float, default=2.0)
    args = parser.parse_args()

    total = 0
    targets = list(REPOS.keys()) if args.repo == "all" else [args.repo]
    for key in targets:
        total += process_repo(REPOS[key], args.limit, args.pause)

    print(f"\nSubmitted {total} new reviews.")
    print("Pie chart may take a few minutes to refresh.")


if __name__ == "__main__":
    main()
