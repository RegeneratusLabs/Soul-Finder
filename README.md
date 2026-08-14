# Soul Finder

Soul Finder is a plugin for Hermes Agent that helps you build or fix your agent's personality.

If you use Hermes, your agent has a personality file called `SOUL.md`. It's how your agent talks, what it cares about, and what it won't do. It usually starts out great — then slowly turns into a mess: old project notes, corporate language, a voice that sounds like a robot reading a style guide.

Soul Finder does two jobs:

1. **First-run onboarding** — if a profile has no SOUL.md yet, the agent offers to build one. Once. If you say skip, it never asks again.
2. **Refinement** — walks you through cleaning up a SOUL.md that's gone stale: seeing what's in there, keeping the good stuff, cutting the clutter, and making the voice sound like a person again.

## What you need

- Hermes Agent (the app your agent runs in)
- No technical skills. If you can copy and paste a link, you can install this.

## Install

Open a terminal and run:

```
hermes plugins install RegeneratusLabs/soul-finder
hermes plugins enable soul-finder
```

Then restart Hermes (start a new session, or restart the gateway). That's the whole install.

## How to use it

**New agent, no personality yet?** Just start a conversation. The agent will offer to build your SOUL.md — answer a few plain questions and it's done. Say "skip" and it won't bring it up again.

**Already have a personality that feels off?** Type `/soul` in a chat and the agent will walk you through refining it.

## What's in the box

- The plugin itself (`__init__.py`)
- The full workflow skill (`skills/soul-finder/SKILL.md`) — audit, condense, and inject personality without losing what's yours
- A worked example showing a flat, corporate voice turned into a human one
- Screenshots of the whole flow running in the terminal and the desktop app

## Similar tools

[Soul Forge](https://github.com/LeventeNagy/soul-forge) by Levente Nagy generates new SOUL.md files from templates. Soul Finder is for onboarding and refining one you already have. Different jobs — they work well side by side.

## Credit

The `SOUL.md` format was created by the team at [Nous Research](https://github.com/NousResearch/hermes-agent) for Hermes Agent. Soul Finder is based on the soul-builder plugin from the Hermes plugin ecosystem — we fixed a loading bug and made the first-run onboarding work on every surface. The credit for the format and the original plugin belongs to its creators.

## License

MIT
