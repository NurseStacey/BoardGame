import tkinter as tk
from my_canvases import Board_Class, Control_Panel_Class, Progress_Class
from game import Game_Class
from tkinter import messagebox
from constants import *
from player import Player_Class
from artificial_intelligence import *
import time

def control_panel_event_handler(event):
    x_coordinate = event.x
    y_coordinate = event.y

    def choose_AI_for_player():
        board_canvas.set_row_column(11, 3)
        board_canvas.build_board()
        board_canvas.set_mouse_event_handler(AI_chooser_event_handler)

        AI_list = AI_Class.__subclasses__()
        AI_labels = []

        for one_AI in AI_list:
            AI_labels.append(one_AI.lable)

        board_canvas.create_AI_list(AI_labels)

    def AI_chooser_event_handler(event):
        nonlocal which_player

        x_coordinate = event.x
        y_coordinate = event.y
        grid_position = board_canvas.convert_coordinates(
            [x_coordinate, y_coordinate])

        if not(grid_position[0]>-1 and grid_position[1]>-1):
            return

        index = grid_position[0]*8+grid_position[1]-1
        AI_list = AI_Class.__subclasses__()
        the_players[which_player].set_AI(AI_list[index]())

        board_canvas.remove_all_pieces()
        board_canvas.set_mouse_event_handler(
            play_board_event_handler)

    def choose_color_for_player():
        board_canvas.set_row_column(11, 11)
        board_canvas.build_board()
        board_canvas.set_mouse_event_handler(color_pallette_event_handler)
        board_canvas.create_palatte(0)
        board_canvas.create_buttons_for_palatte()

    def color_pallette_event_handler(event):
        nonlocal start_index, which_player

        x_coordinate = event.x
        y_coordinate = event.y
        grid_position = board_canvas.convert_coordinates(
            [x_coordinate, y_coordinate])
        
        # are they scrolling forward or back?
        if grid_position[1] == 1:
            if grid_position[0] == 1 and start_index>19:
                start_index -= 20
                board_canvas.create_palatte(start_index)
            if grid_position[0] == 9 and start_index<(len(the_colors)-20):
                start_index += 20              
                board_canvas.create_palatte(start_index)

        # need to convert to an index value
        # the reverse of making a coordinate
        index = ((grid_position[1] - 2)/2)*4
        index += (grid_position[0]-2)/2

        if index.is_integer():
            if index<20 and index>=0:
                the_players[which_player].set_player_color(
                    the_colors[int(index)+start_index].hex)
                control_panel.set_player_color(
                    which_player, the_players[which_player].get_color())
                board_canvas.remove_all_pieces()
                board_canvas.set_mouse_event_handler(
                    play_board_event_handler)

    which_button_pressed = control_panel.which_button_pressed(x_coordinate, y_coordinate)


    # if control_panel.exit_button_clicked(x_coordinate, y_coordinate):
    if which_button_pressed == 'exit':
        root.destroy()

    if which_button_pressed == 'Back_1_Move':
        step_back_forward('go_back')

    if which_button_pressed == 'Forward_1_Move':
        step_back_forward('go_forward')

    if which_button_pressed == 'start':
        start_game()
        
        
        initialize_game_board()

        if not(the_players[0].this_AI == None):
            time.sleep(.5)
            spot_chosen(the_players[0].this_AI.get_move(the_game))
            update_prorgress_bar("Player {0}'s turn".format(
                the_game.current_player.get_player_number()+1))
                
        return

    # if control_panel.test_button_clicked(x_coordinate, y_coordinate):
    # if which_button_pressed == 'player_1_color':
    #     board_canvas.delete_piece([3, 3])
    #     x=1

    which_player = 0
    start_index = 0
    # if control_panel.change_player_1_color_clicked(x_coordinate, y_coordinate):
    if which_button_pressed == 'player_1_color':

        if not(the_game == None):
            if the_game.is_game_in_progress():
                return

        which_player=0
        choose_color_for_player()

   # if control_panel.change_player_2_color_clicked(x_coordinate, y_coordinate):
    if which_button_pressed == 'player_2_color':
        if not(the_game == None):
            if the_game.is_game_in_progress():
                return

        which_player = 1
        choose_color_for_player()

    if which_button_pressed == 'AI_Player_1':
        if not(the_game == None):
            if the_game.is_game_in_progress():
                return
        
        which_player = 0
        choose_AI_for_player()

    if which_button_pressed == 'AI_Player_2':
        if not(the_game == None):
            if the_game.is_game_in_progress():
                return

        which_player = 1
        choose_AI_for_player()


    if which_button_pressed == 'print_moves':
        the_game.print_moves()

