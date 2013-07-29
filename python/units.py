from collections import defaultdict


class Unit(object):
    def __init__(self):
        self.variables = defaultdict(int)

    name = ""
    zoc = []
    abilities = []
    xp_to_upgrade = 4
    upgrades = []
    attack_bonuses = {}
    defence_bonuses = {}

    def __repr__(self):
        return self.name

    def has(self, attribute):
        return hasattr(self, attribute)

    # Frozen
    def freeze(self, n):
        self.variables["frozen"] = max(self.variables["frozen"], n)

    def is_frozen(self):
        return self.variables["frozen"]

    def get_frozen_counters(self):
        return self.variables["frozen"]

    def decrement_frozen(self):
        self.variables["frozen"] = max(self.variables["frozen"] - 1, 0)

    # xp gained this turn
    def set_xp_gained_this_turn(self):
        self.variables["xp_gained_this_turn"] = True

    def get_xp_gained_this_turn(self):
        return self.variables["xp_gained_this_turn"]

    def remove_xp_gained_this_turn(self):
        self.variables["xp_gained_this_turn"] = False

    # Xp
    def increment_xp(self):
        self.variables["xp"] += 1

    def get_xp(self):
        return self.variables["xp"]

    # Used
    def set_used(self):
        self.variables["used"] = 1

    def is_used(self):
        return self.variables["used"]

    def remove_used(self):
        self.variables["used"] = 0

    # Attack frozen
    def set_attack_frozen(self, n):
        self.variables["attack_frozen"] = n

    def is_attack_frozen(self):
        return self.variables["attack_frozen"]

    def get_attack_frozen_counters(self):
        return self.variables["attack_frozen"]

    def decrement_attack_frozen(self):
        self.variables["attack_frozen"] = max(self.variables["attack_frozen"] - 1, 0)

    # Improved weapons
    def improve_weapons(self):
        self.variables["improved_weapons"] = 1

    def has_improved_weapons(self):
        return self.variables["improved_weapons"]

    def remove_improved_weapons(self):
        self.variables["improved_weapons"] = 0

    # Improved weapons_II_A
    def improve_weapons_II_A(self):
        self.variables["improved_weapons_II_A"] = 2

    def has_improved_weapons_II_A(self):
        return self.variables["improved_weapons_II_A"]

    def decrease_improved_weapons_II_A(self):
        self.variables["improved_weapons_II_A"] = max(0, self.variables["improved_weapons"] - 1)

    # Improved weapons_II_B
    def improve_weapons_II_B(self):
        self.variables["improved_weapons_II_B"] = 1
        self.zoc = {"Cavalry"}

    def has_improved_weapons_II_B(self):
        return self.variables["improved_weapons_II_B"]

    def remove_improved_weapons_II_B(self):
        self.variables["improved_weapons_II_B"] = 0
        self.zoc = {}

    # Sabotage
    def sabotage(self):
        self.variables["sabotaged"] = 1

    def is_sabotaged(self):
        return self.variables["sabotaged"]

    def remove_sabotaged(self):
        self.variables["sabotaged"] = 0

    # Sabotage_II
    def sabotage_II(self):
        self.variables["sabotaged_II"] = 1

    def is_sabotaged_II(self):
        return self.variables["sabotaged_II"]

    def remove_sabotaged_II(self):
        self.variables["sabotaged_II"] = 0

    # Bribe
    def set_bribed(self):
        self.variables["bribed"] = 1

    def get_bribed(self):
        return self.variables["bribed"]

    def remove_bribed(self):
        self.variables["is_bribed"] = 0

    def set_recently_bribed(self):
        self.variables["recently_bribed"] = 1

    def is_recently_bribed(self):
        return self.variables["recently_bribed"]

    def remove_recently_bribed(self):
        self.variables["recently_bribed"] = 0

    # Extra life
    def has_extra_life(self):
        return self.name == "Viking" and not self.variables["lost_extra_life"]

    def remove_extra_life(self):
        self.variables["lost_extra_life"] = 1

    #Zoc
    def get_zoc(self):
        if self.has_improved_weapons_II_B():
            return self.zoc + ["Cavalry"]
        else:
            return self.zoc

    #Movement remaining
    def set_movement_remaining(self, n):
        self.variables["movement_remaining"] = n

    def get_movement_remaining(self):
        return self.variables["movement_remaining"]

    #Extra_action
    def set_extra_action(self):
        self.variables["extra_action"] = 1

    def has_extra_action(self):
        return self.variables["extra_action"]

    def remove_extra_action(self):
        self.variables["extra_action"] = 0


