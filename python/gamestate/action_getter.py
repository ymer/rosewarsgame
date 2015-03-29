from gamestate.action import Action
from gamestate.gamestate_library import *
from game.game_library import merge
from itertools import product
import gamestate.action_sets as action_sets


def get_bonus_tiles(gamestate):
    """
    :param gamestate: The gamestate
    :return: The set of tiles that are affected by a friendly Crusader or Flag Bearer.
    """
    bonus_tiles = {
        Trait.crusading: {
            1: set(),
            2: set()
        },
        Trait.flag_bearing: set()
    }

    for pos, unit in gamestate.player_units.items():
        if unit.has(Trait.crusading, 1):
            bonus_tiles[Trait.crusading][1] |= pos.surrounding_tiles()
        if unit.has(Trait.crusading, 2):
            bonus_tiles[Trait.crusading][2] |= pos.surrounding_tiles()
        if unit.has(Trait.flag_bearing, 1):
            bonus_tiles[Trait.flag_bearing] |= pos.adjacent_tiles()
        if unit.has(Trait.flag_bearing, 2):
            bonus_tiles[Trait.flag_bearing] |= pos.surrounding_tiles()

    return bonus_tiles


def get_actions(gamestate):

    is_extra_action = gamestate.is_extra_action()

    if not gamestate.actions_remaining and not is_extra_action:
        return []

    actions = []
    for position, unit in gamestate.player_units.items():
        if can_use_unit(unit, is_extra_action):
            actions += get_unit_actions(unit, position, gamestate)

    return actions


