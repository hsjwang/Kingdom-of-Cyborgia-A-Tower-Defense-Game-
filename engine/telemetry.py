"""Local, privacy-preserving telemetry for classroom deployments.

Design constraints:
  * No network. Everything is written to a local file the student submits.
  * No personally identifying information. Only a participant code that the
    student is given by the instructor (or an anonymous random code).
  * Never crash the game. Every public method swallows its own exceptions,
    so a telemetry failure can never interrupt gameplay.
  * Append-and-flush, one JSON object per line, so a crash or force-quit
    still leaves a usable partial record.

Output: ~/KingdomOfCyborgia_Data/cyborgia_<code>_<timestamp>.jsonl

Usage (already wired into engine/game_server.py):

    from engine.telemetry import TelemetrySession
    t = TelemetrySession()                  # anonymous code
    t = TelemetrySession(participant_code="S014")
    t.session_start("BEGINNER", 100, 700)
    t.purchase("M1047", "Audit", 100, 600, 1)
    t.round_result(75.0, True, ["M1047"], 600, 125, 1, ["T1566"])
    t.session_end()
    print(t.output_path)
"""

from __future__ import annotations

import functools
import json
import os
import random
import string
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = 1

#: Set CYBORGIA_TELEMETRY=0 to disable logging entirely.
ENV_ENABLE = "CYBORGIA_TELEMETRY"
#: Set CYBORGIA_PARTICIPANT=S014 to supply the code without a prompt.
ENV_PARTICIPANT = "CYBORGIA_PARTICIPANT"
#: Set CYBORGIA_TELEMETRY_DIR to override the output directory.
ENV_DIR = "CYBORGIA_TELEMETRY_DIR"

DEFAULT_DIRNAME = "KingdomOfCyborgia_Data"


def _never_raises(method):
    """Telemetry must never be the reason the game stops working."""

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not getattr(self, "enabled", False):
            return None
        try:
            return method(self, *args, **kwargs)
        except Exception:  # noqa: BLE001 - deliberate catch-all
            self.enabled = False
            return None

    return wrapper


def _anonymous_code(length: int = 6) -> str:
    alphabet = string.ascii_uppercase + string.digits
    return "ANON-" + "".join(random.choice(alphabet) for _ in range(length))


def _resolve_output_dir() -> Path:
    """Pick a writable directory. PyInstaller bundles are often read-only."""
    override = os.environ.get(ENV_DIR)
    candidates = []
    if override:
        candidates.append(Path(override))
    candidates.append(Path.home() / DEFAULT_DIRNAME)
    candidates.append(Path(tempfile.gettempdir()) / DEFAULT_DIRNAME)

    for candidate in candidates:
        try:
            candidate.mkdir(parents=True, exist_ok=True)
            probe = candidate / ".write_probe"
            probe.write_text("ok", encoding="utf-8")
            probe.unlink()
            return candidate
        except Exception:  # noqa: BLE001
            continue
    raise OSError("No writable telemetry directory found")


