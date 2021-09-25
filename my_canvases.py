import tkinter as tk
import math
from tkinter.constants import LEFT
from constants import *

#position = [x,y]

class button_class():
    def __init__(self, x_top, y_top, x_bottom, y_bottom, tag):
        self.x_top=x_top
        self.y_top=y_top
        self.x_bottom=x_bottom
        self.y_bottom = y_bottom
        self.tag = tag

    

    def is_in_button(self, x, y):

        return (x>self.x_top and x<self.x_bottom and y>self.y_top and y<self.y_bottom)

class Board_Class(tk.Canvas):
    def __init__(self, button_click_event, * args, **kwargs):
        super().__init__(*args, **kwargs)

        self.number_rows = 8
        self.number_columns = 8
        
        self.canvas_width = kwargs['width']
        self.canvas_height = kwargs['height']
        self.height_delta = self.canvas_height/self.number_rows
        self.width_delta = self.canvas_width/self.number_columns

        self.board_pieces = []
        
        self.bind("<Button-1>", button_click_event)
        self.update()

    def create_outline(self, top_x, top_y, bottom_x, bottom_y):

        top_x_coordinate = top_x * self.width_delta-1
        top_y_coordinate = top_y * self.height_delta-1
        bottom_x_coordinate = bottom_x * self.width_delta+1
        bottom_y_coordinate = bottom_y * self.height_delta+1

        self.create_line(top_x_coordinate, top_y_coordinate,
                         bottom_x_coordinate, top_y_coordinate, width=3, fill=get_color('red'))

        self.create_line(bottom_x_coordinate, top_y_coordinate,
                         bottom_x_coordinate, bottom_y_coordinate, width=3, fill=get_color('red'))

        self.create_line(bottom_x_coordinate, bottom_y_coordinate,
                         top_x_coordinate, bottom_y_coordinate, width=3, fill=get_color('red'))

        self.create_line(top_x_coordinate, bottom_y_coordinate,
                         top_x_coordinate, top_y_coordinate, width=3, fill=get_color('red'))

        self.update()

    def set_row_column(self, row, column):
        self.number_rows = row
        self.number_columns = column
        self.height_delta = self.canvas_height/self.number_rows
        self.width_delta = self.canvas_width/self.number_columns

    def set_mouse_event_handler(self, button_click_event):
        self.bind("<Button-1>", button_click_event)

    def build_board(self):
        # this works but it's an extra calculation
        # canvas_width = self.winfo_width()
        # canvas_height = self.winfo_height()

        # height_delta = canvas_height/self.number_rows
        # width_delta = canvas_width/self.number_columns
        self.delete("all")

        for index in range(self.number_rows+1):
            # because we end at the max height-1, not max height
            this_y = min(self.canvas_height-1, self.height_delta*index)
            self.create_line(0, this_y, self.canvas_width,
                             this_y, fill=get_color('black'))

        for index in range(self.number_columns+1):
            this_x = min(self.canvas_width-1, self.width_delta*index)
            self.create_line(this_x, 0, this_x,
                             self.canvas_height, fill=get_color('black'))

    # coordinate is the screen coordinate
    # grid refers to the playing board
    def convert_coordinates(self, coordinate_position):
        grid_position = [0,0]
        grid_position[0]=math.floor(coordinate_position[0]/self.width_delta)

        if (abs((grid_position[0]+1)*self.width_delta-coordinate_position[0])<10 or
                abs(grid_position[0]*self.width_delta-coordinate_position[0]) < 10):
            grid_position[0]=-1

        grid_position[1] = math.floor(coordinate_position[1]/self.height_delta)
        if (abs((grid_position[1]+1)*self.height_delta-coordinate_position[1])<10 or
            abs(grid_position[1]*self.height_delta-coordinate_position[1]) < 10):
            grid_position[1] = -1

        return grid_position

    def remove_all_pieces(self):
        for one_piece in self.board_pieces:
            self.delete('square{0}{1}'.format(one_piece[0], one_piece[1]))

        self.board_pieces = []

    def add_piece(self, position, color):

        if position in self.board_pieces:
            self.delete_piece(position)

        self.create_oval(int(position[0]*self.width_delta)+8, int(position[1]*self.height_delta)+8,
                         int((position[0]+1)*self.width_delta)-8, int((position[1]+1)*self.height_delta)-8,
                         fill=color, tag='square{0}{1}'.format(position[0], position[1]))

        self.board_pieces.append(position)

    def add_text(self, position, text):
        if position in self.board_pieces:
            self.delete_piece(position)

        self.create_text(int(position[0]*self.width_delta)+4, int(position[1]*self.height_delta)+8, anchor=tk.W, text=text, fill=get_color('black'), tag='square{0}{1}'.format(position[0], position[1]))

        self.board_pieces.append(position)

    def flip_pieces(self, which_pieces, color):
        
        for one_piece in which_pieces:
            self.delete_piece(one_piece)
            self.add_piece(one_piece, color)

    def delete_piece(self, position):
        self.delete('square{0}{1}'.format(position[0], position[1]))
        self.board_pieces.remove(position)

    def create_palatte(self, start_index):

        for index in range(20):
            position = [(index - math.floor(index/4)*4)*2 + 2, math.floor(index/4)*2+2]
            self.add_piece(position, the_colors[index+start_index].hex)

    def create_buttons_for_palatte(self):

        self.add_piece([1,1], the_colors[1].hex)
        self.add_piece([9, 1], the_colors[1].hex)

    def create_AI_list(self, AI_lables):

        for row, one_AI in enumerate(AI_lables):
            self.add_text([int(math.floor(row/8)), (row % 8)+1], one_AI)

