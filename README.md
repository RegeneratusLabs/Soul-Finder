# SOUL.md Refinement Workflow

A Hermes Agent skill for separating durable voice from project context, condensing a bloated personality file down to essentials, and injecting real heat when a SOUL.md reads like a corporate style guide.

## Why this exists

Agent personalities rot. A SOUL.md starts tight and accretes: project details, technical conventions, user background, and a voice section that slowly turns into a grammar guide. When the agent stops sounding like a person, the file has become a liability.

This skill is the cleanup process — and it treats a SOUL.md as two different things depending on what it's for:

| Class | Purpose | Size |
|-------|---------|------|
| **Voice SOUL.md** | Personal assistant / bot voice. Pure tone and style. | ~15–30 lines |
| **Persona SOUL.md** | Full character with operating philosophy. Strategic substance kept intact, heat injected into the voice. | 60–100+ lines |

## The workflow

1. **Audit** — read the current SOUL.md, identify mixed concerns (personality stays, project details move to AGENTS.md or memory, technical conventions move to AGENTS.md).
2. **Draft** — identify the class, then write lean. For Persona-class, preserve the earned strategic sections and rewrite only the voice.
3. **Personality injection** — when a SOUL.md is flat: keep the strategic bones, rewrite the voice with active, punchy language and permission to be casual. Call out what the persona is *for*.
4. **Iterate** — present, condense, iterate. The user will say "more like this, less like that" — expect the loop.
5. **Ship** — explicit user approval, write to `~/.hermes/SOUL.md`, update memory. **Sync to every profile** that should carry the persona — SOUL.md is per-profile (`~/.hermes/profiles/<name>/SOUL.md`), and existing sessions won't pick up changes.

## Pitfalls this skill encodes

- **SOUL.md is per-profile.** Editing the default profile's file does not touch other profiles, which keep their own (often stock) SOUL.md.
- **The desktop app's new-session greeting is NOT driven by SOUL.md.** It reads `display.personality` from config.yaml — and that setting also injects a personality preamble into the system prompt (e.g. `hype` injects "YOOO LET'S GOOOO!!!..."). For persona work, leave it empty; the SOUL is the voice.
- **Plugin message injection is interactive-CLI-only.** The `on_session_start` hook can't inject messages into desktop/gateway sessions (no session key at that point). Model-driven onboarding via a system-prompt section is the portable pattern.
- **Cheeky ≠ bitchy.** When injecting heat into a fun persona, lead with warmth, edge second. Default to "mate's heart" energy.

## Contents

- `SKILL.md` — the workflow itself
- `references/personality-injection-example.md` — before/after case study (flat CEO voice → human energy)
- `screenshots/` — the first-run onboarding flow in the TUI and desktop app

## License

MIT
