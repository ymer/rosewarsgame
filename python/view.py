from __future__ import division
import pygame
import interface_settings as settings
from viewlog import Viewlog
import viewgame
import viewinfo
from viewcommon import *


class View(object):
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.zoom = settings.zoom
        self.interface = settings.interface
        self.interface.load_fonts(self.zoom)
        self.screen = pygame.display.set_mode(self.interface.board_size)
        self.viewlog = Viewlog(self.zoom, self.interface, self.screen)
        self.counter_size = self.interface.counter_size
        self.showing_unit_info = False

        self.sounds = {
            "sword": "sword_sound.wav",
            "War_Elephant": "Elephant.wav",
            "Archer": "bow_fired.wav",
            "Catapult": "catapult_attacksound.wav",
            "unit_defeated": "infantry_defeated_sound.wav",
            "your_turn": "fanfare.wav"
        }

    def get_position_from_mouse_click(self, coordinates):
        return get_position_from_mouseclick(self.interface, coordinates)

    def draw_ask_about_move_with_attack(self, position):
        viewgame.draw_ask_about_move_with_attack(self.screen, self.interface, position)
        write_message(self.screen, self.interface, "Click the tile you want to stand on.")
        self.refresh()

    def save_screenshot(self, name):
        pygame.image.save(self.screen, name)

    def draw_game_end(self, color):
        write_message(self.screen, self.interface, color + " Wins")
        self.refresh()

    def clear_right(self):
        pygame.draw.rect(self.screen, colors["light_grey"], self.interface.right_side_rectangle)
        write(self.screen, "Help", self.interface.help_area[0], self.interface.fonts["normal"])
        self.showing_unit_info = False

    def clear_left(self):
        pygame.draw.rect(self.screen, colors["light_grey"], self.interface.left_side_rectangle)

    def clear_right_tutorial(self):
        pygame.draw.rect(self.screen, colors["light_grey"], self.interface.right_side_rectangle)
        write(self.screen, "To Game", self.interface.help_area[0], self.interface.fonts["normal"])
        write(self.screen, "To Menu", self.interface.to_help_menu_area[0], self.interface.fonts["normal"])
        self.showing_unit_info = False

    def draw_game(self, game, start_at=None, actions=(), redraw_log=False):
        viewgame.draw_game(self.screen, self.interface, game, start_at, actions)
        if redraw_log:
            self.clear_right()
            self.viewlog.draw_logbook()
        self.refresh()

    def show_unit_zoomed(self, unit, attack_hint):
        self.clear_right()
        viewinfo.show_unit_zoomed(self.screen, self.interface, unit, attack_hint)
        self.showing_unit_info = True
        self.refresh()

    def show_unit_zoomed_tutorial(self, unit, attack_hint):
        self.clear_right_tutorial()
        viewinfo.show_unit_zoomed(self.screen, self.interface, unit, attack_hint)
        self.showing_unit_info = True
        write(self.screen, "To Game", self.interface.help_area[0], self.interface.fonts["normal"])
        self.refresh()

    def hide_unit_zoomed(self):
        if self.showing_unit_info:
            self.clear_right()
            self.viewlog.draw_logbook()

    @staticmethod
    def refresh():
        pygame.display.flip()

    def draw_upgrade_options(self, unit):
        viewinfo.draw_upgrade_options(self.screen, self.interface, unit)
        self.refresh()

    def draw_ask_about_ability(self, unit):
        viewinfo.draw_ask_about_ability(self.screen, self.interface, unit)
        self.refresh()

    def draw_action(self, action, outcome, game, flip=False):
        self.viewlog.add_log(action, outcome, game)
        self.viewlog.draw_logbook()
        viewgame.draw_action(self.screen, self.interface, action, outcome, flip)
        self.refresh()

    def draw_post_movement(self, action):
        viewgame.draw_post_movement(self.screen, self.interface, action)
        self.refresh()

    def shade_positions(self, positions, color=None):
        viewgame.shade_positions(self.screen, self.interface, positions, color)
        self.refresh()

    def draw_message(self, message):
        write_message(self.screen, self.interface, message)
        self.refresh()

    def draw_tutorial_message(self, message, draw_on_lower):
        line_distances = self.interface.line_distances["medium"]
        fonts = self.interface.fonts["medium"]
        x_coordinate = 410 * settings.zoom
        if draw_on_lower:
            y_coordinate = 500 * settings.zoom
        else:
            y_coordinate = 10 * settings.zoom
        show_lines(self.screen, message, 42 * settings.zoom, line_distances, fonts, x_coordinate, y_coordinate + 30)
        self.refresh()

    def draw_game_tutorial(self, game):
        viewgame.draw_game(self.screen, self.interface, game)
        self.clear_right_tutorial()
        self.refresh()

    def draw_tutorial_page_number(self, number, total):
        write(self.screen, str(number) + "/" + str(total), (740, 20), self.interface.fonts["normal"])

    def draw_action_tutorial(self, action, rolls):
        viewgame.draw_action(self.screen, self.interface, action, rolls)
        self.refresh()

    def play_sound(self, sound):
        sound = pygame.mixer.Sound("./../sounds/" + self.sounds[sound])
        sound.play()

    def draw_help_menu(self, menu):
        self.screen.fill(colors["light_grey"])
        for i, item in enumerate(menu):
            write(self.screen, item, self.interface.help_menu[i], self.interface.fonts["normal"])
        write(self.screen, "To game", self.interface.help_area[0], self.interface.fonts["normal"])
        self.refresh()

    def show_upgrades_tutorial(self, upgrades):
        self.clear_left()
        message = []
        for index, upgrade in enumerate(upgrades):
            if isinstance(upgrade, int):
                message.append(str(index + 1) + ". " + Unit.write[upgrade])
            else:
                message.append(str(index + 1) + ". ")
                for attribute, level in upgrade.items():
                    if attribute in Trait.name:
                        message.append(Trait.write[attribute])
                        message.append(get_description(attribute, level))
                        message.append("")
                    elif attribute in Ability.name:
                        message.append(Ability.write[attribute])
                        message.append(get_description(attribute, 2))
                        message.append("")
        show_lines(self.screen, message, 52 * settings.zoom, self.interface.line_distances["larger"],
                   self.interface.fonts["normal"], 5, 5)
        self.refresh()
