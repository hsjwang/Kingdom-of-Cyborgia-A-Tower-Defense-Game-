# Contributing to Kingdom of Cyborgia

Thank you for your interest in extending the game. This guide explains how to add new MITRE ATT&CK techniques and defensive countermeasures, which is the most common and impactful contribution.

All game content lives in a single file: **`engine/schema.py`**. The engine and frontend pick up additions automatically, with one exception documented under [Beginner-mode visibility](#beginner-mode-visibility).

`engine/schema.yaml` mirrors `schema.py` as human-readable documentation. **It is not loaded by the game.** If you change content, change `schema.py` and update the YAML to match.

---

## Three taxonomies, and why the distinction matters

This is the single most common source of confusion in the codebase, so it is worth stating plainly:

| Prefix | What it is | Example |
|---|---|---|
| `T####` | ATT&CK **Technique** — an adversary behaviour, i.e. an attack in the game | T1566 Phishing |
| `M####` | ATT&CK **Mitigation** — a broad category of defensive practice, i.e. a purchasable defense | M1049 Antivirus |
| `D3-*` | D3FEND **Technique** — a specific mechanism that implements a mitigation | D3-FH File Hashing |

A purchasable defense in this game is an **ATT&CK Mitigation**, not a D3FEND technique. Earlier revisions of this guide called them "D3FEND mitigations" and described `M####` as a D3FEND identifier. Both were wrong.

D3FEND publishes mappings from its countermeasures to ATT&CK **Techniques**, not to ATT&CK **Mitigations**. There is therefore no published `M####` → `D3-*` crosswalk, and the one in this project is an alignment we authored. Bear that in mind when adding entries.

---

## Adding a new defense (ATT&CK Mitigation)

Add an entry to `defenses_dict` in `engine/schema.py`. The key is the ATT&CK Mitigation ID.

```python
"M1030": Defense(
    "M1030",                       # ATT&CK Mitigation ID (also the dict key)
    "Network Segmentation",        # name, as ATT&CK states it
    250,                           # cost in gold (100-300)
    "Architect sections of the network to isolate critical systems.",
    "VLANs separating guest Wi-Fi from internal servers; DMZ architecture.",
    "The Moat",                    # story name shown to the player
    "A wide moat divides the castle into inner and outer keeps.",
    d3fend=[("D3-BDI", "Broadcast Domain Isolation")],
),
```

The `d3fend` argument is optional and takes a list of `(id, name)` pairs. A mitigation may map to several.

### D3FEND mapping rules

**Leaf techniques only.** Never use a D3FEND parent class. Searching D3FEND for the mechanism a mitigation names will very often surface a parent class first, because ATT&CK Mitigations sit at roughly the same level of abstraction as D3FEND's classes. The implementing mechanisms are one level below. Known traps:

| Do not use | Because it contains |
|---|---|
| D3-CH Credential Hardening | D3-MFA (on M1032), D3-SPP (on M1027) |
| D3-NTA Network Traffic Analysis | D3-NTSA, D3-ANAA (on M1037), D3-CAA (on M1031) |
| D3-UBA User Behavior Analysis | D3-LAM (on M1040) |
| D3-NI Network Isolation | D3-BDI (on M1030) |
| D3-CE Credential Eviction | D3-CR, D3-RIC |

Assigning both a parent and its own child to one mitigation makes the mapping mean two different things at once.

**If no equivalent exists, say so explicitly.** D3FEND models only technical countermeasures, so human-centered and policy-posture controls legitimately have none. Pass no `d3fend` argument and add the key to the `D3FEND_NO_EQUIVALENT` set in `schema.py`, which distinguishes "looked up and absent" from "not yet looked up". Four mitigations are currently in that set: M1017 User Training, M1029 Remote Data Storage, M1033 Limit Software Installation, M1042 Disable or Remove Feature.

Do not force a match. A documented gap is more useful than a wrong mapping.

**Verify against the primary sources:** [MITRE ATT&CK Mitigations](https://attack.mitre.org/mitigations/enterprise/) and [MITRE D3FEND](https://d3fend.mitre.org).

### Cost guidelines

- **100** — low-cost, broadly useful (Audit, Data Backup)
- **150–200** — medium-cost, targeted (User Training, OS Hardening, Antivirus)
- **250–300** — high-cost, powerful (MFA, PAM, Permissions, Web Restrict)

---

## Adding a new attack (ATT&CK Technique)

Add an entry to `attacks_dict`. The key is the ATT&CK Technique ID.

```python
"T1110": Attack(
    "T1110",
    "Brute Force",
    "Adversaries may use brute force to gain access to accounts when "
    "passwords are unknown or hashes are obtained.",
    "Tools like Hydra attempting thousands of combinations against a portal.",
    ["M1032", "M1026", "M1028", "M1047"],   # mitigation keys that counter it
    "The Battering Ram",
    "A ram crashes against the gate, trying every angle until the lock gives way.",
),
```

### Mapping defenses to an attack

Map only mitigations that genuinely counter the technique according to ATT&CK's own mitigation list for it. Existing attacks range from 1 to 11 mapped mitigations, reflecting ATT&CK's real data rather than a target count.

**Understand how scoring uses this list before you tune it.** A level passes when deployed defenses cover at least 70% of the mapped mitigations **that are currently purchasable**, for every active attack. The denominator is the intersection of your `defenses` list with the cabinet available in the current mode — not the full list. So:

- Adding mappings that are *not* in `VISIBLE_DEFENSES` does not change Beginner-mode difficulty at all.
- Adding mappings that *are* visible raises the number of purchases needed, since 70% of a larger set is more defenses.
- An attack whose entire mapped set is unavailable in the current cabinet scores 0 and cannot be passed. Random mode guards against this by validating that a drawn attack set is defendable with the unlocked cabinet before it is used; Beginner and Custom mode do not, so check your own additions.

Confirm a new attack is passable at each level's budget before opening a pull request.

---

## Beginner-mode visibility

`schema.py` defines two subset lists that control what Beginner mode exposes:

```python
VISIBLE_DEFENSES = [...]   # currently 11 of 26
VISIBLE_ATTACKS  = [...]   # currently 5 of 10
```

**Adding to `defenses_dict` or `attacks_dict` alone will not make your content appear in Beginner mode.** Add the key to the relevant list as well. Content outside these lists is reachable in Random mode, which draws from the full pool, and in Custom mode, where the instructor selects explicitly.

Keep Beginner mode small. It is the first thing a new player sees, and a large cabinet presented at once is the main cognitive-load risk in the design.

---

## Adding images

Each attack and defense displays an icon. Add a PNG named with the MITRE identifier to `images/`:

```
images/T1110.png    # attack
images/M1030.png    # defense
```

Recommended size 64×64 or 128×128. Missing images fall back to a placeholder, so the game will not crash, but adding one improves the experience.

---

## Game modes and level structure

| Mode | Attacks | Cabinet | Levels | Start |
|---|---|---|---|---|
| `BEGINNER` | Disclosed in advance via Intel Report; drawn from `VISIBLE_ATTACKS` | All 11 visible defenses from the start | 3 | 100 HP, 700 gold |
| `RANDOM` | Undisclosed; validated sets of 1–3 drawn from the full pool without repeats until the cycle exhausts | 10 unlocked initially, +5 per level | Endless | 100 HP, 700 gold |
| `CUSTOM` | Instructor-selected | Instructor-selected | 3 | 125 HP, 1000 gold |

Mode parameters live in `GAME_MODE_SETTINGS` and the `RANDOM_*` constants at the top of `engine/game_server.py`. Note that Beginner mode draws its attacks randomly from the visible pool; it is disclosed, not fixed. Use `CYBORGIA_SEED` if you need a repeatable scenario.

Passing a level awards +450 gold and +25 health; failing costs 25 health and grants a scaled emergency budget (100/200/300/400 by failure count). Defenses persist across levels.

---

## Session telemetry

`engine/telemetry.py` writes a local, network-free JSONL log per session for classroom research. It records purchase order, budget left unspent, retries, coverage scores, and per-phase durations under an instructor-assigned participant code, with no other identifying information.

| Variable | Effect |
|---|---|
| `CYBORGIA_PARTICIPANT` | Participant code, e.g. `S014`. Unset generates `ANON-XXXXXX`. |
| `CYBORGIA_TELEMETRY` | `0` disables logging entirely. |
| `CYBORGIA_TELEMETRY_DIR` | Override the output directory. |
| `CYBORGIA_SEED` | Fix the random seed so every player faces the same attack draw. |

Output goes to `~/KingdomOfCyborgia_Data/`, falling back to the system temp directory if that is not writable. See `docs/TELEMETRY.md` for the full event schema.

Every telemetry method swallows its own exceptions and self-disables on failure, so logging can never crash the game. If you add hooks, preserve that property — use the `@_never_raises` decorator.

---

## Testing your changes

```bash
python -m gui.main_gui
```

Verify in **all three modes**:

1. Your new attack appears and animates correctly
2. Your new defense appears in the cabinet at the correct cost
3. The Guidebook shows the control name, the ATT&CK Mitigation ID, and the D3FEND technique. Check the longest entries for text overflow — currently Web Restrict, User Account Management, and Encrypt Sensitive Information
4. The Debrief screen credits your defense as blocking the attack
5. The Incident Report identifies your attack as a breach when undefended
6. The level is passable at the available budget

Then confirm `schema.yaml` still matches `schema.py`, and run once with `CYBORGIA_TELEMETRY_DIR=/nonexistent` to confirm the game plays normally with logging disabled.

---

## Submitting changes

1. Fork the repository
2. Create a branch: `git checkout -b add-T1110-brute-force`
3. Edit `engine/schema.py`, add images, update `VISIBLE_*` if needed, and update `engine/schema.yaml`
4. Test thoroughly
5. Open a pull request describing the technique or mitigation added, with a link to its MITRE page and a note on any D3FEND mapping decision you made

---

## Questions

Open an issue or contact the team at **[YOUR CONTACT EMAIL]**.
