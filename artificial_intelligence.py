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
    
    def get_max_location_value(self):
        return_value = 0

        for one_location in self.location_values:
            if return_value<one_location.value:
                return_value = one_location.value

        return return_value

    def add_location(self, x, y, value):

        for one_location in self.location_values:
            if one_location.x==x and one_location.y==y:
                self.location_values.remove(one_location)
                
        self.location_values.append(Location_Value_Class(x,y,value))

    def get_location_value(self, x, y):
        # default is zero
        for one_location in self.location_values:
            if one_location.x == x and one_location.y == y:
                return one_location.value

        return 0


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

    def get_move(self, the_game):
        valid_moves = the_game.get_valid_moves()

        possible_moves = copy.deepcopy(valid_moves)
        best_value = 0

        for one_move in valid_moves:
            this_value = self.get_location_value(one_move[0], one_move[1])
            if this_value>best_value:
                possible_moves = []
                possible_moves.append(one_move)
                best_value=this_value
            elif this_value==best_value:
                possible_moves.append(one_move)

        return possible_moves[random.randrange(len(possible_moves))]


class AI_Location_Value_With_Defense(AI_Class):
    lable = 'Location Value w/ Defense'

    def __init__(self):
        super().__init__()
        #need to overide
        self.uses_location_value = True


    # there is a bug here that needs to be corrected.  Sometimes gets caught in a loop
    def get_move(self, the_game):

        max_location_value = self.get_max_location_value()

        valid_moves = the_game.get_valid_moves()

        possible_moves = []

        for one_move in valid_moves:

            #this is the intrinsic value of the location without concern of the other players next move
            base_value = self.get_location_value(one_move[0], one_move[1])

            game_copy = copy.deepcopy(the_game)
            game_copy.place_piece(one_move)
            game_copy.set_next_player()

            next_player_moves = game_copy.get_valid_moves()

            other_player_value = 0
            #if the next player can't go with a particular move this is the one we want
            if len(next_player_moves) == 0:
                other_player_value = max_location_value*2

            #now find the value of this move to the other player
            local_max_value = 0
            for one_move_other_player in next_player_moves:
                local_max_value = max(self.get_location_value(
                    one_move_other_player[0], one_move_other_player[0]), local_max_value)
            other_player_value -= local_max_value

            possible_moves.append(Location_Value_Class(
                one_move[0], one_move[1], base_value + other_player_value))

        best_value = 0
        for one_move in possible_moves:
            best_value = max(one_move.value, best_value)

        #remove anything that doesn't have the best value
        for one_move in possible_moves:
            if one_move.value<best_value:
                possible_moves.remove(one_move)

        final_move = possible_moves[random.randrange(len(possible_moves))]    
        return [final_move.x, final_move.y]
