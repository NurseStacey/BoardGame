import random
import copy

class Location_Value_Class():

    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        

class AI_Class():
    lable = 'Base AI'

    def __init__(self):
        
        self.location_values = []
        self.uses_location_value = False

    def is_location_value_based(self):
        return self.uses_location_value

    def get_move(self, the_game):
        #this is the default
        #returns the first valid move it finds

        valid_moves = the_game.get_valid_moves()

        return(valid_moves[0])
    
    def add_location(self, x, y, value):

        self.location_values.append(Location_Value_Class(x,y,value))

class AI_Random_Move(AI_Class):
    lable = 'Random Move'

    def __init__(self):
        super().__init__()

    def get_move(self, the_game):

        valid_moves=the_game.get_valid_moves()

        return(valid_moves[random.randrange(len(valid_moves))])

class AI_Best_Score(AI_Class):
    lable = 'Best Score'
    def __init__(self):
        super().__init__()

    def get_move(self, the_game):

        valid_moves=the_game.get_valid_moves()
        
        possible_moves = []

        game_copy = copy.deepcopy(the_game)
        game_copy.place_piece(valid_moves[0])
        
        best_score = game_copy.calculate_current_player_score()

        possible_moves.append(valid_moves[0])

        for one_move in valid_moves:
            if not(one_move == valid_moves[0]):
                game_copy = copy.deepcopy(the_game)
                game_copy.place_piece(one_move)
                the_game_score = game_copy.calculate_current_player_score()

                if best_score < the_game_score:
                    best_score = the_game_score
                    possible_moves = []
                    possible_moves.append(one_move)
                elif best_score == the_game_score:
                    possible_moves.append(one_move)

        return possible_moves[random.randrange(len(possible_moves))]


class AI_Defense(AI_Class):
    lable = 'Defense'

    def __init__(self):
        super().__init__()

    def get_move(self, the_game):
        
        valid_moves = the_game.get_valid_moves()

        possible_moves = []

        game_copy = copy.deepcopy(the_game)
        game_copy.place_piece(valid_moves[0])
        
        game_copy.set_next_player()
        minimum_moves = len(game_copy.get_valid_moves())

        possible_moves.append(valid_moves[0])

        for one_move in valid_moves:
            if not(one_move == valid_moves[0]):
                game_copy = copy.deepcopy(the_game)
                game_copy.place_piece(one_move)
                game_copy.set_next_player()
                
                number_moves = len(game_copy.get_valid_moves())

                if number_moves < minimum_moves:
                    minimum_moves = number_moves
                    possible_moves = []
                    possible_moves.append(one_move)
                elif number_moves == minimum_moves:
                    possible_moves.append(one_move)

        return possible_moves[random.randrange(len(possible_moves))]

class AI_Location_Value(AI_Class):
    lable = 'Location Value'

    def __init__(self):
        super().__init__()
        #need to overide
        self.uses_location_value = True
