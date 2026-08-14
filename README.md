# Soul Finder

A Hermes Agent skill for refining `SOUL.md` personality files — separating durable voice from project context, condensing to essentials, and injecting personality when a soul reads flat.

## What it does

- Audits an existing `SOUL.md` for mixed concerns (personality vs project context)
- Distinguishes **Voice-class** (~15–30 lines, pure tone) from **Persona-class** (60–100+ lines, strategic substance plus voice)
- Rewrites flat voice sections with active, human language while preserving earned operating principles
- Iterates with the user and ships only after explicit approval

## Usage

Install as a Hermes skill and load it when refining a `SOUL.md`:

```bash
cp -r SKILL.md references ~/.hermes/skills/<category>/soul-finder/
```

Then load it in a session with `/skill soul-finder`.

## Contents

- `SKILL.md` — the workflow
- `references/personality-injection-example.md` — before/after voice rewrite example
- `screenshots/` — first-run onboarding flow in the TUI and desktop app

## Credits

`SOUL.md` is the identity file format of [Hermes Agent](https://github.com/NousResearch/hermes-agent) by Nous Research. This skill is a workflow for working with that format, and it builds on the soul-builder plugin from the Hermes plugin ecosystem. Credit for the format belongs to its original creators.

## License

MIT
