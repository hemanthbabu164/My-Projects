import math
import random

class Player:
    def __init__(self,letter):
        #letter x or o
        self.letter=letter

    def get_move(self,game):
        pass

class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        #As a basic tictactoe , computer doesnt concern about the state
        #therefore a rand 'available' spot is taken
        square=random.choice(game.available_moves())
        return square

class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
    
    def get_move(self, game):
        valid_square=False #initialising
        val=None
        while not valid_square:
            square=input(self.letter+'\'s turn. Input move (1-9):')
            #The spot shoulbe valid:
                #1.The input should be int and  in range
                #2.The spot should be available
            try:
                val=int(square)-1
                if val not in game.available_moves():
                    raise ValueError
                valid_square=True
            except ValueError:
                print('Invalid Input Square, Try Again!!.')
        return val

            
class GeniusComputerPlayer(Player):
    #uses MinMax tree or Minimax algorithm
    def __init__(self, letter):
        super().__init__(letter)
    
    def get_move(self,game):
        if len(game.available_moves())==9:#The first move
            square=random.choice(game.available_moves())
        else:
            #get square based off the minimax algorithm
            square=self.minimax(game,self.letter)['position']
        return square
    
    def minimax(self,state,player):
        #recurisve algorithm
        max_player=self.letter #maximise yourself
        other_player= 'O' if player=='X' else 'X'

        #BASE CASES: the leaf nodes are someone winning or a tie
        if state.current_winner== other_player:
            #score is our Heuristic
            #if other_player == max_player means you won, the score=1*(no.of_emptysquares+1)
            #else mean you lost, we dont want that so multiply by -1
            return {'position':None,
                    'score': 1* (state.num_of_empty_squares()+1) if other_player == max_player else -1*(
                        (state.num_of_empty_squares()+1)
                    )                    
                    }
        elif not state.empty_squares():
            return {'position':None,
                    'score':0
                    }
        #initialising the dictionary containing best move
        if player==max_player:
            #we want max score or maximise
            best= {'position':None, 'score':-math.inf} #-math.inf like INT_MIN in cpp
        else:
            #we want to minimise(at higher level we can think it as the opponent making best possible move)
            best= {'position':None, 'score':math.inf} #math.inf like INT_MAX in cpp

        for possible_move in state.available_moves():
            #its like getting all sequences permutations (make a move, recurse to continue after making that move,
                                                            # undo the move, update data structure if necessary) 
            #step 1: Make a move, try that spot
            state.make_move(possible_move,player)
            #step 2: recurse using minimax considering making that move
            sim_score= self.minimax(state,other_player)#passing the play
            #step 3: undo the move
            state.board[possible_move]=' '
            state.current_winner=None
            sim_score['position']=possible_move #the move we made for the score or sim_Score
            #step 4: update the dicts if necessary
            if player==max_player:
                if sim_score['score']> best['score']:
                    best=sim_score
            else:
                if sim_score['score']< best['score']:
                    best=sim_score
        return best