class Control_Panel_Class(tk.Canvas):
   
    def __init__(self, button_click_event, player1_color, player2_color, * args, **kwargs):
        super().__init__(*args, **kwargs)

        self.number_rows = 8
        self.number_columns = 8

        self.the_buttons = []
        self.temp=[]
        #  exit button
        self.make_button(30, 30, 60, 60, 'EXIT',
                         'exit', get_color('firebrick'))

        #   start button
        self.make_button(120, 30, 150, 60, 'START',
                         'start', get_color('lawngreen'))

        #   select player 1 color button
        self.make_button(30, 120, 60, 150, 'Player 1 Color',
                         'player_1_color', player1_color)

        #   select player 2 color button
        self.make_button(120, 120, 150, 150, 'Player 2 Color', 'player_2_color', player2_color)


        self.make_button(30, 210, 60, 240, 'Back 1 Move',
                         'Back_1_Move', 'teal')

        self.make_button(120, 210, 150, 240, 'Forward 1 Move',
                         'Forward_1_Move', 'yellow')

        self.make_button(30, 300, 60, 330, 'AI Player 1',
                         'AI_Player_1', 'pink')

        self.make_button(120, 300, 150, 330, 'AI Player 2',
                         'AI_Player_2', 'DeepPink')

        self.make_button(30, 390, 60, 410, 'Print Moves',
                         'print_moves', 'lavender')

        self.bind("<Button-1>", button_click_event)
        self.update()

    def get_number_of_rows(self):
        return self.number_rows

    def get_number_of_columns(self):
        return self.number_columns

    def set_player_color(self, which_player, color):
        # this_button = self.find_withtag(
        #     'button-player_{0}_color'.format(which_player+1))
        self.itemconfig(
            'button-player_{0}_color'.format(which_player+1), fill=color)

        # self.itemconfigure(self.temp[0], fill='blue')
        self.update()

    def make_button(self, x_top, y_top, x_bottom, y_bottom, button_text, tag, color):
        this_button = button_class(x_top, y_top, x_bottom, y_bottom, tag)
        self.the_buttons.append(this_button)
        x = self.create_rectangle(this_button.x_top, this_button.y_top, this_button.x_bottom,
        this_button.y_bottom, outline = get_color('black'), fill = color, tag = 'button-'+tag)

        self.temp.append(x)
        self.create_text((this_button.x_top + this_button.x_bottom)/2, this_button.y_top-2-10, fill = get_color('black'),
                         font='Times 10', text=button_text, width=150)

    def which_button_pressed(self, x, y):

        for one_button in self.the_buttons:
            if one_button.is_in_button(x, y):
                return one_button.tag

        return ''

    # def exit_button_clicked(self, x, y):
    #     return self.exit_button.is_in_button(x, y)

    # def start_button_clicked(self, x, y):
    #     return self.start_button.is_in_button(x, y)

    # def test_button_clicked(self, x, y):
    #     return self.test_button.is_in_button(x, y)

    # def change_player_1_color_clicked(self, x, y):
    #     return self.select_player_1_color.is_in_button(x, y)

    # def change_player_2_color_clicked(self, x, y):
    #     return self.select_player_2_color.is_in_button(x, y)

class Progress_Class(tk.Canvas):
    
    def __init__(self, button_click_event, * args, **kwargs):
        super().__init__(*args, **kwargs)

        width = kwargs['width']
        height = kwargs['height']
        
        self.whos_turn = self.create_text(width/2, height-20, fill=get_color('black'),
                         font='Times 25', text="Player 1's Turn")

        self.score_player1_lable = self.create_text(
            85, 25, fill=get_color('black'), font='Times 20', text="Player 1")
        self.itemconfigure(self.score_player1_lable, state='hidden')

        self.score_player1 = self.create_text(
            85, 50, fill=get_color('black'), font='Times 20', text="0")
        self.itemconfigure(self.score_player1, state='hidden')

        self.score_player2_lable = self.create_text(
            width-85, 25, fill=get_color('black'), font='Times 20', text="Player 2")

        self.score_player2 = self.create_text(
            width-85, 50, fill=get_color('black'), font='Times 20', text="0")

        self.set_states('hidden')
        self.update()

    def set_states(self, this_state):
        self.itemconfigure(self.score_player2, state=this_state)
        self.itemconfigure(self.score_player2_lable, state=this_state)
        self.itemconfigure(self.score_player1, state=this_state)
        self.itemconfigure(self.score_player1_lable, state=this_state)
        self.itemconfigure(self.whos_turn, state=this_state)

    def clear_objects(self):
        self.delete(tk.ALL)

    def start_game(self):
        self.set_states('normal')
        self.update()

    def set_turn(self, message):

        # the_text = "Player {0}'s turn".format(player.get_player_number()+1)
        self.itemconfigure(self.whos_turn, text=message)

    def set_score(self, score):

        self.itemconfigure(self.score_player1, text=str(score[0]))
        self.itemconfigure(self.score_player2, text=str(score[1]))

    def update_progress(self, player, score, message):
        
        self.set_score(score)
        self.set_turn(message)            

        self.update()

