from __future__ import division
import action_doer
import initializer
import action_getter
import ai_module
import units as units_module
import json
from common import *
from action import Action
from outcome import Outcome
from copy import copy


class Gamestate:
    def __init__(self,
                 player1_units,
                 player2_units,
                 actions_remaining,
                 extra_action=False,
                 created_at=None,
                 game_id=None):
        self.units = [player1_units, player2_units]
        self.actions_remaining = actions_remaining
        self.extra_action = extra_action
        self.action_count = 0
        self.created_at = created_at
        self.game_id = game_id

    @classmethod
    def from_log_document(cls, log_document, shift_turn=False):
        gamestate_document = log_document["initial_gamestate"]
        gamestate = cls.from_document(gamestate_document)
        action_count = int(log_document["action_count"])

        for action_number in range(1, action_count + 1):
            if gamestate.is_turn_done():
                gamestate.shift_turn()

            if not str(action_number) in log_document:
                # This happens when loading replays that are continuations of other replays
                continue

            action_document = log_document[str(action_number)]

            action = Action.from_document(gamestate.all_units(), action_document)

            options = None
            if str(action_number) + "_options" in log_document:
                options = log_document[str(action_number) + "_options"]

            outcome = None
            if action.is_attack():
                outcome_document = log_document[str(action_number) + "_outcome"]
                outcome = Outcome.from_document(outcome_document)
                if options and "move_with_attack" in options:
                    action.move_with_attack = bool(options["move_with_attack"])

            gamestate.do_action(action, outcome)

            if options and "upgrade" in options:
                upgrade_choice = options["upgrade"]
                if getattr(action.unit, "upgrades"):
                    upgraded_unit = getattr(units_module, upgrade_choice.replace(" ", "_"))()
                else:
                    if hasattr(Ability, upgrade_choice.keys()[0]):
                        upgrade_choice = get_ability_enum_dict(upgrade_choice)
                    else:
                        upgrade_choice = get_trait_enum_dict(upgrade_choice)
                    upgraded_unit = action.unit.get_upgraded_unit(upgrade_choice)
                if action.target_at and action.target_at in gamestate.player_units:
                    gamestate.player_units[action.target_at] = upgraded_unit
                else:
                    gamestate.player_units[action.end_at] = upgraded_unit

        if shift_turn:
            if gamestate.is_turn_done():
                gamestate.shift_turn()

        return gamestate

    def all_units(self):
        all_units = self.units[0].copy()
        all_units.update(self.units[1])
        return all_units

    def do_action(self, action, outcome):
        action_doer.do_action(self, action, outcome)
        self.action_count += 1

        if self.actions_remaining > 0 or self.extra_action:
            self.available_actions = action_getter.get_actions(self)
            if not self.available_actions:
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

    def set_network_player(self, local_player):
        for player in range(2):
            if self.players[player].player_id != local_player:
                self.players[player].ai_name = "Network"
                self.players[player].ai = "Network"

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
        if "extra_action" in document:
            extra_action = document["extra_action"]
        else:
            extra_action = False
        if "created_at" in document:
            created_at = document["created_at"]
        else:
            created_at = None
        return cls(player1_units, player2_units, actions_remaining, extra_action, created_at)

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
                unit = getattr(units_module, unit_document.replace(" ", "_"))()

            else:
                unit = getattr(units_module, unit_document["name"].replace(" ", "_"))()

                for attr, value in unit_document.items():
                    if attr == "zoc":
                        unit.zoc = {getattr(Type, unit_type) for unit_type in unit_document["zoc"]}
                    elif attr in state_descriptions:
                        state = getattr(State, attr)
                        unit.set(state, value)
                    elif attr in trait_descriptions:
                        trait = getattr(Trait, attr)
                        unit.set(trait, value)
                    elif attr in ability_descriptions:
                        ability = getattr(Ability, attr)
                        unit.set(ability, value)

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
        if self.extra_action:
            document["extra_action"] = True
        if self.created_at:
            document["created_at"] = self.created_at
        document["actions_remaining"] = self.actions_remaining
        if self.game_id:
            document["game"] = self.game_id
        document["player1_units"] = self.get_units_dict(self.units[0])
        document["player2_units"] = self.get_units_dict(self.units[1])

        return document

    def get_units_dict(self, units):
        units_dict = dict()
        for unit_position, unit in units.items():
            position = str(unit_position)

            states = unit.get_states()
            traits = unit.get_traits_not_in_base()
            attributes = merge(states, traits)

            if attributes:
                unit_dict = readable_attributes(attributes)
                unit_dict["name"] = unit.name
                units_dict[position] = unit_dict
            else:
                units_dict[position] = unit.name

        return units_dict

    def is_turn_done(self):
        return self.actions_remaining < 1 and not getattr(self, "extra_action")

    def shift_turn(self):
        self.flip_units()
        self.units = self.units[::-1]
        self.initialize_turn()

    def move_melee_unit_to_target_tile(self, action):
        action_doer.move_melee_unit_to_target_tile(self, action)

    def __str__(self):
        return document_to_string(self.to_document())

    def flip_units(self):
        self.units = [dict((position.flip(), unit) for position, unit in self.units[0].items()),
                      dict((position.flip(), unit) for position, unit in self.units[1].items())]

    def __eq__(self, other):
        return self.to_document() == other.to_document()

    def is_ended(self):
        backline = 8
        for position, unit in self.player_units.items():
            if not unit.has(State.bribed):
                if position.row == backline:
                    return True

        if not self.enemy_units:
            at_least_one_bribed = False
            for unit in self.player_units:
                if unit.is_bribed():
                    at_least_one_bribed = True
            if not at_least_one_bribed:
                return True

        return False
