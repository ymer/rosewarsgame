from __future__ import division
import action_doer
import initializer
import action_getter
import saver
import settings
import ai_module


class Gamestate:
    
    def __init__(self, player1, player1_units, player2, player2_units, turn=1, actions_remaining=2):
        self.turn = turn
        self.units = [player1_units, player2_units]
        self.players = [player1, player2]
        self.actions_remaining = actions_remaining

    def do_action(self, action):
        action_doer.do_action(self, action)

        if self.actions_remaining > 0:
            self.available_actions = action_getter.get_actions(self)
            if not self.available_actions:
                self.actions_remaining = 0

    def initialize_turn(self):
        initializer.initialize_turn(self)

    def initialize_action(self):
        initializer.initialize_action(self)

    def get_actions(self):
        if hasattr(self.players[0], "extra_action"):
            return action_getter.get_extra_actions(self)
        if self.actions_remaining == 1 and hasattr(self, "available_actions"):
            return self.available_actions
        else:
            return action_getter.get_actions(self)

    def copy(self):
        saved_gamestate = save_gamestate(self)
        return load_gamestate(saved_gamestate)

    def __eq__(self, other):
        pass

    def set_ais(self):
        if self.players[0].ai_name != "Human":
            self.players[0].ai = ai_module.AI(self.players[0].ai_name)
        else:
            self.players[0].ai = "Human"

        if self.players[1].ai_name != "Human":
            self.players[1].ai = ai_module.AI(self.players[1].ai_name)
        else:
            self.players[1].ai = "Human"

    def turn_shift(self):
        if self.players[0].color == "Green":
            self.turn += 1
        self.units = [self.units[1], self.units[0]]
        self.players = [self.players[1], self.players[0]]
        self.initialize_turn()
        self.initialize_action()

    def current_player(self):
        return self.players[0]

    def opponent_player(self):
        return self.players[1]

    def player_units(self):
        return self.units[0]

    def opponent_units(self):
        return self.units[1]

    def get_actions_remaining(self):
        return self.actions_remaining

    def set_actions_remaining(self, actions_remaining):
        self.actions_remaining = actions_remaining

    def decrement_actions_remaining(self):
        self.actions_remaining -= 1


def save_gamestate(gamestate):
    return saver.save_gamestate(gamestate)


def load_gamestate(saved_gamestate):
    return saver.load_gamestate(saved_gamestate)


def write_gamestate(gamestate, path):
    pass


def read_gamestate(path):
    pass