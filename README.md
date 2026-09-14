# dndkit ⚔️

> **The all-in-one desktop toolkit for D&D 5e Dungeon Masters.** Beautiful. Fast. Offline.

Dice roller, character manager, spellbook, initiative tracker, encounter builder, loot generator, and NPC name generator — all in one native desktop app. Built with Python + Flet.

---

## ✨ Features

Seven essential DM tools, perfectly integrated:

| Tool | What it does |
|------|-------------|
| 🎲 **Dice Roller** | Any dice expression, advantage/disadvantage, 4d6 stats, quick-roll buttons, roll history |
| 👤 **Character Manager** | Full PC tracking with ability scores, auto-calculated modifiers, HP & AC chips |
| 📖 **Spellbook** | 75+ SRD spells, search by name/school/class, full stat blocks with class tags |
| ⚔️ **Initiative Tracker** | Auto-sorted combat order, visual HP bars, quick damage/heal controls |
| 🛡️ **Encounter Builder** | 50+ monsters, XP difficulty calculator (Trivial → Deadly), DMG official thresholds |
| ⭐ **Loot Generator** | Random treasure hoards by CR tier — coins, gems, art objects, magic items |
| ➕ **NPC Names** | 9 races × male/female/any × random personality traits with generation history |

---

## 🎨 Design

- **Dark fantasy theme** — deep violet + amber gold palette
- **Card-based UI** — clean, scannable, consistent spacing
- **Keyboard-first** — press Enter to roll dice, Tab through forms
- **Zero dependencies** — one exe, no install, works offline

---

## 🚀 Getting Started

### Windows (recommended)
Download the latest `dndkit.exe` from the [Releases](https://github.com/yourusername/dndkit-gui/releases) page and double-click. No installation required.

### From source
```bash
pip install flet
python main.py
```

### Build your own .exe
```bash
pip install flet pyinstaller
pyinstaller --onefile --name dndkit --collect-all flet --collect-all flet_desktop --add-data "data/*;data/" main.py
```

---

## 📸 Screenshots

*(coming soon — add your own screenshots here after testing)*

---

## 🏗️ Architecture

```
dndkit/
├── main.py              # App entrypoint + all UI
├── data/
│   ├── spells.json      # 75+ D&D 5e SRD spells
│   ├── monsters.json    # 50+ monsters with CR/XP/HP/AC
│   └── names.json       # Name pools for NPC generation
├── requirements.txt
├── LICENSE
└── README.md
```

The app is a single Python file using **Flet** (Flutter for Python). All data is loaded from JSON at startup. No network calls, no accounts, no tracking.

---

## ❓ Why another D&D tool?

Every D&D app I tried was either web-based (slow, needs internet), had a terrible UI, or was missing 2-3 tools I actually needed during sessions. dndkit is the 7 tools I use every session, in one fast native app.

If you DM games and find yourself switching between a dice roller, a spell reference, an encounter calculator, and a notepad — this is for you.

---

## 🤝 Contributing

Contributions welcome! Feel free to open issues or PRs for:
- More spells / monsters / items
- New tools (weather generator, shop generator, etc.)
- UI improvements
- Bug fixes

---

## 📄 License

MIT — do whatever you want with it.

*Dungeons & Dragons is a trademark of Wizards of the Coast. This app is unofficial and not affiliated with WotC.*
