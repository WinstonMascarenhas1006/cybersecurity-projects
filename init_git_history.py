"""
Create backdated git history with daily commits, feature branches, issue refs, and PR merges.

Run: python init_git_history.py

Produces:
  - One commit per calendar day on main (contribution graph)
  - Feature branch work per project with (#N) issue references
  - Merge commits: Merge pull request #N from WinstonMascarenhas1006/feature/...
"""

from __future__ import annotations

import os
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

from project_timeline import AUTHOR, PROJECTS
from workflow_catalog import WORKFLOW

ROOT = Path(__file__).parent
GITHUB_USER_ID = 88363585
GITHUB_LOGIN = "WinstonMascarenhas1006"
EMAIL = f"{GITHUB_USER_ID}+{GITHUB_LOGIN}@users.noreply.github.com"
AUTHOR_ARG = f"{AUTHOR} <{EMAIL}>"

START_DAY = date(2025, 4, 1)
LAST_COMMIT_DAY = date(2026, 6, 19)
ACTIVITY_LOG = ROOT / "activity.log"

BY_FOLDER = {w["folder"]: w for w in WORKFLOW}


def run(cmd: list[str], env: dict | None = None, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd, cwd=ROOT, env=env, text=True, capture_output=True, check=check,
    )


def git_env(d: date, hour: int = 12) -> dict:
    date_str = f"{d.isoformat()} {hour:02d}:00:00 +0000"
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    env["GIT_AUTHOR_NAME"] = AUTHOR
    env["GIT_AUTHOR_EMAIL"] = EMAIL
    env["GIT_COMMITTER_NAME"] = AUTHOR
    env["GIT_COMMITTER_EMAIL"] = EMAIL
    return env


def git_add(*paths: str) -> None:
    for path in paths:
        if not path:
            continue
        p = ROOT / path
        if p.exists() or path.endswith("/"):
            run(["git", "add", "-f", "--", path])


def git_commit(message: str, d: date, hour: int = 12, allow_empty: bool = False) -> bool:
    cmd = ["git", "commit"]
    if allow_empty:
        cmd.append("--allow-empty")
    cmd.extend(["-m", message, "--author", AUTHOR_ARG])
    result = run(cmd, env=git_env(d, hour), check=False)
    if result.returncode != 0:
        combined = result.stdout + result.stderr
        if "nothing to commit" in combined or "nothing added to commit" in combined:
            return False
        print(combined, file=sys.stderr)
        result.check_returncode()
    return True


def git_checkout(branch: str, create: bool = False) -> None:
    has_commits = run(["git", "rev-parse", "HEAD"], check=False).returncode == 0
    if not has_commits and branch == "main":
        return
    cmd = ["git", "checkout"]
    if create:
        cmd.append("-b")
    cmd.append(branch)
    run(cmd)


def git_merge(branch: str, message: str, d: date, hour: int = 14) -> bool:
    result = run(
        ["git", "merge", "--no-ff", branch, "-m", message],
        env=git_env(d, hour),
        check=False,
    )
    if result.returncode != 0:
        print(result.stdout + result.stderr, file=sys.stderr)
        return False
    return True


def scaffold_paths(folder: str) -> list[str]:
    base = ROOT / folder
    paths: list[str] = []
    for name in ("README.md", "DEMO.md"):
        p = base / name
        if p.exists():
            paths.append(str(p.relative_to(ROOT)).replace("\\", "/"))
    learn = base / "learn"
    if learn.exists():
        for f in learn.rglob("*"):
            if f.is_file():
                paths.append(str(f.relative_to(ROOT)).replace("\\", "/"))
    return paths


def project_schedule() -> dict[str, dict]:
    """Per-folder schedule: start, scaffold, merge days and workflow metadata."""
    schedule: dict[str, dict] = {}
    for p in PROJECTS:
        folder = p["folder"]
        start = date.fromisoformat(p["start"])
        end = date.fromisoformat(p["end"])
        if end > LAST_COMMIT_DAY:
            end = LAST_COMMIT_DAY
        wf = BY_FOLDER[folder]
        if p["two_month"]:
            scaffold = start + timedelta(days=10)
            if scaffold > end:
                scaffold = start
        else:
            scaffold = start + timedelta(days=5)
            if scaffold > end:
                scaffold = start
        schedule[folder] = {
            "start": start,
            "scaffold": scaffold,
            "merge": end,
            "workflow": wf,
            "name": p["name"],
            "two_month": p["two_month"],
        }
    return schedule


def daterange(start: date, end: date):
    d = start
    while d <= end:
        yield d
        d += timedelta(days=1)


def active_branches(d: date, schedule: dict[str, dict]) -> list[str]:
    active = []
    for folder, s in schedule.items():
        if s["start"] <= d <= s["merge"]:
            active.append(folder)
    return active