class TelemetrySession:
    """Append-only event log for one play session."""

    def __init__(self, participant_code: str | None = None, enabled: bool | None = None):
        self.enabled = False
        self.output_path: Path | None = None
        self._handle = None
        self._t0 = time.monotonic()
        self._phase_t0 = time.monotonic()
        self._event_seq = 0
        self._purchase_seq = 0
        self.participant_code = "UNSET"

        if enabled is None:
            enabled = os.environ.get(ENV_ENABLE, "1").strip().lower() not in {
                "0",
                "false",
                "no",
                "off",
            }
        if not enabled:
            return

        try:
            code = (
                participant_code
                or os.environ.get(ENV_PARTICIPANT)
                or _anonymous_code()
            )
            self.participant_code = str(code).strip()[:32] or _anonymous_code()

            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            safe_code = "".join(
                ch if ch.isalnum() or ch in "-_" else "_" for ch in self.participant_code
            )
            directory = _resolve_output_dir()
            self.output_path = directory / f"cyborgia_{safe_code}_{stamp}.jsonl"
            self._handle = self.output_path.open("a", encoding="utf-8")
            self.enabled = True
            self._write(
                "file_open",
                {
                    "schema_version": SCHEMA_VERSION,
                    "participant_code": self.participant_code,
                    "utc": datetime.now(timezone.utc).isoformat(),
                },
            )
        except Exception:  # noqa: BLE001
            self.enabled = False
            self._handle = None

    # -- internals ---------------------------------------------------------

    def _write(self, event: str, payload: dict) -> None:
        self._event_seq += 1
        record = {
            "seq": self._event_seq,
            "t": round(time.monotonic() - self._t0, 3),
            "event": event,
        }
        record.update(payload)
        self._handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        self._handle.flush()

    def _mark_phase(self) -> float:
        now = time.monotonic()
        elapsed = round(now - self._phase_t0, 3)
        self._phase_t0 = now
        return elapsed

    # -- public API --------------------------------------------------------

    @_never_raises
    def session_start(self, mode, health, budget, available_defenses=None,
                      available_attacks=None):
        self._t0 = time.monotonic()
        self._phase_t0 = self._t0
        self._purchase_seq = 0
        self._write(
            "session_start",
            {
                "mode": mode,
                "health": health,
                "budget": budget,
                "n_available_defenses": len(available_defenses) if available_defenses else None,
                "n_available_attacks": len(available_attacks) if available_attacks else None,
            },
        )

    @_never_raises
    def level_start(self, level, mode, attacks, available_defenses,
                    active_defenses, budget, health):
        self._purchase_seq = 0
        self._write(
            "level_start",
            {
                "level": level,
                "mode": mode,
                "attacks": list(attacks or []),
                "available_defenses": sorted(available_defenses or []),
                "carried_defenses": sorted(active_defenses or []),
                "budget": budget,
                "health": health,
            },
        )

    @_never_raises
    def purchase(self, defense_id, defense_name, cost, budget_after, level):
        self._purchase_seq += 1
        self._write(
            "purchase",
            {
                "order": self._purchase_seq,
                "defense_id": defense_id,
                "defense_name": defense_name,
                "cost": cost,
                "budget_after": budget_after,
                "level": level,
            },
        )

    @_never_raises
    def purchase_rejected(self, defense_id, reason, budget, level):
        self._write(
            "purchase_rejected",
            {
                "defense_id": defense_id,
                "reason": str(reason)[:200],
                "budget": budget,
                "level": level,
            },
        )

    @_never_raises
    def refund(self, defense_id, defense_name, cost, budget_after, level):
        self._write(
            "refund",
            {
                "defense_id": defense_id,
                "defense_name": defense_name,
                "refund": cost,
                "budget_after": budget_after,
                "level": level,
            },
        )

    @_never_raises
    def launch(self, level, attacks, active_defenses, budget_unspent):
        self._write(
            "launch",
            {
                "level": level,
                "attacks": list(attacks or []),
                "deployed_defenses": sorted(active_defenses or []),
                "n_deployed": len(active_defenses or []),
                "budget_unspent": budget_unspent,
                "build_phase_seconds": self._mark_phase(),
            },
        )

    @_never_raises
    def round_result(self, score, success, active_defenses, budget, health,
                     level, attacks, failures=None):
        self._write(
            "round_result",
            {
                "level": level,
                "attacks": list(attacks or []),
                "coverage_score": round(float(score), 2),
                "passed": bool(success),
                "deployed_defenses": sorted(active_defenses or []),
                "budget_after": budget,
                "health_after": health,
                "cumulative_failures": failures,
                "resolve_seconds": self._mark_phase(),
            },
        )

    @_never_raises
    def level_complete(self, from_level, to_level, budget, health):
        self._write(
            "level_complete",
            {
                "from_level": from_level,
                "to_level": to_level,
                "budget": budget,
                "health": health,
            },
        )

    @_never_raises
    def game_over(self, level, health, budget, failures, attacks):
        self._write(
            "game_over",
            {
                "level": level,
                "health": health,
                "budget": budget,
                "cumulative_failures": failures,
                "final_attacks": list(attacks or []),
            },
        )

    @_never_raises
    def game_complete(self, level, health, budget, failures):
        self._write(
            "game_complete",
            {
                "level": level,
                "health": health,
                "budget": budget,
                "cumulative_failures": failures,
            },
        )

    @_never_raises
    def note(self, label, **fields):
        """Free-form marker, e.g. guidebook opens or survey handoff."""
        payload = {"label": str(label)[:64]}
        payload.update(fields)
        self._write("note", payload)

    @_never_raises
    def session_end(self, reason="exit"):
        self._write(
            "session_end",
            {
                "reason": reason,
                "total_seconds": round(time.monotonic() - self._t0, 3),
            },
        )
        try:
            self._handle.close()
        finally:
            self.enabled = False

    # -- convenience -------------------------------------------------------

    def where(self) -> str:
        if self.output_path is None:
            return "telemetry disabled"
        return str(self.output_path)
