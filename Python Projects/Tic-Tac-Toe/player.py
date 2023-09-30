import math
import random

class Player:
    def __init__(self,letter):
        #x or o
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

            
