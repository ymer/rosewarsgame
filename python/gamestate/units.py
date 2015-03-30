from gamestate.gamestate_library import *
from game.game_library import *
from gamestate.enums import *


class Unit_class():
    def __init__(self):
        self.attributes = {}

    unit = None
    type = None
    experience_to_upgrade = 0
    base_attack = 0
    base_defence = 0
    base_range = 0
    base_movement = 0
    level = 0
    upgrades = []

    @property
    def attack(self):
        return self.base_attack + self.get_level(Trait.attack_skill)

    @property
    def defence(self):
        return self.base_defence + self.get_level(Trait.defence_skill)

    @property
    def range(self):
        return self.base_range + self.get_level(Trait.range_skill)

    @property
    def movement(self):
        return self.base_movement + self.get_level(Trait.movement_skill)

    def __repr__(self):
        return self.unit.name

    def __eq__(self, other):
        return self.to_document() == other.to_document()

    def __ne__(self, other):
        return not self.__eq__(other)

    @property
    def name(self):
        return self.unit.name

    @property
    def pretty_name(self):
        return prettify(self.unit.name)

    @property
    def states(self):
        return [attribute for attribute in self.attributes if attribute in State]

    @property
    def effects(self):
        return [attribute for attribute in self.attributes if attribute in Effect]

    @property
    def abilities(self):
        return [attribute for attribute in self.attributes if attribute in Ability]

    def get_traits(self):
        return [attribute for attribute in self.attributes if attribute in Trait]

    def get_states(self):
        return [attribute for attribute in self.attributes if attribute in State]

    def set(self, attribute, value=None, duration=None, level=1):
        if attribute in State:
            if value is None:
                value = 1
            self.attributes[attribute] = AttributeValues(value=value)
        else:
            self.attributes[attribute] = AttributeValues(value=value, duration=duration, level=level)

    def decrease_duration(self, attribute):
        if attribute in self.attributes:
            duration = self.attributes[attribute].duration - 1
            if duration == 0:
                del self.attributes[attribute]
            else:
                self.attributes[attribute].duration = duration

    def has(self, attribute, number=None):
        """
        :param attribute: A Trait, Effect, Ability or State
        :param number: A level or value depending on the attribute type
        :return: If a number is not given, returns whether the unit has the attribute.
                 If a number is given, returns whether the unit has the attribute at that specific level / value.
        """
        if attribute not in self.attributes:
            return False
        if number is None:
            return True
        if attribute in Trait or attribute in Effect or attribute in Ability:
            return self.attributes[attribute].level == number
        elif attribute in State:
            return self.attributes[attribute].value == number

    def get_duration(self, attribute):
        return self.attributes[attribute].duration

    def get_level(self, attribute):
        return self.attributes[attribute].level if attribute in self.attributes else 0

    def get_state(self, attribute):
        return self.attributes[attribute].value if attribute in self.attributes else 0

    def remove(self, attribute):
        if attribute in self.attributes:
            del self.attributes[attribute]

    def gain_experience(self):
        if not self.has(State.used) and not get_setting("Beginner_mode"):
            if State.experience in self.attributes:
                self.attributes[State.experience].value += 1
            else:
                self.attributes[State.experience] = AttributeValues(value=1)
            self.remove(State.recently_upgraded)

    def remove_states_with_value_zero(self):
        removestates = [state for state in self.states if self.get_state(state) == 0]
        for state in removestates:
            self.remove(state)

    @property
    def has_extra_life(self):
        return self.has(Trait.extra_life) and not self.has(State.lost_extra_life)

    @property
    def has_javelin(self):
        return self.has(Trait.javelin) and not self.has(State.javelin_thrown)

    @property
    def is_melee(self):
        return self.range == 1

    @property
    def is_ranged(self):
        return self.range > 1

    def get_upgraded_unit_from_upgrade(self, upgrade):
        """
        :param upgrade: A unit enum or a dictionary with enums as keys and AttributeValues as values.
        :return: An instance of a Unit_class object, based on the unit and with the upgrade.
        """
        if upgrade in Unit:
            upgraded_unit = self.make(upgrade)
            for attribute in self.attributes:
                if attribute in State or attribute in Effect:
                    upgraded_unit.attributes[attribute] = self.attributes[attribute]
            upgraded_unit.set(State.recently_upgraded)
            upgraded_unit.remove(State.experience)
            return upgraded_unit
        else:
            upgraded_unit = Unit_class.make(self.unit)
            upgraded_unit.attributes = dict(self.attributes)
            for key, attributes in upgrade.items():
                if key in upgraded_unit.attributes:
                    level = attributes.level + upgraded_unit.attributes[key].level
                    if level == 0:
                        del upgraded_unit.attributes[key]
                    else:
                        upgraded_unit.attributes[key] = AttributeValues(level=attributes.level + upgraded_unit.attributes[key].level)
                else:
                    upgraded_unit.attributes[key] = attributes
            upgraded_unit.set(State.recently_upgraded, value=1)

            return upgraded_unit

    def get_upgraded_unit_from_choice(self, choice):
        """
        :param choice: upgrade choice 0 or 1.
        :return: An instance of a Unit_class object, based on the unit and with the upgrade.
        """
        upgrade = self.get_upgrade(choice)
        return self.get_upgraded_unit_from_upgrade(upgrade)

    def get_upgrade(self, choice):
        """
        :param choice: upgrade choice 0 or 1.
        :return: The chosen unit upgrade in enum upgrade format. (Dictionary with enums as keys and AttributeValues as
        values.)
        """
        if get_setting("version") == "1.0":
            if choice == 1:
                return {Trait.attack_skill: AttributeValues(level=1)}
            else:
                return {Trait.defence_skill: AttributeValues(level=1)}

        def has_upgrade(upgrade):
            if upgrade in Unit:
                return False
            for attribute, level in upgrade.items():
                return self.has(attribute, level) and not base_units[self.unit].has(attribute, level)

        def is_final_upgrade(upgrade):
            upgrade_index = self.upgrades.index(upgrade)
            upgrades_count = len(self.upgrades)

            return upgrade_index == upgrades_count - 1 or upgrade_index == upgrades_count - 2

        def translate_to_enum_format(upgrade):
            if upgrade in Unit:
                return upgrade
            else:
                upgrade_enum_format = {}
                for attribute_enum, number in upgrade.items():
                    upgrade_enum_format[attribute_enum] = AttributeValues(level=number)
                return upgrade_enum_format

        possible_upgrade_choices = []
        for upgrade in self.upgrades:
            if not has_upgrade(upgrade) or is_final_upgrade(upgrade):
                possible_upgrade_choices.append(translate_to_enum_format(upgrade))

        return possible_upgrade_choices[choice]



    @property
    def unit_level(self):
        return self.get_state(State.experience) // self.experience_to_upgrade

    def should_be_upgraded(self):
        experience = self.get_state(State.experience)
        return experience and experience % self.experience_to_upgrade == 0 and not self.has(State.recently_upgraded)

    def to_document(self):
        write_attributes = {attribute: attribute_values for attribute, attribute_values in self.attributes.items() if
                            not base_units[self.unit].has(attribute)}

        if write_attributes:
            unit_dict = get_string_attributes(write_attributes)
            unit_dict["name"] = self.name
            return unit_dict
        else:
            return self.name

    @classmethod
    def make(cls, unit):
        return globals()[unit.name]()

    @classmethod
    def from_document(cls, document):
        unit = Unit_class(attributes={"rage": 1, "helmet": 1})
        return unit


