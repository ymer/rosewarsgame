from __future__ import division
from viewcommon import *
from common import *
from rounded_rect import AAfilledRoundedRect


class Viewlog:

    def __init__(self, zoom, interface, screen):
        self.zoom = zoom
        self.interface = interface
        self.screen = screen
        self.maximum_logs = 5
        self.base_height = 48

        unit_height = int((self.base_height - 14) * self.zoom)
        unit_width = int((self.interface.unit_width * unit_height / self.interface.unit_height))
        self.unit_dimensions = (unit_width, unit_height)

        self.box_dimensions = 40 * self.zoom, (self.base_height - 2) * self.zoom
        self.line_thickness = int(3 * self.zoom)

        self.locations = {}
        for i in range(self.maximum_logs):
            base = Location(391, i * self.base_height, self.zoom)
            self.locations[i] = {"unit1": base.adjust(65, 5),
                                 "unit2": base.adjust(165, 5),
                                 "symbol": base.adjust(118, 8),
                                 "outcome": base.adjust(230, 5),
                                 "box": base.adjust(0, 0),
                                 "box_text": base.adjust(7, 0),
                                 "line": base.adjust(0, self.base_height - self.line_thickness / 2)}

    def draw_logbook(self, logbook):

        def clear_log():
            pygame.draw.rect(self.screen, Color.Light_grey, self.interface.right_side_rectangle)

        clear_log()

        while len(logbook) > self.maximum_logs:
            logbook.pop(0)

        for lognumber, log in enumerate(logbook):

            locations = self.locations[lognumber]

            self.draw_turn_box(log.colors[0], log.action_number, locations)
            self.draw_unit(log.unit, locations["unit1"], log.colors[0])

            if log.action_type == ActionType.Attack:
                symbol = self.interface.attack_icon
                self.draw_outcome(log.outcome_string, locations["outcome"])
                self.draw_unit(log.target_unit, locations["unit2"], log.colors[1])

            elif log.action_type == ActionType.Ability:
                symbol = self.interface.ability_icon
                self.draw_unit(log.target_unit, locations["unit2"], log.colors[1])

            else:
                symbol = self.interface.move_icon

            self.draw_symbol(symbol, locations["symbol"])

        write(self.screen, "Help", self.interface.help_area[0], self.interface.fonts["normal"])

    def draw_unit(self, unit, location, color):
        unit_pic = get_unit_pic(self.interface, unit)
        unit_image = get_image(unit_pic, self.unit_dimensions)
        self.draw_unit_box(location, color)
        self.screen.blit(unit_image, location.tuple)

    def draw_symbol(self, symbol, location):
        image = get_image(symbol)
        self.screen.blit(image, location.tuple)

    def draw_turn_box(self, color, action_number, locations):
        border_color = self.interface.green_player_color if color == "Green" else self.interface.red_player_color

        pygame.draw.rect(self.screen, border_color, (locations["box"].tuple, self.box_dimensions))
        write(self.screen, str(action_number), locations["box_text"].tuple, self.interface.fonts["big"])

        line_start = locations["line"]
        line_end = line_start.adjust(600, 0)
        pygame.draw.line(self.screen, Color.Black, line_start.tuple, line_end.tuple, self.line_thickness)

    def draw_unit_box(self, base, color):
        border_color = self.interface.green_player_color if color == "Green" else self.interface.red_player_color
        thickness = int(3 * self.zoom)

        rectangle_style = [base.tuple[0], base.tuple[1], self.unit_dimensions[0], self.unit_dimensions[1]]
        rectangle_style[0] -= thickness
        rectangle_style[1] -= thickness
        rectangle_style[2] += 2 * thickness
        rectangle_style[3] += 2 * thickness

        AAfilledRoundedRect(self.screen, tuple(rectangle_style), border_color, 0.2)

    def draw_outcome(self, outcome_string, location):
        write(self.screen, outcome_string, location.tuple, self.interface.fonts["larger"])

