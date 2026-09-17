# Classroom Telemetry

Local, network-free session logging for research deployments. Added in
`engine/telemetry.py`, hooked into `engine/game_server.py`.

## What it records

One JSON object per line (JSONL), flushed immediately so a force-quit still
leaves a usable partial file. Events:

| Event | Key fields |
|---|---|
| `session_start` | mode, starting health/budget |
| `level_start` | level, attacks drawn, available defenses, carried-over defenses |
| `purchase` | defense ID/name, cost, **purchase order**, budget after |
| `purchase_rejected` | defense ID, reason (e.g. insufficient funds) |
| `refund` | defense removed during Build Phase |
| `launch` | deployed set, **budget left unspent**, **Build Phase duration** |
| `round_result` | **coverage score**, pass/fail, health after, cumulative failures |
| `level_complete` | from/to level |
| `game_over` | level reached, failures |
| `session_end` | total session seconds |

The bolded fields are the ones you cannot recover after the fact and that a
survey cannot give you reliably. Purchase order in particular shows whether a
student reasoned about the threat or bought cheapest-first.

## Where the file goes

`~/KingdomOfCyborgia_Data/cyborgia_<code>_<UTC timestamp>.jsonl`

Falls back to the system temp directory if the home directory is not writable
(relevant for PyInstaller bundles and locked-down lab images). Students submit
this file.

## Environment variables

| Variable | Effect |
|---|---|
| `CYBORGIA_PARTICIPANT` | Participant code, e.g. `S014`. Unset generates `ANON-XXXXXX`. |
| `CYBORGIA_TELEMETRY` | `0` disables logging entirely. |
| `CYBORGIA_TELEMETRY_DIR` | Override output directory. |
| `CYBORGIA_SEED` | Fixes the random seed so every student faces the **same** attack draw. |

`CYBORGIA_SEED` matters for your Phase 1 run. Beginner mode calls
`random.sample()` to pick each level's attacks, so without a seed students get
different scenarios and their coverage scores are not comparable. Set the same
seed for the whole section.

Example launcher for a lab machine:

```bash
CYBORGIA_PARTICIPANT=S014 CYBORGIA_SEED=2026 python main.py   # Phase 1
CYBORGIA_PARTICIPANT=S014 python main.py                      # Phase 2, Random mode
```

## Privacy

No network calls, no hostname, no username, no filesystem paths beyond the
output file. The participant code is the only identifier and it is whatever you
assign. Nothing is written unless the game runs.

## Failure behavior

Every public method is wrapped so exceptions are swallowed and logging
self-disables. Telemetry cannot crash the game or interrupt a class. Verify by
running with `CYBORGIA_TELEMETRY_DIR=/nonexistent/path` — the game should play
normally with logging silently off.

## Two other fixes in the same patch

1. **Stale reward text.** The success message said `+250 Budget`;
   `logic.calculate_new_budget()` awards 450. Message corrected.

2. **Vestigial branch in `resolve_round()`.** The `if self.game_mode ==
   "RANDOM"` arm and its `else` were byte-identical. Collapsed to one call,
   with a comment explaining why: the docstring on
   `calculate_round_results()` describes standard mode scoring against the
   *full* schema mapping, and if anyone "fixes" the branch to match that,
   Beginner mode becomes unwinnable — T1566 caps at 4/6 = 67% and T1552 at
   5/11 = 45%, both under the 70% threshold. Worth correcting that docstring
   too.

## Verification performed

A scripted playthrough (`START_GAME` → purchases → rejection → refund →
`LOCK_DEFENSES` → `LAUNCH_ATTACK` → `RESOLVE_ROUND` → `EXIT`) produced all
expected events with correct coverage scores and phase timings. Seed
determinism confirmed: `CYBORGIA_SEED=42` yields the same Level 1 draw on
repeated runs. The pygame frontend was **not** exercised — please run the
actual GUI once before class.
