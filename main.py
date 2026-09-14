"""
dndkit — D&D 5e DM Toolkit
A beautiful desktop toolkit for Dungeon Masters.
"""
import flet as ft
import json
import random
import re
import os
from pathlib import Path

# ─────────────────────────────────────────────────────────────
#  DATA LOADING
# ─────────────────────────────────────────────────────────────
DATA_DIR = Path(__file__).parent / "data"

with open(DATA_DIR / "spells.json", encoding="utf-8") as f:
    SPELLS = json.load(f)
with open(DATA_DIR / "monsters.json", encoding="utf-8") as f:
    MONSTERS = json.load(f)
with open(DATA_DIR / "names.json", encoding="utf-8") as f:
    NAMES_DATA = json.load(f)

# ─── Extra spells ────────────────────────────────────────────
EXTRA_SPELLS = [
    {"name":"Fire Bolt","level":0,"school":"Evocation","casting_time":"1 action","range":"120 ft","components":"V,S","duration":"Instantaneous","description":"A bright streak of flame flashes from you to a creature or object within range. Make a ranged spell attack against the target. On a hit, the target takes 1d10 fire damage.","classes":["Sorcerer","Wizard","Warlock"]},
    {"name":"Mage Armor","level":1,"school":"Abjuration","casting_time":"1 action","range":"Touch","components":"V,S,M","duration":"8 hours","description":"You touch a willing creature who isn't wearing armor, and a protective magical force surrounds it until the spell ends. The target's base AC becomes 13 + its Dexterity modifier.","classes":["Sorcerer","Wizard"]},
    {"name":"Magic Missile","level":1,"school":"Evocation","casting_time":"1 action","range":"120 ft","components":"V,S","duration":"Instantaneous","description":"You create three glowing darts of magical force. Each dart hits a creature of your choice that you can see within range. A dart deals 1d4 + 1 force damage to its target.","classes":["Sorcerer","Wizard","Warlock"]},
    {"name":"Shield","level":1,"school":"Abjuration","casting_time":"1 reaction","range":"Self","components":"V,S","duration":"1 round","description":"An invisible barrier of magical force appears and protects you. Until the start of your next turn, you have a +5 bonus to AC, including against the triggering attack, and you take no damage from magic missile.","classes":["Sorcerer","Wizard"]},
    {"name":"Sleep","level":1,"school":"Enchantment","casting_time":"1 action","range":"90 ft","components":"V,S,M","duration":"1 minute","description":"This spell sends creatures into a magical slumber. Roll 5d8; the total is how many hit points of creatures this spell can affect.","classes":["Bard","Sorcerer","Wizard"]},
    {"name":"Thunderwave","level":1,"school":"Evocation","casting_time":"1 action","range":"Self (15-ft cube)","components":"V,S","duration":"Instantaneous","description":"A wave of thunderous force sweeps out from you. Each creature in a 15-foot cube originating from you must make a Constitution saving throw. On a failed save, a creature takes 2d8 thunder damage and is pushed 10 feet away.","classes":["Bard","Druid","Sorcerer","Wizard"]},
    {"name":"Misty Step","level":2,"school":"Conjuration","casting_time":"1 bonus action","range":"Self","components":"V","duration":"Instantaneous","description":"Briefly surrounded by silvery mist, you teleport up to 30 feet to an unoccupied space that you can see.","classes":["Sorcerer","Warlock","Wizard"]},
    {"name":"Scorching Ray","level":2,"school":"Evocation","casting_time":"1 action","range":"120 ft","components":"V,S","duration":"Instantaneous","description":"You create three rays of fire and hurl them at targets within range. You can hurl them at one target or several. Make a ranged spell attack for each ray. On a hit, the target takes 2d6 fire damage.","classes":["Sorcerer","Wizard"]},
    {"name":"Web","level":2,"school":"Conjuration","casting_time":"1 action","range":"60 ft","components":"V,S,M","duration":"Concentration, up to 1 hour","description":"You conjure a mass of thick, sticky webbing at a point of your choice within range. The webs fill a 20-foot cube from that point for the duration.","classes":["Sorcerer","Wizard"]},
    {"name":"Fireball","level":3,"school":"Evocation","casting_time":"1 action","range":"150 ft","components":"V,S,M","duration":"Instantaneous","description":"A bright streak flashes from your pointing finger to a point you choose and then blossoms with a low roar into an explosion of flame. Each creature in a 20-foot-radius sphere centered on that point must make a Dexterity saving throw. A target takes 8d6 fire damage on a failed save.","classes":["Sorcerer","Wizard"]},
    {"name":"Counterspell","level":3,"school":"Abjuration","casting_time":"1 reaction","range":"60 ft","components":"S","duration":"Instantaneous","description":"You attempt to interrupt a creature in the process of casting a spell. If the creature is casting a spell of 3rd level or lower, its spell fails and has no effect.","classes":["Sorcerer","Warlock","Wizard"]},
    {"name":"Hypnotic Pattern","level":3,"school":"Illusion","casting_time":"1 action","range":"120 ft","components":"S,M","duration":"Concentration, up to 1 minute","description":"You create a twisting pattern of colors that weaves through the air inside a 30-foot cube within range. Each creature in the area who sees the pattern must make a Wisdom saving throw. On a failed save, the creature becomes charmed for the duration.","classes":["Bard","Sorcerer","Warlock","Wizard"]},
    {"name":"Dimension Door","level":4,"school":"Conjuration","casting_time":"1 action","range":"500 feet","components":"V","duration":"Instantaneous","description":"You teleport yourself from your current location to any other spot within range. You arrive at exactly the spot desired.","classes":["Bard","Sorcerer","Warlock","Wizard"]},
    {"name":"Wall of Fire","level":4,"school":"Evocation","casting_time":"1 action","range":"120 ft","components":"V,S,M","duration":"Concentration, up to 1 minute","description":"You create a wall of fire on a solid surface within range. You can make the wall up to 60 feet long, 20 feet high, and 1 foot thick, or a ringed wall up to 20 feet in diameter, 20 feet high, and 1 foot thick.","classes":["Druid","Sorcerer","Wizard"]},
    {"name":"Cone of Cold","level":5,"school":"Evocation","casting_time":"1 action","range":"Self (60-ft cone)","components":"V,S,M","duration":"Instantaneous","description":"A blast of cold air erupts from your hands. Each creature in a 60-foot cone must make a Constitution saving throw. A creature takes 8d8 cold damage on a failed save.","classes":["Sorcerer","Wizard"]},
    {"name":"Dominate Person","level":5,"school":"Enchantment","casting_time":"1 action","range":"60 ft","components":"V,S","duration":"Concentration, up to 1 minute","description":"You attempt to beguile a humanoid that you can see within range. It must succeed on a Wisdom saving throw or be charmed by you for the duration.","classes":["Bard","Sorcerer","Warlock","Wizard"]},
    {"name":"Chain Lightning","level":6,"school":"Evocation","casting_time":"1 action","range":"150 ft","components":"V,S,M","duration":"Instantaneous","description":"You create a bolt of lightning that arcs toward a target of your choice that you can see within range. Three bolts then leap from that target to as many as three other targets, each of which must be within 30 feet of the first target.","classes":["Sorcerer","Wizard"]},
    {"name":"Disintegrate","level":6,"school":"Transmutation","casting_time":"1 action","range":"60 ft","components":"V,S,M","duration":"Instantaneous","description":"A thin green ray springs from your pointing finger to a target that you can see within range. The target can be a creature, an object, or a creation of magical force.","classes":["Sorcerer","Wizard"]},
    {"name":"Fire Storm","level":7,"school":"Evocation","casting_time":"1 action","range":"150 ft","components":"V,S","duration":"Instantaneous","description":"A storm made up of sheets of roaring flame appears in a location you choose within range. Each creature in a 20-foot-radius sphere centered on that point must make a Dexterity saving throw. A creature takes 7d10 fire damage on a failed save.","classes":["Cleric","Druid","Sorcerer","Wizard"]},
    {"name":"Teleport","level":7,"school":"Conjuration","casting_time":"1 action","range":"10 ft","components":"V","duration":"Instantaneous","description":"This program instantly transports you and up to eight willing creatures of your choice that you can see within range, or a single object that you can see within range, to a destination you select.","classes":["Bard","Sorcerer","Wizard"]},
    {"name":"Sunburst","level":8,"school":"Evocation","casting_time":"1 action","range":"150 ft","components":"V,S,M","duration":"Instantaneous","description":"Brilliant sunlight flashes in a 60-foot radius centered on a point you choose within range. Each creature in that area must make a Constitution saving throw. A creature takes 12d6 radiant damage on a failed save.","classes":["Cleric","Druid","Wizard"]},
    {"name":"Maze","level":8,"school":"Conjuration","casting_time":"1 action","range":"60 ft","components":"V,S","duration":"10 minutes","description":"You banish a creature that you can see within range into a labyrinthine demiplane. The target remains there for the duration or until it escapes the maze.","classes":["Wizard"]},
    {"name":"Meteor Swarm","level":9,"school":"Evocation","casting_time":"1 action","range":"1 mile","components":"V,S","duration":"Instantaneous","description":"Blazing orbs of fire plummet to the ground at four different points you can see within range. Each creature in a 40-foot-radius sphere centered on each point you choose must make a Dexterity saving throw. The sphere spreads around corners. A creature takes 20d6 fire damage and 20d6 bludgeoning damage on a failed save.","classes":["Sorcerer","Wizard"]},
    {"name":"Time Stop","level":9,"school":"Transmutation","casting_time":"1 action","range":"Self","components":"V","duration":"Instantaneous","description":"You briefly stop the flow of time for everyone but yourself. No time passes for other creatures, while you take 1d4 + 1 turns in a row, during which you can use actions and move as normal.","classes":["Wizard"]},
    {"name":"Wish","level":9,"school":"Conjuration","casting_time":"1 action","range":"Self","components":"V","duration":"Instantaneous","description":"Wish is the mightiest spell a mortal creature can cast. By simply speaking aloud, you can alter the very foundations of reality in accord with what you desire.","classes":["Sorcerer","Wizard"]},
    {"name":"Sacred Flame","level":0,"school":"Evocation","casting_time":"1 action","range":"60 ft","components":"V,S","duration":"Instantaneous","description":"Flame-like radiance descends on a creature that you can see within range. The target must succeed on a Dexterity saving throw or take 1d8 radiant damage.","classes":["Cleric"]},
    {"name":"Guidance","level":0,"school":"Divination","casting_time":"1 action","range":"Touch","components":"V,S","duration":"Concentration, up to 1 minute","description":"You touch one willing creature. Once before the spell ends, the target can roll a d4 and add the number rolled to one ability check of its choice.","classes":["Cleric","Druid"]},
    {"name":"Cure Wounds","level":1,"school":"Evocation","casting_time":"1 action","range":"Touch","components":"V,S","duration":"Instantaneous","description":"A creature you touch regains a number of hit points equal to 1d8 + your spellcasting ability modifier.","classes":["Bard","Cleric","Druid","Paladin","Ranger"]},
    {"name":"Healing Word","level":1,"school":"Evocation","casting_time":"1 bonus action","range":"60 ft","components":"V","duration":"Instantaneous","description":"A creature of your choice that you can see within range regains hit points equal to 1d4 + your spellcasting ability modifier.","classes":["Bard","Cleric","Druid"]},
    {"name":"Bless","level":1,"school":"Enchantment","casting_time":"1 action","range":"30 ft","components":"V,S,M","duration":"Concentration, up to 1 minute","description":"You bless up to three creatures of your choice within range. Whenever a target makes an attack roll or a saving throw before the spell ends, the target can roll a d4 and add the number rolled to the attack roll or saving throw.","classes":["Cleric","Paladin"]},
    {"name":"Faerie Fire","level":1,"school":"Evocation","casting_time":"1 action","range":"60 ft","components":"V","duration":"Concentration, up to 1 minute","description":"Each object in a 20-foot cube within range is outlined in blue, green, or violet light (your choice). Any creature in the area when the spell is cast is also outlined in light if it fails a Dexterity saving throw.","classes":["Bard","Druid"]},
]
SPELLS = SPELLS + EXTRA_SPELLS
seen = set()
unique_spells = []
for s in SPELLS:
    if s["name"] not in seen:
        seen.add(s["name"])
        unique_spells.append(s)
