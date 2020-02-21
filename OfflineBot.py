#!/usr/bin/env python

from subprocess import Popen, PIPE
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
		to_flip = []
		flip = False
		#Check upwards
		for i in range(move[0]-1,-1,-1):
			print(i,move[1])
			if self.board[i][move[1]] == 1:
				print(1)
				flip = True
				break
			elif self.board[i][move[1]] == 0:
				print(2)
				break
			elif self.board[i][move[1]] == -1:
				print(3)
				to_flip.append((i,move[1]))
			if flip:
				for coord in to_flip:
					print(coord)
					self.board[coord] = 1

				
		print("After flip")          
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


