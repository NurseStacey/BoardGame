from constants import *

class Player_Class():
    def __init__(self, color, which_player):
        
        self.player_color_hex = color
        self.which_player = which_player

    def get_color(self):

        return self.player_color_hex

    def get_player_number(self):

        return self.which_player

    def set_player_color(self, color):
        self.player_color_hex = color
