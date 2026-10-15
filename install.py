#!/usr/bin/env python3
"""Install shared rules and skills into a workspace."""

import argparse
import difflib
import os
from pathlib import Path
import stat
import sys
import tempfile


BEGIN = "<!-- agent-toolkit:begin -->"
END = "<!-- agent-toolkit:end -->"
TOOLKIT = Path(__file__).resolve().parent


def managed_block() -> str:
    source = (TOOLKIT / "AGENTS.md").read_text(encoding="utf-8").strip()
    return f"{BEGIN}\n{source}\n{END}\n"


def updated_content(existing: str, block: str) -> str:
    begin_count = existing.count(BEGIN)
    end_count = existing.count(END)
    if begin_count != end_count or begin_count > 1 or (
        begin_count == 1 and existing.index(END) < existing.index(BEGIN)
    ):
        raise ValueError("AGENTS.md has incomplete or duplicate agent-toolkit markers")

    if begin_count == 0:
        return f"{existing.rstrip()}\n\n{block}" if existing.strip() else block

    start = existing.index(BEGIN)
    end = existing.index(END, start) + len(END)
    return existing[:start] + block.rstrip("\n") + existing[end:]


def preview(before: str, after: str, target: Path) -> None:
    diff = difflib.unified_diff(
        before.splitlines(keepends=True),
        after.splitlines(keepends=True),
        fromfile=f"{target} (current)",
        tofile=f"{target} (proposed)",
    )
    sys.stdout.writelines(diff)


def skill_links(workspace: Path) -> list[tuple[Path, Path]]:
    agents_dir = workspace / ".agents"
    skills_dir = agents_dir / "skills"
    if agents_dir.is_symlink() or skills_dir.is_symlink():
        raise ValueError("refusing to install through a symlinked .agents directory")
    if agents_dir.exists() and not agents_dir.is_dir():
        raise ValueError(f"agents path is not a directory: {agents_dir}")
    if skills_dir.exists() and not skills_dir.is_dir():
        raise ValueError(f"skills path is not a directory: {skills_dir}")

    links = []
    for source in sorted((TOOLKIT / "skills").iterdir()):
        if not source.is_dir() or not (source / "SKILL.md").is_file():
            continue
        target = skills_dir / source.name
        if target.is_symlink():
            if target.resolve() == source.resolve():
                continue
            raise ValueError(f"skill link already points elsewhere: {target}")
        if target.exists():
            raise ValueError(f"skill path already exists: {target}")
        links.append((source, target))
    return links


def install_links(links: list[tuple[Path, Path]]) -> list[Path]:
    created = []
    try:
        for source, target in links:
            target.parent.mkdir(parents=True, exist_ok=True)
            relative_source = os.path.relpath(source, target.parent)
            target.symlink_to(relative_source, target_is_directory=True)
            created.append(target)
    except OSError:
        for link in created:
            link.unlink(missing_ok=True)
        raise
    return created


def write_atomically(target: Path, content: str) -> None:
    mode = stat.S_IMODE(target.stat().st_mode) if target.exists() else None
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n", dir=target.parent,
            prefix=".AGENTS.md.", delete=False,
        ) as output:
            temporary = Path(output.name)
            output.write(content)
        if mode is not None:
            temporary.chmod(mode)
        temporary.replace(target)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, help="Workspace root (default: toolkit parent)")
    parser.add_argument("--yes", action="store_true", help="Apply without prompting")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    workspace_input = args.workspace
    if workspace_input is None and not args.yes and not args.dry_run:
        try:
            answer = input(f"Workspace directory [{TOOLKIT.parent}]: ").strip()
        except EOFError:
            answer = ""
        workspace_input = Path(answer) if answer else TOOLKIT.parent
    workspace = (workspace_input or TOOLKIT.parent).expanduser().resolve()
    if not workspace.is_dir():
        parser.error(f"workspace is not a directory: {workspace}")
    target = workspace / "AGENTS.md"
    if target.is_symlink():
        parser.error(f"refusing to replace symlink: {target}")

    try:
        before = target.read_text(encoding="utf-8") if target.exists() else ""
        after = updated_content(before, managed_block())
        links = skill_links(workspace)
    except (OSError, UnicodeError, ValueError) as error:
        parser.error(str(error))

    if before == after and not links:
        print(f"Already up to date: {workspace}")
        return 0

    if before != after:
        preview(before, after, target)
    for source, link in links:
        print(f"Create skill link: {link} -> {os.path.relpath(source, link.parent)}")
    if args.dry_run:
        return 0
    if not args.yes:
        try:
            answer = input("\nApply this change? [y/N] ").strip().lower()
        except EOFError:
            answer = ""
        if answer not in {"y", "yes"}:
            print("No changes made.")
            return 0

    created = []
    try:
        created = install_links(links)
        if before != after:
            write_atomically(target, after)
    except OSError as error:
        for link in created:
            link.unlink(missing_ok=True)
        parser.error(str(error))
    print(f"Installed agent-toolkit in {workspace}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