class Archer(Unit):

    name = "Archer"
    image = "Archer"
    attack = 2
    defence = 2
    movement = 1
    range = 4
    attack_bonuses = {"Infantry": 1}
    defence_bonuses = {}
    type = "Infantry"
    upgrades = ["Longbowman", "Crossbow Archer"]


class Longbowman(Unit):
    name = "Longbowman"
    image = "Archer"
    attack = 2
    defence = 2
    movement = 1
    range = 4
    type = "Infantry"
    upgrades = ["Longbowman II_A", "Longbowman II_B"]

    sharpshooter = True

    descriptions = {"sharpshooter": "Targets have their defence reduced to 1 during the attack"}


class Longbowman_II_A(Unit):
    name = "Longbowman II_A"
    image = "Archer"
    attack = 3
    defence = 2
    movement = 1
    range = 4
    attack_bonuses = {"Infantry": 1}
    defence_bonuses = {}
    type = "Infantry"

    sharpshooter = True

    descriptions = {"sharpshooter": "Targets have their defence reduced to 1 during the attack"}


class Longbowman_II_B(Unit):
    name = "Longbowman II_B"
    image = "Archer"
    attack = 2
    defence = 3
    movement = 1
    range = 4
    attack_bonuses = {"Infantry": 1}
    defence_bonuses = {}
    type = "Infantry"

    sharpshooter = True

    descriptions = {"sharpshooter": "Targets have their defence reduced to 1 during the attack"}


class Crossbow_Archer(Unit):
    name = "Crossbow Archer"
    image = "Archer"
    attack = 2
    defence = 3
    movement = 1
    range = 4
    attack_bonuses = {"Infantry": 1}
    defence_bonuses = {}
    type = "Infantry"
    upgrades = ["Crossbow Archer II_A", "Crossbow Archer II_B"]


class Crossbow_Archer_II_A(Unit):
    name = "Crossbow Archer II_A"
    image = "Archer"
    attack = 3
    defence = 3
    movement = 1
    range = 4
    attack_bonuses = {"Infantry": 1}
    defence_bonuses = {}
    type = "Infantry"


class Crossbow_Archer_II_B(Unit):
    name = "Crossbow Archer II_B"
    image = "Archer"
    attack = 2
    defence = 4
    movement = 1
    range = 4
    attack_bonuses = {"Infantry": 1}
    defence_bonuses = {}
    type = "Infantry"


class Pikeman(Unit):

    name = "Pikeman"
    image = "Pikeman"
    attack = 2
    defence = 2
    movement = 1
    range = 1
    attack_bonuses = {"Cavalry": 1}
    defence_bonuses = {"Cavalry": 1}
    type = "Infantry"   
    zoc = ["Cavalry"]
    upgrades = ["Halberdier", "Royal Guard"]
    xp_to_upgrade = 3


class Halberdier(Unit):
    name = "Halberdier"
    image = "Pikeman"
    attack = 4
    defence = 3
    movement = 1
    range = 1
    type = "Infantry"

    push = True

    descriptions = {"push": "If attack and defence rolls both succeed, it can still move forward. If not on back line, "
                            "opponents units must retreat directly backwards or die."}


class Halberdier_II_A(Unit):
    name = "Halberdier"
    image = "Pikeman"
    attack = 5
    defence = 3
    movement = 1
    range = 1
    type = "Infantry"

    push = True

    descriptions = {"push": "If attack and defence rolls both succeed, it can still move forward. If not on back line, "
                            "opponents units must retreat directly backwards or die."}


