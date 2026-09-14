# dndkit

A desktop app with the D&D tools I actually use during sessions.

I got tired of switching between 5 different websites and a notepad while DMing online with my friends, so I built this. It's a single .exe with everything in one place — dice roller, initiative tracker, encounter builder, spellbook, loot generator, NPC names, and a character manager.

Works offline

## What's in it

- **Dice Roller** — type any dice expression (like `2d6+3`), roll with advantage/disadvantage, 4d6 stats, roll history
- **Character Manager** — track PCs with ability scores, modifiers, HP, AC
- **Spellbook** — ~75 SRD spells, search by name/school/class
- **Initiative Tracker** — auto-sorted combat order, HP bars, quick damage/heal
- **Encounter Builder** — ~50 monsters, XP difficulty calculator (follows DMG guidelines)
- **Loot Generator** — random treasure by CR tier (coins, gems, art, magic items)
- **NPC Names** — 9 races, male/female/any, random personality traits

## How to run

### Windows
Download `dndkit.exe` from the [Releases](https://github.com/cris3096/dndkit/releases) page and double-click it.

### Run from source
pip install flet python main.py
pip install flet pyinstaller pyinstaller dndkit.spec