SPELLS = sorted(unique_spells, key=lambda s: (s.get("level", 0), s["name"]))

# ─── Extra monsters ─────────────────────────────────────────
EXTRA_MONSTERS = [
    {"name":"Goblin","cr":"1/4","xp":50,"hp":7,"ac":15,"type":"Humanoid (goblinoid)","size":"Small","alignment":"Neutral evil"},
    {"name":"Orc","cr":"1/2","xp":100,"hp":15,"ac":13,"type":"Humanoid (orc)","size":"Medium","alignment":"Chaotic evil"},
    {"name":"Wolf","cr":"1/4","xp":50,"hp":11,"ac":13,"type":"Beast","size":"Medium","alignment":"Unaligned"},
    {"name":"Giant Spider","cr":"1","xp":200,"hp":26,"ac":14,"type":"Beast","size":"Large","alignment":"Unaligned"},
    {"name":"Ogre","cr":"2","xp":450,"hp":59,"ac":11,"type":"Giant","size":"Large","alignment":"Chaotic evil"},
    {"name":"Troll","cr":"5","xp":1800,"hp":84,"ac":15,"type":"Giant","size":"Large","alignment":"Chaotic evil"},
    {"name":"Vampire","cr":"13","xp":10000,"hp":144,"ac":16,"type":"Undead","size":"Medium","alignment":"Lawful evil"},
    {"name":"Adult Red Dragon","cr":"17","xp":18000,"hp":256,"ac":19,"type":"Dragon","size":"Huge","alignment":"Chaotic evil"},
    {"name":"Ancient Black Dragon","cr":"21","xp":33000,"hp":367,"ac":22,"type":"Dragon","size":"Gargantuan","alignment":"Chaotic evil"},
    {"name":"Lich","cr":"21","xp":33000,"hp":135,"ac":17,"type":"Undead","size":"Medium","alignment":"Neutral evil"},
    {"name":"Tarrasque","cr":"30","xp":155000,"hp":676,"ac":25,"type":"Monstrosity","size":"Gargantuan","alignment":"Unaligned"},
    {"name":"Skeleton","cr":"1/4","xp":50,"hp":13,"ac":13,"type":"Undead","size":"Medium","alignment":"Lawful evil"},
    {"name":"Zombie","cr":"1/4","xp":50,"hp":22,"ac":8,"type":"Undead","size":"Medium","alignment":"Neutral evil"},
    {"name":"Ghoul","cr":"1","xp":200,"hp":22,"ac":12,"type":"Undead","size":"Medium","alignment":"Chaotic evil"},
    {"name":"Wraith","cr":"5","xp":1800,"hp":67,"ac":13,"type":"Undead","size":"Medium","alignment":"Neutral evil"},
    {"name":"Beholder","cr":"13","xp":10000,"hp":180,"ac":18,"type":"Aberration","size":"Large","alignment":"Lawful evil"},
    {"name":"Mind Flayer","cr":"7","xp":2900,"hp":71,"ac":15,"type":"Aberration","size":"Medium","alignment":"Lawful evil"},
    {"name":"Harpy","cr":"1","xp":200,"hp":38,"ac":11,"type":"Monstrosity","size":"Medium","alignment":"Chaotic evil"},
    {"name":"Griffin","cr":"2","xp":450,"hp":59,"ac":12,"type":"Monstrosity","size":"Large","alignment":"Unaligned"},
    {"name":"Hydra","cr":"8","xp":3900,"hp":172,"ac":15,"type":"Monstrosity","size":"Huge","alignment":"Unaligned"},
]
MONSTERS = MONSTERS + EXTRA_MONSTERS
seen_m = set()
unique_monsters = []
for m in MONSTERS:
    if m["name"] not in seen_m:
        seen_m.add(m["name"])
        unique_monsters.append(m)

def cr_sort_key(m):
    cr = str(m.get("cr", "0"))
    if "/" in cr:
        parts = cr.split("/")
        return float(parts[0]) / float(parts[1])
    try:
        return float(cr)
    except ValueError:
        return 0.0
MONSTERS = sorted(unique_monsters, key=cr_sort_key)

# ─────────────────────────────────────────────────────────────
#  THEME & DESIGN SYSTEM
# ─────────────────────────────────────────────────────────────
class Theme:
    """Design tokens for the dndkit UI."""
    PRIMARY = "#7C3AED"
    PRIMARY_DARK = "#5B21B6"
    PRIMARY_LIGHT = "#A78BFA"
    ACCENT = "#F59E0B"
    ACCENT_LIGHT = "#FCD34D"
    ACCENT_DARK = "#D97706"
    BG = "#0F0A1F"
    SURFACE = "#1A1430"
    SURFACE_HOVER = "#251D40"
    SURFACE_HIGH = "#2D2450"
    BORDER = "#3D3366"
    TEXT_PRIMARY = "#F1EFFF"
    TEXT_SECONDARY = "#A89FC9"
    TEXT_MUTED = "#746999"
    SUCCESS = "#10B981"
    WARNING = "#F59E0B"
    DANGER = "#EF4444"
    INFO = "#3B82F6"
    DIFF_TRIVIAL = "#6EE7B7"
    DIFF_EASY = "#86EFAC"
    DIFF_MEDIUM = "#FCD34D"
    DIFF_HARD = "#FB923C"
    DIFF_DEADLY = "#F87171"
    RADIUS_SM = 6
    RADIUS_MD = 10
    RADIUS_LG = 16
    SHADOW_CARD = ft.BoxShadow(
        spread_radius=0,
        blur_radius=20,
        color="#00000066",
        offset=ft.Offset(0, 4),
    )

