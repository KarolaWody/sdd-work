# Validation — {{feature_name}}

> Tip: Write the test procedure BEFORE implementing. It clarifies what "done" means.

## Validation criteria
### VC1 — <!-- short name -->
1. <!-- expected behavior -->

### VC2 — <!-- short name -->
1. <!-- expected behavior -->

## Test procedure
```bash
# Write commands to test, e.g.:
# python -c "print('hello')"
```

## Post-group validation
After EVERY group:
1. Agent runs `@code_checker` sub-agent
2. Agent presents findings
3. User MUST review and approve
4. Only then: next group