class Halberdier_II_B(Unit):
    name = "Halberdier"
    image = "Pikeman"
    attack = 4
    defence = 4
    movement = 1
    range = 1
    type = "Infantry"

    push = True

    descriptions = {"push": "If attack and defence rolls both succeed, it can still move forward. If not on back line, "
                            "opponents units must retreat directly backwards or die."}


class Light_Cavalry(Unit):

    name = "Light Cavalry"
    image = "Light Cavalry"
    attack = 2
    defence = 2
    movement = 4
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Cavalry"

    upgrades = ["Dragoon", "Cavalry Lieutenant"]
    xp_to_upgrade = 3


class Dragoon(Unit):

    name = "Dragoon"
    image = "Light Cavalry"
    attack = 2
    defence = 2
    movement = 4
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Cavalry"
    upgrades = ["Dragoon II_A", "Dragoon II_B"]

    swiftness = True

    descriptions = {"swiftness": "Can use remaining moves after attacking."}


class Dragoon_II_A(Unit):

    name = "Dragoon"
    image = "Light Cavalry"
    attack = 3
    defence = 2
    movement = 4
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Cavalry"
    upgrades = ["Dragoon II_A", "Dragoon II_B"]

    swiftness = True

    descriptions = {"swiftness": "Can use remaining moves after attacking."}


class Dragoon_II_B(Unit):

    name = "Dragoon"
    image = "Light Cavalry"
    attack = 2
    defence = 3
    movement = 4
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Cavalry"
    upgrades = ["Dragoon II_A", "Dragoon II_B"]

    swiftness = True

    descriptions = {"swiftness": "Can use remaining moves after attacking."}


class Cavalry_Lieutenant(Unit):

    name = "Cavalry Lieutenant"
    image = "Light Cavalry"
    attack = 3
    defence = 2
    movement = 3
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Cavalry"
    upgrades = ["Cavalry_Luitenant_II_A", "Cavalry_Luitenant_II_B"]

    cavalry_charging = True

    descriptions = {"cavalry_charging": "All cavalry units starting their turn in the 8 surrounding tiles have +1 "
                                        "Movement"}


class Cavalry_Lieutenant_II_A(Unit):

    name = "Cavalry Lieutenant II_A"
    image = "Light Cavalry"
    attack = 3
    defence = 3
    movement = 4
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Cavalry"

    cavalry_charging = True

    descriptions = {"cavalry_charging": "All cavalry units starting their turn in the 8 surrounding tiles have +1 "
                                        "Movement"}


class Cavalry_Lieutenant_II_B(Unit):

    name = "Cavalry Lieutenant II_B"
    image = "Light Cavalry"
    attack = 4
    defence = 3
    movement = 3
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Cavalry"

    cavalry_charging = True

    descriptions = {"cavalry_charging": "All cavalry units starting their turn in the 8 surrounding tiles have +1 "
                                        "Movement"}


class Knight(Unit):

    name = "Knight"
    image = "Knight"
    attack = 3
    defence = 3
    movement = 2
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Cavalry"
    upgrades = ["Lancer", "Hobelar"]


class Ballista(Unit):
 
    name = "Ballista"
    image = "Ballista"
    attack = 4
    defence = 1
    movement = 1
    range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Siege Weapon"
    upgrades = ["Cannon", "Trebuchet"]


class Trebuchet(Unit):

    name = "Trebuchet"
    image = "Ballista"
    attack = 5
    defence = 1
    movement = 1
    range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Siege Weapon"
    upgrades = ["Trebuchet II_A", "Trebuchet II_A"]


class Trebuchet_II_A(Unit):

    name = "Trebuchet II_A"
    image = "Ballista"
    attack = 6
    defence = 1
    movement = 1
    range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Siege Weapon"


class Trebuchet_II_B(Unit):

    name = "Trebuchet II_B"
    image = "Ballista"
    attack = 5
    defence = 2
    movement = 1
    range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Siege Weapon"


class Catapult(Unit):

    name = "Catapult"
    image = "Catapult"
    attack = 6
    defence = 2
    movement = 1
    range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Siege Weapon"
        
    double_attack_cost = True
    xp_to_upgrade = 2

    descriptions = {"double_attack_cost": "Attack takes two actions."}