# ─────────────────────────────────────────────────────────────
#  UTILITY FUNCTIONS
# ─────────────────────────────────────────────────────────────
def format_cr(cr_val):
    """Format CR value for display."""
    if isinstance(cr_val, (int, float)):
        if cr_val == int(cr_val):
            return str(int(cr_val))
        fracs = {0.125: "1/8", 0.25: "1/4", 0.5: "1/2", 0.333: "1/3", 0.667: "2/3", 0.75: "3/4"}
        for k, v in fracs.items():
            if abs(cr_val - k) < 0.02:
                return v
        return str(cr_val)
    return str(cr_val)

CR_TO_XP = {
    "0": 10, "1/8": 25, "1/4": 50, "1/2": 100,
    "1": 200, "2": 450, "3": 700, "4": 1100,
    "5": 1800, "6": 2300, "7": 2900, "8": 3900,
    "9": 5000, "10": 5900, "11": 7200, "12": 8400,
    "13": 10000, "14": 11500, "15": 13000, "16": 15000,
    "17": 18000, "18": 20000, "19": 22000, "20": 25000,
    "21": 33000, "22": 41000, "23": 50000, "24": 62000,
    "30": 155000,
}

def cr_xp(cr_val):
    if isinstance(cr_val, (int, float)):
        for key, xp in CR_TO_XP.items():
            if "/" in key:
                parts = key.split("/")
                val = float(parts[0]) / float(parts[1])
            else:
                val = float(key)
            if abs(val - cr_val) < 0.01:
                return xp
        return 0
    return CR_TO_XP.get(str(cr_val), 0)

XP_THRESHOLDS = {
    1:  (25, 50, 75, 100),
    2:  (50, 100, 150, 200),
    3:  (75, 150, 225, 400),
    4:  (125, 250, 375, 500),
    5:  (250, 500, 750, 1100),
    6:  (300, 600, 900, 1400),
    7:  (350, 750, 1100, 1700),
    8:  (450, 900, 1400, 2100),
    9:  (550, 1100, 1600, 2400),
    10: (600, 1200, 1900, 2800),
    11: (800, 1600, 2400, 3600),
    12: (1000, 2000, 3000, 4500),
    13: (1100, 2200, 3400, 5100),
    14: (1250, 2500, 3800, 5700),
    15: (1400, 2800, 4300, 6400),
    16: (1600, 3200, 4800, 7200),
    17: (2000, 3900, 5900, 8800),
    18: (2100, 4200, 6300, 9500),
    19: (2400, 4900, 7300, 10900),
    20: (2800, 5700, 8500, 12700),
}

def encounter_multiplier(num_monsters):
    if num_monsters == 0: return 0.0
    if num_monsters == 1: return 1.0
    if num_monsters == 2: return 1.5
    if num_monsters <= 6: return 2.0
    if num_monsters <= 10: return 2.5
    if num_monsters <= 14: return 3.0
    return 4.0

def difficulty_label(adjusted_xp, party_levels):
    n = len(party_levels)
    if n == 0: return "Trivial"
    easy = sum(XP_THRESHOLDS.get(lvl, (0,0,0,0))[1] for lvl in party_levels)
    medium = sum(XP_THRESHOLDS.get(lvl, (0,0,0,0))[2] for lvl in party_levels)
    hard = sum(XP_THRESHOLDS.get(lvl, (0,0,0,0))[3] for lvl in party_levels)
    deadly = hard * 1.5
    if adjusted_xp < easy: return "Trivial"
    if adjusted_xp < medium: return "Easy"
    if adjusted_xp < hard: return "Medium"
    if adjusted_xp < deadly: return "Hard"
    return "Deadly"

def difficulty_color(diff):
    return {
        "Trivial": Theme.DIFF_TRIVIAL,
        "Easy": Theme.DIFF_EASY,
        "Medium": Theme.DIFF_MEDIUM,
        "Hard": Theme.DIFF_HARD,
        "Deadly": Theme.DIFF_DEADLY,
    }.get(diff, Theme.TEXT_PRIMARY)

# ─── Dice rolling ───────────────────────────────────────────
def roll_dice(expr):
    """Parse and roll a dice expression like '2d6+3' or 'adv' or '4d6'"""
    expr = expr.strip().lower()
    if expr in ("adv", "advantage"):
        r1, r2 = random.randint(1,20), random.randint(1,20)
        return f"2d20 (advantage): [{r1}, {r2}] → {max(r1,r2)} (keep highest)", [max(r1,r2)]
    if expr in ("dis", "disadv", "disadvantage"):
        r1, r2 = random.randint(1,20), random.randint(1,20)
        return f"2d20 (disadvantage): [{r1}, {r2}] → {min(r1,r2)} (keep lowest)", [min(r1,r2)]
    if expr == "4":
        rolls = [random.randint(1,6) for _ in range(4)]
        sorted_rolls = sorted(rolls, reverse=True)
        best = sum(sorted_rolls[:3])
        return f"4d6 drop lowest: {rolls} → {best} (drop {min(rolls)})", [best]
    if expr == "stats":
        results = []
        for _ in range(6):
            rolls = [random.randint(1,6) for _ in range(4)]
            sorted_rolls = sorted(rolls, reverse=True)
            results.append(sum(sorted_rolls[:3]))
        return f"Ability scores (4d6 drop lowest ×6):  {'  '.join(str(r) for r in results)}", results

    # Parse general dice expression
    tokens = re.findall(r'[+-]?\s*(?:\d*d\d+kh?\d*|\d+)', expr)
    if not tokens:
        m = re.match(r'(\d*)d(\d+)(kh?\d+)?\s*([+-]\s*\d+)?', expr)
        if not m:
            return f"Invalid: {expr}", []
        num_dice = int(m.group(1) or 1)
        sides = int(m.group(2))
        keep = m.group(3)
        modifier = int(m.group(4).replace(" ","")) if m.group(4) else 0
        rolls = [random.randint(1, sides) for _ in range(num_dice)]
        if keep and 'k' in keep:
            keep_n = int(keep.replace('kh','').replace('k',''))
            sorted_rolls = sorted(rolls, reverse=True)
            kept = sorted_rolls[:keep_n]
            total = sum(kept) + modifier
            detail = f"{num_dice}d{sides}{keep}+{modifier}: {rolls} → keep {keep_n} highest {kept} = {sum(kept)} + {modifier} = {total}"
            return detail, [total]
        else:
            total = sum(rolls) + modifier
            detail = f"{num_dice}d{sides} + {modifier}: {rolls} = {sum(rolls)} + {modifier} = {total}"
            return detail, [total]

    total = 0
    detail_parts = []
    for token in tokens:
        token = token.strip()
        if 'd' in token:
            m = re.match(r'([+-]?)\s*(\d*)d(\d+)(kh?\d+)?', token)
            if m:
                sign = -1 if m.group(1) == '-' else 1
                num = int(m.group(2) or 1)
                sides = int(m.group(3))
                rolls = [random.randint(1, sides) * sign for _ in range(num)]
                total += sum(rolls)
                detail_parts.append(f"{num}d{sides}:{rolls}")
        else:
            val = int(token.replace(" ",""))
            total += val
            detail_parts.append(f"{val:+}")

    return f"{expr} = {total}  ({' '.join(detail_parts)})", [total]

