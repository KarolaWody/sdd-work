---
name: sdd-work
description: Spec-Driven Development workflow for OpenCode. Automates constitution, feature spec, implementation, validation, and replanning.
---

# sdd-work — Spec-Driven Development Skill

## Workflow

Agent MUST follow this sequence. No step may be skipped, combined, or reordered.

1. **Constitution** — Ask user 8 onboarding questions (see `AGENTS.md`), then create mission.md, tech-stack.md, roadmap.md in a `specs/` folder. User MUST approve. Commit ONLY after approval.

2. **Feature spec** — Create plan.md, requirements.md, validation.md in `specs/`. User MUST approve. Commit ONLY after approval.

3. **Implementation + Validation (per group)**:
   a. Agent MUST implement ONE task group from the plan
   b. Agent MUST present all changes to user
   c. Agent MUST run `@code_checker` sub-agent
   d. Agent MUST present findings to user
   e. User MUST review and explicitly approve
   f. Agent MUST NOT proceed without explicit approval

4. **Replanning** — Propose improvements. User MUST approve before applying.

## State file
At the end of each SDD step, write `specs/state.md` with:
- what was done, decisions, next steps, pending issues
Enables model handoff — new model reads this file to continue.

## Rules
- **One step at a time.** Agent MUST do exactly ONE task from plan, then stop and present. NO grouping, NO batching.
- **Ask first.** Agent MUST ask user for a specific decision before proceeding. NO assumptions of consent.
- **Wait for answer.** Agent MUST wait for explicit user response. No proceeding without clear answer.
- **@code_checker after EVERY group.** Mandatory. NO exceptions.
- **Questions ≠ consent.** User questions, observations, or statements are NOT approval. Only explicit commands ('fix', 'remove', 'do', 'change', 'implement') count as consent. After answering a question, agent MUST ask "Should I apply this change?" and wait for explicit 'yes'.
- **No autonomy.** Agent MUST NOT make any decision without user approval. Without approval: STOP.
- English only. Small steps. Specs versioned.
