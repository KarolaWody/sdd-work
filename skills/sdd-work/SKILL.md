---
name: sdd-work
description: Spec-Driven Development workflow for OpenCode. Automates constitution, feature spec, implementation, validation, and replanning.
---

# sdd-work — Spec-Driven Development Skill

## Workflow

1. **Constitution** — Ask user 8 onboarding questions (see `AGENTS.md`), then create mission.md, tech-stack.md, roadmap.md in a `specs/` folder. Wait for user approval. Commit.

2. **Feature spec** — Create a feature branch. Discuss the next roadmap item with the user. Create plan.md, requirements.md, validation.md in `specs/features/<feature-name>/`. Wait for user approval. Commit.

3. **Implementation** — Implement per task groups from the plan. Present all changes to user. Do NOT commit without approval.

4. **Validation** — Run `@code_checker` sub-agent to scan code for weakest spots. Present findings to user. Run any configured tests. Wait for explicit OK before commit or merge.

5. **Replanning** — Propose constitution and process improvements to user. Wait for approval before applying changes.

## State file
At the end of each step, write `specs/state.md` with:
- what was done, decisions, next steps, pending issues
Enables model handoff — new model reads this file to continue.

## Rules
- Human-in-the-loop always. No autonomous changes.
- English only.
- Small steps, frequent commits.
- Specs are versioned — commit alongside code.
