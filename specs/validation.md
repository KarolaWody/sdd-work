# Validation — SDD Workflow CLI

## Validation criteria

### VC1 — Init
1. Run `python sdd.py init` in empty directory → `specs/` created with 4 template files
2. Run again → prompts about overwrite

### VC2 — Feature
3. `python sdd.py feature my-thing` → creates 3 spec files with "my-thing" as feature name
4. Run again → prompts about overwrite

### VC3 — State
5. `python sdd.py state` → appends entry to state.md with timestamp
6. `python sdd.py state --current` → prints current state content

### VC4 — Validate
7. `python sdd.py validate` — reports file status

### VC5 — Status
8. `python sdd.py status` — shows all spec files with status

### VC6 — Help & errors
9. `python sdd.py --help` and `python sdd.py init --help` show meaningful help
10. Invalid command → exit code 1 + error message

### VC7 — Post-group @code_checker
11. Agent implements ONE task group
12. Agent runs `@code_checker` sub-agent
13. Agent presents all findings to user

### VC8 — User approval gate
14. User MUST review findings
15. User MUST explicitly approve
16. Agent MUST STOP and MUST NOT proceed without approval

### VC9 — No batching
17. Agent MUST NOT implement >1 group without approval
18. Agent MUST NOT combine, skip, or reorder any steps

## Test procedure
```bash
# Create temp directory
mkdir -p /tmp/sdd-test && cd /tmp/sdd-test

# Test init
python /path/to/sdd.py init
ls specs/

# Test feature
python /path/to/sdd.py feature login
ls specs/

# Test state
python /path/to/sdd.py state
cat specs/state.md

# Test status
python /path/to/sdd.py status

# Cleanup
rm -rf /tmp/sdd-test
```