class Catapult_II_A(Unit):

    name = "Catapult II_A"
    image = "Catapult"
    attack = 7
    defence = 2
    movement = 1
    range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Siege Weapon"

    double_attack_cost = True
    xp_to_upgrade = 3

    descriptions = {"double_attack_cost": "Attack takes two actions."}

    upgrades = ["Catapult III_A", "Catapult III_B"]


class Catapult_II_B(Unit):

    name = "Catapult II_B"
    image = "Catapult"
    attack = 6
    defence = 2
    movement = 1
    range = 4
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Siege Weapon"

    double_attack_cost = True
    xp_to_upgrade = 3

    descriptions = {"double_attack_cost": "Attack takes two actions."}

    upgrades = ["Catapult III_B", "Catapult IIIC"]


class Catapult_III_A(Unit):

    name = "Catapult III_A"
    image = "Catapult"
    attack = 8
    defence = 2
    movement = 1
    range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Siege Weapon"

    double_attack_cost = True

    descriptions = {"double_attack_cost": "Attack takes two actions."}


class Catapult_III_B(Unit):

    name = "Catapult III_B"
    image = "Catapult"
    attack = 7
    defence = 2
    movement = 1
    range = 4
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Siege Weapon"

    double_attack_cost = True

    descriptions = {"double_attack_cost": "Attack takes two actions."}


class Catapult_III_C(Unit):

    name = "Catapult III_C"
    image = "Catapult"
    attack = 6
    defence = 2
    movement = 1
    range = 5
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Siege Weapon"

    double_attack_cost = True

    descriptions = {"double_attack_cost": "Attack takes two actions."}


class Royal_Guard(Unit):
  
    name = "Royal Guard"
    image = "Royal Guard"
    attack = 3
    defence = 3
    movement = 1
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Infantry"
    
    zoc = ["Cavalry", "Infantry", "Siege Weapon", "Specialist"]
    defence_maneuverability = True
    xp_to_upgrade = 3

    descriptions = {"defence_maneuverability": "Can move two tiles if one of them is sideways."}

    upgrades = ["Royal Guard II_A", "Royal Guard II_B"]


class Royal_Guard_II_A(Unit):

    name = "Royal Guard II_A"
    image = "Royal Guard"
    attack = 3
    defence = 3
    movement = 1
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Infantry"

    zoc = ["Cavalry", "Infantry", "Siege Weapon", "Specialist"]
    defence_maneuverability = True
    melee_expert = True

    descriptions = {"defence_maneuverability": "Can move two tiles if one of them is sideways.", "melee_expert":
                    "+1A, +1D vs melee units."}


class Royal_Guard_II_B(Unit):

    name = "Royal Guard II_B"
    image = "Royal Guard"
    attack = 3
    defence = 3
    movement = 1
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Infantry"

    zoc = ["Cavalry", "Infantry", "Siege Weapon", "Specialist"]
    defence_maneuverability = True
    tall_shield = True
    melee_freeze = True

    descriptions = {"defence_maneuverability": "Can move two tiles if one of them is sideways.", "tall_shield":
                    "+1D against ranged attacks", "melee_freeze": "Units adjacent to it can only attack it, not move."}


class Scout(Unit):
    
    name = "Scout"
    image = "Scout"
    attack = False
    defence = 2
    movement = 4
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = "Cavalry"
        
    scouting = True
    xp_to_upgrade = 2

    descriptions = {"scouting": "Can move past all units."}

    upgrades = ["Scout II_A", "Scout II_B"]


class Scout_II_A(Unit):

    name = "Scout II_A"
    image = "Scout"
    attack = 2
    defence = 3
    movement = 4
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = "Cavalry"

    scouting = True

    descriptions = {"scouting": "Can move past all units."}


class Scout_II_B(Unit):

    name = "Scout II_B"
    image = "Scout"
    attack = False
    defence = 2
    movement = 5
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = "Cavalry"

    scouting = True
    tall_shield = "True"

    descriptions = {"scouting": "Can move past all units.", "tall_shield": "+1D against ranged attacks"}


