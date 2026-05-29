from constants import *

class Player_Class():
    def __init__(self, color, which_player):
        
        self.player_color = color
        self.which_player = which_player
        self.is_human=True

    def IsAI(self):
        return not self.is_human
    
    def IsHuman(self):
        return self.is_human
    
    def ChangeIsHuman(self):
        self.is_human=not self.is_human

    def get_color(self):

        return self.player_color

    def get_color_name(self):

        #this_color = next([x for x in the_colors if x.hex==self.player_color])
        return self.player_color.name.capitalize()
  
    
    def get_player_number(self):

        return self.which_player

    def set_player_color(self, color):
        self.player_color_hex = color
