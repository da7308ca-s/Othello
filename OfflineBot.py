#!/usr/bin/env python

from subprocess import Popen, PIPE
import numpy as np

process = Popen("./othello", stdout=PIPE, stderr=PIPE, stdin=PIPE)
my_color = "w"
pos = Position()

def read():
        return process.stdout.readline().decode()

def write(msg):
        process.stdin.write(str.encode(msg + "\n"))
        process.stdin.flush()
        print(msg)

def text_to_coord(text):
        s = "abcdefgh"
        return (s.index(text[0]), int(text[1]) - 1)

class Position:
        def __init__(self):
                self.board = np.zeros(8,8)
                self.board[3][3] = -1
                self.board[4][4] = -1
                self.board[3][4] = 1
                self.board[4][3] = 1

        def print_board(self):
                print(self.board)

        def place_piece(self,move,player):
                move = text_to_coord(move)
                self.board[move[0]][move[1]] = 1 if player == "d" else -1
                self.print_board()

def main(msg):
        print(msg)
        if str(msg) == "hi! I am your othello server.\n":
                write('da7308ca-s')
                print(read())
                print(read())
                main(read())
        elif msg == "choose colour, 'd' for dark, 'w' for white.\n":
                write(my_color)
                print(read())
                main(read())
        elif msg == "The game is finished\n":
                print(read())
                print(read())
                print(read())
        elif msg == "my move\n":
                move = read()
                print(move)
                place_piece(move)
                main(read())
        elif msg == "your move\n":
                move = "d6"
                write(move)
                place_piece(move)
                main(read())
        elif msg == "\"The game is finished\" White: \n":
                print(read())
                print(read())
                print(read())
        else:
                print("Unknown response:")
                print(read())
                print(read())
                print(read())
                print(read())
  
if __name__== "__main__":
        main(read())


