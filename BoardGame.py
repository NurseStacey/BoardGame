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

        if not(grid_position[0] > -1 and grid_position[1] > -1):
            return

        index = grid_position[0]*8+grid_position[1]-1
        AI_list = AI_Class.__subclasses__()
        the_players[which_player].set_AI(AI_list[index]())

        board_canvas.remove_all_pieces()

        if the_players[which_player].this_AI.is_location_value_based():
            location_value_for_AI()
        else:
            board_canvas.set_mouse_event_handler(
                play_board_event_handler)

    def location_value_for_AI():
        board_canvas.set_row_column(
            control_panel.get_number_of_rows()+2, control_panel.get_number_of_columns()+2)
        board_canvas.build_board()
        board_canvas.create_outline(1, 1, control_panel.get_number_of_columns(
        )+1, control_panel.get_number_of_rows()+1)

        #make all squares green
        for this_row in range(control_panel.get_number_of_rows()):
            for this_column in range(control_panel.get_number_of_columns()):
                board_canvas.set_square_color(
                    [this_column+1, this_row+1], get_color('LimeGreen'))

        board_canvas.add_text([1, 0], 'Value', tk.W)
        board_canvas.add_text([2, 0], '0', tk.W)
        board_canvas.set_square_color([3, 0], get_color('yellow'))
        board_canvas.add_text([3, 0], '\n   Set\n Values', tk.W)

        board_canvas.set_square_color([4, 0], get_color('red'))
        board_canvas.add_text([4, 0], '\n   Done', tk.W)

        board_canvas.set_mouse_event_handler(AI_location_valueMouseClicked)
        board_canvas.set_mouse_release_event_handler(
            AI_location_valueMouseReleased)
        board_canvas.set_mouse_motion_handler(None)

        root.bind_all('<Key>', AI_location_value_Keyboard)

    def AI_location_value_MouseMoved(event):

        nonlocal location_value_direction

        x_coordinate = event.x
        y_coordinate = event.y
        grid_position = board_canvas.convert_coordinates(
            [x_coordinate, y_coordinate])

        if (grid_position[0] > 0 and grid_position[0] < (control_panel.get_number_of_columns()+1)) and (grid_position[1] > 0 and grid_position[1] < (control_panel.get_number_of_rows()+1)):
            current_color = board_canvas.get_color(grid_position)

            if location_value_direction == 'selecting' and current_color == get_color('limegreen'):
                board_canvas.set_square_color(grid_position, get_color('red'))
            elif location_value_direction == 'deselecting' and current_color == get_color('red'):
                board_canvas.set_square_color(
                    grid_position, get_color('limegreen'))

        x=1

    def AI_location_valueMouseReleased(event):
        # not sure why but if I set to None that doesn't do it.
        board_canvas.set_mouse_motion_handler(None)

    def AI_location_valueMouseClicked(event):

        nonlocal location_value_direction
        nonlocal which_player

        x_coordinate = event.x
        y_coordinate = event.y
        grid_position = board_canvas.convert_coordinates(
            [x_coordinate, y_coordinate])

        if (grid_position[0] == 4 and grid_position[1] == 0):
            board_canvas.set_mouse_event_handler(None)
            board_canvas.set_mouse_motion_handler(None)
            board_canvas.set_mouse_release_event_handler(None)
            board_canvas.set_row_column(
                control_panel.get_number_of_rows(), control_panel.get_number_of_columns())
            board_canvas.build_board()
            return

        if (grid_position[0] == 3 and grid_position[1] == 0):
            #yellow box pressed
            current_value = board_canvas.get_text([2, 0])
            if current_value == '':
                current_value = '0'

            value = int(current_value)

            for this_row in range(1, control_panel.get_number_of_rows()+1):
                for this_column in range(1, control_panel.get_number_of_columns()+1):
                    if board_canvas.get_color([this_column, this_row]) == get_color('red'):
                        the_players[which_player].this_AI.add_location(
                            this_column-1, this_row-1, value)
                        board_canvas.set_square_color(
                            [this_column, this_row], get_color('limegreen'))
                        this_text = '\n\n    ' + current_value
                        board_canvas.add_text(
                            [this_column, this_row], this_text, tk.W)

            board_canvas.add_text([2, 0], '0', tk.W)

        if (grid_position[0] > 0 and grid_position[0] < (control_panel.get_number_of_columns()+1)) and (grid_position[1] > 0 and grid_position[1] < (control_panel.get_number_of_rows()+1)):
            current_color = board_canvas.get_color(grid_position)
            if current_color == get_color('limegreen'):
                location_value_direction = 'selecting'
                board_canvas.set_square_color(grid_position, get_color('red'))
            elif current_color == get_color('red'):
                location_value_direction = 'deselecting'
                board_canvas.set_square_color(
                    grid_position, get_color('limegreen'))

        board_canvas.set_mouse_motion_handler(AI_location_value_MouseMoved)

    def AI_location_value_Keyboard(event):

        this_key = event.char

        if event.keycode == BACKSPACE:
            current_value = board_canvas.get_text([2, 0])
            new_value = current_value[:max(0, len(current_value)-1)]
            board_canvas.add_text([2, 0], new_value, tk.W)
        elif this_key.isnumeric():
            current_value = board_canvas.get_text([2, 0])
            if current_value == '0':
                current_value = ''

            new_value = current_value + this_key
            board_canvas.add_text([2, 0], new_value, tk.W)

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
            if grid_position[0] == 1 and start_index > 19:
                start_index -= 20
                board_canvas.create_palatte(start_index)
            if grid_position[0] == 9 and start_index < (len(the_colors)-20):
                start_index += 20
                board_canvas.create_palatte(start_index)

        # need to convert to an index value
        # the reverse of making a coordinate
        index = ((grid_position[1] - 2)/2)*4
        index += (grid_position[0]-2)/2

        if index.is_integer():
            if index < 20 and index >= 0:
                the_players[which_player].set_player_color(
                    the_colors[int(index)+start_index].hex)
                control_panel.set_player_color(
                    which_player, the_players[which_player].get_color())
                board_canvas.remove_all_pieces()
                board_canvas.set_mouse_event_handler(
                    play_board_event_handler)

    which_button_pressed = control_panel.which_button_pressed(
        x_coordinate, y_coordinate)

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

    location_value_direction = 'selecting'

    which_player = 0
    start_index = 0
    # if control_panel.change_player_1_color_clicked(x_coordinate, y_coordinate):
    if which_button_pressed == 'player_1_color':

        if not(the_game == None):
            if the_game.is_game_in_progress():
                return

        which_player = 0
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

def play_board_event_handler(event):
    
    try:
        # this needs to be fixed.  Just isn't clean
        if the_game.is_game_in_progress():
            x_coordinate = event.x
            y_coordinate = event.y
            grid_position = board_canvas.convert_coordinates(
                [x_coordinate, y_coordinate])

            if the_game.is_valid_move(grid_position):
                spot_chosen(grid_position)
                
                evaluate_for_more_moves()

                while not(the_game.current_player.this_AI==None):
                    time.sleep(.5)
                    if evaluate_for_more_moves():
                        spot_chosen(the_game.current_player.this_AI.get_move(the_game))
                        
                    while evaluate_for_more_moves():
                        time.sleep(1)
                        spot_chosen(the_game.current_player.this_AI.get_move(the_game))

    except AttributeError as error:
        pass

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

    board_canvas.set_mouse_release_event_handler(play_board_event_handler)
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

board_canvas = Board_Class(root, width=500,
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
