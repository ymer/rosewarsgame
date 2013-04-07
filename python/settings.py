import interfaces


pause_for_animation_attack = 700
pause_for_animation = 400

pause_for_attack_until_click = False

interface = interfaces.Rectangles(1.3)

player1_ai = "Human"
player2_ai = "Evaluator"

document_ai_actions = True

use_special_units = []  # Special units that must be present in the game
dont_use_special_units = ["Chariot", "Samurai", "Diplomat"]  # Special units that must not be present in the game


# Rows that the units can start on, in the pseudo-random computer-generated start position
basic_units = {"Archer": (2, 3),
               "Ballista": (2, 3),
               "Catapult": (2, 3),
               "Heavy Cavalry": (2, 3, 4),
               "Light Cavalry": (2, 3),
               "Pikeman": (2, 3, 4)}

special_units = {"Berserker": (2, 3),
                 "Cannon": (2, ),
                 "Chariot": (3, 4),
                 "Crusader": (3, 4),
                 "Diplomat": (2, 3),
                 "Flag Bearer": (3, 4),
                 "Lancer": (3, 4),
                 "Longswordsman": (4,),
                 "Royal Guard": (2, 3),
                 "Saboteur": (2, 3),
                 "Samurai": (4,),
                 "Scout": (2, 3),
                 "Viking": (4,),
                 "War Elephant": (4,),
                 "Weaponsmith": (2, 3)}

unit_bag_size = 3
special_unit_count = 3
basic_unit_count = 6
