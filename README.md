# Kingdom of Cyborgia

**A tower-defense educational game that teaches MITRE ATT&CK and D3FEND concepts to high school students.**

Players take on the role of the Castellan — the defender of a castle kingdom under siege by the Shadow Guild. Each attack the Guild launches maps directly to a real [MITRE ATT&CK](https://attack.mitre.org) technique. Each defense the player deploys maps to a real [MITRE D3FEND](https://d3fend.mitre.org) mitigation. Players must allocate a limited budget strategically across three escalating levels, learning through consequence that cybersecurity is fundamentally about tradeoffs, resource allocation, and risk management under uncertainty.

Developed as an undergraduate capstone project. Presented at [SIGCSE TS 2027 — citation to be added upon publication].

---

## Quick Start

### For Mac Users
1. Download the latest release from the [Releases](../../releases) page and unzip the MacOS package.
2. Run the following command in Terminal to clear the macOS quarantine attribute:
   ```bash
   xattr -dr com.apple.quarantine "MITRE Game.app"
   ```
3. Launch **MITRE Game** from the folder.

### For Windows Users
1. Download the latest release from the [Releases](../../releases) page and unzip the Windows package.
2. Run **MITRE Game.exe** to begin.

No installation, internet connection, or prior software configuration required.

---

## What's Included

```
kingdom-of-cyborgia/
├── engine/
│   ├── game_server.py        # State management and phase transitions
│   ├── logic.py              # Budget, health, attack–defense mapping, round resolution
│   └── schema.py             # ATT&CK attack and D3FEND defense dictionaries
├── gui/
│   ├── main_gui.py           # Entry point and main game loop
│   ├── button.py             # Button and defense icon components
│   ├── view_renderer.py      # Screen rendering for all game states
│   ├── fire_particle.py      # Fire animation (game over screen)
│   ├── gui_state.py          # UI state management
│   ├── image_handling.py     # Asset loading
│   └── design_specs.py       # Colors, fonts, layout constants
├── images/                   # Game assets
├── fonts/                    # Font files
├── docs/
│   ├── MITRE Game Teacher Resource Guide.pdf
│   └── MITRE Game User Guide.pdf
├── requirements.txt
├── CITATION.cff
├── CONTRIBUTING.md
└── README.md
```

---

## Running from Source

**Requirements:** Python 3.11+

```bash
# Clone the repository
git clone https://github.com/[YOUR-USERNAME]/kingdom-of-cyborgia.git
cd kingdom-of-cyborgia

# Install dependencies
pip install -r requirements.txt

# Run the game
python -m gui.main_gui
```

---

## How to Play

The game progresses through three levels of escalating difficulty.

### Phase 1 — Build Phase
- Click the **Intel Report** button to see which attacks are incoming.
- Drag defenses from the cabinet onto the castle map to deploy them.
- Each defense displays its story name, MITRE D3FEND identifier, and technical description.
- Consult the **Guidebook** at any time for a full breakdown of every defense and attack.
- Defenses can be refunded by dragging them to the trash can during this phase.

### Phase 2 — Attack Phase
- Click **Launch Attack** when ready.
- Watch the Shadow Guild's attack animate toward the castle.
- Defenses are locked — no changes can be made once the attack is in flight.

### Phase 3 — Mission Debrief
- Your defenses must cover at least **70%** of the required mitigations for every active attack to pass.
- **Pass:** Receive a budget bonus and health boost before advancing to the next level.
- **Fail:** Lose health and receive a strategic hint. A scaled budget injection helps you retry.
- **Game Over:** The Incident Report identifies which attacks breached your defenses, maps each to its MITRE ATT&CK technique and real-world impact, and provides a professional advisory — modeling the post-incident analysis process used in security operations.

**Key rules:**
- Defenses persist across levels — build a layered posture over time.
- Health carries over between levels. If it hits zero, the kingdom falls.
- Budget wisely — not all defenses counter all attacks.

---

## MITRE ATT&CK / D3FEND Coverage

The current release covers **5 ATT&CK techniques** and **11 D3FEND mitigations**:

| ATT&CK Technique | ID | Story Name | Valid D3FEND Mitigations |
|---|---|---|---|
| Phishing | T1566 | Poisoned Messenger | Antivirus (M1049), Audit (M1047), Web Restrict (M1021), User Training (M1017) |
| Unsecured Credentials | T1552 | Undercover Spy | Audit (M1047), OS Hardening (M1028), PAM (M1026), Permissions (M1022), User Training (M1017) |
| Account Manipulation | T1098 | Corrupt Seneschal | MFA (M1032), OS Hardening (M1028), PAM (M1026), Permissions (M1022) |
| Obfuscated Files | T1027 | Trojan Crate | Antivirus (M1049), Audit (M1047), User Training (M1017) |
| Command & Scripting Interpreter | T1059 | Sorcerer's Script | Antivirus (M1049), Audit (M1047), PAM (M1026), Web Restrict (M1021) |

Planned future releases will expand coverage to a larger subset of the ATT&CK and D3FEND frameworks. See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add new techniques.

---

## For Educators

Download the **Teacher Resource Guide** from the `docs/` folder or the Releases page. It includes:
- Learning objectives aligned to the game's mechanics
- Suggested pre/post discussion questions
- A glossary of MITRE ATT&CK and D3FEND terms encountered in the game
- Three classroom integration patterns:
  - **Standalone session** (45–60 minutes): Play, then debrief using Incident Reports as discussion artifacts
  - **Curriculum complement**: Deploy at the start of a cybersecurity unit to motivate the content that follows
  - **Enrichment/after-school**: GenCyber camps, CyberPatriot prep, cybersecurity clubs

The game requires no installation, internet access, or prior technical knowledge from instructors or students.

---

## Collaborators Wanted

We are actively seeking educators and researchers interested in deploying the game and collecting pre/post evaluation data. We are particularly interested in reaching students from Title I schools, rural districts, and programs with limited access to formal cybersecurity curriculum.

If you are interested in:
- Deploying the game in your classroom or program
- Co-designing an evaluation instrument
- Co-authoring a follow-on empirical paper

Please [open an issue](../../issues) or contact the team at **[YOUR CONTACT EMAIL]**.

We are also proposing *Kingdom of Cyborgia* as a **SIGCSE Nifty Assignment** candidate and as a **SIGCSE TS 2027 workshop activity**.

---

## Extending the Game

The game is designed for easy extension. All ATT&CK techniques and D3FEND mitigations live in a single file (`engine/schema.py`). Adding a new attack or defense requires only adding an entry to the relevant dictionary — no changes to the game engine or frontend are needed. See [CONTRIBUTING.md](CONTRIBUTING.md) for step-by-step instructions.

**Planned extensions:**
- Randomized attack mode (no Intel Report hint) for advanced play
- Constrained procurement mode (randomized available defenses each level)
- Expanded ATT&CK/D3FEND coverage across a broader subset of the framework
- Web-based deployment for Chromebook and mobile environments

---

## Built With

- [Python 3.11](https://www.python.org)
- [pygame](https://www.pygame.org)
- [PyInstaller](https://pyinstaller.org) — for cross-platform executable packaging
- [MITRE ATT&CK](https://attack.mitre.org) — adversary tactics and techniques
- [MITRE D3FEND](https://d3fend.mitre.org) — defensive countermeasures

---

## Team

- Sophia Campione
- Anne Drago
- Annie Meaney
- [Supervising faculty — camera-ready]

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Citation

If you use this game in research or teaching, please cite it using the information in [CITATION.cff](CITATION.cff) or the "Cite this repository" button on the GitHub page.