def main() -> None:
    if (ROOT / ".git").exists():
        print("Removing existing .git for clean history rebuild...")
        import shutil
        shutil.rmtree(ROOT / ".git", ignore_errors=True)

    run(["git", "init", "-b", "main"])
    schedule = project_schedule()

    if ACTIVITY_LOG.exists():
        ACTIVITY_LOG.unlink()
    ACTIVITY_LOG.write_text("", encoding="utf-8")

    # Track which branches exist and which are merged
    created_branches: set[str] = set()
    merged_branches: set[str] = set()
    commit_count = 0

    for i, d in enumerate(daterange(START_DAY, LAST_COMMIT_DAY)):
        hour_main = 10 + (i % 5)

        # --- Daily main branch activity log (first — main must exist) ---
        git_checkout("main")
        with ACTIVITY_LOG.open("a", encoding="utf-8") as f:
            f.write(f"{d.isoformat()}  portfolio work log\n")
        git_add("activity.log", ".gitignore")

        messages: list[str] = []
        if d == START_DAY:
            messages.append("Initialize cybersecurity portfolio")
            git_add("README.md", ".gitignore")
        if d == LAST_COMMIT_DAY:
            for item in (
                "README.md", "setup.ps1", "project_timeline.py", "apply_timeline.py",
                "generate_report.py", "generate_documentation.py", "init_git_history.py",
                "workflow_catalog.py", "seed_github_workflow.py", "docs/",
            ):
                if (ROOT / item).exists():
                    git_add(item)

        active = active_branches(d, schedule)
        if active and d not in (START_DAY, LAST_COMMIT_DAY):
            names = ", ".join(active[:2])
            messages.append(f"Daily development log — active: {names}")
        elif not messages:
            messages.append("Daily development log")

        hour_daily = 11 + (i % 7)
        msg = "; ".join(messages)
        if git_commit(msg, d, hour_daily):
            commit_count += 1
            if d.day == 1 or d in {s["merge"] for s in schedule.values()} or d == LAST_COMMIT_DAY:
                print(f"  {d.isoformat()}  {msg[:72]}")

        # --- Feature branch work ---
        for folder, s in schedule.items():
            if folder in merged_branches:
                continue
            wf = s["workflow"]
            branch = wf["branch"]
            issues = wf["issues"]

            if d == s["start"] and folder not in created_branches:
                git_checkout("main")
                git_checkout(branch, create=True)
                created_branches.add(folder)
                commit_count += 1 if git_commit(
                    f"chore({folder}): open feature branch for {s['name']} (#{issues[0]['number']})",
                    d, hour_main + 1, allow_empty=True,
                ) else 0

            if folder in created_branches and s["start"] < d < s["merge"]:
                git_checkout(branch)
                if d == s["scaffold"]:
                    for path in scaffold_paths(folder):
                        git_add(path)
                    commit_count += 1 if git_commit(
                        f"docs({folder}): add README and learning scaffold (#{issues[0]['number']})",
                        d, hour_main + 2,
                    ) else 0
                elif d.day % 7 == 0:
                    readme = ROOT / folder / "README.md"
                    if readme.exists():
                        git_add(f"{folder}/README.md")
                    issue = issues[1]["number"]
                    git_commit(
                        f"feat({folder}): incremental implementation progress (#{issue})",
                        d, hour_main + 2, allow_empty=True,
                    )

            if d == s["merge"] and folder not in merged_branches:
                git_checkout(branch)
                git_add(folder)
                i0, i1, i2 = issues[0]["number"], issues[1]["number"], issues[2]["number"]
                commit_count += 1 if git_commit(
                    f"feat({folder}): complete {s['name']} (closes #{i0}, #{i1}, #{i2})",
                    d, hour_main + 1,
                ) else 0

                git_checkout("main")
                pr_num = wf["pr"]["number"]
                merge_msg = (
                    f"Merge pull request #{pr_num} from {GITHUB_LOGIN}/{branch}\n\n"
                    f"{wf['pr']['title']}"
                )
                if git_merge(branch, merge_msg, d, hour_main + 3):
                    commit_count += 1
                    merged_branches.add(folder)

    # Ensure we end on main
    git_checkout("main")

    log = run(["git", "log", "--format=%ad %s", "--date=short", "-5"])
    print(f"\nDone: {commit_count} commits (approx)")
    print("Recent:")
    for line in log.stdout.strip().splitlines():
        print(f"  {line}")
    print(f"\nAuthor email: {EMAIL}")
    print("Branches:")
    run(["git", "branch", "-a"])
    print("\nNext steps:")
    print("  1. git push -u origin main --force")
    print("  2. git push origin 'refs/heads/feature/*' --force")
    print("  3. python seed_github_workflow.py")


if __name__ == "__main__":
    main()
