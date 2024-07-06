import time
from player import RandomComputerPlayer,HumanPlayer,GeniusComputerPlayer

class TicTacToe:
    def __init__(self):
        #we need a 3/3 board
        self.board=[' ' for _ in range(9)]#a single list
        self.current_winner=None #tracking winner

    def print_board(self):
        #for display only, printing a row(three elements an iteration only)
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| '+' | '.join(row)+' |')
            # print('________')
        
    @staticmethod
    def print_board_nums():
        #available number or number corresponding to each box
        number_board=[[str(i) for i in range(j*3+1,(j+1)*3+1)] for j in range(3)] #its just a 3*3 matrix display of 1-9
        for row in number_board:
            print('| '+' | '.join(row)+' |')

    def available_moves(self):
        #return list []
        moves=[]
        for (i,spot) in enumerate(self.board):
            if spot==' ':
                moves.append(i)
        return moves
        #we can do the whole thing in one line like:
        #return [i for i,spot in enumerate(self.board) if spot==' ']
    
    def empty_squares(self):
        return ' ' in self.board #bool

    def num_of_empty_squares(self):
        return self.board.count(' ') 
    
    def make_move(self, square, letter):
        #if valid move, then make the move and return true,
        # i.e assign the letter to the board list with the given pos
        #if invalid move, return false
        if(self.board[square]==' '):
            self.board[square]=letter  
            if self.isWinner(square,letter):
                self.current_winner=letter
            return True
        return False

    def isWinner(self,square,letter):
        #a row, a diagonal or a column
        #1.a row
        row_ind=square//3 #gives us the 1st point of the row
        row=self.board[row_ind*3 : (row_ind+1)*3] #the whole row
        if all([spot== letter for spot in row]):
            return True

        #2.Column
        col_ind=square %3
        column=[self.board[col_ind+i*3] for i in range(3)]
        if all([spot== letter for spot in column]):
            return True
        
        #3. Diagonal
        #[0,4,8] and [2,4,6]
        if square%2==0:
            diagonal1=[self.board[i] for i in [0,4,8]]
            diagonal2=[self.board[i] for i in [2,4,6]]
            if all([spot ==letter for spot in diagonal1]):
                return True
            if all([spot ==letter for spot in diagonal2]):
                return True
       
        return False



def play(game, x_player,o_player, print_game=True):
    #returns the winner/Tie    
    if print_game:
        game.print_board_nums()
    letter='X'
    #Now we iterate while the board/game still has ' '/empty Squares
    while game.empty_squares():
        #getting the move based on the letter 
        if letter=='X':
            square=x_player.get_move(game)
        else:
            square=o_player.get_move(game)

        #making the move
        if(game.make_move(square,letter)):
            if(print_game):
                print(f'{letter} makes a move to square {square+1}')
                game.print_board()
                if game.isWinner(square,letter):
                    return f'\n{letter}_player Won The Match!'

                print('')#Just some spacing in between

            #now to give the other player the move, we change the letter(toggling)
            letter='O' if letter=='X' else 'X'
        time.sleep(0.8)#a small break for each move
    if print_game:
        return 'It\'s a TIE!'
    

if __name__=='__main__':
    x_player=HumanPlayer('X')
    n_player=int(input("Press 2 for 2 players, anything else for 1 player: "))
    if(n_player==2):
        o_player=HumanPlayer('O')
    else:
        difficulty=int(input("Press 1 For EASY MODE , anything else If You Dont Want to win. : "))
        if difficulty==1:
            o_player=RandomComputerPlayer('O')
        else:
            o_player=GeniusComputerPlayer('O')
    
    t=TicTacToe()
    print(play(t,x_player,o_player,print_game=True))