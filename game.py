import copy
from player import Player_Class

#position = [x,y]
class One_Piece_Class():

    def __init__(self, position, color, action):
        # there may be a redundancy between color and action.  Meant to give greater functionality if other games are developed
        self.position = position
        self.color = color
        self.action = action

class One_Board_Class():

    def __init__(self, which_player, this_board):

        self.which_player = which_player  #this is the player who made the move that led to this board
        self.this_board = this_board  #these are all the pieces and their color and the action associate 
                                        #after the move that was made
    def find_piece(self, piece):
        
        for one_piece in self.this_board:
            if one_piece.position == piece.position:
                return (one_piece)
        
        #if the piece isn't here then return -1
        return -1

class Game_Class():
    
    def __init__(self, the_players):

        self.moves = []
        self.pieces = []
        self.game_in_progress = False
        self.number_rows=8
        self.number_columns = 8
        self.the_players = the_players

        self.the_boards = [] 
        self.which_move = 0

    def set_pieces_current_board(self):

        self.pieces = []
        
        for one_piece in self.the_boards[self.which_move].this_board:
            self.pieces.append(copy.deepcopy(one_piece))


    def start_game(self, which):
        self.moves=[]   # reset the moves
        self.the_boards=[]
        self.game_in_progress = True
        self.current_player = which

    def back_forward_move(self, direction):

        if direction == 'go_back':
            self.back_one_move()
        elif direction == 'go_forward':
            self.forward_one_move()
            
    def forward_one_move(self):
        # self.pieces.pop()
        self.which_move += 1

    def back_one_move(self):

        self.which_move -= 1

    def add_board(self):

        this_board = []
        for one_piece in self.pieces:
            this_board.append(copy.deepcopy(one_piece))

        self.the_boards.append(One_Board_Class(self.current_player, this_board))

    def is_game_in_progress(self):
        return self.game_in_progress

    def set_which_player(self, which):
        self.current_player = which

    def get_tile_state(self, position):
        
        for this_piece in self.pieces:
            if position == this_piece.position:
                return this_piece.color

        return -1
    
    def set_number_rows_columns(self, rows, columns):

        self.number_rows = rows
        self.number_columns = columns
        
    def is_tile_opposite_from_current_player(self, position):
        tile_state = self.get_tile_state(position)
        return not(tile_state == -1) and not(tile_state == self.current_player.get_color())

    def is_the_end(self):
        return self.which_move==(len(self.the_boards)-1)

    def is_the_beginning(self):
        return self.which_move==0

    def get_valid_moves(self):
        
        valid_moves = []
        for x_coordinate in range(self.number_columns):
            for y_coordinate in range(self.number_rows):
                if self.is_valid_move([x_coordinate, y_coordinate]):
                    valid_moves.append([x_coordinate, y_coordinate])
                    
        return valid_moves


    def build_surrounding_squares(self, position):

        surrounding_squares = []

        for x in range(max(position[0]-1, 0), min(position[0]+1, self.number_rows-1)+1):
            for y in range(max(position[1]-1, 0), min(position[1]+1, self.number_columns-1)+1):
                # don't include the position in question
                if not(x == position[0] and y == position[1]):
                    surrounding_squares.append([x, y])

        return surrounding_squares

    def build_surrounding_squares_different_color(self, surrounding_squares):
        surrounding_squares_different_color = []
        for one_square in surrounding_squares:
            if self.is_tile_opposite_from_current_player(one_square):
                surrounding_squares_different_color.append(one_square)
        
        return surrounding_squares_different_color

    def is_a_valid_line(self, potential_position, test_position):

        # these will be either +1 or -1 depending on positioning
        x_direction = test_position[0] - potential_position[0]
        y_direction = test_position[1] - potential_position[1]

        next_tile = test_position
        while True:
            next_tile[0] = next_tile[0] + x_direction
            next_tile[1] = next_tile[1] + y_direction

             # first check to see if this tile is still on the board
            if not(next_tile[0] < self.number_rows) or next_tile[0] < 0 or not(next_tile[1] < self.number_rows) or next_tile[1] < 0:
                    break

                # this tile is empty
            if self.get_tile_state(test_position) == -1:
                break
            elif not self.is_tile_opposite_from_current_player(test_position):
                    #this is the piece we're looking for - we're done
                    #we can leave - no need to continue
                return True

        return False

    # this function helps defines the game along with score function
    # when building a new game this needs to be changed
    # much of this will be used when we actually play a piece so we put everying into smaller functions
    def is_valid_move(self, position):


        if position[0]<0 or position[1]<0:
            return False
        #for backgammon, if piece is taken up by another tile it isn't valie
        if not(self.get_tile_state(position)==-1):
            return False

        #next examine surrounding squares

        # 1 - build an array of surrounding square
        surrounding_squares = self.build_surrounding_squares(position)

        # 2 - go through array and find tiles that have a piece with opposite color
        surrounding_squares_different_color = self.build_surrounding_squares_different_color(
            surrounding_squares)

        # 3 - if no potential squares surround of the opposite color than not a valid move
        if len(surrounding_squares_different_color) == 0:
            return False

        # 4 - for each surrounding tile of a different color check to see if there is a line leading to a tile of the same color
        for one_square in surrounding_squares_different_color:
        
            if self.is_a_valid_line(position, one_square):
                return True

        return False

    def new_move(self):
        self.which_move += 1

    def last_move(self):
        self.which_move -= 1

    def add_move(self, position, color, which_pieces_flipped):

        self.moves.append(One_Piece_Class(position, color, 'new_piece'))
        self.pieces.append(One_Piece_Class(position, color, 'new_piece'))

    def get_current_board(self):

        return self.the_boards[self.which_move] 

    def add_piece(self, position, color):
        self.pieces.append(One_Piece_Class(position, color, 'new_piece'))

    def change_piece(self, position, color):
        
        for this_piece in self.pieces:
            if this_piece.position==position:
                this_piece.color=color

    def place_piece(self, position):
        # self.add_move(position, self.which_player_turn)

        pieces_flipped = [] 

        surrounding_squares = self.build_surrounding_squares(position)

        # 2 - go through array and find tiles that have a piece with opposite color
        surrounding_squares_different_color = self.build_surrounding_squares_different_color(
            surrounding_squares)

        for one_square in surrounding_squares_different_color:

            # these will be either +1 or -1 depending on positioning
            x_direction = one_square[0] - position[0]
            y_direction = one_square[1] - position[1]

            next_tile = one_square
            
            while True:
                next_tile[0] = next_tile[0] + x_direction
                next_tile[1] = next_tile[1] + y_direction

                # first check to see if this tile is still on the board
                if not(next_tile[0] < self.number_rows) or next_tile[0] < 0 or not(next_tile[1] < self.number_rows) or next_tile[1] < 0:
                    break

                    # this tile is empty
                if self.get_tile_state(one_square) == -1:
                    break
                elif not self.is_tile_opposite_from_current_player(one_square):
                    #we found an end point
                    #we just go backwards and change the color of each piece
                    next_tile[0] = next_tile[0] - x_direction
                    next_tile[1] = next_tile[1] - y_direction
                    while not(next_tile==position):
                        self.change_piece(next_tile, self.current_player.get_color())
                        pieces_flipped.append(copy.deepcopy(next_tile))
                        next_tile[0] = next_tile[0] - x_direction
                        next_tile[1] = next_tile[1] - y_direction
                    break
        
        self.new_move()

        # need to remove the old boards if they undid moves
        while self.which_move<len(self.the_boards):
            self.the_boards.pop()

        
        
        return pieces_flipped

    def set_next_player(self):

        for which_player in range(len(self.the_players)):
            if self.current_player == self.the_players[which_player]:
                self.current_player = self.the_players[(
                    which_player+1) % len(self.the_players)]
                break

    def set_last_player(self):

        for which_player in range(len(self.the_players)):
            if self.current_player == self.the_players[which_player]:
                self.current_player = self.the_players[(
                    which_player-1) % len(self.the_players)]
                break

    def calculate_score(self):

        score = [0] * len(self.the_players)

        for one_piece in self.pieces:
            for which_player in range(len(self.the_players)):
                if one_piece.color == self.the_players[which_player].get_color():
                    score[which_player] += 1

        return score

    def print_moves(self):

        file1 = open('moves.txt', 'w')

        for one_move in self.moves:
            one_line = '{0} \t {1} \t'.format(
                one_move.position[0], one_move.position[1]) + one_move.color + '\n'
                
            file1.write(one_line)

        file1.close()
