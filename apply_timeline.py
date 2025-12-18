"""
Apply development timeline metadata across the portfolio.
Run: python apply_timeline.py
"""

from __future__ import annotations

import re
from pathlib import Path

from project_timeline import AUTHOR, BY_FOLDER, GITHUB, PROJECTS, readme_meta

ROOT = Path(__file__).parent
SKIP_DIRS = {
    ".venv", "venv", "node_modules", "build", ".git", "__pycache__",
    ".pytest_cache", "dist", "assets", "testdata", "pnpm-lock.yaml",
}
TEXT_EXT = {
    ".py", ".go", ".v", ".cpp", ".hpp", ".h", ".c", ".ts", ".tsx",
    ".html", ".scss", ".md", ".toml", ".sh", ".sql", ".yml", ".yaml",
    ".json", ".js", ".conf", ".nginx", ".tmpl", ".ignore", ".npmrc",
}


def project_for_path(path: Path) -> dict | None:
    rel = path.relative_to(ROOT)
    parts = rel.parts
    if not parts:
        return None
    folder = parts[0]
    if folder in BY_FOLDER:
        return BY_FOLDER[folder]
    return None


def should_skip(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def update_copyright(content: str, year: int) -> tuple[str, bool]:
    new = re.sub(r"© \| 2026", f"© | {year}", content)
    new = re.sub(r"© \| 2025", f"© | {year}", new)
    return new, new != content


def patch_readme(path: Path, meta: str) -> bool:
    text = path.read_text(encoding="utf-8")
    marker = "**Author:**"
    if marker in text:
        text = re.sub(
            r"\*\*Author:\*\*[^\n]*\n(\*\*Development[^\n]*\n)?(\*\*Started:\*\*[^\n]*\n)?",
            meta,
            text,
            count=1,
        )
    else:
        lines = text.splitlines(keepends=True)
        if not lines:
            return False
        insert_at = 1
        if len(lines) > 1 and lines[1].strip() == "":
            insert_at = 2
        lines.insert(insert_at, meta + "\n")
        text = "".join(lines)
    if text != path.read_text(encoding="utf-8"):
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    copyright_updates = 0
    readme_updates = 0

    for path in ROOT.rglob("*"):
        if not path.is_file() or should_skip(path):
            continue
        if path.suffix.lower() not in TEXT_EXT and path.name not in {
            ".npmrc", ".stylelintignore", "CMakeLists.txt", "justfile", "Justfile",
        }:
            continue
        proj = project_for_path(path)
        if not proj:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        new_content, changed = update_copyright(content, proj["year"])
        if changed:
            path.write_text(new_content, encoding="utf-8")
            copyright_updates += 1

    readme_paths: list[tuple[Path, dict]] = []
    for p in PROJECTS:
        folder = ROOT / p["folder"]
        readme_paths.append((folder / "README.md", p))
        if p["folder"] == "network-traffic-analyzer":
            readme_paths.append((folder / "python" / "README.md", p))
            readme_paths.append((folder / "cpp" / "README.md", p))

    for readme_path, proj in readme_paths:
        if readme_path.exists():
            if patch_readme(readme_path, readme_meta(proj)):
                readme_updates += 1

    overview_updates = 0
    for p in PROJECTS:
        for overview in (ROOT / p["folder"]).rglob("learn/00-OVERVIEW.md"):
            text = overview.read_text(encoding="utf-8")
            blurb = (
                f"> **Author:** [{AUTHOR}]({GITHUB}) · "
                f"**Built:** {p['label']} ({p['duration']})\n"
            )
            if "**Built:**" in text:
                text = re.sub(
                    r"> \*\*Author:\*\*[^\n]+\n",
                    blurb,
                    text,
                    count=1,
                )
            else:
                lines = text.splitlines(keepends=True)
                insert_at = 1
                if len(lines) > 1 and lines[1].strip() == "":
                    insert_at = 2
                lines.insert(insert_at, blurb + "\n")
                text = "".join(lines)
            if text != overview.read_text(encoding="utf-8"):
                overview.write_text(text, encoding="utf-8")
                overview_updates += 1

    print(f"Copyright headers updated: {copyright_updates} files")
    print(f"README metadata updated: {readme_updates} files")
    print(f"Overview docs updated: {overview_updates} files")


if __name__ == "__main__":
    main()
