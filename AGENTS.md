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

## Commands
```bash
opencode run skill/sdd_work.md
```

## SDD Workflow
1. **Constitution** — mission.md, tech-stack.md, roadmap.md
2. **Feature spec** — plan.md, requirements.md, validation.md
3. **Implementation** — agent implements per task groups
4. **Validation** — agent presents changes, then **waits for human approval**
   before any commit or merge. Run `@code_checker` sub-agent to scan code
   for weakest spots (AI code review). No commit/merge without explicit OK.
5. **Replanning** — agent proposes constitution updates and process improvements,
   then waits for human approval before applying changes

## Conventions
- English only for code, docs, and comments
- Small steps with frequent commits
- Specs are versioned — commit alongside code
- Prefer CLI+Skills over MCP servers when possible
- **Human-in-the-loop always** — agent must clearly communicate every pending
  change to the user and wait for explicit confirmation before acting. No
  autonomous decisions or silent changes. Without user approval, agent
  cannot proceed and must inform the user.

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
