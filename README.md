# Soul Finder

Soul Finder is a plugin for Hermes Agent that helps you build or fix your agent's personality.

If you use Hermes, your agent has a personality file called `SOUL.md`. It's how your agent talks, what it cares about, and what it won't do. It usually ends up sounding like corporate language, a voice that sounds like a robot reading a style guide.

Soul Finder does two jobs:

1. **First-run onboarding** — if a profile has no SOUL.md yet, the agent offers to build one. Once. If you say skip, it never asks again.
2. **Refinement** — walks you through cleaning up a SOUL.md that's gone stale: seeing what's in there, keeping the good stuff, cutting the clutter, and making the voice sound like a person again. This is through a multi step questionnaire. 

## What you need

- Hermes Agent (the app your agent runs in)
- No technical skills. If you can copy and paste a link, you can install this.

## Install

Open a terminal (or point this repo at your Hermes agent) and run:

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


## What it touches

- **Reads** `$HERMES_HOME/SOUL.md` to decide which flow to run — new or refine.
- **Writes** `SOUL.md` only through the agent's own file tools, and only after you approve the draft it shows you.
- **Writes** two booleans to the plugin's own state file, `$HERMES_HOME/plugin-data/soul-finder/state.json`, so the first-run offer happens once and never nags again.
- No network calls, no credentials, nothing leaves your machine.

## License

MIT
