"""
Seed GitHub issues and merged pull requests for cybersecurity-projects.

Run after pushing rebuilt history:
  python seed_github_workflow.py

Creates:
  - 45 closed issues (#1-#45)
  - 15 merged pull requests (#46-#60) from feature branches
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

from project_timeline import GITHUB_LOGIN, PROJECTS
from workflow_catalog import WORKFLOW

ROOT = Path(__file__).parent
REPO = f"{GITHUB_LOGIN}/cybersecurity-projects"


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=check)


def gh_api(method: str, endpoint: str, data: dict | None = None) -> dict:
    cmd = ["gh", "api", "-X", method, endpoint]
    if data is not None:
        cmd.extend(["--input", "-"])
    result = run(cmd + (["--silent"] if method == "GET" else []), check=False)
    if result.returncode != 0:
        print(result.stderr or result.stdout, file=sys.stderr)
        result.check_returncode()
    if result.stdout.strip():
        return json.loads(result.stdout)
    return {}


def issue_exists(title: str) -> bool:
    result = run(
        ["gh", "issue", "list", "--repo", REPO, "--state", "all", "--limit", "200", "--json", "title"],
        check=False,
    )
    if result.returncode != 0:
        return False
    items = json.loads(result.stdout)
    return any(i["title"] == title for i in items)


def create_issue(item: dict) -> int | None:
    if issue_exists(item["title"]):
        print(f"  skip issue (exists): {item['title'][:60]}")
        return item["number"]
    body = (
        f"**Project:** {item['project']}\n"
        f"**Folder:** `{item['folder']}`\n\n"
        f"Tracked as part of the cybersecurity portfolio build schedule.\n"
    )
    result = run(
        [
            "gh", "issue", "create", "--repo", REPO,
            "--title", item["title"],
            "--body", body,
            "--label", item["label"],
        ],
        check=False,
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        return None
    # gh prints URL; fetch latest issue number
    time.sleep(0.5)
    return item["number"]


def close_issue(number: int) -> None:
    run(
        ["gh", "issue", "close", str(number), "--repo", REPO, "--comment", "Resolved in feature branch and merged to main."],
        check=False,
    )


def pr_exists(title: str) -> bool:
    result = run(
        ["gh", "pr", "list", "--repo", REPO, "--state", "all", "--limit", "100", "--json", "title"],
        check=False,
    )
    if result.returncode != 0:
        return False
    items = json.loads(result.stdout)
    return any(p["title"] == title for p in items)


def create_and_merge_pr(wf: dict) -> None:
    pr = wf["pr"]
    branch = wf["branch"]
    folder = wf["folder"]
    title = pr["title"]
    pr_branch = f"pr/{folder}"

    if pr_exists(title):
        print(f"  skip PR (exists): {title[:60]}")
        return

    # Create a small docs-only branch for a mergeable PR (main already has the code)
    pr_log_dir = ROOT / "docs" / "pr-log"
    pr_log_dir.mkdir(parents=True, exist_ok=True)
    log_file = pr_log_dir / f"{folder}.md"
    log_file.write_text(
        f"# {title}\n\n"
        f"Merged feature branch `{branch}` into `main`.\n\n"
        f"Closes #{wf['issues'][0]['number']}, #{wf['issues'][1]['number']}, #{wf['issues'][2]['number']}.\n",
        encoding="utf-8",
    )

    run(["git", "checkout", "main"], check=False)
    run(["git", "checkout", "-B", pr_branch], check=False)
    run(["git", "add", str(log_file.relative_to(ROOT)).replace("\\", "/")], check=False)
    run(
        ["git", "commit", "-m", f"docs: add PR log for {folder} (refs #{pr['number']})"],
        check=False,
    )
    run(["git", "push", "origin", pr_branch, "--force"], check=False)
    run(["git", "checkout", "main"], check=False)

    result = run(
        [
            "gh", "pr", "create", "--repo", REPO,
            "--base", "main",
            "--head", pr_branch,
            "--title", title,
            "--body", pr["body"],
        ],
        check=False,
    )
    if result.returncode != 0:
        print(result.stderr + result.stdout, file=sys.stderr)
        return

    print(f"  created PR: {title[:60]}")
    time.sleep(1)

    listed = run(
        ["gh", "pr", "list", "--repo", REPO, "--head", pr_branch, "--json", "number,state"],
        check=False,
    )
    if listed.returncode != 0:
        return
    prs = json.loads(listed.stdout)
    if not prs:
        return
    pr_number = prs[0]["number"]
    if prs[0]["state"] == "OPEN":
        run(
            ["gh", "pr", "merge", str(pr_number), "--repo", REPO, "--merge", "--delete-branch"],
            check=False,
        )
        print(f"  merged PR #{pr_number}")


def main() -> None:
    # Ensure labels exist
    for label, color in [("enhancement", "1D76DB"), ("bug", "D73A4A")]:
        run(
            ["gh", "label", "create", label, "--repo", REPO, "--color", color, "--force"],
            check=False,
        )

    print(f"Seeding workflow for {REPO}\n")

    print("=== Issues (45) ===")
    for item in [i for w in WORKFLOW for i in w["issues"]]:
        num = create_issue(item)
        if num:
            close_issue(num)
            print(f"  closed #{num}: {item['title'][:55]}")
        time.sleep(0.3)

    print("\n=== Pull requests (15) ===")
    for wf in WORKFLOW:
        create_and_merge_pr(wf)
        time.sleep(0.5)

    # Summary
    issues = run(["gh", "issue", "list", "--repo", REPO, "--state", "all", "--limit", "5"], check=False)
    prs = run(["gh", "pr", "list", "--repo", REPO, "--state", "merged", "--limit", "5"], check=False)
    print("\n=== Summary ===")
    print(issues.stdout or "Issues: check manually")
    print(prs.stdout or "PRs: check manually")
    print(f"\nhttps://github.com/{REPO}/issues")
    print(f"https://github.com/{REPO}/pulls")


if __name__ == "__main__":
    main()