# ─── Loot generation ────────────────────────────────────────
GEMS = [
    "Azurite (10 gp)", "Banded agate (10 gp)", "Blue quartz (10 gp)",
    "Carnelian (50 gp)", "Chrysoprase (100 gp)", "Citrine (50 gp)",
    "Jasper (50 gp)", "Moonstone (50 gp)", "Onyx (50 gp)",
    "Amethyst (100 gp)", "Garnet (100 gp)", "Jade (100 gp)",
    "Golden pearl (100 gp)", "Pink pearl (100 gp)", "Silver pearl (100 gp)",
    "Spinel (100 gp)", "Tourmaline (100 gp)",
    "Black pearl (500 gp)", "Bloodstone (500 gp)", "Coral (100 gp)",
]
MAGIC_ITEMS_COMMON = [
    "Potion of Healing", "Spell Scroll (1st level)", "Potion of Climbing",
    "Cloak of the Manta Ray", "Gauntlets of Ogre Power", "Goggles of Night",
    "Potion of Greater Healing", "Ring of Water Walking", "Slippers of Spider Climbing",
    "Wand of Magic Detection", "Bag of Holding", "Boots of Striding and Springing",
    "Broom of Flying", "Cloak of Protection +1", "Pearl of Power",
    "Potion of Superior Healing", "Ring of Protection +1",
]
MAGIC_ITEMS_RARE = [
    "Ammunition, +2", "Amulet of Health", "Armor +2", "Belt of Giant Strength",
    "Boots of Speed", "Cloak of Displacement", "Dagger of Venom",
    "Flame Tongue (longsword)", "Helm of Telepathy", "Ioun Stone (absorption)",
    "Potion of Invulnerability", "Rapier +2", "Ring of Free Action",
    "Rod of Rulership", "Scimitar of Speed", "Sword of Life Stealing",
    "Wand of Fear", "Wings of Flying",
]
MAGIC_ITEMS_VERY_RARE = [
    "Amulet of the Planes", "Belt of Cloud Giant Strength", "Cloak of Invisibility",
    "Dancing Sword", "Demon Armor", "Efreeti Bottle", "Hammer of Thunderbolts",
    "Holy Avenger", "Luck Blade", "Plate Armor +3", "Ring of Spell Turning",
    "Sword of Sharpness", "Tome of the Stilled Tongue", "Vorpal Sword",
    "Wand of Orcus", "Well of Many Worlds",
]
ART_OBJECTS = [
    "Silver chalice (25 gp)", "Gold ring (25 gp)", "Embroidered silk (25 gp)",
    "Carved ivory (75 gp)", "Gold locket (75 gp)", "Bronze scimitar (100 gp)",
    "Fine painting (200 gp)", "Necklace of blue quartz (250 gp)",
    "Silver-and-pearl earring (500 gp)", "Gold-and-platinum chalice (750 gp)",
    "Jeweled gold crown (5000 gp)", "Bejewelled platinum sceptre (7500 gp)",
]

def generate_loot(cr_tier="1"):
    result = {}
    if cr_tier == "1":
        coins = {"cp": random.randint(1,20)*100, "sp": random.randint(1,12)*10, "gp": random.randint(1,8)*5}
    elif cr_tier == "2":
        coins = {"cp": random.randint(2,20)*100, "sp": random.randint(2,20)*100, "gp": random.randint(1,12)*50, "pp": random.randint(1,3)*5}
    elif cr_tier == "3":
        coins = {"gp": random.randint(2,16)*100, "pp": random.randint(1,8)*10}
    else:
        coins = {"gp": random.randint(10,40)*1000, "pp": random.randint(2,20)*100}
    result["coins"] = coins

    items = []
    if cr_tier in ("1","2"):
        if random.random() < 0.5: items.append(random.choice(GEMS))
        if random.random() < 0.3: items.append(random.choice(ART_OBJECTS[:6]))
        if random.random() < 0.2: items.append(random.choice(MAGIC_ITEMS_COMMON[:10]))
    elif cr_tier == "3":
        if random.random() < 0.7: items.append(random.choice(GEMS[10:]))
        if random.random() < 0.5: items.append(random.choice(ART_OBJECTS[4:]))
        if random.random() < 0.6: items.append(random.choice(MAGIC_ITEMS_COMMON + MAGIC_ITEMS_RARE[:8]))
    else:
        if random.random() < 0.8: items.append(random.choice(GEMS[15:]))
        if random.random() < 0.6: items.append(random.choice(ART_OBJECTS[7:]))
        if random.random() < 0.7: items.append(random.choice(MAGIC_ITEMS_RARE + MAGIC_ITEMS_VERY_RARE[:6]))
    result["items"] = items
    return result

# ─── Name generation ────────────────────────────────────────
def generate_name(race="Human", gender="any"):
    first_male = NAMES_DATA.get("first_male", ["Aldric","Borin","Caelum","Darian","Erion"])
    first_female = NAMES_DATA.get("first_female", ["Aelwen","Brielle","Cerys","Dara","Elara"])
    surnames = NAMES_DATA.get("surnames", ["Stonehelm","Ironvein","Swiftfoot","Stormwind","Oakenshield"])

    if gender == "male":
        first = random.choice(first_male)
    elif gender == "female":
        first = random.choice(first_female)
    else:
        first = random.choice(first_male + first_female)

    surname = random.choice(surnames)
    return f"{first} {surname}"

TRAITS = [
    "Always speaks in a whisper", "Laughs at inappropriate times",
    "Collects shiny rocks", "Hates being indoors",
    "Always sings to themselves", "Extremely polite",
    "Suspicious of everyone", "Tells terrible jokes constantly",
    "Always late to everything", "Obsessed with cleanliness",
    "Loves gambling", "Afraid of the dark",
    "Always chewing on something", "Draws in the dirt with a stick",
    "Refuses to sit on chairs", "Always wears a hat indoors",
    "Rambles about the old days", "Knows everyone's name somehow",
    "Constantly polishing their equipment", "Hums while they work",
]

# ─────────────────────────────────────────────────────────────
#  UI COMPONENTS
# ─────────────────────────────────────────────────────────────
def card(content, padding=20, bgcolor=Theme.SURFACE, radius=Theme.RADIUS_LG, shadow=True, expand=False):
    return ft.Container(
        content=content,
        padding=padding,
        bgcolor=bgcolor,
        border_radius=radius,
        shadow=Theme.SHADOW_CARD if shadow else None,
        border=ft.Border.all(1, Theme.BORDER),
        expand=expand,
    )

def chip(text, color=Theme.PRIMARY, text_color=Theme.TEXT_PRIMARY, size=12):
    return ft.Container(
        ft.Text(text, size=size, weight=ft.FontWeight.BOLD, color=text_color),
        padding=ft.Padding.symmetric(horizontal=10, vertical=4),
        bgcolor=color + "33",
        border_radius=20,
    )

