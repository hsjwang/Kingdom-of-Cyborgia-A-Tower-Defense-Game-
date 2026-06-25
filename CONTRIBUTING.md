# Contributing to Kingdom of Cyborgia

Thank you for your interest in extending the game. This guide explains how to add new ATT&CK techniques and D3FEND mitigations, which is the most common and impactful contribution.

All game content — attacks and defenses — lives in a single file: **`engine/schema.py`**. The game engine and frontend automatically pick up any additions to that file. No other code changes are required.

---

## Adding a New Defense (D3FEND Mitigation)

Open `engine/schema.py` and add a new entry to `defenses_dict`. Each entry follows this pattern:

```python
"YourKey": Defense(
    name="Display Name",           # MITRE D3FEND mitigation name
    mitre_id="M1XXX",              # MITRE D3FEND identifier
    cost=200,                      # Gold cost (100–300 recommended)
    mitre_description="...",       # Technical description from D3FEND
    real_world_examples="...",     # One or two concrete real-world tools/examples
    story_name="The Story Name",   # Fantasy name shown to the player
    story_description="..."        # Fantasy description of the defense
)
```

**Example — adding Network Segmentation (M1030):**

```python
"NetSegment": Defense(
    name="Network Segmentation",
    mitre_id="M1030",
    cost=250,
    mitre_description="Architect sections of the network to isolate critical systems, functions, or resources.",
    real_world_examples="VLANs separating guest Wi-Fi from internal servers; DMZ architecture for public-facing services.",
    story_name="The Moat",
    story_description="A wide moat divides the castle into protected inner and outer keeps, ensuring that even if the outer walls fall, the throne room remains defended."
)
```

**Cost guidelines:**
- 100 — Low-cost, broadly useful (e.g., Audit, Data Backup)
- 150–200 — Medium-cost, targeted mitigations
- 250–300 — High-cost, powerful mitigations (e.g., MFA, PAM, Web Restrict)

Keep the total cost of valid defenses for any one attack within a range that is achievable in a single level's budget — otherwise the level may become unbeatable.

---

## Adding a New Attack (ATT&CK Technique)

Add a new entry to `attacks_dict` in `engine/schema.py`:

```python
"TXXXX": Attack(
    mitre_id="TXXXX",             # MITRE ATT&CK technique ID
    name="Technique Name",         # MITRE ATT&CK technique name
    mitre_description="...",       # Technical description from ATT&CK
    real_world_examples="...",     # One or two concrete real-world examples
    defenses=["Key1", "Key2"],     # List of defense keys from defenses_dict
    story_name="The Story Name",   # Fantasy name shown to the player
    story_description="..."        # Fantasy description of the attack
)
```

**Example — adding Brute Force (T1110):**

```python
"T1110": Attack(
    mitre_id="T1110",
    name="Brute Force",
    mitre_description="Adversaries may use brute force techniques to gain access to accounts when passwords are unknown or when password hashes are obtained.",
    real_world_examples="Automated tools like Hydra or Hashcat attempting thousands of password combinations per second against a login portal.",
    defenses=["MFA", "PAM", "OSConfig", "Audit"],
    story_name="The Battering Ram",
    story_description="A massive battering ram crashes against the castle gate again and again, trying every combination of force and angle until the lock gives way."
)
```

**Defense mapping guidelines:**
- Map only defenses that genuinely mitigate the technique per the MITRE frameworks
- Aim for 3–5 valid defenses per attack — fewer than 3 makes the attack trivial; more than 6 makes it easy to stumble into a pass without strategic thinking
- Verify your mappings against [MITRE ATT&CK](https://attack.mitre.org) and [MITRE D3FEND](https://d3fend.mitre.org)

---

## Adding an Attack Image

Each attack displays a visual icon during the Attack Phase. Add a PNG image named with the ATT&CK technique ID to the `images/` folder:

```
images/T1110.png    # for Brute Force
```

Recommended size: 64×64px or 128×128px. The game will fall back gracefully if the image is missing, but adding one improves the visual experience.

---

## Level Scaling

The game currently uses a fixed level structure:
- Level 1: 1 random attack
- Level 2: 2 random attacks
- Level 3: 3 random attacks

Adding more attacks to `attacks_dict` automatically increases the pool from which each level's attacks are randomly drawn. The level count itself is controlled in `engine/game_server.py`.

---

## Testing Your Changes

Run the game from source after making changes:

```bash
python -m gui.main_gui
```

Play through all three levels and verify:
1. Your new attack appears and animates correctly
2. Your new defense appears in the cabinet with the correct cost
3. The Debrief screen correctly identifies your defense as blocking the attack
4. The Incident Report correctly identifies your attack as a breach when undefended

---

## Submitting Changes

1. Fork the repository
2. Create a branch: `git checkout -b add-T1110-brute-force`
3. Make your changes to `engine/schema.py` and `images/`
4. Test thoroughly
5. Open a pull request with a brief description of the technique or mitigation added and a link to its MITRE page

---

## Questions

Open an issue or contact the team at **[YOUR CONTACT EMAIL]**.