class Viking(Unit):

    name = "Viking"
    image = "Viking"
    attack = 3
    defence = 2
    movement = 1
    range = 1
    attack_bonuses = {}
    defence_bonuses = {"Siege Weapon": 1}
    zoc = []
    type = "Infantry"

    rage = True

    descriptions = {"rage": "Can make an attack after it's move. (But not a second move.)",
                    "extra_life": "It takes two successful hits to kill Viking"}

    upgrades = ["Viking II_A", "Viking II_B"]


class Viking_II_A(Unit):

    name = "Viking"
    image = "Viking"
    attack = 3
    defence = 2
    movement = 1
    range = 1
    attack_bonuses = {}
    defence_bonuses = {"Siege Weapon": 1}
    zoc = []
    type = "Infantry"

    rage_II = True

    descriptions = {"rage": "Can move up to two tiles to make an attack. (But cannot take over the attacked tile if "
                            "it's 3 tiles away.)",
                    "extra_life": "It takes two successful hits to kill Viking"}

    upgrades = ["Viking II_A", "Viking II_B"]


class Viking_II_B(Unit):

    name = "Viking"
    image = "Viking"
    attack = 3
    defence = 2
    movement = 1
    range = 1
    attack_bonuses = {"Siege Weapons": 1}
    defence_bonuses = {"Siege Weapons": 2}
    zoc = []
    type = "Infantry"

    rage = True

    descriptions = {"rage": "Can make an attack after it's move. (But not a second move.)",
                    "extra_life": "It takes two successful hits to kill Viking"}

    upgrades = ["Viking II_A", "Viking II_B"]


class Cannon(Unit):
    
    name = "Cannon"
    image = "Cannon"
    attack = 5
    defence = 1
    movement = 1
    range = 4
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = "Siege Weapon"
        
    attack_cooldown = 3
    xp_to_upgrade = 3

    descriptions = {"attack_cooldown": "Can only attack every third turn."}

    upgrades = ["Cannon II_A", "Cannon II_B"]


class Cannon_II_A(Unit):

    name = "Cannon II_A"
    image = "Cannon"
    attack = 5
    defence = 1
    movement = 1
    range = 4
    attack_bonuses = {"Siege_weapons": 2}
    defence_bonuses = {}
    zoc = []
    type = "Siege Weapon"

    attack_cooldown = 3

    descriptions = {"attack_cooldown": "Can only attack every third turn."}


class Cannon_II_B(Unit):

    name = "Cannon II_B"
    image = "Cannon"
    attack = 5
    defence = 1
    movement = 1
    range = 4
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = "Siege Weapon"

    attack_cooldown = 2
    far_sighted = True

    descriptions = {"attack_cooldown": "Can only attack every third turn.",
                    "far_sighted": "-1A if target is less than 4 tiles away."}


class Lancer(Unit):
    
    name = "Lancer"
    image = "Lancer"
    attack = 2
    defence = 3
    movement = 3
    range = 1
    attack_bonuses = {"Cavalry": 1}
    defence_bonuses = {}
    zoc = []
    type = "Cavalry"
        
    lancing = True

    descriptions = {"lancing": "If it starts movement with 2 empty tiles between lancer and the unit it attacks, +2A."}

    upgrades = ["Lancer II_A", "Lancer II_B"]


class Lancer_II_A(Unit):

    name = "Lancer II_A"
    image = "Lancer"
    attack = 2
    defence = 3
    movement = 3
    range = 1
    attack_bonuses = {"Cavalry": 2}
    defence_bonuses = {"Cavalry": 1}
    zoc = []
    type = "Cavalry"

    lancing = True

    descriptions = {"lancing": "If it starts movement with 2 empty tiles between lancer and the unit it attacks, +2A."}


class Lancer_II_B(Unit):

    name = "Lancer II_B"
    image = "Lancer"
    attack = 2
    defence = 3
    movement = 4
    range = 1
    attack_bonuses = {"Cavalry": 1}
    defence_bonuses = {}
    zoc = []
    type = "Cavalry"

    lancing_II = True

    descriptions = {"lancing_II": "If it starts movement with 3 empty tiles between lancer and the unit it attacks, +3A."}