def stat_block(label, value, value_color=Theme.TEXT_PRIMARY):
    return ft.Column([
        ft.Text(label.upper(), size=10, color=Theme.TEXT_MUTED, weight=ft.FontWeight.BOLD),
        ft.Text(str(value), size=22, weight=ft.FontWeight.BOLD, color=value_color),
    ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

def page_header(title, subtitle, icon=ft.Icons.CASINO):
    return ft.Container(
        ft.Row([
            ft.Container(
                ft.Icon(icon, size=32, color=Theme.ACCENT_LIGHT),
                width=56, height=56,
                bgcolor=Theme.PRIMARY_DARK,
                border_radius=16,
                alignment=ft.alignment.Alignment.CENTER,
            ),
            ft.Column([
                ft.Text(title, size=28, weight=ft.FontWeight.BOLD, color=Theme.TEXT_PRIMARY),
                ft.Text(subtitle, size=13, color=Theme.TEXT_SECONDARY),
            ], tight=True),
        ], spacing=16),
        padding=ft.Padding.only(bottom=20),
    )

def section_title(text, icon=None):
    parts = []
    if icon:
        parts.append(ft.Icon(icon, size=16, color=Theme.ACCENT))
    parts.append(ft.Text(text, size=15, weight=ft.FontWeight.BOLD, color=Theme.TEXT_PRIMARY))
    return ft.Container(
        ft.Row(parts, spacing=8),
        padding=ft.Padding.only(top=16, bottom=8),
    )

def dice_button(label, expr, on_click, icon_name=None):
    """A styled quick-roll dice button."""
    parts = []
    if icon_name:
        parts.append(ft.Icon(icon_name, size=14))
    parts.append(ft.Text(label, size=12, weight=ft.FontWeight.BOLD))
    btn = ft.ElevatedButton(
        content=ft.Row(parts, spacing=6, alignment=ft.MainAxisAlignment.CENTER),
        on_click=lambda e: on_click(expr),
        style=ft.ButtonStyle(
            bgcolor={
                ft.ControlState.HOVERED: Theme.PRIMARY,
                ft.ControlState.DEFAULT: Theme.SURFACE_HIGH,
            },
            color=Theme.TEXT_PRIMARY,
            shape=ft.RoundedRectangleBorder(radius=Theme.RADIUS_MD),
            padding=ft.Padding.symmetric(horizontal=16, vertical=12),
        ),
    )
    return btn

def primary_button(text, on_click, icon_name=None, expand=False):
    """A prominent primary action button."""
    parts = []
    if icon_name:
        parts.append(ft.Icon(icon_name, size=16))
    parts.append(ft.Text(text, size=13, weight=ft.FontWeight.BOLD))
    btn = ft.ElevatedButton(
        content=ft.Row(parts, spacing=8, alignment=ft.MainAxisAlignment.CENTER),
        on_click=on_click,
        style=ft.ButtonStyle(
            bgcolor={
                ft.ControlState.HOVERED: Theme.PRIMARY,
                ft.ControlState.DEFAULT: Theme.PRIMARY_DARK,
            },
            color=Theme.TEXT_PRIMARY,
            shape=ft.RoundedRectangleBorder(radius=Theme.RADIUS_MD),
            padding=ft.Padding.symmetric(horizontal=20, vertical=14),
        ),
        expand=expand,
    )
    return btn

def list_item_card(content, on_click=None, hover=True, padding=12):
    ctrl = ft.Container(
        content=content,
        padding=padding,
        bgcolor=Theme.SURFACE,
        border_radius=Theme.RADIUS_MD,
        border=ft.Border.all(1, Theme.BORDER),
        on_click=on_click,
    )
    if hover:
        def on_hover(e):
            if e.data == "true" or e.data is True:
                e.control.bgcolor = Theme.SURFACE_HOVER
            else:
                e.control.bgcolor = Theme.SURFACE
            e.control.update()
        ctrl.on_hover = on_hover
    return ctrl

# ─────────────────────────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────────────────────────
def main(page: ft.Page):
    page.title = "dndkit — D&D 5e DM Toolkit"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = Theme.BG
    page.window_width = 1180
    page.window_height = 780
    page.window_min_width = 900
    page.window_min_height = 600
    page.padding = 0
    page.spacing = 0
    page.theme = ft.Theme(color_scheme_seed=Theme.PRIMARY)

    # ─── State ────────────────────────────────────────────
    selected_page = "dice"
    dice_history = []
    characters = []
    initiative_list = []
    party_levels = [5, 5, 5, 5]
    encounter_monsters = []
    name_history = []

    # ─── Navigation ───────────────────────────────────────
    nav_items = [
        ("dice", ft.Icons.CASINO, "Dice Roller"),
        ("characters", ft.Icons.PERSON_OUTLINE, "Characters"),
        ("spells", ft.Icons.MENU_BOOK, "Spellbook"),
        ("initiative", ft.Icons.SWAP_VERT, "Initiative"),
        ("encounter", ft.Icons.SHIELD_OUTLINED, "Encounter"),
        ("loot", ft.Icons.STAR, "Loot"),
        ("names", ft.Icons.PERSON_ADD, "NPC Names"),
    ]

    nav_destinations = [
        ft.NavigationRailDestination(
            icon=icon,
            label=label,
            padding=ft.Padding.symmetric(vertical=4),
        )
        for _, icon, label in nav_items
    ]

    def nav_click(e):
        nonlocal selected_page
        idx = e.control.selected_index
        selected_page = nav_items[idx][0]
        content.content = build_page(selected_page)
        page.update()

    # Sidebar with branding
    sidebar_logo = ft.Container(
        ft.Column([
            ft.Container(
                ft.Text("⚔️", size=28),
                width=52, height=52,
                bgcolor=Theme.PRIMARY_DARK,
                border_radius=14,
                alignment=ft.alignment.Alignment.CENTER,
                margin=ft.Margin.only(bottom=8),
            ),
            ft.Text("dndkit", size=20, weight=ft.FontWeight.BOLD, color=Theme.TEXT_PRIMARY),
            ft.Text("DM Toolkit", size=11, color=Theme.TEXT_MUTED),
        ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=20,
    )

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=120,
        min_extended_width=200,
        group_alignment=-0.9,
        destinations=nav_destinations,
        on_change=nav_click,
        bgcolor=Theme.SURFACE,
        indicator_color=Theme.PRIMARY + "44",
        indicator_shape=ft.RoundedRectangleBorder(radius=8),
        expand=True,
    )

    sidebar = ft.Column(
        [sidebar_logo, ft.Divider(height=1, color=Theme.BORDER), rail],
        expand=True,
    )

    # ─── Dice Roller Page ─────────────────────────────────
    dice_result_text = ft.Text(
        "Roll some dice to get started!",
        size=16,
        color=Theme.TEXT_PRIMARY,
    )
    history_list = ft.ListView(height=260, spacing=6)

    def update_history():
        history_list.controls = [
            ft.Container(
                ft.Text(h, size=12, color=Theme.TEXT_PRIMARY),
                padding=10,
                bgcolor=Theme.SURFACE,
                border_radius=Theme.RADIUS_SM,
                border=ft.Border.all(1, Theme.BORDER),
            ) for h in dice_history
        ]

    dice_input = ft.TextField(
        label="Dice expression",
        hint_text="e.g. 2d6+3, adv, dis, stats, 1d20+5",
        expand=True,
        on_submit=lambda e: do_roll(dice_input.value),
        border_color=Theme.BORDER,
        focused_border_color=Theme.PRIMARY,
        bgcolor=Theme.SURFACE,
    )

    def do_roll(expr):
        expr = (expr or "").strip()
        if not expr:
            return
        result, rolls = roll_dice(expr)
        dice_history.insert(0, result)
        if len(dice_history) > 15:
            dice_history.pop()
        dice_result_text.value = result
        update_history()
        page.update()

    def quick_roll(expr):
        dice_input.value = expr
        do_roll(expr)

    def build_dice_page():
        return ft.Column([
            page_header("Dice Roller", "Roll any dice combination. Press Enter to roll.", ft.Icons.CASINO),
            ft.Row([
                dice_input,
                primary_button("Roll!", lambda e: do_roll(dice_input.value), ft.Icons.CASINO),
            ]),
            ft.Container(height=16),
            card(
                ft.Column([
                    ft.Text("Result", size=11, color=Theme.TEXT_MUTED, weight=ft.FontWeight.BOLD),
                    ft.Container(height=6),
                    ft.Container(
                        dice_result_text,
                        padding=16,
                        bgcolor=Theme.SURFACE_HIGH,
                        border_radius=Theme.RADIUS_MD,
                    ),
                ], tight=True),
            ),
            ft.Container(height=12),
            ft.Row([
                ft.Text("Quick Roll", size=13, weight=ft.FontWeight.BOLD, color=Theme.TEXT_SECONDARY),
            ]),
            ft.Row([
                dice_button("d20", "1d20", quick_roll),
                dice_button("d12", "1d12", quick_roll),
                dice_button("d10", "1d10", quick_roll),
                dice_button("d8", "1d8", quick_roll),
                dice_button("d6", "1d6", quick_roll),
                dice_button("d4", "1d4", quick_roll),
                dice_button("d100", "1d100", quick_roll),
            ], wrap=True, spacing=8),
            ft.Container(height=8),
            ft.Row([
                dice_button("Advantage", "adv", quick_roll),
                dice_button("Disadvantage", "dis", quick_roll),
                dice_button("4d6 Stats", "stats", quick_roll),
            ], wrap=True, spacing=8),
            section_title("Roll History", ft.Icons.HISTORY),
            history_list,
        ], scroll=ft.ScrollMode.AUTO, expand=True)

    # ─── Characters Page ───────────────────────────────────
    char_name = ft.TextField(label="Name", width=160, bgcolor=Theme.SURFACE, border_color=Theme.BORDER, focused_border_color=Theme.PRIMARY)
    char_level = ft.TextField(label="Level", value="1", width=70, bgcolor=Theme.SURFACE, border_color=Theme.BORDER, focused_border_color=Theme.PRIMARY, keyboard_type=ft.KeyboardType.NUMBER)
    char_hp = ft.TextField(label="Max HP", value="10", width=80, bgcolor=Theme.SURFACE, border_color=Theme.BORDER, focused_border_color=Theme.PRIMARY, keyboard_type=ft.KeyboardType.NUMBER)
    char_ac = ft.TextField(label="AC", value="10", width=60, bgcolor=Theme.SURFACE, border_color=Theme.BORDER, focused_border_color=Theme.PRIMARY, keyboard_type=ft.KeyboardType.NUMBER)
    char_str = ft.TextField(label="STR", value="10", width=55, bgcolor=Theme.SURFACE, border_color=Theme.BORDER, focused_border_color=Theme.PRIMARY, keyboard_type=ft.KeyboardType.NUMBER)
    char_dex = ft.TextField(label="DEX", value="10", width=55, bgcolor=Theme.SURFACE, border_color=Theme.BORDER, focused_border_color=Theme.PRIMARY, keyboard_type=ft.KeyboardType.NUMBER)
    char_con = ft.TextField(label="CON", value="10", width=55, bgcolor=Theme.SURFACE, border_color=Theme.BORDER, focused_border_color=Theme.PRIMARY, keyboard_type=ft.KeyboardType.NUMBER)
    char_int = ft.TextField(label="INT", value="10", width=55, bgcolor=Theme.SURFACE, border_color=Theme.BORDER, focused_border_color=Theme.PRIMARY, keyboard_type=ft.KeyboardType.NUMBER)
    char_wis = ft.TextField(label="WIS", value="10", width=55, bgcolor=Theme.SURFACE, border_color=Theme.BORDER, focused_border_color=Theme.PRIMARY, keyboard_type=ft.KeyboardType.NUMBER)
    char_cha = ft.TextField(label="CHA", value="10", width=55, bgcolor=Theme.SURFACE, border_color=Theme.BORDER, focused_border_color=Theme.PRIMARY, keyboard_type=ft.KeyboardType.NUMBER)
    char_list = ft.ListView(height=350, spacing=6)

    def add_char(e):
        name = char_name.value.strip()
        if not name:
            return
        try:
            characters.append({
                "name": name,
                "level": int(char_level.value),
                "hp": int(char_hp.value),
                "max_hp": int(char_hp.value),
                "ac": int(char_ac.value),
                "str": int(char_str.value),
                "dex": int(char_dex.value),
                "con": int(char_con.value),
                "int": int(char_int.value),
                "wis": int(char_wis.value),
                "cha": int(char_cha.value),
            })
            char_name.value = ""
            update_char_list()
            page.update()
        except ValueError:
            pass

    def update_char_list():
        char_list.controls = []
        for i, c in enumerate(characters):
            mods = {k: (c[k.lower()] - 10) // 2 for k in ["STR","DEX","CON","INT","WIS","CHA"]}
            mod_str = "  ".join(f"{k} {v:+}" for k, v in mods.items())

            def delete_char(idx, _e=None):
                del characters[idx]
                update_char_list()
                page.update()

            char_list.controls.append(
                list_item_card(
                    ft.Column([
                        ft.Row([
                            ft.Text(c["name"], size=16, weight=ft.FontWeight.BOLD, color=Theme.TEXT_PRIMARY, expand=True),
                            chip(f"Lv.{c['level']}", Theme.PRIMARY_DARK),
                            ft.Container(width=6),
                            chip(f"AC {c['ac']}", Theme.SURFACE_HIGH),
                            ft.Container(width=6),
                            chip(f"HP {c['hp']}/{c['max_hp']}", Theme.DIFF_HARD),
                            ft.IconButton(
                                ft.Icons.DELETE_OUTLINE,
                                icon_size=18,
                                icon_color=Theme.TEXT_MUTED,
                                on_click=lambda e, idx=i: delete_char(idx),
                            ),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Text(mod_str, size=11, color=Theme.TEXT_SECONDARY, font_family="monospace"),
                    ], tight=True),
                )
            )

    def build_characters_page():
        return ft.Column([
            page_header("Character Manager", "Track player characters and their ability scores.", ft.Icons.PERSON_OUTLINE),
            card(
                ft.Column([
                    ft.Text("Add Character", size=14, weight=ft.FontWeight.BOLD, color=Theme.TEXT_PRIMARY),
                    ft.Container(height=8),
                    ft.Row([char_name, char_level, char_hp, char_ac], wrap=True, spacing=8),
                    ft.Row([char_str, char_dex, char_con, char_int, char_wis, char_cha], wrap=True, spacing=8),
                    ft.Container(height=8),
                    primary_button("Add Character", add_char, ft.Icons.ADD),
                ], tight=True),
            ),
            section_title(f"Characters ({len(characters)})", ft.Icons.GROUP),
            char_list,
        ], scroll=ft.ScrollMode.AUTO, expand=True)

    # ─── Spellbook Page ────────────────────────────────────
    spell_search = ft.TextField(
        label="Search spells...",
        hint_text="Filter by name, school, or class",
        on_change=lambda e: filter_spells(e.control.value.lower()),
        bgcolor=Theme.SURFACE,
        border_color=Theme.BORDER,
        focused_border_color=Theme.PRIMARY,
    )
    spell_list_view = ft.ListView(width=300, height=550, spacing=2)
    spell_detail = ft.Container(
        ft.Column([
            ft.Text("Select a spell", size=18, weight=ft.FontWeight.BOLD, color=Theme.TEXT_MUTED),
            ft.Container(height=4),
            ft.Text("Choose from the list to see full details.", size=13, color=Theme.TEXT_MUTED),
        ], tight=True, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=24,
        expand=True,
    )

    def show_spell(e):
        name = e.control.data
        spell = next((s for s in SPELLS if s["name"] == name), None)
        if not spell:
            return
        level_str = "Cantrip" if spell.get("level", 0) == 0 else f"Level {spell['level']}"
        spell_detail.content = ft.Column([
            ft.Text(spell["name"], size=24, weight=ft.FontWeight.BOLD, color=Theme.ACCENT_LIGHT),
            ft.Text(f"{level_str} · {spell.get('school','')}", size=12, color=Theme.TEXT_SECONDARY),
            ft.Divider(color=Theme.BORDER, height=20),
            ft.Row([
                stat_block("Casting Time", spell.get("casting_time","—")),
                stat_block("Range", spell.get("range","—")),
                stat_block("Components", spell.get("components","—")),
                stat_block("Duration", spell.get("duration","—")),
            ], wrap=True, spacing=20),
            ft.Container(height=12),
            ft.Text("DESCRIPTION", size=10, color=Theme.TEXT_MUTED, weight=ft.FontWeight.BOLD),
            ft.Container(height=4),
            ft.Text(spell.get("description","—"), size=13, color=Theme.TEXT_PRIMARY),
            ft.Container(height=12),
            ft.Text("CLASSES", size=10, color=Theme.TEXT_MUTED, weight=ft.FontWeight.BOLD),
            ft.Container(height=4),
            ft.Row([chip(cls, Theme.PRIMARY_DARK, Theme.PRIMARY_LIGHT) for cls in spell.get("classes", [])], wrap=True),
        ], tight=True, scroll=ft.ScrollMode.AUTO)
        page.update()

    def filter_spells(query):
        spell_list_view.controls = []
        for s in SPELLS:
            txt = f"{s['name']} {s.get('school','')} {' '.join(s.get('classes',[]))}".lower()
            if query in txt:
                lvl = s.get("level", 0)
                lvl_str = "C" if lvl == 0 else str(lvl)
                lvl_color = Theme.ACCENT if lvl == 0 else Theme.PRIMARY
                spell_list_view.controls.append(
                    ft.Container(
                        ft.Row([
                            ft.Container(
                                ft.Text(lvl_str, size=10, weight=ft.FontWeight.BOLD, color=Theme.TEXT_PRIMARY),
                                width=24, height=24,
                                bgcolor=lvl_color,
                                border_radius=12,
                                alignment=ft.alignment.Alignment.CENTER,
                            ),
                            ft.Text(s["name"], size=13, color=Theme.TEXT_PRIMARY, expand=True),
                        ], spacing=10),
                        padding=ft.Padding.symmetric(vertical=6, horizontal=10),
                        on_click=show_spell,
                        data=s["name"],
                        border_radius=Theme.RADIUS_SM,
                        on_hover=lambda e: setattr(e.control, 'bgcolor',
                            Theme.SURFACE_HOVER if e.data == 'true' or e.data is True else None),
                    )
                )
        page.update()

    filter_spells("")

    def build_spells_page():
        return ft.Column([
            page_header(f"Spellbook", f"Browse {len(SPELLS)} D&D 5e spells with full details.", ft.Icons.MENU_BOOK),
            spell_search,
            ft.Container(height=12),
            ft.Row([
                ft.Container(
                    spell_list_view,
                    bgcolor=Theme.SURFACE,
                    border_radius=Theme.RADIUS_LG,
                    border=ft.Border.all(1, Theme.BORDER),
                    padding=8,
                    width=320,
                ),
                card(spell_detail, expand=True),
            ], expand=True, spacing=12),
        ], expand=True)

    # ─── Initiative Page ───────────────────────────────────
    init_name = ft.TextField(label="Name", width=150, bgcolor=Theme.SURFACE, border_color=Theme.BORDER, focused_border_color=Theme.PRIMARY)
    init_init = ft.TextField(label="Initiative", value="10", width=90, bgcolor=Theme.SURFACE, border_color=Theme.BORDER, focused_border_color=Theme.PRIMARY, keyboard_type=ft.KeyboardType.NUMBER)
    init_hp = ft.TextField(label="HP", value="20", width=70, bgcolor=Theme.SURFACE, border_color=Theme.BORDER, focused_border_color=Theme.PRIMARY, keyboard_type=ft.KeyboardType.NUMBER)
    init_ac = ft.TextField(label="AC", value="12", width=60, bgcolor=Theme.SURFACE, border_color=Theme.BORDER, focused_border_color=Theme.PRIMARY, keyboard_type=ft.KeyboardType.NUMBER)
    init_view = ft.ListView(height=420, spacing=6)

    def add_init(e):
        name = init_name.value.strip()
        if not name:
            return
        try:
            initiative_list.append({
                "name": name,
                "init": int(init_init.value),
                "hp": int(init_hp.value),
                "max_hp": int(init_hp.value),
                "ac": int(init_ac.value),
                "conditions": [],
            })
            initiative_list.sort(key=lambda x: -x["init"])
            init_name.value = ""
            update_init_view()
            page.update()
        except ValueError:
            pass

    def damage_init(idx, amount):
        initiative_list[idx]["hp"] = max(0, initiative_list[idx]["hp"] + amount)
        update_init_view()
        page.update()

    def remove_init(idx):
        del initiative_list[idx]
        update_init_view()
        page.update()

    def update_init_view():
        init_view.controls = []
        for i, c in enumerate(initiative_list):
            hp_pct = max(0, min(100, c["hp"] / c["max_hp"] * 100)) if c["max_hp"] > 0 else 0
            hp_color = Theme.SUCCESS if hp_pct > 50 else Theme.WARNING if hp_pct > 25 else Theme.DANGER

            init_view.controls.append(
                list_item_card(
                    ft.Row([
                        ft.Container(
                            ft.Text(str(c["init"]), size=14, weight=ft.FontWeight.BOLD, color=Theme.TEXT_PRIMARY),
                            width=42, height=42,
                            bgcolor=Theme.PRIMARY_DARK,
                            border_radius=21,
                            alignment=ft.alignment.Alignment.CENTER,
                        ),
                        ft.Column([
                            ft.Text(c["name"], size=14, weight=ft.FontWeight.BOLD, color=Theme.TEXT_PRIMARY),
                            ft.Container(height=2),
                            ft.ProgressBar(value=hp_pct/100, width=220, color=hp_color, bgcolor=Theme.SURFACE_HIGH, border_radius=4),
                            ft.Container(height=2),
                            ft.Text(f"HP: {c['hp']}/{c['max_hp']}  ·  AC: {c['ac']}", size=11, color=Theme.TEXT_SECONDARY),
                        ], tight=True, expand=True),
                        ft.Row([
                            ft.IconButton(ft.Icons.REMOVE_CIRCLE_OUTLINE, icon_size=18, icon_color=Theme.TEXT_MUTED,
                                          on_click=lambda e, idx=i: damage_init(idx, -1), tooltip="Damage 1"),
                            ft.IconButton(ft.Icons.ADD_CIRCLE_OUTLINE, icon_size=18, icon_color=Theme.TEXT_MUTED,
                                          on_click=lambda e, idx=i: damage_init(idx, 1), tooltip="Heal 1"),
                            ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_size=18, icon_color=Theme.DANGER,
                                          on_click=lambda e, idx=i: remove_init(idx), tooltip="Remove"),
                        ], spacing=0),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    hover=False,
                )
            )

    def build_initiative_page():
        return ft.Column([
            page_header("Initiative Tracker", "Manage combat turns, HP, and conditions at a glance.", ft.Icons.SWAP_VERT),
            card(
                ft.Column([
                    ft.Text("Add Combatant", size=14, weight=ft.FontWeight.BOLD, color=Theme.TEXT_PRIMARY),
                    ft.Container(height=8),
                    ft.Row([init_name, init_init, init_hp, init_ac], wrap=True, spacing=8),
                    ft.Container(height=8),
                    primary_button("Add", add_init, ft.Icons.ADD),
                ], tight=True),
            ),
            section_title(f"Combat Order ({len(initiative_list)})", ft.Icons.LIST),
            init_view,
        ], scroll=ft.ScrollMode.AUTO, expand=True)

    # ─── Encounter Page ────────────────────────────────────
    monster_search = ft.TextField(
        label="Search monsters...",
        on_change=lambda e: filter_monsters(e.control.value.lower()),
        bgcolor=Theme.SURFACE,
        border_color=Theme.BORDER,
        focused_border_color=Theme.PRIMARY,
    )
    monster_select = ft.Dropdown(
        label="Monster",
        width=260,
        options=[ft.dropdown.Option(m["name"]) for m in MONSTERS[:30]],
        bgcolor=Theme.SURFACE,
        border_color=Theme.BORDER,
    )
    monster_list_view = ft.ListView(height=280, spacing=6)
    encounter_summary = ft.Container()

    def update_encounter():
        total_xp = sum(cr_xp(m.get("cr","0")) for m in encounter_monsters)
        mult = encounter_multiplier(len(encounter_monsters))
        adjusted_xp = int(total_xp * mult) if mult > 0 else 0
        diff = difficulty_label(adjusted_xp, party_levels)
        diff_col = difficulty_color(diff)

        encounter_summary.content = card(
            ft.Column([
                ft.Text("Encounter Summary", size=16, weight=ft.FontWeight.BOLD, color=Theme.TEXT_PRIMARY),
                ft.Container(height=12),
                ft.Row([
                    stat_block("Monsters", len(encounter_monsters)),
                    stat_block("Total XP", total_xp),
                    stat_block("Adjusted XP", adjusted_xp, Theme.ACCENT),
                    stat_block("Difficulty", diff, diff_col),
                ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
            ], tight=True),
            bgcolor=Theme.SURFACE_HIGH,
        )

        monster_list_view.controls = []
        for i, m in enumerate(encounter_monsters):
            monster_list_view.controls.append(
                list_item_card(
                    ft.Row([
                        ft.Column([
                            ft.Text(m["name"], size=13, weight=ft.FontWeight.BOLD, color=Theme.TEXT_PRIMARY),
                            ft.Text(f"CR {format_cr(m.get('cr','?'))} · {cr_xp(m.get('cr',0))} XP", size=11, color=Theme.TEXT_SECONDARY),
                        ], tight=True, expand=True),
                        ft.IconButton(
                            ft.Icons.REMOVE_CIRCLE_OUTLINE,
                            icon_size=18,
                            icon_color=Theme.DANGER,
                            on_click=lambda e, idx=i: remove_monster(idx),
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                )
            )
        page.update()

    def add_monster(e):
        name = monster_select.value
        if not name:
            return
        monster = next((m for m in MONSTERS if m["name"] == name), None)
        if monster:
            encounter_monsters.append(dict(monster))
            update_encounter()

    def remove_monster(idx):
        del encounter_monsters[idx]
        update_encounter()

    def update_party_size(e):
        nonlocal party_levels
        val = e.control.value if e.control.value else e.data
        n = int(val)
        party_levels = [5] * n
        update_encounter()

    def update_party_level(level):
        nonlocal party_levels
        party_levels = [level] * len(party_levels)
        update_encounter()

    def filter_monsters(query):
        filtered = [m for m in MONSTERS if query in m["name"].lower()][:30]
        monster_select.options = [ft.dropdown.Option(m["name"]) for m in filtered]
        page.update()

    update_encounter()

    def build_encounter_page():
        return ft.Column([
            page_header("Encounter Builder", "Build balanced encounters and calculate XP difficulty.", ft.Icons.SHIELD_OUTLINED),
            encounter_summary,
            ft.Container(height=12),
            card(
                ft.Column([
                    ft.Text("Party Setup", size=14, weight=ft.FontWeight.BOLD, color=Theme.TEXT_PRIMARY),
                    ft.Container(height=8),
                    ft.Row([
                        ft.Text("Party Size:", size=13, color=Theme.TEXT_SECONDARY),
                        ft.Dropdown(
                            value="4",
                            options=[ft.dropdown.Option(str(i)) for i in range(1,9)],
                            width=80,
                            on_select=update_party_size,
                            bgcolor=Theme.SURFACE,
                            border_color=Theme.BORDER,
                        ),
                        ft.Container(width=16),
                        ft.Text("Party Level:", size=13, color=Theme.TEXT_SECONDARY),
                        ft.Dropdown(
                            value="5",
                            options=[ft.dropdown.Option(str(i)) for i in range(1,21)],
                            width=80,
                            on_select=lambda e: update_party_level(int(e.control.value)),
                            bgcolor=Theme.SURFACE,
                            border_color=Theme.BORDER,
                        ),
                    ], wrap=True),
                ], tight=True),
            ),
            ft.Container(height=12),
            card(
                ft.Column([
                    ft.Text("Add Monsters", size=14, weight=ft.FontWeight.BOLD, color=Theme.TEXT_PRIMARY),
                    ft.Container(height=8),
                    monster_search,
                    ft.Container(height=4),
                    monster_select,
                    ft.Container(height=8),
                    primary_button("Add to Encounter", add_monster, ft.Icons.ADD),
                ], tight=True),
            ),
            section_title(f"Monsters ({len(encounter_monsters)})", ft.Icons.LIST),
            monster_list_view,
        ], scroll=ft.ScrollMode.AUTO, expand=True)

    # ─── Loot Page ─────────────────────────────────────────
    loot_result = ft.Container(
        ft.Column([
            ft.Text("💰", size=32),
            ft.Container(height=8),
            ft.Text("Generate some loot!", size=16, weight=ft.FontWeight.BOLD, color=Theme.TEXT_MUTED),
            ft.Container(height=4),
            ft.Text("Select a CR tier and roll for treasure.", size=12, color=Theme.TEXT_MUTED),
        ], tight=True, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        expand=True,
    )

    def generate_loot_click(e):
        tier = loot_tier.value
        loot = generate_loot(tier)

        coin_rows = [
            ft.Row([
                ft.Container(
                    ft.Column([
                        ft.Text(k.upper(), size=10, color=Theme.TEXT_MUTED, weight=ft.FontWeight.BOLD),
                        ft.Text(str(v), size=16, weight=ft.FontWeight.BOLD, color=Theme.ACCENT_LIGHT),
                    ], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    expand=True,
                    padding=10,
                    bgcolor=Theme.SURFACE_HIGH,
                    border_radius=Theme.RADIUS_SM,
                    alignment=ft.alignment.Alignment.CENTER,
                ) for k, v in loot["coins"].items()
            ], spacing=6),
        ]

        items_widget = ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.STAR_BORDER, size=16, color=Theme.ACCENT),
                ft.Text("Treasure Items", size=13, weight=ft.FontWeight.BOLD, color=Theme.TEXT_PRIMARY),
            ], spacing=8),
            ft.Container(height=6),
        ] + [
            ft.Container(
                ft.Row([
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, size=14, color=Theme.PRIMARY_LIGHT),
                    ft.Text(item, size=12, color=Theme.TEXT_PRIMARY),
                ], spacing=6),
                padding=ft.Padding.symmetric(vertical=6, horizontal=8),
                bgcolor=Theme.SURFACE_HIGH,
                border_radius=Theme.RADIUS_SM,
            ) for item in loot["items"]
        ] if loot["items"] else [
            ft.Text("No magic items this time.", size=12, color=Theme.TEXT_MUTED, italic=True),
        ], tight=True, spacing=4)

        loot_result.content = ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.STAR, size=28, color=Theme.ACCENT),
                ft.Column([
                    ft.Text(f"CR Tier {tier} Loot", size=18, weight=ft.FontWeight.BOLD, color=Theme.ACCENT_LIGHT),
                    ft.Text("Generated treasure hoard", size=11, color=Theme.TEXT_SECONDARY),
                ], tight=True),
            ], spacing=12),
            ft.Divider(color=Theme.BORDER, height=20),
            ft.Text("COINS", size=10, color=Theme.TEXT_MUTED, weight=ft.FontWeight.BOLD),
            ft.Container(height=6),
        ] + coin_rows + [
            ft.Container(height=12),
            items_widget,
        ], tight=True, scroll=ft.ScrollMode.AUTO)
        page.update()

    loot_tier = ft.Dropdown(
        label="CR Tier",
        value="1",
        options=[
            ft.dropdown.Option("1", "CR 1–4 (Low)"),
            ft.dropdown.Option("2", "CR 5–10 (Medium)"),
            ft.dropdown.Option("3", "CR 11–16 (High)"),
            ft.dropdown.Option("4", "CR 17+ (Epic)"),
        ],
        width=220,
        bgcolor=Theme.SURFACE,
        border_color=Theme.BORDER,
    )

    def build_loot_page():
        return ft.Column([
            page_header("Loot Generator", "Generate random treasure hoards based on CR tier.", ft.Icons.STAR),
            card(
                ft.Column([
                    loot_tier,
                    ft.Container(height=8),
                    primary_button("Generate Loot!", generate_loot_click, ft.Icons.CASINO),
                ], tight=True),
            ),
            ft.Container(height=12),
            card(loot_result, expand=True),
        ], scroll=ft.ScrollMode.AUTO, expand=True)

    # ─── NPC Names Page ────────────────────────────────────
    name_result = ft.Container(
        ft.Column([
            ft.Text("🎭", size=32),
            ft.Container(height=8),
            ft.Text("Generate an NPC", size=16, weight=ft.FontWeight.BOLD, color=Theme.TEXT_MUTED),
            ft.Container(height=4),
            ft.Text("Select a race and gender to get started.", size=12, color=Theme.TEXT_MUTED),
        ], tight=True, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        expand=True,
    )
    name_history_list = ft.ListView(height=200, spacing=4)

    def generate_name_click(e):
        race = name_race.value
        gender = name_gender.value
        name = generate_name(race, gender)
        trait = random.choice(TRAITS)

        name_history.insert(0, f"{name} — {trait}")
        if len(name_history) > 10:
            name_history.pop()

        name_history_list.controls = [
            ft.Container(
                ft.Text(n, size=12, color=Theme.TEXT_SECONDARY),
                padding=8,
                bgcolor=Theme.SURFACE,
                border_radius=Theme.RADIUS_SM,
                border=ft.Border.all(1, Theme.BORDER),
            ) for n in name_history
        ]

        name_result.content = ft.Column([
            ft.Text(name, size=30, weight=ft.FontWeight.BOLD, color=Theme.ACCENT_LIGHT),
            ft.Text(f"{race} · {gender.title()}", size=12, color=Theme.TEXT_SECONDARY),
            ft.Container(height=16),
            ft.Container(
                ft.Column([
                    ft.Text("PERSONALITY TRAIT", size=10, color=Theme.TEXT_MUTED, weight=ft.FontWeight.BOLD),
                    ft.Container(height=6),
                    ft.Text(f'"{trait}"', size=14, italic=True, color=Theme.TEXT_PRIMARY),
                ], tight=True),
                padding=16,
                bgcolor=Theme.SURFACE_HIGH,
                border_radius=Theme.RADIUS_MD,
            ),
        ], tight=True, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        page.update()

    name_race = ft.Dropdown(
        label="Race",
        value="Human",
        options=[ft.dropdown.Option(r) for r in [
            "Human", "Elf", "Dwarf", "Halfling", "Dragonborn",
            "Gnome", "Half-Orc", "Tiefling", "Half-Elf",
        ]],
        width=160,
        bgcolor=Theme.SURFACE,
        border_color=Theme.BORDER,
    )

    name_gender = ft.Dropdown(
        label="Gender",
        value="any",
        options=[
            ft.dropdown.Option("any", "Any"),
            ft.dropdown.Option("male", "Male"),
            ft.dropdown.Option("female", "Female"),
        ],
        width=130,
        bgcolor=Theme.SURFACE,
        border_color=Theme.BORDER,
    )

    def build_names_page():
        return ft.Column([
            page_header("NPC Name Generator", "Generate random NPC names with personality traits.", ft.Icons.PERSON_ADD),
            card(
                ft.Column([
                    ft.Row([
                        name_race,
                        name_gender,
                    ], wrap=True, spacing=8),
                    ft.Container(height=8),
                    primary_button("Generate!", generate_name_click, ft.Icons.REFRESH),
                ], tight=True),
            ),
            ft.Container(height=12),
            card(name_result, expand=True),
            section_title("Recent NPCs", ft.Icons.HISTORY),
            name_history_list,
        ], scroll=ft.ScrollMode.AUTO, expand=True)

    # ─── Page routing ──────────────────────────────────────
    page_builders = {
        "dice": build_dice_page,
        "characters": build_characters_page,
        "spells": build_spells_page,
        "initiative": build_initiative_page,
        "encounter": build_encounter_page,
        "loot": build_loot_page,
        "names": build_names_page,
    }

    def build_page(page_id):
        return page_builders.get(page_id, build_dice_page)()

    content = ft.Container(
        build_dice_page(),
        padding=24,
        expand=True,
    )

    # Main layout — sidebar has fixed width, content expands
    page.add(
        ft.Row(
            [
                ft.Container(sidebar, width=180, bgcolor=Theme.SURFACE),
                ft.VerticalDivider(width=1, color=Theme.BORDER),
                content,
            ],
            expand=True,
            spacing=0,
        )
    )


if __name__ == "__main__":
    ft.run(main)
