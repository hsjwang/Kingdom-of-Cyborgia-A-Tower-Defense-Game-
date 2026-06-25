# python object for a defense 
class Defense: 
    def __init__(self, name, mitre_id, cost, mitre_description, real_world_examples, story_name, story_description):
        self.name = name 
        self.id = mitre_id
        self.cost = cost
        self.mitre_description = mitre_description
        self.real_world_examples = real_world_examples
        self.story_name = story_name
        self.story_description = story_description

# python object for an attack 
class Attack:
    def __init__(self, mitre_id, name, mitre_description, real_world_examples, defenses, story_name, story_description):
        self.id = mitre_id
        self.name = name 
        self.mitre_description = mitre_description
        self.real_world_examples = real_world_examples
        self.defenses = defenses
        self.story_name = story_name
        self.story_description = story_description

# class for the guidebook which gives the user more information on attacks/defenses 
# can be further implemented in the future if more functionality is needed
class Guidebook:
    def __init__(self, how_to_play_pages, defense_dict, attack_dict): 
        self.how_to_play_pages = how_to_play_pages
        self.defense_dict = defense_dict 
        self.attack_dict = attack_dict

# defenses dictionary 
defenses_dict = {
    "AV": Defense("Antivirus", "M1049", 200, "Detects and quarantines malicious files", "Windows Defender or CrowdStrike scanning downloads.",
                  "The Kennel Hounds", "Trained beasts that sniff out poisoned items, hidden daggers, or any 'unnatural' objects brought into the keep."),
    
    "Audit": Defense("Audit", "M1047", 100, "Logs system events for threat detection", "SIEM tools like Splunk or Azure Monitor logs.",
                     "The Scribe's Ledger", "A meticulous monk sits by the gate and records every single soul who enters, leaves, or moves between rooms. It doesn't stop a crime, but it tells you exactly who did it."),
    
    "WebRestrict": Defense("Web Restrict", "M1021", 300, "Blocks malicious domains and payloads", "Corporate Firewalls or Cisco Umbrella DNS filtering.",
                           "The Portcullis Toll", "A checkpoint at the edge of the kingdom that stops merchants from known 'enemy lands' and bans the entry of strange, unknown crates."),
    
    "Training": Defense("User Training", "M1017", 150, "Teaches users to spot social engineering", "Phishing simulations like KnowBe4.",
                        "The Village Drills", "Regular town halls where peasants are taught that 'The King' will never ask for their gold coins via a random messenger bird."),
    
    "OSConfig": Defense("OS Hardening", "M1028", 200, "Disables risky services and ports", "Disabling RDP on workstations; closing unused ports like 445; removing default \"Guest\" accounts.",
                        "Wall Reinforcement", "Laborers fill in old cracks, seal unused drainage pipes, and remove hidden 'thief holes' in the masonry."),
    
    "PAM": Defense("PAM", "M1026", 250, "Enforces least-privilege admin access", "CyberArk, HashiCorp Vault, or requiring 'sudo' for every command with timed sessions.",
                   "The Royal Guard", "Elite soldiers who shadow high- ranking officials. They ensure only the most trusted hands touch the Royal Scepter."),
    
    "RestrictPerms": Defense("Permissions", "M1022", 250, "Locks down sensitive system folders", "Linux 'chmod' settings, Windows NTFS permissions, or cloud IAM bucket policies.",
                            "Iron-Bound Chests", "Sensitive documents are locked in specific rooms. A cook doesn't need the key to the armory, and a stablehand doesn't need the key to the treasury."),
    
    "MFA": Defense("MFA", "M1032", 250, "Requires secondary login verification", "Google Authenticator, Duo Push, or YubiKeys.",
                   "The Two-Key Vault", "Requires a physical seal and a secret whisper. Even if a guard's keys are stolen, the vault stays shut."),
    
    "DataBackup" : Defense("Data Backup", "M1053", 100, "Creates restorable copies of critical data", "Veeam backups stored on an air-gapped server or AWS S3 Glacier.",
                           "The Scribe's Vault", "Keeps reserve copies of the kingdom's records so losses can be restored after an attack."),
    
    "RemoteData" : Defense("Remote Data Storage", "M1029", 200, "Off-site data storage to prevent local loss", "Off-site disaster recovery sites or \"The Cloud\" (Azure/AWS/GCP).",
                           "The Outland Post", "Stores copies far from the castle so a local disaster cannot destroy everything at once."),
    
    "SSLInspect" : Defense("SSL/TLS Inspection", "M1020", 200, "Decrypts traffic to find hidden threats", "Fortinet Deep Packet Inspection or Palo Alto Networks SSL decryption.",
                           "The Royal Inquisitor", "Examines sealed deliveries for hidden dangers before allowing them into the keep.")
}

