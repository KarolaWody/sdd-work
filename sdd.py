#!/usr/bin/env python3
"""SDD Workflow CLI — Automates Spec-Driven Development workflow."""

import argparse
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def _get_templates_dir():
    if env := os.environ.get("SDD_TEMPLATES_DIR"):
        p = Path(env)
        if p.exists():
            return p
    local = Path(__file__).resolve().parent / "skills" / "sdd-work" / "templates"
    if local.exists():
        return local
    raise RuntimeError(
        "Templates directory not found. "
        "Set SDD_TEMPLATES_DIR env var or run from project root."
    )


TEMPLATES_DIR = _get_templates_dir()
_FEATURE_NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")


def _has_content(path, min_chars=50):
    if not path.exists():
        return False
    text = path.read_text().strip()
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL).strip()
    return len(text) >= min_chars


def _sanitize_md(text, max_len=2000):
    if not text:
        return ""
    text = text[:max_len]
    for ch in ['`', '*', '_', '#', '>', '|', '[', ']', '(', ')']:
        text = text.replace(ch, f"\\{ch}")
    return " ".join(text.splitlines())


def _load_template(name):
    path = TEMPLATES_DIR / name
    if not path.exists():
        available = [p.name for p in TEMPLATES_DIR.glob("*.md")]
        raise FileNotFoundError(
            f"Template not found: {name}. Available: {available}"
        )
    return path.read_text()


def _run_code_checker():
    cmd = os.environ.get("SDD_CODE_CHECKER_CMD", "opencode run @code_checker").split()
    if not shutil.which(cmd[0]):
        print("Warning: 'opencode' not found. Run '@code_checker' manually.", file=sys.stderr)
        return False
    try:
        subprocess.run(cmd, check=True, timeout=120)
        return True
    except subprocess.TimeoutExpired:
        print("Warning: code checker timed out after 120s", file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Warning: code checker failed (exit {e.returncode})", file=sys.stderr)
    return False


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

    if not _FEATURE_NAME_PATTERN.match(name):
        print(
            f"Error: '{name}' is not a valid feature name. "
            "Use lowercase alphanumeric, hyphens, underscores (max 64 chars).",
            file=sys.stderr,
        )
        sys.exit(1)

    overwrite_plan = specs_dir.joinpath("plan.md").exists()
    overwrite_req = specs_dir.joinpath("requirements.md").exists()
    overwrite_val = specs_dir.joinpath("validation.md").exists()

    if overwrite_plan or overwrite_req or overwrite_val:
        answer = input("Some feature spec files already exist. Overwrite? [y/N] ")
        if answer.lower() != "y":
            print("Aborted.")
            return

    for tmpl, filename in [("plan.md", "plan.md"),
                           ("requirements.md", "requirements.md"),
                           ("validation.md", "validation.md")]:
        content = _load_template(tmpl).replace("{{feature_name}}", name)
        (specs_dir / filename).write_text(content)
        print(f"  Created specs/{filename}")

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
        f"- **Done:** {_sanitize_md(what)}\n"
        f"- **Decisions:** {_sanitize_md(decisions)}\n"
        f"- **Next:** {_sanitize_md(next_steps)}\n"
        f"- **Issues:** {_sanitize_md(issues)}\n"
    )

    state_path.write_text(content + entry)
    print("State updated.")


def cmd_validate(run_checker=False):
    specs_dir = Path("specs")
    if not specs_dir.exists():
        print("Error: specs/ directory not found.", file=sys.stderr)
        sys.exit(1)

    print("=== Validation Report ===")
    all_ok = True
    for name in ["mission.md", "tech-stack.md", "roadmap.md", "state.md"]:
        path = specs_dir / name
        if _has_content(path):
            status = "OK"
        elif path.exists():
            status = "EMPTY or placeholder only"
            all_ok = False
        else:
            status = "MISSING"
            all_ok = False
        print(f"  {name}: {status}")

    has_feature = all(_has_content(specs_dir / n) for n in ["plan.md", "requirements.md", "validation.md"])
    if has_feature:
        print("  feature spec: OK")
    elif any((specs_dir / n).exists() for n in ["plan.md", "requirements.md", "validation.md"]):
        print("  feature spec: EMPTY or placeholder only")
        all_ok = False
    else:
        print("  feature spec: not started (optional)")

    if run_checker:
        print("\nRunning @code_checker...")
        _run_code_checker()
    else:
        print("\nHint: run 'sdd validate --checker' to invoke @code_checker")
        print("Or in OpenCode TUI: @code_checker")

    if all_ok:
        print("\nResult: PASS")
    else:
        print("\nResult: FAIL — see issues above")
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

    p_validate = sub.add_parser("validate", help="Validate project state")
    p_validate.add_argument("--checker", action="store_true", help="Run @code_checker after validation")

    sub.add_parser("status", help="Show spec files status")

    args = parser.parse_args()

    if args.command == "init":
        cmd_init()
    elif args.command == "feature":
        cmd_feature(args.name)
    elif args.command == "state":
        cmd_state(args.current)
    elif args.command == "validate":
        cmd_validate(run_checker=args.checker)
    elif args.command == "status":
        cmd_status()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
