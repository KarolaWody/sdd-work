# sdd-work — SpecDD OpenCode Skill

## Purpose
Spec-Driven Development skill for OpenCode (`sdd-work`). Automates the SDD workflow:
constitution drafting, feature planning, implementation, validation, and
replanning.

## Stack
- Python 3
- OpenCode CLI
- SDD methodology

## Repo layout
- `README.md` — English description of the skill
- `skills/sdd-work/SKILL.md` — skill definition for OpenCode
- `docs/agent.md` — agent prompt and workflow
- `docs/examples.md` — usage examples
- `docs/tools-vscode.md` — required VSCode extensions/tools
- `opencode.json` — project-level OpenCode config

## State file
At the end of each SDD step, write a `specs/state.md` summary with:
- what was done, decisions made, next steps, pending issues
- allows model handoff: new model reads state.md to continue work
- `specs/state.md` is registered in `opencode.json` `instructions` —
  every new OpenCode session loads it automatically

## SDD Workflow

Agent MUST follow this sequence. No step may be skipped, combined, or reordered.

1. **Constitution** — mission.md, tech-stack.md, roadmap.md
2. **Feature spec** — plan.md, requirements.md, validation.md
3. **Implementation + Validation (per group)**:
   a. Agent MUST implement ONE task group from the plan
   b. Agent MUST present all changes to user
   c. Agent MUST run `@code_checker` sub-agent
   d. Agent MUST present findings to user
   e. User MUST review and explicitly approve
   f. Agent MUST NOT proceed without explicit approval
4. **Replanning** — agent proposes improvements. User MUST approve before applying.

Stopping rule for EVERY step: agent MUST present the single next task and wait for explicit user answer. Without approval, agent MUST STOP and MUST NOT proceed.

## Conventions
- **Human-in-the-loop.** Agent MUST present every change and MUST get explicit user approval. NO autonomous decisions. Without approval: agent MUST stop and MUST NOT proceed.
- **One step at a time.** Agent MUST do exactly ONE task from plan, then stop and present. NO grouping, NO batching.
- **@code_checker after EVERY group.** Agent MUST run after each task group. NO exceptions.
- **Questions ≠ consent.** User questions, observations, or statements are NOT approval. Only explicit action commands ('fix', 'remove', 'do', 'change', 'implement', 'zrób', 'popraw', 'usuń') count as consent. After answering a question, agent MUST ask "Should I apply this change?" and wait for explicit 'yes' before acting.
- English only for code, docs, and comments.
- Small steps, frequent commits (ONLY after user approval).
- Specs are versioned — commit alongside code.
- Prefer CLI+Skills over MCP servers when possible.

## Questions asked to user (onboarding)
When starting a new project, the skill asks 8 questions in 3 sections:

**Segment question (Q0):** "Do you have programming experience?"
Adjusts language and detail for beginners vs. experienced devs.

**Section 1 — Mission:**
1. Describe the project in detail. Who is it for (target audience, niche)?
   What does it do? What key functions should it perform?
2. What problem does it solve? What motivated you?
3. Do you have any existing code, site, or prototype?

**Section 2 — Stack:**
4. Do you know what technologies you want to use?
   - No → agent proposes simplest stack (HTML+CSS+JS or Python)
   - Yes → agent asks about versions, conventions
5. (Beginner) Should it run in a browser, as a website, mobile app, or something else?
6. (Experienced) Any constraints? Preferred libraries? Hosting? Budget?

**Section 3 — Roadmap:**
7. List 3-5 things the app must do, from most important.
8. Do you want an MVP first, then add features? (Default: yes)