class Flag_Bearer(Unit):
   
    name = "Flag Bearer"
    image = "Flag Bearer"
    attack = 2
    defence = 3
    movement = 3
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = "Cavalry"
        
    flag_bearing = True

    descriptions = {"flag_bearing": "Friendly melee units receive +2A while adjacent to Flag Bearer."}

    upgrades = ["Flag Bearer II_A", "Flag Bearer II_B"]


class Flag_Bearer_II_A(Unit):

    name = "Flag Bearer II_A"
    image = "Flag Bearer"
    attack = 2
    defence = 3
    movement = 3
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = "Cavalry"

    flag_bearing_II_A = True

    descriptions = {"flag_bearing_II_A": "Friendly melee units receive +2A while surrounding Flag Bearer."}


class Flag_Bearer_II_B(Unit):

    name = "Flag Bearer II_B"
    image = "Flag Bearer"
    attack = 2
    defence = 3
    movement = 3
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = "Cavalry"

    flag_bearing_II_B = True

    descriptions = {"flag_bearing_II_B": "Friendly melee units receive +3A while adjacent to Flag Bearer."}


class Longswordsman(Unit):

    name = "Longswordsman"
    image = "Longswordsman"
    attack = 3
    defence = 3
    movement = 1
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = "Infantry"
        
    longsword = True

    descriptions = {"longsword": "Also hits the 4 nearby tiles in the attack direction."}

    upgrades = ["Longswordsman II_A", "Longswordsman II_B"]


class Longswordsman_II_A(Unit):

    name = "Longswordsman II_A"
    image = "Longswordsman"
    attack = 3
    defence = 3
    movement = 1
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = "Infantry"

    longsword = True

    descriptions = {"longsword": "Also hits the 4 nearby tiles in the attack direction."}


class Longswordsman_II_B(Unit):

    name = "Longswordsman II_B"
    image = "Longswordsman"
    attack = 3
    defence = 3
    movement = 1
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = "Infantry"

    longsword = True

    descriptions = {"longsword": "Also hits the 4 nearby tiles in the attack direction."}


class Crusader(Unit):

    name = "Crusader"
    image = "Crusader"
    attack = 3
    defence = 3
    movement = 3
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = "Cavalry"
        
    crusading = True

    descriptions = {"crusading": "Friendly melee units starting their movement in one of the 8 tiles surrounding "
                                 "Crusader get +1A."}

    upgrades = ["Crusader II_A", "Crusader II_B"]


class Crusader_II_A(Unit):

    name = "Crusader II_A"
    image = "Crusader"
    attack = 4
    defence = 3
    movement = 3
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = "Cavalry"

    crusading = True

    descriptions = {"crusading": "Friendly melee units starting their movement in one of the 8 tiles surrounding "
                                 "Crusader get +1A."}


class Crusader_II_B(Unit):

    name = "Crusader II_B"
    image = "Crusader"
    attack = 3
    defence = 3
    movement = 3
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = "Cavalry"

    crusading_II = True

    descriptions = {"crusading_II": "Friendly melee units starting their movement in one of the 8 tiles surrounding "
                                 "Crusader get +1A, +1D."}


class Berserker(Unit):

    name = "Berserker"
    image = "Berserker"
    attack = 5
    defence = 1
    movement = 1
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = "Infantry"
        
    berserking = True

    descriptions = {"berserking": "Can move 4 tiles if movement ends with an attack."}

    upgrades = ["Berserker II_A", "Berserker II_B"]


class Berserker_II_A(Unit):

    name = "Berserker II_A"
    image = "Berserker"
    attack = 5
    defence = 1
    movement = 1
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = "Infantry"

    berserking = True
    big_shield = True

    descriptions = {"berserking": "Can move 4 tiles if movement ends with an attack.",
                    "big_shield": "+2D v melee"}


class Berserker_II_B(Unit):

    name = "Berserker II_B"
    image = "Berserker"
    attack = 7
    defence = 1
    movement = 1
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = "Infantry"

    berserking = True

    descriptions = {"berserking": "Can move 4 tiles if movement ends with an attack."}


