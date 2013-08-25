from __future__ import division
import action_doer
import initializer
import action_getter
import ai_module
from units import Unit
import json
from common import *
from copy import copy


class Gamestate:
    def __init__(self,
                 player1_units,
                 player2_units,
                 actions_remaining,
                 created_at=None,
                 game_id=None):
        self.units = [player1_units, player2_units]
        self.actions_remaining = actions_remaining
        self.action_count = 0
        self.created_at = created_at
        self.game_id = game_id

    def all_units(self):
        all_units = self.units[0].copy()
        all_units.update(self.units[1])
        return all_units

    def do_action(self, action, outcome):
        action_doer.do_action(self, action, outcome)
        self.action_count += 1

        if action.move_with_attack in [True, False] and \
                (self.actions_remaining > 0 or action.unit.has(State.extra_action)):
            self.set_available_actions()

            self.decrement_actions_if_none_available(action)

    def decrement_actions_if_none_available(self, action):
        if not self.available_actions:
            if action.unit.has(State.extra_action):
                action.unit.remove_state(State.extra_action)
                action.unit.remove_state(State.movement_remaining)
                self.set_available_actions()
            else:
                self.actions_remaining = 0

    def initialize_turn(self):
        initializer.initialize_turn(self)

    def get_actions(self):
        return self.available_actions

    def get_actions_with_none(self):
        actions_with_none = copy(self.available_actions)
        for action in self.available_actions:
            if action.move_with_attack:
                action_option = action.copy()
                action_option.move_with_attack = None
                actions_with_none.append(action_option)
        return actions_with_none

    def copy(self):
        gamestate_document = self.to_document()
        return self.from_document(gamestate_document)

    def __eq__(self, other):
        pass

    def set_available_actions(self):
        self.available_actions = action_getter.get_actions(self)

    @property
    def player_units(self):
        return self.units[0]

    @property
    def enemy_units(self):
        return self.units[1]

    def get_actions_remaining(self):
        return self.actions_remaining

    def set_actions_remaining(self, actions_remaining):
        self.actions_remaining = actions_remaining

    def decrement_actions_remaining(self):
        self.actions_remaining -= 1

    @classmethod
    def from_document(cls, document):
        player1_units = cls.units_from_document(document["player1_units"])
        player2_units = cls.units_from_document(document["player2_units"])
        actions_remaining = document["actions_remaining"]

        if "created_at" in document:
            created_at = document["created_at"]
        else:
            created_at = None
        return cls(player1_units, player2_units, actions_remaining, created_at)

    @classmethod
    def from_file(cls, path):
        document = json.loads(open(path).read())
        return Gamestate.from_document(document)

    @classmethod
    def units_from_document(cls, document):
        units = {}
        for position_string, unit_document in document.items():
            position = Position.from_string(position_string)

            if isinstance(unit_document, basestring):
                unit = Unit.make(unit_document)
            else:
                unit = Unit.make(unit_document["name"])

                for attribute, value in unit_document.items():
                    if attribute == "zoc":
                        unit.zoc = {getattr(Type, unit_type) for unit_type in unit_document["zoc"]}
                    elif attribute in state_descriptions:
                        state = getattr(State, attribute)
                        unit.set(state, value)
                    elif attribute in trait_descriptions:
                        trait = getattr(Trait, attribute)
                        unit.set(trait, value=value)
                    elif attribute in ability_descriptions:
                        ability = getattr(Ability, attribute)
                        unit.set(ability, value=value)
                    elif attribute in effect_descriptions:
                        effect = getattr(Effect, attribute)
                        if isinstance(value, int):
                            unit.set_effect(effect, 1, value)
                        else:
                            unit.set_effect(effect, level=value[0], duration=value[1])

            units[position] = unit

        return units

    @classmethod
    def get_ai_from_name(cls, name):
        if name == "Human":
            return name
        else:
            return ai_module.AI(name)

    def to_document(self):
        document = {}
        if self.created_at:
            document["created_at"] = self.created_at
        document["actions_remaining"] = self.actions_remaining
        if self.game_id:
            document["game"] = self.game_id

        document["player1_units"] = {str(position): unit.to_document() for (position, unit) in self.units[0].items()}
        document["player2_units"] = {str(position): unit.to_document() for (position, unit) in self.units[1].items()}

        return document

    def is_turn_done(self):
        return self.actions_remaining < 1 and not self.is_extra_action()

    def shift_turn(self):
        self.flip_all_units()
        self.units = self.units[::-1]
        self.initialize_turn()

    def move_melee_unit_to_target_tile(self, rolls, action):
        action_doer.move_melee_unit_to_target_tile(self, rolls, action)
        self.set_available_actions()
        self.decrement_actions_if_none_available(action)

    def __str__(self):
        return document_to_string(self.to_document())

    def flip_all_units(self):
        self.units = [flip_units(self.player_units), flip_units(self.enemy_units)]

    def __eq__(self, other):
        return self.to_document() == other.to_document()

    def is_ended(self):
        backline = 8
        for position, unit in self.player_units.items():
            if not unit.has(Effect.bribed):
                if position.row == backline:
                    return True

        if not self.enemy_units:
            at_least_one_bribed = False
            for position, unit in self.player_units.items():
                if unit.is_bribed():
                    at_least_one_bribed = True
            if not at_least_one_bribed:
                return True

        return False

    def get_unit_from_action_document(self, action_document):
        unit_position = Position.from_string(action_document["end_at"])

        if not unit_position in self.player_units and not unit_position in self.enemy_units:
            unit_position = Position.from_string(action_document["target_at"])

        if unit_position in self.player_units:
            return self.player_units[unit_position], unit_position
        else:
            return self.enemy_units[unit_position], unit_position

    def is_extra_action(self):
        for position, unit in self.player_units.items():
            if unit.has(State.extra_action):
                return True

        return False

    def get_upgradeable_unit(self):
        for position, unit in self.player_units.items():
            if unit.is_milf():
                return position, unit