class Archer(Unit_class):
    def __init__(self):
        super(Archer, self).__init__()
        self.set(Trait.arrows, level=1)
    unit = Unit.Archer
    type = Type.Infantry
    base_attack = 2
    base_defence = 2
    base_movement = 1
    base_range = 4
    upgrades = [{Trait.sharpshooting: 1}, {Trait.fire_arrows: 1}, {Trait.range_skill: 1}, {Trait.attack_skill: 1}]
    experience_to_upgrade = 4


class Pikeman(Unit_class):
    def __init__(self):
        super(Pikeman, self).__init__()
        self.set(Trait.cavalry_specialist, level=1)
        self.set(Trait.zoc_cavalry, level=1)
    unit = Unit.Pikeman
    type = Type.Infantry
    base_attack = 2
    base_defence = 2
    base_movement = 1
    base_range = 1
    upgrades = [Unit.Halberdier, Unit.Royal_Guard]
    experience_to_upgrade = 3


class Halberdier(Unit_class):
    def __init__(self):
        super(Halberdier, self).__init__()
        self.set(Trait.push, level=1)
        self.set(Trait.cavalry_specialist, level=1)
        self.set(Trait.zoc_cavalry, level=1)
    unit = Unit.Halberdier
    type = Type.Infantry
    base_attack = 3
    base_defence = 2
    base_movement = 1
    base_range = 1
    upgrades = [{Trait.attack_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4


class Light_Cavalry(Unit_class):

    unit = Unit.Light_Cavalry
    type = Type.Cavalry
    base_attack = 2
    base_defence = 2
    base_movement = 4
    base_range = 1
    upgrades = [Unit.Flanking_Cavalry, Unit.Hussar]
    experience_to_upgrade = 3


class Flanking_Cavalry(Unit_class):
    def __init__(self):
        super(Flanking_Cavalry, self).__init__()
        self.set(Trait.flanking, level=1)

    unit = Unit.Flanking_Cavalry
    type = Type.Cavalry
    base_attack = 2
    base_defence = 2
    base_movement = 4
    base_range = 1
    upgrades = [{Trait.flanking: 1}, {Trait.movement_skill: 1}, {Trait.attack_skill: 2}]
    experience_to_upgrade = 4


class Hussar(Unit_class):
    def __init__(self):
        super(Hussar, self).__init__()
        self.set(Trait.ride_through, level=1)

    unit = Unit.Hussar
    type = Type.Cavalry
    base_attack = 2
    base_defence = 2
    base_movement = 4
    base_range = 1
    upgrades = [{Trait.attack_skill: 1}, {Trait.movement_skill: 1}]
    experience_to_upgrade = 4


class Knight(Unit_class):

    unit = Unit.Knight
    type = Type.Cavalry
    base_attack = 3
    base_defence = 3
    base_movement = 2
    base_range = 1
    upgrades = [Unit.Lancer, Unit.Hobelar]
    experience_to_upgrade = 4


class Lancer(Unit_class):
    def __init__(self):
        super(Lancer, self).__init__()
        self.set(Trait.lancing, level=1)
        self.set(Trait.cavalry_specialist, level=1)

    unit = Unit.Lancer
    type = Type.Cavalry
    base_attack = 2
    base_defence = 3
    base_movement = 3
    base_range = 1
    upgrades = [{Trait.lancing: 1, Trait.movement_skill: 1}, {Trait.attack_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4


class Hobelar(Unit_class):
    def __init__(self):
        super(Hobelar, self).__init__()
        self.set(Trait.swiftness, level=1)

    unit = Unit.Hobelar
    type = Type.Cavalry
    base_attack = 3
    base_defence = 3
    base_movement = 3
    base_range = 1
    upgrades = [{Trait.cavalry_specialist: 1}, {Trait.attack_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4


class Ballista(Unit_class):
 
    unit = Unit.Ballista
    type = Type.War_Machine
    base_attack = 4
    base_defence = 1
    base_movement = 1
    base_range = 3
    upgrades = [{Trait.fire_arrows: 1}, {Trait.attack_skill: 1}, {Trait.range_skill: 1}]
    experience_to_upgrade = 4


class Catapult(Unit_class):
    def __init__(self):
        super(Catapult, self).__init__()
        self.set(Trait.double_attack_cost, level=1)

    unit = Unit.Catapult
    type = Type.War_Machine
    base_attack = 6
    base_defence = 2
    base_movement = 1
    base_range = 3
    upgrades = [{Trait.attack_skill: 1}, {Trait.range_skill: 1, Trait.attack_skill: -1}]
    experience_to_upgrade = 3


class Royal_Guard(Unit_class):
    def __init__(self):
        super(Royal_Guard, self).__init__()
        self.set(Trait.defence_maneuverability, level=1)
        self.set(Trait.zoc_all)
  
    unit = Unit.Royal_Guard
    type = Type.Infantry
    base_attack = 3
    base_defence = 3
    base_movement = 1
    base_range = 1
    upgrades = [{Trait.melee_expert: 1}, {Trait.attack_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 3


class Scout(Unit_class):
    def __init__(self):
        super(Scout, self).__init__()
        self.set(Trait.scouting, level=1)
    
    unit = Unit.Scout
    type = Type.Cavalry
    base_attack = 0
    base_defence = 2
    base_movement = 4
    base_range = 1
    upgrades = [{Trait.tall_shield: 1}, {Trait.attack_skill: 2}, {Trait.movement_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 2


class Viking(Unit_class):
    def __init__(self):
        super(Viking, self).__init__()
        self.set(Trait.rage, level=1)
        self.set(Trait.extra_life, level=1)
        self.set(Trait.helmet, level=1)

    unit = Unit.Viking
    type = Type.Infantry
    base_attack = 3
    base_defence = 2
    base_movement = 1
    base_range = 1
    upgrades = [{Trait.war_machine_specialist: 1}, {Trait.attack_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4


class Javeliner(Unit_class):
    def __init__(self):
        super(Javeliner, self).__init__()
        self.set(Trait.javelin, level=1)

    unit = Unit.Javeliner
    type = Type.Infantry
    base_attack = 4
    base_defence = 3
    base_movement = 1
    base_range = 1
    upgrades = [{Trait.attack_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4


class Cannon(Unit_class):
    def __init__(self):
        super(Cannon, self).__init__()
        self.set(Trait.attack_cooldown, level=1)
    
    unit = Unit.Cannon
    base_attack = 5
    base_defence = 1
    base_movement = 1
    base_range = 4
    type = Type.War_Machine
    upgrades = [{Trait.attack_cooldown: 1, Trait.far_sighted: 1}, {Trait.attack_skill: 1}, {Trait.range_skill: 1}]
    experience_to_upgrade = 3


class Trebuchet(Unit_class):
    def __init__(self):
        super(Trebuchet, self).__init__()
        self.set(Trait.spread_attack, level=1)

    unit = Unit.Trebuchet
    type = Type.War_Machine
    base_attack = 3
    base_defence = 1
    base_movement = 1
    base_range = 3
    upgrades = [{Trait.attack_skill: 1}, {Trait.range_skill: 1}]
    experience_to_upgrade = 4


class Flag_Bearer(Unit_class):
    def __init__(self):
        super(Flag_Bearer, self).__init__()
        self.set(Trait.flag_bearing, level=1)
   
    unit = Unit.Flag_Bearer
    type = Type.Cavalry
    base_attack = 2
    base_defence = 3
    base_movement = 3
    base_range = 1
    upgrades = [{Trait.flag_bearing: 1}, {Trait.attack_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 3


class Longswordsman(Unit_class):
    def __init__(self):
        super(Longswordsman, self).__init__()
        self.set(Trait.longsword, level=1)

    unit = Unit.Longswordsman
    type = Type.Infantry
    base_attack = 3
    base_defence = 3
    base_movement = 1
    base_range = 1
    upgrades = [{Trait.rage: 1}, {Trait.attack_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4


class Crusader(Unit_class):
    def __init__(self):
        super(Crusader, self).__init__()
        self.set(Trait.crusading, level=1)

    unit = Unit.Crusader
    type = Type.Cavalry
    base_attack = 3
    base_defence = 3
    base_movement = 3
    base_range = 1
    upgrades = [{Trait.crusading: 1}, {Trait.attack_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4


class Berserker(Unit_class):
    def __init__(self):
        super(Berserker, self).__init__()
        self.set(Trait.berserking, level=1)

    unit = Unit.Berserker
    type = Type.Infantry
    base_attack = 5
    base_defence = 1
    base_movement = 1
    base_range = 1
    upgrades = [{Trait.big_shield: 1}, {Trait.attack_skill: 2}, {Trait.attack_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4


class War_Elephant(Unit_class):
    def __init__(self):
        super(War_Elephant, self).__init__()
        self.set(Trait.double_attack_cost, level=1)
        self.set(Trait.triple_attack, level=1)
        self.set(Trait.push, level=1)

    unit = Unit.War_Elephant
    type = Type.Cavalry
    base_attack = 3
    base_defence = 3
    base_movement = 2
    base_range = 1
    upgrades = [{Trait.defence_skill: 1}, {Trait.attack_skill: 1}]
    experience_to_upgrade = 3


class Fencer(Unit_class):
    def __init__(self):
        super(Fencer, self).__init__()
        self.set(Trait.combat_agility, level=1)
        self.set(Trait.rapier, level=1)

    unit = Unit.Fencer
    type = Type.Infantry
    base_attack = 3
    base_defence = 3
    base_movement = 1
    base_range = 1
    upgrades = [{Trait.attack_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4


class Saboteur(Unit_class):
    def __init__(self):
        super(Saboteur, self).__init__()
        self.set(Ability.sabotage, level=1)
        self.set(Ability.poison, level=1)
    unit = Unit.Saboteur
    type = Type.Specialist
    base_attack = 0
    base_defence = 2
    base_movement = 1
    base_range = 3
    upgrades = [{Ability.sabotage: 1}, {Ability.poison: 1}, {Trait.range_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4


class Diplomat(Unit_class):
    def __init__(self):
        super(Diplomat, self).__init__()
        self.set(Ability.bribe, level=1)
    unit = Unit.Diplomat
    type = Type.Specialist
    base_attack = 0
    base_defence = 2
    base_movement = 1
    base_range = 3
    upgrades = [{Ability.bribe: 1}, {Trait.range_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4


class Assassin(Unit_class):
    def __init__(self):
        super(Assassin, self).__init__()
        self.set(Ability.assassinate, level=1)
    unit = Unit.Assassin
    type = Type.Specialist
    base_attack = 0
    base_defence = 2
    base_movement = 1
    base_range = 11
    upgrades = [{Ability.assassinate: 1}, {Trait.defence_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 2


class Weaponsmith(Unit_class):
    def __init__(self):
        super(Weaponsmith, self).__init__()
        self.set(Ability.improve_weapons, level=1)

    unit = Unit.Weaponsmith
    type = Type.Specialist
    base_attack = 0
    base_defence = 2
    base_movement = 1
    base_range = 4
    upgrades = [{Ability.improve_weapons: 1}, {Trait.range_skill: 1}, {Trait.defence_skill: 1}]
    experience_to_upgrade = 4


base_units = {unit: Unit_class.make(unit) for unit in list(Unit)}