class Hobelar(Unit):

    name = "Hobelar"
    image = "Hobelar"
    attack = 3
    defence = 3
    movement = 3
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = "Cavalry"

    swiftness = True

    descriptions = {"swiftness": "Can use remaining moves after attacking."}

    upgrades = ["Hobelar II_A", "Hobelar II_B"]


class Hobelar_II_A(Unit):

    name = "Hobelar II_A"
    image = "Hobelar"
    attack = 3
    defence = 3
    movement = 4
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = "Cavalry"

    swiftness = True

    descriptions = {"swiftness": "Can use remaining moves after attacking."}


class Hobelar_II_B(Unit):

    name = "Hobelar II_B"
    image = "Hobelar"
    attack = 3
    defence = 3
    movement = 3
    range = 1
    attack_bonuses = {"Infantry": 2}
    defence_bonuses = {}
    zoc = []
    type = "Cavalry"

    swiftness = True

    descriptions = {"swiftness": "Can use remaining moves after attacking."}


class War_Elephant(Unit):

    name = "War Elephant"
    image = "War Elephant"
    attack = 3
    defence = 3
    movement = 2
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = "Cavalry"
        
    double_attack_cost = True
    triple_attack = True
    push = True
    xp_to_upgrade = 3

    descriptions = {"double_attack_cost": "Attack takes two actions.",
                    "triple_attack": "Also hits the two diagonally nearby tiles in the attack direction.",
                    "push": "If attack and defence rolls both succeed, it can still move forward. If not on back line, "
                            "opponents units must retreat directly backwards or die."}

    upgrades = ["War Elephant II_A", "War Elephant II_B"]


class War_Elephant_II_A(Unit):

    name = "War Elephant II_A"
    image = "War Elephant"
    attack = 4
    defence = 3
    movement = 2
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = "Cavalry"

    double_attack_cost = True
    triple_attack = True
    push = True

    descriptions = {"double_attack_cost": "Attack takes two actions.",
                    "triple_attack": "Also hits the two diagonally nearby tiles in the attack direction.",
                    "push": "If attack and defence rolls both succeed, it can still move forward. If not on back line, "
                            "opponents units must retreat directly backwards or die."}


class War_Elephant_II_B(Unit):

    name = "War Elephant II_B"
    image = "War Elephant"
    attack = 3
    defence = 4
    movement = 2
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = "Cavalry"

    double_attack_cost = True
    triple_attack = True
    push = True

    descriptions = {"double_attack_cost": "Attack takes two actions.",
                    "triple_attack": "Also hits the two diagonally nearby tiles in the attack direction.",
                    "push": "If attack and defence rolls both succeed, it can still move forward. If not on back line, "
                            "opponents units must retreat directly backwards or die."}


class Samurai(Unit):
    
    name = "Samurai"
    image = "Samurai"
    attack = 3
    defence = 3
    movement = 1
    range = 1
    attack_bonuses = {"Infantry": 1}
    defence_bonuses = {}
    zoc = []
    type = "Infantry"
        
    combat_agility = True

    descriptions = {"combat_agility": "Can make an attack after its first action. (But not a second move.)"}

    upgrades = ["Samurai II_A", "Samurai II_B"]


class Samurai_II_A(Unit):

    name = "Samurai II_A"
    image = "Samurai"
    attack = 4
    defence = 3
    movement = 1
    range = 1
    attack_bonuses = {"Infantry": 1}
    defence_bonuses = {}
    zoc = []
    type = "Infantry"

    combat_agility = True

    descriptions = {"combat_agility": "Can make an attack after its first action. (But not a second move.)"}


class Samurai_II_B(Unit):

    name = "Samurai II_B"
    image = "Samurai"
    attack = 3
    defence = 3
    movement = 1
    range = 1
    attack_bonuses = {"Infantry": 1}
    defence_bonuses = {}
    zoc = []
    type = "Infantry"

    combat_agility = True
    bloodlust = True

    descriptions = {"combat_agility": "Can make an attack after its first action. (But not a second move.)",
                    "bloodlust": "Every kill gives it an extra attack"}


