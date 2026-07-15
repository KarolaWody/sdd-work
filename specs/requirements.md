# Requirements — SDD Workflow CLI

## Feature summary
A Python CLI tool (`sdd.py`) that automates Spec-Driven Development workflow steps.
Users invoke it instead of manually creating spec files.

## Functional requirements

### FR1 — Init project
- `sdd init` creates `specs/` directory with template files:
  - `mission.md` — blank template with prompts
  - `tech-stack.md` — blank template
  - `roadmap.md` — blank template
  - `state.md` — initial state placeholder
- If `specs/` already exists, ask before overwriting

### FR2 — Create feature spec
- `sdd feature <name>` creates `specs/plan.md`, `specs/requirements.md`, `specs/validation.md`
- Fills in the feature name from argument
- If files exist, ask before overwriting

### FR3 — Update state
- `sdd state` appends a new entry to `specs/state.md` with:
  - Timestamp
  - What was done (user input)
  - Decisions (user input)
  - Next steps (user input)
- `sdd state --current` prints current state

### FR4 — Validate
- `sdd validate` runs `@code_checker` sub-agent invocation
- Checks that all specs files are in sync with state.md
- Reports missing or stale files

### FR5 — Status board
- `sdd status` prints a summary of all spec files and their status (exists/missing/stale)

### FR6 — Mandatory validation gate
- After EVERY task group: agent MUST run `@code_checker`
- Agent MUST present all findings to user
- User MUST review and explicitly approve
- Agent MUST NOT proceed to next group without approval
- Agent MUST NOT combine or skip any group

## Non-functional requirements
- Python 3.10+, no external dependencies (stdlib only)
- Must work on Linux and macOS
- Help text via `sdd --help` and `sdd <command> --help`
- Exit codes: 0 success, 1 user error, 2 internal error