def get_unit_actions(unit, start_at, gamestate):

    def melee_attack_actions(moveset):
        return [Action(units, start_at, **terms) for terms in attack_generator(moveset)]

    def ranged_attack_actions(attackset):
        return [Action(units, start_at, end_at=start_at, target_at=target_at) for target_at in attackset]

    def ability_actions(abilityset, ability):
        return [Action(units, start_at, end_at=start_at, target_at=position, ability=ability) for position in abilityset]

    def move_actions(moveset):
        return [Action(units, start_at, end_at) for end_at in moveset]

    def generate_movesets(movement):
        return action_sets.moves_sets(start_at, frozenset(units), zoc_blocks, movement, movement)

    def generate_extra_moveset():
        movement = unit.get_state(State.movement_remaining)
        return action_sets.moves_set(start_at, frozenset(units), zoc_blocks, movement, movement)

    def attack_generator(moveset):
        """ Generates all the tiles a unit can attack based on the places it can move to. """
        for position, direction in product(moveset, directions):
            new_position = position.move(direction)
            if new_position in enemy_units:
                if not zoc_block(position, direction, zoc_blocks) and \
                        (not enemy_units[new_position].has_extra_life or unit.has(Trait.push)):
                    yield {"end_at": position, "target_at": new_position, "move_with_attack": True}
                yield {"end_at": position, "target_at": new_position, "move_with_attack": False}

    def attack_generator_no_zoc_check(moveset):
        """ Generates all the tiles a unit can attack based on the places it can move to, without accounting for ZOC """
        for position, direction in product(moveset, directions):
            new_position = position.move(direction)
            if new_position in enemy_units:
                if enemy_units[new_position].has_extra_life and not unit.has(Trait.push):
                    yield {"end_at": position, "target_at": new_position, "move_with_attack": False}
                else:
                    yield {"end_at": position, "target_at": new_position}

    def get_defence_maneuverability_actions():

        moveset_with_leftover, moveset_no_leftover = generate_movesets(2)
        moveset = moveset_with_leftover | moveset_no_leftover
        attacks = melee_attack_actions(moveset_with_leftover | {start_at})
        moves = move_actions(moveset)

        moves = [move for move in moves if abs(move.start_at.row - move.end_at.row) < 2]
        attacks = [attack for attack in attacks if abs(attack.start_at.row - attack.target_at.row) < 2]

        return moves, attacks

    def get_javelin_attacks():
        javelin_attacks = ranged_attack_actions(action_sets.ranged_attacks_set(start_at, frozenset(enemy_units), 3))
        javelin_attacks = [attack for attack in javelin_attacks if distance(attack.end_at, attack.target_at) > 1]
        return javelin_attacks

    def get_extra_actions():

        def get_actions_combat_agility():
            for terms in attack_generator({start_at}):
                if terms["move_with_attack"]:
                    if unit.get_state(State.movement_remaining):
                        attacks.append(Action(units, start_at, **terms))
                else:
                    attacks.append(Action(units, start_at, **terms))
            return attacks

        moveset = generate_extra_moveset()
        moves = move_actions(moveset)

        attacks = []

        if unit.has(Trait.combat_agility):
            attacks = get_actions_combat_agility()
            moves = []

        return moves, attacks

    def get_ride_through_attacks():
        ride_through_attacks = []
        for direction in directions:
            one_tile_away = start_at.move(direction)
            if not one_tile_away:
                continue
            two_tiles_away = one_tile_away.move(direction)
            if not two_tiles_away:
                continue
            if one_tile_away in enemy_units and two_tiles_away not in units:
                ride_through_attacks.append(Action(units, start_at, end_at=two_tiles_away, target_at=one_tile_away,
                                                   move_with_attack=False))
        return ride_through_attacks

    def get_abilities():
        abilities = []
        for ability in unit.abilities:
            if ability in [Ability.sabotage, Ability.poison, Ability.assassinate]:
                target_positions = enemy_units
            elif ability in [Ability.improve_weapons]:
                target_positions = [pos for pos, target in player_units.items() if target.attack and target.is_melee]
            elif ability == Ability.bribe:
                target_positions = [pos for pos, target in enemy_units.items() if not target.has(Effect.bribed)]
            else:
                target_positions = []

            abilityset = action_sets.ranged_attacks_set(start_at, frozenset(target_positions), unit.range)
            if ability != Ability.assassinate or gamestate.actions_remaining == 1:
                abilities += ability_actions(abilityset, ability)

        return abilities

    player_units = gamestate.player_units
    enemy_units = gamestate.enemy_units
    units = merge(player_units, enemy_units)

    zoc_blocks = frozenset(position for position, enemy_unit in enemy_units.items() if unit.type in enemy_unit.zoc)

    moveset_with_leftover, moveset_no_leftover = generate_movesets(unit.movement)
    moveset = moveset_with_leftover | moveset_no_leftover
    moves = move_actions(moveset)
    if unit.is_ranged:
        attacks = ranged_attack_actions(action_sets.ranged_attacks_set(start_at, frozenset(enemy_units), unit.range))
    else:
        attacks = melee_attack_actions(moveset_with_leftover | {start_at})
    abilities = get_abilities()

    if unit.has(Trait.rage):
        attacks += [Action(units, start_at, end_at=terms["end_at"], target_at=terms["target_at"], move_with_attack=False)
                    for terms in attack_generator_no_zoc_check(moveset_no_leftover)]

    if unit.has(Trait.berserking):

        moveset_with_leftover, moveset_no_leftover = action_sets.moves_sets(start_at, frozenset(units), zoc_blocks, 4, 4)
        attacks = melee_attack_actions(moveset_with_leftover | {start_at})

    if unit.has(Trait.scouting):
        moves = move_actions(action_sets.moves_set(start_at, frozenset(units), frozenset([]), unit.movement, unit.movement))

    if unit.has(Trait.defence_maneuverability):
        moves, attacks = get_defence_maneuverability_actions()

    if unit.has(State.extra_action):
        moves, attacks = get_extra_actions()

    if unit.has(Trait.ride_through):
        attacks += get_ride_through_attacks()

    if unit.has_javelin:
        attacks += get_javelin_attacks()

    if not can_attack_with_unit(gamestate, unit) or unit.attack == 0:
        attacks = []

    if melee_frozen(gamestate.enemy_units, start_at):
        moves = []

    return moves + attacks + abilities


def zoc_block(position, direction, zoc_blocks):
    """
    :param position: The starting position of the unit
    :param direction: The Direction the unit wants to move
    :param zoc_blocks: Positions occupied by enemy units with ZOC against the unit
    :return: Whether the unit is prevented from going in the direction by a ZOC block
    """
    return any(pos in zoc_blocks for pos in position.perpendicular(direction))


def can_use_unit(unit, is_extra_action):
    if unit.has(Effect.poisoned) or unit.has(State.recently_bribed):
        return False
    elif is_extra_action:
        return unit.has(State.extra_action)
    else:
        return not unit.has(State.used)


def melee_frozen(enemy_units, start_at):
    return any(pos for pos in start_at.adjacent_tiles() if unit_with_attribute_at(pos, Trait.melee_freeze, enemy_units))


def can_attack_with_unit(gamestate, unit):
    return not (gamestate.actions_remaining == 1 and unit.has(Trait.double_attack_cost)) \
        and not unit.has(State.attack_frozen)