class Saboteur(Unit):
    
    name = "Saboteur"
    image = "Saboteur"
    attack = False
    defence = 2
    movement = 1
    range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Specialist"
    
    abilities = ["sabotage", "poison"]

    descriptions = {"sabotage": "Reduces a units defence to 0 for 1 turn.", "poison": "Freezes a unit for 2 turns."}

    upgrades = ["Saboteur II_A", "Saboteur II_B"]


class Saboteur_II_A(Unit):

    name = "Saboteur II_A"
    image = "Saboteur"
    attack = False
    defence = 2
    movement = 1
    range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Specialist"

    abilities = ["sabotage", "poison_II"]

    descriptions = {"sabotage": "Reduces a units defence to 0 for 1 turn.", "poison_II": "Freezes a unit for 3 turns."}


class Saboteur_II_B(Unit):

    name = "Saboteur II_B"
    image = "Saboteur"
    attack = False
    defence = 2
    movement = 1
    range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Specialist"

    abilities = ["sabotage_II", "poison"]

    descriptions = {"sabotage_II": "Reduces a units defence to -1 for 1 turn.", "poison": "Freezes a unit for 2 turns."}


class Diplomat(Unit):
    
    name = "Diplomat"
    image = "Diplomat"
    attack = False
    defence = 2
    movement = 1
    range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Specialist"
        
    abilities = ["bribe"]

    descriptions = {"bribe": "You can use an opponent's unit this turn. Your opponent can't use it on his next turn. "
                             "You can't bribe the same unit on your next turn. The unit gets +1A until end of turn."}

    upgrades = ["Diplomat II_A", "Diplomat II_B"]


class Diplomat_II_A(Unit):

    name = "Diplomat II_A"
    image = "Diplomat"
    attack = False
    defence = 2
    movement = 1
    range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Specialist"

    abilities = ["bribe"]

    descriptions = {"bribe": "You can use an opponent's unit this turn. Your opponent can't use it on his next turn. "
                             "You can't bribe the same unit on your next turn. The unit gets +1A until end of turn."}


class Diplomat_II_B(Unit):

    name = "Diplomat II_B"
    image = "Diplomat"
    attack = False
    defence = 2
    movement = 1
    range = 3
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Specialist"

    abilities = ["bribe"]

    descriptions = {"bribe": "You can use an opponent's unit this turn. Your opponent can't use it on his next turn. "
                             "You can't bribe the same unit on your next turn. The unit gets +1A until end of turn."}


class Weaponsmith(Unit):
    
    name = "Weaponsmith"
    image = "Weaponsmith"
    attack = False   
    defence = 2
    movement = 1
    range = 4
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Specialist"
    
    abilities = ["improve_weapons"]

    descriptions = {"improve_weapons": "Give melee unit +3 attack, +1 defence until your next turn"}

    upgrades = ["Weaponsmith II_A", "Weaponsmith II_B"]


class Weaponsmith_II_A(Unit):

    name = "Weaponsmith II_A"
    image = "Weaponsmith"
    attack = False
    defence = 2
    movement = 1
    range = 4
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Specialist"

    abilities = ["improve_weapons_II_A"]

    descriptions = {"improve_weapons_II_A": "Give melee unit +2 attack, +1 defence for two turns"}


class Weaponsmith_II_B(Unit):

    name = "Weaponsmith II_B"
    image = "Weaponsmith"
    attack = False
    defence = 2
    movement = 1
    range = 4
    attack_bonuses = {}
    defence_bonuses = {}
    type = "Specialist"

    abilities = ["improve_weapons_II_B"]

    descriptions = {"improve_weapons": "Give melee unit +3 attack, +2 defence, and "
                                       "zoc against cavalry until your next turn"}


class Hussar(Unit):

    name = "Hussar"
    image = "Hussar"
    attack = 2
    defence = 2
    movement = 3
    range = 1
    attack_bonuses = {}
    defence_bonuses = {}
    zoc = []
    type = "Cavalry"

    triple_attack = True
    triple_attack = True
    pikeman_specialist = True

    descriptions = {"triple_attack": "Also hits the two diagonally nearby tiles in the attack direction.",
                    "pikeman_specialist": "Pikemen do not get +1D against Hussar."}

    upgrades = ["Hussar II_A", "Hussar II_B"]
