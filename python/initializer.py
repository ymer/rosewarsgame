from __future__ import division
from common import *

remove_states = [State.used, State.recently_bribed]


def initialize_turn(gamestate):
    def resolve_bribe(unit):
        if unit.has(Effect.bribed):
            unit.decrement(Effect.bribed)
            gamestate.player_units[position] = gamestate.enemy_units.pop(position)
            unit.set(State.recently_bribed)

    gamestate.set_actions_remaining(2)

    for position, unit in gamestate.player_units.items():
        for state in remove_states:
            unit.remove_state(state)
        unit.wear_off_effects()

    # We just got the turn. Any bribed units we own is still controlled by the enemy,
    # at least until we take it back at the start of our turn (now)
    for position, unit in gamestate.enemy_units.items():
        resolve_bribe(unit)
        unit.remove_state(State.used)
