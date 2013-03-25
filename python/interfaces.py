class Interface(object):
    base_coordinates = (0, 0)

    normal_font_name = "arial"
    normal_font_size = 18
    big_font_size = 28
    bigger_font_size = 38
    dice_font_size = 78

    move_attack_icon = "./other/moveattack.gif"
    attack_icon = "./other/attack.gif"
    star_icon = "./other/star.gif"
    ability_icon = "./other/ability.gif"
    crusading_icon = "./other/flag.gif"
    high_morale_icon = "./other/flag.gif"
    move_icon = "./other/move.gif"

    # The rest of these will be set in the interface module
    board_image = ""
    unit_folder = ""

    unit_width = 0
    unit_height = 0
    board_size = None
    x_border = None
    y_border_top = None
    y_border_bottom = None

    center_coordinates = None

    symbol_coordinates = None

    first_symbol_coordinates = None
    second_symbol_coordinates = None

    first_counter_coordinates = None
    second_counter_coordinates = None
    third_counter_coordinates = None

    first_font_coordinates = None
    second_font_coordinates = None
    third_font_coordinates = None

    unit_padding_width = 0
    unit_padding_height = 0
    x_border = 0

    green_player_color = None
    red_player_color = None


class Rectangles(Interface):
    board_image = "./rectangles/board.gif"
    unit_folder = "./rectangles/"
    
    unit_padding_width = 17
    unit_padding_height = 15.13
    unit_width = 53
    unit_height = 72
    board_size = [782, 743]
    x_border = 29
    y_border_top = 26
    y_border_bottom = 26
    
    counter_base_x = 45
    counter_base_y = 0
    
    center_coordinates = (unit_width / 2, unit_height / 2)
    symbol_coordinates = (unit_width / 2 - 15, unit_height / 2 - 15)
    
    first_symbol_coordinates = (2, counter_base_y + 58)
    second_symbol_coordinates = (18, counter_base_y + 58)
    
    first_counter_coordinates = (counter_base_x, counter_base_y + 58)
    second_counter_coordinates = (counter_base_x, counter_base_y + 38)
    third_counter_coordinates = (counter_base_x, counter_base_y + 18)
    
    first_font_coordinates = (counter_base_x - 5, counter_base_y + 48)
    second_font_coordinates = (counter_base_x - 5, counter_base_y + 28)
    third_font_coordinates = (counter_base_x - 5, counter_base_y + 8)
    
    green_player_color = (150, 130, 15)
    red_player_color = (190, 55, 55)

    counter_circle_color = (0, 0, 0)
