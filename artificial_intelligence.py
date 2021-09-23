import random

class AI_Class():
    lable = 'Base AI'

    def __init__(self):
        pass

    def get_move(self, the_game):
        valid_moves = the_game.get_valid_moves()
        return(valid_moves[0])

class AI_Random_Move(AI_Class):
    lable = 'Random Move'

    def __init__(self):
        pass

    def get_move(self, the_game):
        valid_moves=the_game.get_valid_moves()

        return(valid_moves[random.randrange(len(valid_moves))])



class AI_Best_Score(AI_Class):
    lable = 'Best Score'
    def __init__():
        pass


class AI_Defense(AI_Class):
    lable = 'Defense'
    def __init__():
        pass

