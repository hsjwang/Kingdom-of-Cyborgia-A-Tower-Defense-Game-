# python object for a defense 
class Defense: 
    def __init__(self, mitre_id, name, cost, mitre_description, real_world_examples, story_name, story_description):
        self.id = mitre_id
        self.name = name 
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

# visible defenses in beginner mode 
VISIBLE_DEFENSES = [
    "M1049",
    "M1047",
    "M1053",
    "M1021",
    "M1026",
    "M1017",
    "M1028",
    "M1029",
    "M1032",
    "M1022",
    "M1020"
]


# visible attacks in beginner mode
VISIBLE_ATTACKS = [
    "T1566",
    "T1552",
    "T1098",
    "T1027",
    "T1059"
]

# defenses dictionary 
defenses_dict = {
    "M1049": Defense("M1049", "Antivirus/Antimalware", 200, "Detects and quarantines malicious files", "Windows Defender or CrowdStrike scanning downloads.",
                  "The Kennel Hounds", "Trained beasts that sniff out poisoned items, hidden daggers, or any 'unnatural' objects brought into the keep."),
    
    "M1047": Defense("M1047", "Audit", 100, "Logs system events for threat detection", "SIEM tools like Splunk or Azure Monitor logs.",
                     "The Scribe's Ledger", "A meticulous monk sits by the gate and records every single soul who enters, leaves, or moves between rooms. It doesn't stop a crime, but it tells you exactly who did it."),
    
    "M1021": Defense("M1021", "Web Restrict (Restrict Web-Based Content)", 300, "Blocks malicious domains and payloads", "Corporate Firewalls or Cisco Umbrella DNS filtering.",
                           "The Portcullis Toll", "A checkpoint at the edge of the kingdom that stops merchants from known 'enemy lands' and bans the entry of strange, unknown crates."),
    
    "M1017": Defense("M1017", "User Training", 150, "Teaches users to spot social engineering", "Phishing simulations like KnowBe4.",
                        "The Village Drills", "Regular town halls where peasants are taught that 'The King' will never ask for their gold coins via a random messenger bird."),
    
    "M1028": Defense("M1028", "OS Hardening (Operating System Configuration)", 200, "Disables risky services and ports", "Disabling RDP on workstations; closing unused ports like 445; removing default \"Guest\" accounts.",
                        "Wall Reinforcement", "Laborers fill in old cracks, seal unused drainage pipes, and remove hidden 'thief holes' in the masonry."),
    
    "M1026": Defense("M1026", "PAM", 250, "Enforces least-privilege admin access", "CyberArk, HashiCorp Vault, or requiring 'sudo' for every command with timed sessions.",
                   "The Royal Guard", "Elite soldiers who shadow high- ranking officials. They ensure only the most trusted hands touch the Royal Scepter."),
    
    "M1022": Defense("M1022", "Permissions (Restrict File and Directory Permissions)", 250, "Locks down sensitive system folders", "Linux 'chmod' settings, Windows NTFS permissions, or cloud IAM bucket policies.",
                            "Iron-Bound Chests", "Sensitive documents are locked in specific rooms. A cook doesn't need the key to the armory, and a stablehand doesn't need the key to the treasury."),
    
    "M1032": Defense("M1032", "MFA", 250, "Requires secondary login verification", "Google Authenticator, Duo Push, or YubiKeys.",
                   "The Two-Key Vault", "Requires a physical seal and a secret whisper. Even if a guard's keys are stolen, the vault stays shut."),
    
    "M1053" : Defense("M1053", "Data Backup", 100, "Creates restorable copies of critical data", "Veeam backups stored on an air-gapped server or AWS S3 Glacier.",
                           "The Scribe's Vault", "Keeps reserve copies of the kingdom's records so losses can be restored after an attack."),
    
    "M1029" : Defense("M1029", "Remote Data Storage", 200, "Off-site data storage to prevent local loss", "Off-site disaster recovery sites or \"The Cloud\" (Azure/AWS/GCP).",
                           "The Outland Post", "Stores copies far from the castle so a local disaster cannot destroy everything at once."),
    
    "M1020" : Defense("M1020", "SSL/TLS Inspection", 200, "Decrypts traffic to find hidden threats", "Fortinet Deep Packet Inspection or Palo Alto Networks SSL decryption.",
                           "The Royal Inquisitor", "Examines sealed deliveries for hidden dangers before allowing them into the keep."),
    
    "M1015" : Defense("M1015", "Active Directory Configuration", 200, "Configures directory services securely to prevent privilege escalation and credential theft", "Disabling LLMNR/NBT-NS, restricting Domain Admin logins to Tier 0 systems, and enforcing SMB signing.",
                           "The Royal Lineage", "A strict hierarchy of nobles and titles is enforced. A mere squire cannot simply declare themselves a Duke to command the castle guards or access the treasury."),
    
    "M1018" : Defense("M1018", "User Account Management", 150, "Manages the lifecycle of user accounts to limit unnecessary or stale privileges", "Disabling inactive accounts, performing quarterly access reviews, and enforcing strict offboarding processes.",
                           "The Steward's Roster", "The Steward actively revokes castle access from mercenaries whose contracts have expired and banishes idle loiterers from the courtyard."),
    
    "M1027" : Defense("M1027", "Password Policies", 100, "Enforces strong password complexity, length, and rotation requirements", "Enforcing a minimum 14-character length, blocking common phrases, and preventing password reuse.",
                           "The Riddler's Gate", "Guards demand a complex, ever-changing passphrase from travelers—no more using \"password\" or the King's birthday to gain entry."),        
    
    "M1030" : Defense("M1030", "Network Segmentation", 250, "Divides a network into smaller, isolated segments to contain lateral movement during a breach", "Isolating the guest Wi-Fi from corporate networks, using VLANs, and setting up internal firewalls.",
                           "The Walled Districts", "The castle is divided into isolated rings. Even if the outer bailey falls to the Shadow Guild, the inner keep remains sealed behind raised drawbridges."),
    
    "M1031" : Defense("M1031", "Network Intrusion Prevention", 300, "Monitors network traffic to actively detect and block malicious exploits", "Deploying Snort, Suricata, or Cisco Firepower IPS appliances to drop packets matching known exploit patterns.",
                           "The Tower Ballistas", "Vigilant archers actively scan the horizon, immediately shooting down any incoming projectiles, siege weapons, or suspicious ravens before they land."),
    
    "M1033" : Defense("M1033", "Limit Software Installation", 150, "Restricts users from installing unauthorized software applications", "Removing local administrator privileges from standard users and using AppLocker or GPOs to block unapproved installers.",
                           "The Blacksmith's Seal", "Only tools and weapons forged by the official royal armory are allowed. Peasants are forbidden from bringing their own makeshift swords into the barracks."),
   
    "M1035" : Defense("M1035", "Limit Access to Resource Over Network", 200, "Restricts access to specific network resources based on logical business needs", "Restricting SSH or database management ports to only accept connections from a dedicated admin jump box.",
                           "The Privy Council", "Only designated, high-ranking advisors are allowed into the map room; the doors are completely hidden and walled off from the rest of the kingdom."),
    
    "M1037" : Defense("M1037", "Filter Network Traffic", 200, "Filters incoming and outgoing network traffic based on IP addresses, ports, or protocols", "Configuring stateless or stateful network firewalls (like AWS Security Groups) to drop unapproved inbound connections.",
                           "The Customs Officers", "Guards rigorously inspect all incoming merchant carts and outgoing messengers, turning away anyone lacking the proper royal travel permits."),
    
    "M1038" : Defense("M1038", "Execution Prevention", 250, "Blocks unauthorized scripts, binaries, or untrusted code from executing on endpoints", "Using Microsoft AppLocker, WDAC, or application whitelisting tools to run only verified software.",
                           "The King's Decree", "A magical ward that instantly paralyzes anyone attempting to cast unauthorized spells or read from forbidden tomes within the castle walls."),
    
    "M1040" : Defense("M1040", "Behavior Prevention on Endpoint", 250, "Monitors and blocks active processes exhibiting suspicious or anomalous behavior patterns", "EDR tools like CrowdStrike or SentinelOne blocking a standard word processor from suddenly launching a command shell.",
                           "The Suspicion Ward", "Guards closely monitor the behavior of the staff. If the court jester suddenly starts drawing a sword instead of juggling, he is tackled immediately."),
    
    "M1041" : Defense("M1041", "Encrypt Sensitive Information", 200, "Encrypts sensitive data at rest or in transit to protect confidentiality from unauthorized eyes", "Using BitLocker for full disk encryption or enforcing TLS 1.3 for all web data transmissions.",
                           "The Ciphered Scrolls", "Royal decrees are written in a dead, magical language. Even if a Shadow Guild spy steals the scroll, they cannot read a single word of it."),
    
    "M1042" : Defense("M1042", "Disable or Remove Feature or Program", 150, "Disables or removes unnecessary software features or protocols to reduce the overall attack surface", "Disabling macros in Microsoft Office or completely turning off legacy protocols like TLS 1.0 and SMBv1.",
                           "The Sealed Catacombs", "Laborers purposely collapse old, forgotten tunnels and board up abandoned secret passages so thieves cannot use them to bypass the gates."),
    
    "M1045" : Defense("M1045", "Code Signing", 200, "Digitally signs software to verify the identity of the author and ensure it hasn't been altered", "Verifying valid Microsoft, Apple, or custom internal developer certificates before allowing software to run.",
                           "The Royal Wax Seal", "Every official missive must bear the King's enchanted wax seal. Forgeries lacking the proper crest are immediately thrown into the hearth."),
    
    "M1051" : Defense("M1051", "Update Software", 150, "Applies security patches to software and operating systems to remediate known vulnerabilities", "Running monthly Windows Update cycles or patching vulnerable open-source dependencies (like Log4j updates).",
                           "The Mason's Upkeep", "Stonemasons constantly patch weathering walls, reinforce rusting iron gates, and upgrade the defenses against newly discovered Shadow Guild siege tactics."),

    "M1054" : Defense("M1054", "Software Configuration", 150, "Configures software applications securely to minimize corporate risk and enforce safety baselines", 
                           "Configuring web browsers via GPO to block malicious extensions, disable pop-ups, and enforce strict privacy settings.", "The Keep's Protocols", "Strict rules govern the castle's daily operations. Fires must be extinguished at night, and weapons must be locked away, ensuring the castle operates safely."),

}