# attack dictionary 
#I added the story names so I could display them in the gui 
#Also I commented out the last attack because it wasn't in the guidebook or teacher guide so I assume we aren't doing that one?
attacks_dict = {
    "T1566": Attack("T1566", "Phishing", 
                    "Adversaries may send phishing messages to gain access to victim systems. All forms of phishing are centered on tricking a user into performing a specific action, such as clicking a link or opening an attachment, often to execute malicious code or harvest credentials.", 
                    "Emails, SMS, or chat messages that look legitimate but contain malicious payloads or links to fake login pages.",
                    ["AV", "Audit", "WebRestrict", "Training"], 
                    "Poisoned Messenger",
                    "A courier is delivering a letter, but the ink is infused with a toxin designed to incapacitate whoever handles the parchment."),
    
    "T1552": Attack("T1552", "Unsecured Credentials", 
                    "Adversaries may search local system sources to find insecurely stored credentials. These can include passwords, certificates, or tokens stored in files (like .txt or .config), environment variables, or the system registry.", 
                    "A developer leaving a \"passwords.txt\" file on their desktop or hardcoding an API key into a script that everyone in the company can read.",
                    ["Audit", "OSConfig", "PAM", "RestrictPerms", "Training"], 
                    "Undercover Spy",
                    "A member of the Shadow Guild is infiltrating the castle in the guise of a servant, searching for physical keys left on hooks or eavesdropping on whispered secrets in the corridors."),
    
    "T1098": Attack("T1098", "Account Manipulation", 
                    "Adversaries may manipulate accounts to maintain access to victim systems. This includes modifying account permissions, adding new accounts to privileged groups (like \"Domain Admins\"), or resetting passwords to take over existing legitimate accounts.", 
                    "After gaining initial access, an attacker adds their own \"backdoor\" account to the server's Administrators group so they can log in easily later.",
                    ["MFA", "OSConfig", "PAM", "RestrictPerms"], 
                    "Corrupt Seneschal",
                    "An enemy agent is attempting to bribe the castle's record-keeper to alter the laws of the realm. They want to be declared a Duke, providing them with unrestricted access to the castle gates."),

    "T1027": Attack("T1027", "Obfuscated Files", 
                    "Adversaries may attempt to make an executable or file difficult to discover or analyze by encrypting, encoding, or otherwise concealing its contents. This is intended to bypass security tools (like Antivirus) that look for known malicious signatures.", 
                    "Using \"packing software\" or complex encoding (like Base64) to hide a virus's code so that it looks like random, harmless text to a scanner.",
                    ["AV", "Audit", "Training"], 
                    "Trojan Crate",
                    "A merchant is trying to enter the castle with a crate of supposedly standard supplies. This crate may house a magical parasite made to spread through and weaken the castle's stone structure."),

    "T1059": Attack("T1059", "Command and Scripting Interpreter", 
                    "Adversaries may abuse command and script interpreters to execute commands, scripts, or binaries. These interfaces (like PowerShell, Python, or Windows Command Shell) are powerful tools that attackers use to interact with systems and automate their activities.",
                    "An attacker uses a PowerShell script to automatically download more malware or scan the internal network for other vulnerable computers.",
                    ["AV", "Audit", "PAM", "WebRestrict"], "Sorcerer’s Script",
                    "An enemy mage stands beyond the castle walls, chanting ancient, complex commands to his Shadow Guild. These incantations are designed to exploit the mechanical logic of the drawbridge, forcing it to lower against the will of the defenders.")
}

# --- How to play data for the guide pages --- 
HOW_TO_PLAY_DATA = [
    {
        "title": "Welcome to the Kingdom of Cyborgia, located on a server far far away.....",
        "description": "The Shadow Guild is at our borders. As the newly appointed Castellan, your job is to allocate the King’s Gold to build the right defenses. You have a limited budget each round—choose wisely. Once a defense is built, it remains part of your castle, but every turn the Guild will try a new, more devious tactic."
    },
    {
        "title": "Build Phase",
        "description": "You can view the incoming attacks by clicking on the Intel Report button. Defenses are available in the cabinet, with your allocated budget on top. Drag the selected defense to its correpsonding location on the game board to purchase it. Once the defenses are placed, they can't be moved. When you are ready, click LOCK DEFENCES to begin the attack."
    },
    {
        "title": "Attack Phase",
        "description": "Once defenses are locked, the attacker launches threats against your castle. If chosen correctly, your placed defenses help block attacks and protect your health. If chosen incorrectly, you will lose health and have to repeat the level."
    },
    {
        "title": "Winning and Losing",
        "description": "There are three total levels. Survive each round to move to the next level. If your health reaches zero, the castle falls and the game ends. You can earn additional shield health by successfully passing levels."
    }
]