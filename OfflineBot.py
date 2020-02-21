#!/usr/bin/env python

from subprocess import Popen, PIPE
from prettytable import PrettyTable
import numpy as np

def read():
	return process.stdout.readline().decode()

def write(msg):
	process.stdin.write(str.encode(msg + "\n"))
	process.stdin.flush()
	print(msg)

def text_to_coord(text):
	s = "abcdefgh"
	return (int(text[1]) - 1,s.index(text[0]))

class Position:
	def __init__(self):
		self.board = np.zeros((8,8))
		self.board[3][3] = -1
		self.board[4][4] = -1
		self.board[3][4] = 1
		self.board[4][3] = 1

	def print_board(self):
		print(self.board)

	def place_piece(self,move,player):
		move = text_to_coord(move)
		self.board[move] = 1 if player == "d" else -1
		print("Before flip")
		self.print_board()	

		self.flip(move, 1 if player == "d" else -1)

		print("After flip")          
		self.print_board()

	def flip(self,move,player):
		for dir in range(8):
			r,c = move	
			to_flip = []
			flip = False
			for i in range(7):
				if dir == 0: 
					r-=1
				elif dir == 1:
					r-=1
					c+=1
				elif dir == 2:
					c+=1
				elif dir == 3:
					r+=1
					c+=1
				elif dir == 4:
					r+=1
				elif dir == 5:
					r+=1
					c-=1
				elif dir == 6:
					c-=1
				elif dir == 7:
					r-=1
					c-=1

				if r>7 or r<0 or c>7 or c<0:
					break

				if self.board[r][c] == player:
					flip = True
					break
				elif self.board[r][c] == 0:
					break
				elif self.board[r][c] == -player:
					to_flip.append((r,c))
			if flip:
				for coord in to_flip:
					self.board[coord] = -self.board[coord]


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
		pos.place_piece(move,"d" if my_color == "w" else "w")
		main(read())
	elif msg == "your move\n":
		move = "d6"
		write(move)
		pos.place_piece(move,"w" if my_color == "w" else "d")
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

process = Popen("./othello", stdout=PIPE, stderr=PIPE, stdin=PIPE)
my_color = "w"
pos = Position()
  
if __name__== "__main__":
	main(read())


