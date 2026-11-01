"""Soul Finder — build or refine your agent's SOUL.md personality.

One plugin, two flows:
  NEW    — first-run interview that drafts a SOUL.md from scratch (voice-class).
  REFINE — audits an existing SOUL.md against the gold-standard structure,
           asks targeted gap questions, and ships a diff.

Trigger surface:
  /soul [new|refine|status]   slash command (auto-detects mode with no args)
  on_session_start hook       one-time first-run nudge (never nags again)
  plugin:soul-finder          bundled workflow skill (the real product)
  soul_finder_status          tool — file/mode state for the agent
  soul_finder_complete        tool — marks flow finished after user-approved write
"""

import json
import os
from pathlib import Path

PLUGIN_DIR = Path(__file__).parent

# --------------------------------------------------------------------------
# State — two booleans in the plugin's own PluginState (profile-scoped, under
# $HERMES_HOME/plugin-data/). Bound to ctx.state in register(); nothing is
# written into the plugin checkout, so an update never trips over local files.
# --------------------------------------------------------------------------

_STATE = None


def _flag(name: str) -> bool:
    return bool(_STATE.get(name, False)) if _STATE is not None else False


def _set_flag(name: str) -> None:
    if _STATE is not None:
        _STATE.set(name, True)


def _soul_path() -> Path:
    """Resolve $HERMES_HOME/SOUL.md (profile-safe)."""
    try:
        from hermes_constants import get_hermes_home  # type: ignore
        return Path(get_hermes_home()) / "SOUL.md"
    except Exception:
        home = os.environ.get("HERMES_HOME")
        base = Path(home).expanduser() if home else Path.home() / ".hermes"
        return base / "SOUL.md"


def _has_real_soul() -> bool:
    """Heuristic: a meaningful SOUL.md exists (not missing / not a tiny seed)."""
    p = _soul_path()
    if not p.exists():
        return False
    try:
        text = p.read_text(encoding="utf-8")
    except Exception:
        return False
    non_blank = [ln for ln in text.splitlines() if ln.strip()]
    return len(non_blank) >= 8 and len(text) >= 200


def _mode() -> str:
    """new if there's no real soul yet; refine if one exists and is meaningful."""
    return "refine" if _has_real_soul() else "new"


def _status() -> str:
    p = _soul_path()
    return json.dumps({
        "mode": _mode(),
        "soul_path": str(p),
        "soul_exists": p.exists(),
        "soul_size": p.stat().st_size if p.exists() else 0,
        "flow_complete": _flag("flow_complete"),
        "nudge_sent": _flag("nudge_sent"),
    })


def _mark_complete() -> str:
    _set_flag("flow_complete")
    return json.dumps({"success": True, "message": "SOUL.md flow marked complete"})


# --------------------------------------------------------------------------
# Kickoff messages
# --------------------------------------------------------------------------

KICKOFF_NEW = (
    "Let's build my SOUL.md — the personality file that shapes every "
    "conversation. Load the skill `plugin:soul-finder` and walk me through it. "
    "Start with the mode question."
)

KICKOFF_REFINE = (
    "Let's audit my SOUL.md. Load the skill `plugin:soul-finder`, read "
    "$HERMES_HOME/SOUL.md, compare it against the gold-standard structure, "
    "and walk me through the refine flow."
)

NUDGE = (
    "👋 Quick one before we dive in: your agent's voice lives in SOUL.md — it's "
    "the first thing loaded into every conversation. Want to shape it now? "
    "I'll walk you through it in ~5 minutes. (Just say 'skip' if you'd rather "
    "get on with things — I won't ask again.)"
)


# --------------------------------------------------------------------------
# register()
# --------------------------------------------------------------------------

def register(ctx):
    global _STATE
    # ``state`` is a property on the real PluginContext; the catalog's
    # capability probe exposes methods only, so bind defensively.
    _STATE = getattr(ctx, "state", None)

    # --- Slash command: /soul [new|refine|status] -------------------------
    def soul_cmd(raw_args: str):
        arg = (raw_args or "").strip().lower()
        if arg in ("status", "info", "check"):
            ctx.inject_message(
                "Run `soul_finder_status` and report what it returns.",
                role="user")
        elif arg == "new":
            ctx.inject_message(KICKOFF_NEW, role="user")
        elif arg == "refine":
            ctx.inject_message(KICKOFF_REFINE, role="user")
        else:
            kick = KICKOFF_NEW if _mode() == "new" else KICKOFF_REFINE
            ctx.inject_message(kick, role="user")
        return json.dumps({"ok": True})

    ctx.register_command(
        "soul",
        soul_cmd,
        description="Build or refine your SOUL.md (new|refine|status)",
    )

    # --- First-run nudge: once per profile, never again -------------------
    def on_session_start(session_id, model, platform, **kwargs):
        if _flag("nudge_sent") or _flag("flow_complete"):
            return
        # Don't nudge people who already have a real soul (hand-written).
        if _has_real_soul():
            _set_flag("nudge_sent")
            return
        # Only mark the nudge as sent if the injection actually landed.
        # In desktop/gateway surfaces injection may be unavailable — the
        # system-prompt section (below) drives the offer there instead.
        if ctx.inject_message(NUDGE, role="user"):
            _set_flag("nudge_sent")

    ctx.register_hook("on_session_start", on_session_start)

    # --- Model-driven first-run offer (works in every surface) ------------
    def _first_run_section(session_info):
        # Deterministic offer-once: rendering this section IS the nudge.
        # The marker is written here by the plugin (not left to the model),
        # so a user who declines is NEVER asked again — no dependence on
        # model behavior or tool calls.
        if _flag("flow_complete") or _has_real_soul() or _flag("nudge_sent"):
            return ""
        _set_flag("nudge_sent")
        return (
            "FIRST-RUN ONBOARDING: this profile has no SOUL.md yet — the file that "
            "defines the agent's personality and voice, loaded into every "
            "conversation. Offer once to create one: "
            "'Your agent's voice lives in SOUL.md — want to shape it now? "
            "Takes ~5 minutes, or say skip.' If the user accepts, load the "
            "`plugin:soul-finder` skill and walk them through the interview. If "
            "they decline, accept it and move on — don't push, and don't repeat "
            "the offer in future sessions."
        )

    ctx.register_system_prompt_section(
        "soul-finder-first-run",
        _first_run_section,
        position="after_memory",
    )

    # --- Bundled workflow skill -------------------------------------------
    skill_path = PLUGIN_DIR / "skills" / "soul-finder" / "SKILL.md"
    if skill_path.exists():
        ctx.register_skill("soul-finder", skill_path)

    # --- Tools ------------------------------------------------------------
    ctx.register_tool(
        name="soul_finder_status",
        toolset="soul_finder",
        schema={
            "name": "soul_finder_status",
            "description": (
                "Return SOUL.md state: mode (new|refine), path, size, "
                "completion markers. Use before starting a soul flow."
            ),
            "parameters": {"type": "object", "properties": {}},
        },
        handler=lambda params, **kw: _status(),
    )

    ctx.register_tool(
        name="soul_finder_complete",
        toolset="soul_finder",
        schema={
            "name": "soul_finder_complete",
            "description": (
                "Mark the SOUL.md flow as finished. Call ONLY after the user "
                "explicitly approved and the file was written to "
                "$HERMES_HOME/SOUL.md."
            ),
            "parameters": {"type": "object", "properties": {}},
        },
        handler=lambda params, **kw: _mark_complete(),
    )
