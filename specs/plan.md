# Plan — SDD Workflow CLI

## Task groups

### Group 1: Project skeleton
1. Create `sdd.py` with CLI entry point (argparse)
2. Implement `sdd init` — scaffold specs/ directory
3. Create template files in `skills/sdd-work/templates/`

### Group 2: State management
4. Implement `sdd state` — read/update state.md
5. Implement `sdd state --current` — print current state

### Group 3: Feature spec
6. Implement `sdd feature <name>` — create feature spec files

### Group 4: Validation & status
7. Implement `sdd validate` — check consistency
8. Implement `sdd status` — summary board
9. Wire `--help` for all commands

### Group 5: Integration
10. Update `SKILL.md` to reference `sdd.py`
11. Update `README.md` with installation/usage
12. Update `specs/state.md`

## Dependencies
- Python 3.10+ stdlib only (argparse, pathlib, datetime)
- No pip install needed — user runs `python sdd.py`

## Order
Group 1 → Group 2 → Group 3 → Group 4 → Group 5.

After EVERY group:
1. Agent runs `@code_checker`
2. Agent presents findings to user
3. User MUST review and approve
4. ONLY then: next group
