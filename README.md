# sdd-work — Spec-Driven Development Skill for OpenCode

`sdd-work` automates the Spec-Driven Development (SDD) workflow in OpenCode. It guides the agent through the full cycle: constitution, feature spec, implementation, validation, and replanning — with human-in-the-loop at every step.

## About this project

This is a **portfolio project** demonstrating Spec-Driven Development with AI assistance:

- **Methodology:** Every feature goes through plan → spec → implementation → validation → iteration. No step proceeds without human approval.
- **AI in the loop:** OpenCode agent drives development; `@code_checker` sub-agent performs automated code review before any merge.
- **Tools:** Python, git/GitHub, OpenCode CLI, AI code review agents.
- **Documentation-first:** All decisions, specs, and architecture are recorded and versioned alongside code.

**Why this matters:** Software built by vibecoding alone is fragile. This project shows a structured, review-driven alternative — the way professional AI-assisted development should work.

👉 [github.com/KarolaWody/sdd-work](https://github.com/KarolaWody/sdd-work)

## Workflow

1. **Constitution** — define mission, tech stack, and roadmap via agent interview
2. **Feature spec** — plan, requirements, and validation criteria per feature
3. **Implementation** — agent builds per task groups
4. **Validation** — human review + `@code_checker` AI code review; no merge without approval
5. **Replanning** — update constitution and process, approved by user

## Step-by-step installation (for beginners)

You only need a terminal and OpenCode. Here's how to install this skill:

### 1. Open a terminal
On Linux: `Ctrl` + `Alt` + `T`. On Mac: `Cmd` + `Space`, type "terminal".

### 2. Check if OpenCode is installed
Type in terminal:
```bash
opencode --version
```
If you see a version number — you're good. If not — first [install OpenCode](https://opencode.ai).

### 3. Clone this repository
```bash
git clone https://github.com/KarolaWody/sdd-work /tmp/sdd-work
```

### 4. Local or global?
Decide where to install the skill:

- **Local** — skill works only in the current project
- **Global** — skill works in all projects

#### Local install (single project)
In the root directory of YOUR project (where you want to use the skill):
```bash
mkdir -p .opencode/skills
cp -r /tmp/sdd-work/skills/sdd-work .opencode/skills/sdd-work
```

#### Global install (all projects)
```bash
mkdir -p ~/.config/opencode/skills
cp -r /tmp/sdd-work/skills/sdd-work ~/.config/opencode/skills/sdd-work
```

### 5. Done!
Run OpenCode in terminal:
```bash
opencode
```
Skill `sdd-work` will be available automatically. The agent will suggest it when relevant, or you can type: "use skill sdd-work".

## Usage

Once the skill is installed, just work with the OpenCode agent. The agent will recognize when to use the `sdd-work` skill. You can also explicitly ask:

```
use skill sdd-work. I want to start a new project.
```

## Stack
- Python 3
- OpenCode CLI
- SDD methodology

## Files in this repo
- `skills/sdd-work/SKILL.md` — skill definition
- `docs/agent.md` — agent prompt and workflow
- `docs/examples.md` — usage examples
- `docs/tools-vscode.md` — required VSCode extensions
- `opencode.json` — project config with `@code_checker` sub-agent