def step_back_forward(direction):
    # basically the same for each direction

    if direction == 'go_back' and the_game.is_the_beginning():
        return

    if direction == 'go_forward' and the_game.is_the_end():
        return

    current_board = the_game.get_current_board()
    the_game.back_forward_move(direction)

    new_board = the_game.get_current_board()
    the_game.set_which_player(current_board.which_player)
    # if direction == 'go_back':
    #     the_game.set_which_player(current_board.which_player)
    # elif direction == 'go_forward':
    #     the_game.set_which_player(new_board.which_player)

    #the_game.set_next_player()

    # while(the_game.current_player.is_AI()):
    #     time.sleep(.5)

    #     the_game.back_forward_move(direction)

    #     new_board = the_game.get_current_board()

    #     if direction == 'go_back':
    #         the_game.set_which_player(current_board.which_player)
    #     elif direction == 'go_forward':
    #         the_game.set_which_player(new_board.which_player)

    the_game.set_pieces_current_board()

    pieces_to_remove = []
    pieces_to_flip = []
    pieces_to_add = []  # for othello this is always empty
    # now we compare the current_board with prior_board


    for one_piece in current_board.this_board:
        new_piece = new_board.find_piece(one_piece)
        if new_piece == -1:  # need to remove this piece
            pieces_to_remove.append(one_piece)
        elif not(new_piece.color == one_piece.color):
            pieces_to_flip.append(new_piece)

    for one_piece in new_board.this_board:
        same_piece = current_board.find_piece(one_piece)
        if same_piece == -1:
            pieces_to_add.append(one_piece)
    # now take care of canvas
    for one_piece in pieces_to_remove:
        board_canvas.delete_piece(one_piece.position)
    for one_piece in pieces_to_add:
        board_canvas.add_piece(one_piece.position, one_piece.color)
    for one_piece in pieces_to_flip:
        board_canvas.add_piece(one_piece.position, one_piece.color)

    update_prorgress_bar("Player {0}'s turn".format(
        the_game.current_player.get_player_number()+1))

# def go_forward_one_move():



#     current_board = the_game.get_current_board()
#     the_game.forward_one_move()
#     new_board = the_game.get_current_board()
#     the_game.set_which_player(new_board.which_player)
#     the_game.set_next_player()
#     the_game.set_pieces_current_board()
#     pieces_to_remove = []
#     pieces_to_flip = []
#     pieces_to_add = []  # for othello this is always empty
#     # now we compare the current_board with prior_board
#     for one_piece in current_board.this_board:
#         new_piece = new_board.find_piece(one_piece)
#         if new_piece == -1:  # need to remove this piece
#             pieces_to_remove.append(one_piece)
#         elif not(new_piece.color == one_piece.color):
#             pieces_to_flip.append(new_piece)
#     for one_piece in new_board.this_board:
#         same_piece = current_board.find_piece(one_piece)
#         if same_piece == -1:
#             pieces_to_add.append(one_piece)
#     # now take care of canvas
#     for one_piece in pieces_to_remove:
#         board_canvas.delete_piece(one_piece.position)
#     for one_piece in pieces_to_add:
#         board_canvas.add_piece(one_piece.position, one_piece.color)
#     for one_piece in pieces_to_flip:
#         board_canvas.add_piece(one_piece.position, one_piece.color)

#     update_prorgress_bar("Player {0}'s turn".format(
#         the_game.current_player.get_player_number()+1))

# def go_back_one_move():


#     current_board = the_game.get_current_board()
#     the_game.back_one_move()
#     new_board = the_game.get_current_board()
#     the_game.set_which_player(current_board.which_player)
#     the_game.set_pieces_current_board()
#     pieces_to_remove = []
#     pieces_to_flip = []
#     pieces_to_add = [] #for othello this is always empty
#     # now we compare the current_board with prior_board

#     for one_piece in current_board.this_board:
#         new_piece = new_board.find_piece(one_piece)
#         if  new_piece == -1:  # need to remove this piece
#             pieces_to_remove.append(one_piece)
#         elif not(new_piece.color == one_piece.color):
#             pieces_to_flip.append(new_piece)

#     for one_piece in new_board.this_board:
#         same_piece = current_board.find_piece(one_piece)
#         if same_piece == -1:
#             pieces_to_add.append(one_piece)
#     # now take care of canvas
#     for one_piece in pieces_to_remove:
#         board_canvas.delete_piece(one_piece.position)
#     for one_piece in pieces_to_add:
#         board_canvas.add_piece(one_piece.position, one_piece.color)
#     for one_piece in pieces_to_flip:
#         board_canvas.add_piece(one_piece.position, one_piece.color)

