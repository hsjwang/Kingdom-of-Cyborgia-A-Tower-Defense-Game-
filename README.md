# Kingdom of Cyborgia

**A tower-defense educational game that teaches MITRE ATT&CK and Mitigation concepts to high school students.**

Players take on the role of the Castellan — the defender of a castle kingdom under siege by the Shadow Guild. Each attack the Guild launches maps directly to a real [MITRE ATT&CK](https://attack.mitre.org) technique. Each defense the player deploys maps to a real [MITRE ATT&CK Mitigations](https://attack.mitre.org). Players must allocate a limited budget strategically across three escalating levels, learning through consequence that cybersecurity is fundamentally about tradeoffs, resource allocation, and risk management under uncertainty.

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
│   └── schema.py             # ATT&CK attack and mitigation defense dictionaries
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
│   ├── MITRE ATT&CK Game Teacher Resource Guide.pdf
│   └── MITRE ATT&CK Game User Guide.pdf
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
- Each defense displays its story name, MITRE ATT&CK Mitigation identifier, and technical description.
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

### Game Modes

The game features three distinct gameplay modes tailored to different learning objectives, skill levels, and strategic playstyles:

* **Beginner Mode:** Features a structured, three-level simulation where players defend against a tiered progression of attacks that gradually increase in difficulty and threat complexity. Using a set of 11 defenses and 5 attacks, players manage an initial budget and must strategically purchase and commit to defenses (including decoys) before viewing attack outcomes.
* **Random Mode:** Maximizes replayability by introducing unpredictability into every session. The mode starts players with 10 initial defenses, then randomly shuffles and unlocks 5 defenses while generating 1 to 3 random attacks per level. To ensure fairness, the system dynamically calculates budgets and validates attack combinations so every level remains winnable, automatically resetting the environment and generating a new scenario upon completion.
* **Custom Mode:** Designed for educators and students looking to target specific cyber threats and mitigations. This mode provides full control by allowing players to manually select the exact attacks and defense systems in play. The system verifies strategy viability and dynamically computes budgets to guarantee that custom scenarios are balanced and beatable.

---

## MITRE ATT&CK / Mitigation Coverage

The project covers **10 ATT&CK techniques** and **26 unique Mitigations**:

| ATT&CK Technique | ID | Tactic(s) | Status | Valid Mitigations |
|---|---|---|---|---|
| Phishing | T1566 | Initial Access | Implemented | M1049 (Antivirus), M1047 (Audit), M1021 (Web Restrict), M1017 (User Training), M1031 (Network NIPS), M1054 (Software Config) |
| Unsecured Credentials | T1552 | Credential Access | Implemented | M1047 (Audit), M1028 (OS Hardening), M1026 (PAM), M1022 (Permissions), M1017 (User Training), M1015 (User Account Control), M1041 (Encrypt Info), M1037 (Filter Traffic), M1035 (SSL/TLS Inspection), M1027 (Password Policies), M1051 (Update Software) |
| Account Manipulation | T1098 | Persistence, Privilege Escalation | Implemented | M1032 (MFA), M1028 (OS Hardening), M1026 (PAM), M1022 (Permissions), M1042 (Disable Features), M1030 (Network Segmentation), M1018 (User Account Management) |
| Obfuscated Files | T1027 | Defense Evasion | Implemented | M1049 (Antivirus), M1047 (Audit), M1017 (User Training), M1040 (Behavioral Analytics) |
| Command and Scripting Interpreter | T1059 | Execution | Implemented | M1049 (Antivirus), M1047 (Audit), M1026 (PAM), M1021 (Web Restrict), M1040 (Behavioral Analytics), M1045 (Code Signing), M1042 (Disable Features), M1038 (Execution Prevention), M1033 (Limit Software) |
| User Execution | T1204 | Execution | Planned | M1040 (Behavioral Analytics), M1038 (Execution Prevention), M1033 (Limit Software), M1031 (Network NIPS), M1021 (Web Restrict), M1017 (User Training) |
| Adversary-in-the-Middle | T1557 | Credential Access, Collection | Planned | M1017 (User Training), M1030 (Network Segmentation), M1031 (Network NIPS), M1035 (SSL/TLS Inspection), M1037 (Filter Traffic), M1041 (Encrypt Info), M1042 (Disable Features) |
| Application Layer Protocol | T1071 | Command and Control | Planned | M1037 (Filter Traffic), M1031 (Network NIPS) |
| Endpoint Denial of Service | T1499 | Impact | Planned | M1037 (Filter Traffic) |
| Exfiltration Over Alternative Protocol | T1048 | Exfiltration | Planned | M1018 (User Account Management), M1022 (Permissions), M1030 (Network Segmentation), M1031 (Network NIPS), M1037 (Filter Traffic) |

Planned future releases will expand coverage to a larger subset of the ATT&CK and Mitigations framework. See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add new techniques.

---

## For Educators

Download the **Teacher Resource Guide** from the `docs/` folder or the Releases page. It includes:
- Learning objectives aligned to the game's mechanics
- Suggested pre/post discussion questions
- A glossary of MITRE ATT&CK and Mitigations terms encountered in the game
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

Please [open an issue](../../issues) or contact the team at hs.wang@northeastern.edu.

We are also proposing *Kingdom of Cyborgia* as a **SIGCSE Nifty Assignment** candidate and as a **SIGCSE TS 2027 workshop activity**.

---

## Extending the Game

The game is designed for easy extension. All ATT&CK techniques and mitigations live in a single file (`engine/schema.py`). Adding a new attack or defense requires only adding an entry to the relevant dictionary — no changes to the game engine or frontend are needed. See [CONTRIBUTING.md](CONTRIBUTING.md) for step-by-step instructions.

**Planned extensions:**
- Randomized attack mode (no Intel Report hint) for advanced play
- Constrained procurement mode (randomized available defenses at each level)
- Expanded ATT&CK/Mitigation coverage across a broader subset of the framework
- Web-based deployment for Chromebook and mobile environments

---

## Built With

- [Python 3.11](https://www.python.org)
- [pygame](https://www.pygame.org)
- [PyInstaller](https://pyinstaller.org) — for cross-platform executable packaging
- [MITRE ATT&CK](https://attack.mitre.org) — adversary tactics and techniques

---

## Team

- Sophia Campione
- Anne Drago
- Annie Meaney
- Hsiao An Wang

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## Citation

If you use this game in research or teaching, please cite it using the information in [CITATION.cff](CITATION.cff) or the "Cite this repository" button on the GitHub page.
