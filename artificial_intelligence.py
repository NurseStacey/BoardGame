import copy
import random
from constants import NUMBER_ROWS, NUMBER_COLUMNS,get_AI_Matrix

def calculate_position_scores(which_AI):
    global PIECES_SCORES
    PIECES_SCORES=[]

    for row in range(NUMBER_ROWS):
        PIECES_SCORES.append([0]*NUMBER_COLUMNS)

    AI_Matrix = get_AI_Matrix(which_AI)
    # return_value[0][0]=10
    # return_value[0][1]=1
    # return_value[0][2]=2
    # return_value[0][3]=3
    # return_value[1][1]=4
    # return_value[1][2]=5
    # return_value[1][3]=6
    # return_value[2][2]=7
    # return_value[2][3]=8
    # return_value[3][3]=9

    for i in range(4):
        for j in range(i,4):
            PIECES_SCORES[i][j]=AI_Matrix[i][j]
            PIECES_SCORES[j][i]=AI_Matrix[i][j]
            PIECES_SCORES[7-i][j]=AI_Matrix[i][j]
            PIECES_SCORES[7-j][i]=AI_Matrix[i][j]
            PIECES_SCORES[j][7-i]=AI_Matrix[i][j]
            PIECES_SCORES[i][7-j]=AI_Matrix[i][j]
            PIECES_SCORES[7-i][7-j]=AI_Matrix[i][j]
            PIECES_SCORES[7-j][7-i]=AI_Matrix[i][j]
            pass

    # for column in range(NUMBER_COLUMNS):
    #     for row in range(NUMBER_ROWS):
    #         pass
    #         return_value[column][row] =(
    #             max(0,(column-int(0.5*NUMBER_COLUMNS))) + 
    #             max(0,((int(.5*NUMBER_COLUMNS)-column)-1)) +
    #             max(0,(row-int(0.5*NUMBER_ROWS))) +
    #             max(0,((int(.5*NUMBER_ROWS)-row)-1))
    #         )
    #         pass

    # return_value[1][1]=-10
    # return_value[0][1]=-10
    # return_value[1][0]=-10

    # return_value[NUMBER_COLUMNS-1][1]=-10
    # return_value[NUMBER_COLUMNS-1][0]=-10
    # return_value[NUMBER_COLUMNS-2][1]=-10

    # return_value[1][NUMBER_ROWS-1]=-10
    # return_value[1][NUMBER_ROWS-2]=-10
    # return_value[0][NUMBER_ROWS-2]=-10

    # return_value[NUMBER_COLUMNS-2][NUMBER_ROWS-2]=-10
    # return_value[NUMBER_COLUMNS-2][NUMBER_ROWS-1]=-10
    # return_value[NUMBER_COLUMNS-1][NUMBER_ROWS-2]=-10               

    #return return_value

PIECES_SCORES=None
pass

class AI_Class():
    def __init__(self,the_game):
        self.the_game=the_game
        self.pieces_scores=[[0]*NUMBER_COLUMNS]*NUMBER_ROWS
        self.number_columns = NUMBER_COLUMNS
        self.number_rows = NUMBER_ROWS

        self.pieces_scores=[]


        for row in range(self.number_rows):
            self.pieces_scores.append([0]*NUMBER_COLUMNS)

    # def calculate_position_scores(self):


    #     for column in range(NUMBER_COLUMNS):
    #         for row in range(NUMBER_ROWS):
    #             pass
    #             self.pieces_scores[column][row] =(
    #                 max(0,(column-int(0.5*NUMBER_COLUMNS))) + 
    #                 max(0,((int(.5*NUMBER_COLUMNS)-column)-1)) +
    #                 max(0,(row-int(0.5*NUMBER_ROWS))) +
    #                 max(0,((int(.5*NUMBER_ROWS)-row)-1))
    #             )
    #             pass

    #     self.pieces_scores[1][1]=0
    #     self.pieces_scores[0][1]=0
    #     self.pieces_scores[1][0]=0

    #     self.pieces_scores[self.number_columns-1][1]=0
    #     self.pieces_scores[self.number_columns-1][0]=0
    #     self.pieces_scores[self.number_columns-2][1]=0

    #     self.pieces_scores[1][self.number_rows-1]=0
    #     self.pieces_scores[1][self.number_rows-2]=0
    #     self.pieces_scores[0][self.number_rows-2]=0

    #     self.pieces_scores[self.number_columns-2][self.number_rows-2]=0
    #     self.pieces_scores[self.number_columns-2][self.number_rows-1]=0
    #     self.pieces_scores[self.number_columns-1][self.number_rows-2]=0                

    #     pass

    def GetPossibleMoves(self):
        #self.calculate_position_scores()

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

        try:
            #self.calculate_position_scores()
            possible_moves = self.the_game.get_valid_moves()
            
            if len(possible_moves)==0:
                return None
            
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
        
        except Exception as e:
            print(e)
            pass

    def value_board(self,the_game):

        return_value = 0
        number_columns = the_game.number_columns
        number_rows = the_game.number_rows
        current_player_color = the_game.current_player.player_color

        for one_piece in the_game.get_alll_pieces():
            player_factor = -2
            score=-1
            if one_piece.color == current_player_color:
                player_factor = 2
                score=1

            score += PIECES_SCORES[one_piece.position[0]][one_piece.position[1]]*player_factor    
           # score += self.pieces_scores[one_piece.position[0]][one_piece.position[1]]*player_factor    
            
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
