# sdd-work — Spec-Driven Development Skill for OpenCode

`sdd-work` automates the Spec-Driven Development (SDD) workflow in OpenCode. It guides the agent through the full cycle: constitution, feature spec, implementation, validation, and replanning — with human-in-the-loop at every step.

## Workflow

1. **Constitution** — define mission, tech stack, and roadmap via agent interview
2. **Feature spec** — plan, requirements, and validation criteria per feature
3. **Implementation** — agent builds per task groups
4. **Validation** — human review + `@code_checker` AI code review; no merge without approval
5. **Replanning** — update constitution and process, approved by user

## Instalacja krok po kroku (dla początkujących)

Potrzebujesz tylko terminala i OpenCode. Oto jak zainstalować tego skilla:

### 1. Otwórz terminal
Na Linux: `Ctrl` + `Alt` + `T`. Na Mac: `Cmd` + `Spacja`, wpisz "terminal".

### 2. Sprawdź czy OpenCode jest zainstalowane
Wpisz w terminalu:
```bash
opencode --version
```
Jeśli widzisz numer wersji — idziesz dalej. Jeśli nie — najpierw [zainstaluj OpenCode](https://opencode.ai).

### 3. Sklonuj to repozytorium
```bash
git clone https://github.com/KarolaWody/sdd-work /tmp/sdd-work
```

### 4. Lokalnie czy globalnie?
Zdecyduj gdzie chcesz zainstalować skilla:

- **Lokalnie** — skill działa tylko w bieżącym projekcie
- **Globalnie** — skill działa we wszystkich projektach

#### Instalacja lokalna (dla jednego projektu)
W katalogu głównym TWOJEGO projektu (tam gdzie chcesz używać skilla):
```bash
mkdir -p .opencode/skills
cp -r /tmp/sdd-work/skills/sdd-work .opencode/skills/sdd-work
```

#### Instalacja globalna (dla wszystkich projektów)
```bash
mkdir -p ~/.config/opencode/skills
cp -r /tmp/sdd-work/skills/sdd-work ~/.config/opencode/skills/sdd-work
```

### 5. Gotowe!
Uruchom OpenCode w terminalu:
```bash
opencode
```
Skill `sdd-work` będzie automatycznie dostępny. Agent sam go zaproponuje gdy będzie pasował do zadania, albo możesz napisać: "użyj skilla sdd-work".

## Użycie

Gdy skill jest zainstalowany, po prostu pracuj z agentem OpenCode. Agent sam rozpozna kiedy użyć skilla `sdd-work`. Możesz też jawnie poprosić:

```
użyj skilla sdd-work. Chcę zacząć nowy projekt.
```

## Stack
- Python 3
- OpenCode CLI
- SDD methodology

## Pliki w repozytorium
- `skills/sdd-work/SKILL.md` — definicja skilla
- `docs/agent.md` — prompt i workflow agenta
- `docs/examples.md` — przykłady użycia
- `docs/tools-vscode.md` — wymagane rozszerzenia VSCode
- `opencode.json` — konfiguracja projektu z sub-agentem `@code_checker`
