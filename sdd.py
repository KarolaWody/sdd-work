#!/usr/bin/env python3
"""SDD Workflow CLI — Automates Spec-Driven Development workflow."""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

TEMPLATES_DIR = Path(__file__).resolve().parent / "skills" / "sdd-work" / "templates"


def _load_template(name):
    path = TEMPLATES_DIR / name
    if path.exists():
        return path.read_text()
    return f"# {name}\n\n<!-- TODO: fill in -->\n"


def cmd_init():
    specs_dir = Path("specs")
    overwrite = False

    if specs_dir.exists():
        answer = input(f"'{specs_dir}/' already exists. Overwrite? [y/N] ")
        if answer.lower() != "y":
            print("Aborted.")
            return
        overwrite = True

    specs_dir.mkdir(parents=True, exist_ok=True)

    files = ["mission.md", "tech-stack.md", "roadmap.md", "state.md"]
    for name in files:
        path = specs_dir / name
        if path.exists() and not overwrite:
            continue
        path.write_text(_load_template(name))
        print(f"  Created {path}")

    print("Done. Edit the files in specs/ to match your project.")


def cmd_feature(name):
    specs_dir = Path("specs")
    if not specs_dir.exists():
        print("Error: specs/ directory not found. Run 'sdd init' first.", file=sys.stderr)
        sys.exit(1)

    overwrite_plan = specs_dir.joinpath("plan.md").exists()
    overwrite_req = specs_dir.joinpath("requirements.md").exists()
    overwrite_val = specs_dir.joinpath("validation.md").exists()

    if overwrite_plan or overwrite_req or overwrite_val:
        answer = input("Some feature spec files already exist. Overwrite? [y/N] ")
        if answer.lower() != "y":
            print("Aborted.")
            return

    (specs_dir / "plan.md").write_text(
        f"# Plan — {name}\n\n"
        f"## Task groups\n\n"
        f"1. TBD\n\n"
        f"## Dependencies\n- none\n\n"
        f"## Order\nTBD\n"
    )
    print(f"  Created specs/plan.md")

    (specs_dir / "requirements.md").write_text(
        f"# Requirements — {name}\n\n"
        f"## Feature summary\n\n"
        f"## Functional requirements\n\n"
        f"### FR1 — TBD\n- none\n\n"
        f"## Non-functional requirements\n- none\n"
    )
    print(f"  Created specs/requirements.md")

    (specs_dir / "validation.md").write_text(
        f"# Validation — {name}\n\n"
        f"## Validation criteria\n\n"
        f"### VC1 — TBD\n- none\n\n"
        f"## Test procedure\n```bash\n# TODO\n```\n"
    )
    print(f"  Created specs/validation.md")

    print(f"Done. Feature '{name}' scaffolding ready in specs/.")


def cmd_state(show_current):
    state_path = Path("specs") / "state.md"
    if not state_path.exists():
        print("Error: specs/state.md not found. Run 'sdd init' first.", file=sys.stderr)
        sys.exit(1)

    if show_current:
        print(state_path.read_text())
        return

    content = state_path.read_text()
    print("Appending to specs/state.md...")

    what = input("What was done? ")
    decisions = input("Decisions made? ")
    next_steps = input("Next steps? ")
    issues = input("Pending issues? ")

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = (
        f"\n## [{now}]\n"
        f"- **Done:** {what}\n"
        f"- **Decisions:** {decisions}\n"
        f"- **Next:** {next_steps}\n"
        f"- **Issues:** {issues}\n"
    )

    state_path.write_text(content + entry)
    print("State updated.")


def cmd_validate():
    specs_dir = Path("specs")
    if not specs_dir.exists():
        print("Error: specs/ directory not found.", file=sys.stderr)
        sys.exit(1)

    state_path = specs_dir / "state.md"
    if not state_path.exists():
        print("Missing: specs/state.md")
        sys.exit(1)

    print("=== Validation Report ===")
    all_ok = True
    for name in ["mission.md", "tech-stack.md", "roadmap.md", "state.md"]:
        path = specs_dir / name
        status = "OK" if path.exists() else "MISSING"
        if status != "OK":
            all_ok = False
        print(f"  {name}: {status}")

    has_feature = all((specs_dir / n).exists() for n in ["plan.md", "requirements.md", "validation.md"])
    if has_feature:
        print("  feature spec: OK")
    else:
        print("  feature spec: not started (optional)")

    print("Checking @code_checker...")
    print("  Note: Run '@code_checker' in OpenCode to review the code.")
    print("  Automatic invocation TBD — run `opencode run '@code_checker'` manually.")

    if all_ok:
        print("Result: PASS")
    else:
        print("Result: FAIL — missing required files")
        sys.exit(1)


def cmd_status():
    specs_dir = Path("specs")
    if not specs_dir.exists():
        print("No specs/ directory found.")
        return

    print("=== Spec Files Status ===")
    required = ["mission.md", "tech-stack.md", "roadmap.md", "state.md"]
    optional = ["plan.md", "requirements.md", "validation.md"]

    for name in required:
        path = specs_dir / name
        if path.exists():
            size = path.stat().st_size
            print(f"  {name}: OK ({size} bytes)")
        else:
            print(f"  {name}: MISSING")

    print("--- Feature spec ---")
    for name in optional:
        path = specs_dir / name
        if path.exists():
            size = path.stat().st_size
            print(f"  {name}: OK ({size} bytes)")
        else:
            print(f"  {name}: not started")


def main():
    parser = argparse.ArgumentParser(
        prog="sdd",
        description="Spec-Driven Development (SDD) workflow CLI",
    )
    sub = parser.add_subparsers(dest="command")

    p_init = sub.add_parser("init", help="Scaffold specs/ directory with templates")
    p_feature = sub.add_parser("feature", help="Create feature spec files")
    p_feature.add_argument("name", help="Feature name (e.g. 'user-auth')")

    p_state = sub.add_parser("state", help="Manage state.md")
    p_state.add_argument("--current", action="store_true", help="Print current state")

    sub.add_parser("validate", help="Validate project state")
    sub.add_parser("status", help="Show spec files status")

    args = parser.parse_args()

    if args.command == "init":
        cmd_init()
    elif args.command == "feature":
        cmd_feature(args.name)
    elif args.command == "state":
        cmd_state(args.current)
    elif args.command == "validate":
        cmd_validate()
    elif args.command == "status":
        cmd_status()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