# attack dictionary 
#I added the story names so I could display them in the gui 
#Also I commented out the last attack because it wasn't in the guidebook or teacher guide so I assume we aren't doing that one?
attacks_dict = {
    "T1566": Attack("T1566", "Phishing", 
                    "Adversaries may send phishing messages to gain access to victim systems. All forms of phishing are centered on tricking a user into performing a specific action, such as clicking a link or opening an attachment, often to execute malicious code or harvest credentials.", 
                    "Emails, SMS, or chat messages that look legitimate but contain malicious payloads or links to fake login pages.",
                    ["M1049", "M1047", "M1021", "M1017", "M1031", "M1054"], 
                    "Poisoned Messenger",
                    "A courier is delivering a letter, but the ink is infused with a toxin designed to incapacitate whoever handles the parchment."),
    
    "T1552": Attack("T1552", "Unsecured Credentials", 
                    "Adversaries may search local system sources to find insecurely stored credentials. These can include passwords, certificates, or tokens stored in files (like .txt or .config), environment variables, or the system registry.", 
                    "A developer leaving a \"passwords.txt\" file on their desktop or hardcoding an API key into a script that everyone in the company can read.",
                    ["M1047", "M1028", "M1026", "M1022",  "M1017", "M1015", "M1041", "M1037", "M1035", "M1027", "M1051"], 
                    "Undercover Spy",
                    "A member of the Shadow Guild is infiltrating the castle in the guise of a servant, searching for physical keys left on hooks or eavesdropping on whispered secrets in the corridors."),
    
    "T1098": Attack("T1098", "Account Manipulation", 
                    "Adversaries may manipulate accounts to maintain access to victim systems. This includes modifying account permissions, adding new accounts to privileged groups (like \"Domain Admins\"), or resetting passwords to take over existing legitimate accounts.", 
                    "After gaining initial access, an attacker adds their own \"backdoor\" account to the server's Administrators group so they can log in easily later.",
                    ["M1032", "M1028", "M1026", "M1022", "M1042", "M1030", "M1018"], 
                    "Corrupt Seneschal",
                    "An enemy agent is attempting to bribe the castle's record-keeper to alter the laws of the realm. They want to be declared a Duke, providing them with unrestricted access to the castle gates."),

    "T1027": Attack("T1027", "Obfuscated Files", 
                    "Adversaries may attempt to make an executable or file difficult to discover or analyze by encrypting, encoding, or otherwise concealing its contents. This is intended to bypass security tools (like Antivirus) that look for known malicious signatures.", 
                    "Using \"packing software\" or complex encoding (like Base64) to hide a virus's code so that it looks like random, harmless text to a scanner.",
                    ["M1049", "M1047", "M1017", "M1040"], 
                    "Trojan Crate",
                    "A merchant is trying to enter the castle with a crate of supposedly standard supplies. This crate may house a magical parasite made to spread through and weaken the castle's stone structure."),

    "T1059": Attack("T1059", "Command and Scripting Interpreter", 
                    "Adversaries may abuse command and script interpreters to execute commands, scripts, or binaries. These interfaces (like PowerShell, Python, or Windows Command Shell) are powerful tools that attackers use to interact with systems and automate their activities.",
                    "An attacker uses a PowerShell script to automatically download more malware or scan the internal network for other vulnerable computers.",
                    ["M1049", "M1047", "M1026", "M1021", "M1040", "M1045", "M1042", "M1038", "M1033"], "Sorcerer’s Script",
                    "An enemy mage stands beyond the castle walls, chanting ancient, complex commands to his Shadow Guild. These incantations are designed to exploit the mechanical logic of the drawbridge, forcing it to lower against the will of the defenders."),
    
    "T1204": Attack("T1204", "User Execution", 
                    "Adversaries may rely on a user to execute a malicious file or run commands for initial access or lateral movement. This typically happens when a user opens an email attachment, runs a macro in a document, or double-clicks a disguised executable file.",
                    "An employee opening a malicious email attachment named 'Q4_Bonus_Report.xlsm' and clicking 'Enable Macros', which triggers an invisible malware installation.",
                    ["M1040", "M1038", "M1033", "M1031", "M1021", "M1017"], 
                    "The Bewitched Relic", 
                    "The Guild leaves a beautifully crafted, seemingly harmless music box in the bustling courtyard. Overcome by curiosity, a young stablehand turns the crank, unwittingly triggering a dormant spell that unbars the barracks doors."),

    "T1557": Attack("T1557", "Adversary-in-the-Middle", 
                    "Adversaries may position themselves between two or more networked devices to intercept, monitor, alter, or redirect communications. This allows them to harvest sensitive credentials, session tokens, or manipulate payloads in transit.",
                    "An attacker setting up a rogue Wi-Fi hotspot in a coffee shop to intercept unencrypted HTTP traffic or session cookies from unsuspecting victims.", 
                    ["M1017", "M1030", "M1031", "M1035", "M1037", "M1041", "M1042"], 
                    "The False Raven", 
                    "Shadow Guild rogues quietly intercept messenger birds flying between the kingdom's watchtowers. They meticulously swap the real scrolls with forged orders and send the birds on their way, manipulating the guard patrol routes from the shadows."),
    
    "T1071": Attack("T1071", "Application Layer Protocol", 
                    "Adversaries may communicate using application layer protocols to blend their command and control (C2) traffic with normal, legitimate network activity. Common protocols abused include HTTP, HTTPS, DNS, and SMTP.",
                    "Malware installed on an endpoint making regular HTTPS requests to an attacker's external web server, masking its malicious communication as basic web browsing traffic.",
                    ["M1037","M1031"], "The Merchant's Disguise", "Shadow Guild spies masquerade as regular apple merchants and bards, passing secret hand signals and hidden messages right under the noses of the guards in the bustling town square."),
    
    "T1499": Attack("T1499", "Endpoint Denial of Service", 
                    "Adversaries may conduct Denial of Service (DoS) attacks targeted at endpoints to degrade, disrupt, or completely exhaust the availability of services, applications, or system resources, rendering them unavailable to legitimate users.",
                    "Flooding a critical internal web server or authentication domain controller with thousands of bogus requests per second until it crashes or freezes.", 
                    ["M1037"], "The Peasant Stampede", "The Guild pays a massive mob of fake peasants to crowd the drawbridge and riot at the gates, completely freezing castle operations and preventing legitimate royal messengers from entering or leaving."),
    
    "T1048": Attack("T1048", "Exfiltration Over Alternative Protocol", 
                    "Adversaries may steal or exfiltrate data from a victim network using a different protocol than the one originally used to compromise or control the system. This helps them bypass standard data loss prevention (DLP) filters.",
                    "An attacker copying sensitive corporate database files and exfiltrating them out of the corporate network using DNS queries or FTP transfers instead of standard web traffic.",
                    ["M1018", "M1022", "M1030", "M1031", "M1037"], "The Smuggler's Tunnel", "Instead of trying to carry stolen gold out through the heavily guarded main gate, thieves bypass the checkpoints by sneaking the kingdom's secrets out through sewer grates and underground rivers.")

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
    },
    {
        "title": "Game Modes",
        "description": "Choose between the following 3 game modes:",
        "items": [
            "1. Beginner Mode — Play through three levels with limited attacks and defenses.",
            "2. Custom Mode — Select custom attacks and defenses to build your own scenarios.",
            "3. Random Mode — Face a wider range of attacks and utilize more defenses."
        ]
    }
]
