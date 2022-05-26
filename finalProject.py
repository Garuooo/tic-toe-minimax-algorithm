from cgitb import text
import math
from operator import le
import time
import random
from tkinter import *
from tkinter import messagebox
from prompt_toolkit import print_formatted_text

global x_player,t


class Player():
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass

#plays based on minimax algorithms 
class SmartComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
    ## where to play
    def get_move(self, game):
        if len(game.available_moves()) == 9:
            #square is where the letter will be placed
            square = random.choice(game.available_moves())
            print("random")
        else:
            #square is where the letter will be placed
            square = self.minimax(game, self.letter)['position']
        return square
    ## Use minimax algorithm to know when to play
    def minimax(self, state, player):
        max_player = self.letter  # yourself
        other_player = 'O' if player == 'X' else 'X'

        # first we want to check if the previous move is a winner
        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (
                        state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}  # each score should maximize
        else:
            best = {'position': None, 'score': math.inf}  # each score should minimize
        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player)  # simulate a game after making that move

            # undo move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move  # this represents the move optimal next move

            if player == max_player:  # X is max player
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best


class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            #Where the letter is being played
            square = input(self.letter + '\'s turn. Input move (0-9): ')
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.')
        return val


clicked = True
count = 0
class TicTacToe:
    def __init__(self):
        # the board on which we are playing
        self.board = self.make_board()
        # who is the winner
        self.current_winner = None
        global root
        root = self.createTableTkinter(self)
        # X starts so true

    def b_click(self,b,square):
        global count,clicked
        if b["text"] == " " and clicked == True:
            clicked = False
            count += 1
            b["text"] = "X"
            self.make_move(square,"X")

        elif b["text"] == " " and clicked == False:
            b["text"] = "O"
            clicked = True
            count += 1
            self.make_move(square,"O")
        else:
            messagebox.showerror("Tic Tac Toe", "Hey! That box has already been selected\nPick Another Box..." )

        return
    
    @staticmethod
    def createTableTkinter(self):
        # Build our buttons
        root = Tk()
        root.title('Tic-Tac-Toe')
        global b1,b2,b3,b4,b5,b6,b7,b8,b9 
        b1 = Button(root,text=' ' , font=("Helvetica", 20), height=3, width=6, bg="SystemButtonFace", command=lambda: self.b_click(b1,0))
        b2 = Button(root,text=' ' , font=("Helvetica", 20), height=3, width=6, bg="SystemButtonFace", command=lambda: self.b_click(b2,1))
        b3 = Button(root,text=' ' , font=("Helvetica", 20), height=3, width=6, bg="SystemButtonFace", command=lambda: self.b_click(b3,2))

        b4 = Button(root,text=' ' , font=("Helvetica", 20), height=3, width=6, bg="SystemButtonFace", command=lambda: self.b_click(b4,3))
        b5 = Button(root,text=' ' , font=("Helvetica", 20), height=3, width=6, bg="SystemButtonFace", command=lambda: self.b_click(b5,4))
        b6 = Button(root,text=' ' , font=("Helvetica", 20), height=3, width=6, bg="SystemButtonFace", command=lambda: self.b_click(b6,5))

        b7 = Button(root, text=' ', font=("Helvetica", 20), height=3, width=6, bg="SystemButtonFace", command=lambda: self.b_click(b7,6))
        b8 = Button(root,text=' ' , font=("Helvetica", 20), height=3, width=6, bg="SystemButtonFace", command=lambda: self.b_click(b8,7))
        b9 = Button(root,text=' ' , font=("Helvetica", 20), height=3, width=6, bg="SystemButtonFace", command=lambda: self.b_click(b9,8))
        b10 = Button(root,text='AI Turn' , font=("Helvetica", 20), height=3, width=6, bg="SystemButtonFace", command=lambda : robotMove(self))

        # Grid our buttons to the screen
        b1.grid(row=0, column=0)
        b2.grid(row=0, column=1)
        b3.grid(row=0, column=2)

        b4.grid(row=1, column=0)
        b5.grid(row=1, column=1)
        b6.grid(row=1, column=2)

        b7.grid(row=2, column=0)
        b8.grid(row=2, column=1)
        b9.grid(row=2, column=2)
        b10.grid(row=3)

        root.mainloop()
        return root
    
    @staticmethod
    def robotGuiMove (square):
        if(square == 0):
            return b1
        elif(square==1):
            return b2
        elif(square==2):
            return b3
        elif(square==3):
            return b4
        elif(square==4):
            return b5
        elif(square==5):
            return b6
        elif(square==6):
            return b7
        elif(square==7):
            return b8
        elif(square==8):
            return b9

    # Creating the board
    @staticmethod
    def make_board():
        #create empty 9 places = the board2
        return [' ' for _ in range(9)]

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
                self.checkButtonWinner()

            return True
        return False

    def checkButtonWinner(self):
        if b1["text"] == "X" and b2["text"] == "X" and b3["text"]  == "X":
            b1.config(bg="red")
            b2.config(bg="red")
            b3.config(bg="red")
            self.current_winner = "X"
            messagebox.showinfo("Tic Tac Toe", "CONGRATULATIONS!  X Wins!!")
            disable_all_buttons()
        elif b4["text"] == "X" and b5["text"] == "X" and b6["text"]  == "X":
            b4.config(bg="red")
            b5.config(bg="red")
            b6.config(bg="red")
            self.current_winner = "X"
            messagebox.showinfo("Tic Tac Toe", "CONGRATULATIONS!  X Wins!!")
            disable_all_buttons()

        elif b7["text"] == "X" and b8["text"] == "X" and b9["text"]  == "X":
            b7.config(bg="red")
            b8.config(bg="red")
            b9.config(bg="red")
            self.current_winner = "X"
            messagebox.showinfo("Tic Tac Toe", "CONGRATULATIONS!  X Wins!!")
            disable_all_buttons()

        elif b1["text"] == "X" and b4["text"] == "X" and b7["text"]  == "X":
            b1.config(bg="red")
            b4.config(bg="red")
            b7.config(bg="red")
            self.current_winner = "X"
            messagebox.showinfo("Tic Tac Toe", "CONGRATULATIONS!  X Wins!!")
            disable_all_buttons()

        elif b2["text"] == "X" and b5["text"] == "X" and b8["text"]  == "X":
            b2.config(bg="red")
            b5.config(bg="red")
            b8.config(bg="red")
            self.current_winner = "X"
            messagebox.showinfo("Tic Tac Toe", "CONGRATULATIONS!  X Wins!!")
            disable_all_buttons()

        elif b3["text"] == "X" and b6["text"] == "X" and b9["text"]  == "X":
            b3.config(bg="red")
            b6.config(bg="red")
            b9.config(bg="red")
            self.current_winner = "X"
            messagebox.showinfo("Tic Tac Toe", "CONGRATULATIONS!  X Wins!!")
            disable_all_buttons()

        elif b1["text"] == "X" and b5["text"] == "X" and b9["text"]  == "X":
            b1.config(bg="red")
            b5.config(bg="red")
            b9.config(bg="red")
            self.current_winner = "X"
            messagebox.showinfo("Tic Tac Toe", "CONGRATULATIONS!  X Wins!!")
            disable_all_buttons()

        elif b3["text"] == "X" and b5["text"] == "X" and b7["text"]  == "X":
            b3.config(bg="red")
            b5.config(bg="red")
            b7.config(bg="red")
            self.current_winner = "X"
            messagebox.showinfo("Tic Tac Toe", "CONGRATULATIONS!  X Wins!!")
            disable_all_buttons()

        #### CHECK FOR O's Win
        elif b1["text"] == "O" and b2["text"] == "O" and b3["text"]  == "O":
            b1.config(bg="red")
            b2.config(bg="red")
            b3.config(bg="red")
            self.current_winner = "O"
            messagebox.showinfo("Tic Tac Toe", "CONGRATULATIONS!  O Wins!!")
            disable_all_buttons()
        elif b4["text"] == "O" and b5["text"] == "O" and b6["text"]  == "O":
            b4.config(bg="red")
            b5.config(bg="red")
            b6.config(bg="red")
            self.current_winner = "O"
            messagebox.showinfo("Tic Tac Toe", "CONGRATULATIONS!  O Wins!!")
            disable_all_buttons()

        elif b7["text"] == "O" and b8["text"] == "O" and b9["text"]  == "O":
            b7.config(bg="red")
            b8.config(bg="red")
            b9.config(bg="red")
            self.current_winner = "O"
            messagebox.showinfo("Tic Tac Toe", "CONGRATULATIONS!  O Wins!!")
            disable_all_buttons()

        elif b1["text"] == "O" and b4["text"] == "O" and b7["text"]  == "O":
            b1.config(bg="red")
            b4.config(bg="red")
            b7.config(bg="red")
            self.current_winner = "O"
            messagebox.showinfo("Tic Tac Toe", "CONGRATULATIONS!  O Wins!!")
            disable_all_buttons()

        elif b2["text"] == "O" and b5["text"] == "O" and b8["text"]  == "O":
            b2.config(bg="red")
            b5.config(bg="red")
            b8.config(bg="red")
            self.current_winner = "O"
            messagebox.showinfo("Tic Tac Toe", "CONGRATULATIONS!  O Wins!!")
            disable_all_buttons()

        elif b3["text"] == "O" and b6["text"] == "O" and b9["text"]  == "O":
            b3.config(bg="red")
            b6.config(bg="red")
            b9.config(bg="red")
            self.current_winner = "O"
            messagebox.showinfo("Tic Tac Toe", "CONGRATULATIONS!  O Wins!!")
            disable_all_buttons()

        elif b1["text"] == "O" and b5["text"] == "O" and b9["text"]  == "O":
            b1.config(bg="red")
            b5.config(bg="red")
            b9.config(bg="red")
            self.current_winner = "O"
            messagebox.showinfo("Tic Tac Toe", "CONGRATULATIONS!  O Wins!!")
            disable_all_buttons()

        elif b3["text"] == "O" and b5["text"] == "O" and b7["text"]  == "O":
            b3.config(bg="red")
            b5.config(bg="red")
            b7.config(bg="red")
            self.current_winner = "O"
            messagebox.showinfo("Tic Tac Toe", "CONGRATULATIONS!  O Wins!!")
            disable_all_buttons()

        # Check if tie
        if count == 9 and self.current_winner == None:
            messagebox.showinfo("Tic Tac Toe", "It's A Tie!\n No One Wins!")
            disable_all_buttons()
   
    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def available_moves(self):
        return [i for i, x in enumerate(self.board) if x == " "]

    def winner(self, square, letter):
        # check the row
        row_ind = math.floor(square / 3)
        row = self.board[row_ind*3:(row_ind+1)*3]
        # print('row', row)
        if all([s == letter for s in row]):
            return True
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        # print('col', column)
        if all([s == letter for s in column]):
            return True
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            # print('diag1', diagonal1)
            if all([s == letter for s in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            # print('diag2', diagonal2)
            if all([s == letter for s in diagonal2]):
                return True
        return False


# start the game
def robotMove(game):
    game.checkButtonWinner()
    x_player=SmartComputerPlayer("X")
    square = x_player.get_move(game)
    button = game.robotGuiMove(square)
    game.b_click(button,square)

def disable_all_buttons():
	b1.config(state=DISABLED)
	b2.config(state=DISABLED)
	b3.config(state=DISABLED)
	b4.config(state=DISABLED)
	b5.config(state=DISABLED)
	b6.config(state=DISABLED)
	b7.config(state=DISABLED)
	b8.config(state=DISABLED)
	b9.config(state=DISABLED)

if __name__ == '__main__':
    print_formatted_text(__name__)
    t = TicTacToe()





