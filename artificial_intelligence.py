import copy
import random

class AI_Class():
    def __init__(self,the_game):
        self.the_game=the_game
        self.pieces_scores=[[0]*the_game.number_columns]*the_game.number_rows
        self.number_columns = self.the_game.number_columns
        self.number_rows = self.the_game.number_rows

        self.pieces_scores=[]


        for row in range(self.number_rows):
            self.pieces_scores.append([0]*self.number_columns)

    def calculate_position_scores(self):


        for column in range(self.number_columns):
            for row in range(self.number_rows):
                pass
                self.pieces_scores[column][row] =(
                    max(0,(column-int(0.5*self.number_columns))) + 
                    max(0,((int(.5*self.number_columns)-column)-1)) +
                    max(0,(row-int(0.5*self.number_rows))) +
                    max(0,((int(.5*self.number_rows)-row)-1))
                )
                pass

        self.pieces_scores[1][1]=0
        self.pieces_scores[0][1]=0
        self.pieces_scores[1][0]=0

        self.pieces_scores[self.number_columns-1][1]=0
        self.pieces_scores[self.number_columns-1][0]=0
        self.pieces_scores[self.number_columns-2][1]=0

        self.pieces_scores[1][self.number_rows-1]=0
        self.pieces_scores[1][self.number_rows-2]=0
        self.pieces_scores[0][self.number_rows-2]=0

        self.pieces_scores[self.number_columns-2][self.number_rows-2]=0
        self.pieces_scores[self.number_columns-2][self.number_rows-1]=0
        self.pieces_scores[self.number_columns-1][self.number_rows-2]=0                


    def GetPossibleMoves(self):
        self.calculate_position_scores()

        possible_moves = self.the_game.get_valid_moves()
        
        return_list=[]

        best_score = -100000000
        best_moves=[]
        for one_move in possible_moves:
            game_copy = copy.deepcopy(self.the_game)

            which_pieces_flipped = game_copy.place_piece(one_move)
            game_copy.add_move(one_move, game_copy.current_player.get_color(), which_pieces_flipped)
            this_move_score = self.value_board(game_copy)
            if this_move_score==best_score:
                best_moves.append(one_move)
            elif this_move_score>best_score:
                best_moves=[one_move]

            return_list.append({
                'position':one_move,
                'score':this_move_score
            })

        return return_list
                
    
    def GetMove(self):
        self.calculate_position_scores()
        possible_moves = self.the_game.get_valid_moves()
        
        best_score = -100000000
        best_moves=[]
        for one_move in possible_moves:
            game_copy = copy.deepcopy(self.the_game)

            which_pieces_flipped = game_copy.place_piece(one_move)
            game_copy.add_move(one_move, game_copy.current_player.get_color(), which_pieces_flipped)
            this_move_score = self.value_board(game_copy)
            if this_move_score==best_score:
                best_moves.append(one_move)
            elif this_move_score>best_score:
                best_moves=[one_move]
                best_score=this_move_score

        if len(best_moves)==1:
            return best_moves[0]
        else:
            return best_moves[random.randint(0,len(best_moves)-1)] 

    def value_board(self,the_game):

        return_value = 0
        number_columns = the_game.number_columns
        number_rows = the_game.number_rows
        current_player_coler = the_game.current_player.player_color_hex

        for one_piece in the_game.get_alll_pieces():
            player_factor = -2
            score=-1
            if one_piece.color == current_player_coler:
                player_factor = 2
                score=1

            score += self.pieces_scores[one_piece.position[0]][one_piece.position[1]]*player_factor    
            
            return_value += score

        return return_value
    
class AI_Random_Move(AI_Class):

    def __init__():
        pass


class AI_Best_Score(AI_Class):

    def __init__():
        pass


class AI_Defense(AI_Class):

    def __init__():
        pass
