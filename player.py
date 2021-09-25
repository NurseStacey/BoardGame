from constants import *

class Player_Class():
    def __init__(self, color, which_player):
        
        self.player_color_hex = color
        self.which_player = which_player
        self.this_AI = None

    def set_AI(self, this_AI):
        self.this_AI = this_AI

    def is_AI(self):
        return not(self.this_AI==None)
    def get_color(self):

        return self.player_color_hex

    def get_player_number(self):

        return self.which_player

    def set_player_color(self, color):
        self.player_color_hex = color