#     update_prorgress_bar("Player {0}'s turn".format(the_game.current_player.get_player_number()+1))


def play_board_event_handler(event):
    
    if the_game.is_game_in_progress():
        x_coordinate = event.x
        y_coordinate = event.y
        grid_position = board_canvas.convert_coordinates(
            [x_coordinate, y_coordinate])

        if the_game.is_valid_move(grid_position):
            spot_chosen(grid_position)
            # which_pieces_flipped = the_game.place_piece(grid_position)

            # #  update the board
            # # this is not the game, just represents the game visually

            # place_piece(
            #     grid_position, the_game.current_player.get_color(), which_pieces_flipped)
            # board_canvas.flip_pieces(
            #     which_pieces_flipped,  the_game.current_player.get_color())
            # the_game.add_board()
            
            # board_canvas.update()

            # #now get the game ready for the next player
            # the_game.set_next_player()

            # can the next player go
            evaluate_for_more_moves()

            if not(the_game.current_player.this_AI==None):
                time.sleep(.5)
                spot_chosen(the_game.current_player.this_AI.get_move(the_game))
                while evaluate_for_more_moves():
                    time.sleep(1)
                    spot_chosen(the_game.current_player.this_AI.get_move(the_game))

def evaluate_for_more_moves():

    return_value = False  # this is if there is an AI

    if len(the_game.get_valid_moves()) == 0:
        this_player = the_game.current_player
        the_game.set_next_player()
        if len(the_game.get_valid_moves()) == 0:
                    # in a two player game no one can go.
                    # Will need to make additional changes here for more than two player
            the_game.game_over()
            update_prorgress_bar('No Moves Left')
        else:
            update_prorgress_bar('No Moves for Player {0}'.format(
                this_player.get_player_number()+1))
            return_value =  True
    else:
        update_prorgress_bar("Player {0}'s turn".format(
            the_game.current_player.get_player_number()+1))

    return return_value

def spot_chosen(grid_position):
    
    which_pieces_flipped = the_game.place_piece(grid_position)

            #  update the board
            # this is not the game, just represents the game visually

    place_piece(
        grid_position, the_game.current_player.get_color(), which_pieces_flipped)
    board_canvas.flip_pieces(
        which_pieces_flipped,  the_game.current_player.get_color())
    the_game.add_board()
            
    board_canvas.update()

            #now get the game ready for the next player
    the_game.set_next_player()

def update_prorgress_bar(message):
    current_score = the_game.calculate_score()
    game_progress.update_progress(the_game.current_player, current_score, message)


def place_piece(position, color, which_pieces_flipped):
    board_canvas.add_piece(position, color)
    the_game.add_move(position, color, which_pieces_flipped)
    

def initialize_game_board():
    board_canvas.build_board()

    # these are the initial pieces
    # perhaps they should live in the_game and get pulled forward?
    place_piece([3, 3], the_players[0].get_color(), [])
    place_piece([3, 4], the_players[1].get_color(), [])
    place_piece([4, 4], the_players[0].get_color(), [])
    place_piece([4, 3], the_players[1].get_color(), [])

    the_game.add_board()

def start_game():
    global the_game

    game_progress.start_game()
    the_game = Game_Class(the_players)
    the_game.start_game(the_players[0])
    set_rows_columns(8,8)


def set_rows_columns(rows, columns):
    the_game.set_number_rows_columns(rows, columns)
    board_canvas.set_row_column(rows, columns)

#   Make the initial GUI
root = tk.Tk()
root.geometry("750x600")
root.title('Board Game')

# these are the players
the_players = []
the_players.append(Player_Class(get_color('white'), 0))
the_players.append(Player_Class(get_color('black'), 1))

#   Make the different canvases
control_panel = Control_Panel_Class(control_panel_event_handler, the_players[0].get_color(), the_players[1].get_color(),
                                    root, width=250, height=600, background=get_color('LightGoldenrodYellow'), highlightthickness=0)
control_panel.pack(side=tk.LEFT)

board_canvas = Board_Class(play_board_event_handler, root, width=500,
                           height=500, background=get_color('Light Green'), highlightthickness=0)
board_canvas.pack(side=tk.TOP)

game_progress = Progress_Class(
    root, width=500, height=100, background=get_color('MintCream'), highlightthickness=0)
game_progress.pack(side=tk.BOTTOM)



# this is where the game is played
# It is not the board
# the board is mearly a visual representation of the game
the_game = None

root.mainloop()
