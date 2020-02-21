#!/usr/bin/env python

from subprocess import Popen, PIPE
from copy import deepcopy
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

def coord_to_text(coord):
	s = "abcdefgh"
	return str(coord[1] + 1) + s[coord[0]]

def move_in_direction(r,c,direction):
	if direction == 0: 
		r-=1
	elif direction == 1:
		r-=1
		c+=1
	elif direction == 2:
		c+=1
	elif direction == 3:
		r+=1
		c+=1
	elif direction == 4:
		r+=1
	elif direction == 5:
		r+=1
		c-=1
	elif direction == 6:
		c-=1
	elif direction == 7:
		r-=1
		c-=1
	return r,c

class Position:
	def __init__(self):
		self.player = 1
		self.board = np.zeros((8,8))
		self.board[3][3] = -1
		self.board[4][4] = -1
		self.board[3][4] = 1
		self.board[4][3] = 1
		self.valid_moves = self.calculate_valid_moves()

	def print_board(self):
		print(self.board)
		print(self.evaluate_position())

	def place_piece(self,move):
		self.board[move] = self.player
		self.flip(move)
		self.player = -self.player
		self.valid_moves = self.calculate_valid_moves()

	def flip(self,move):
		for direction in range(8):
			r,c = move	
			to_flip = []
			flip = False
			for i in range(7):
				r,c = move_in_direction(r,c,direction)
				if r>7 or r<0 or c>7 or c<0:
					break
				if self.board[r][c] == self.player:
					flip = True
					break
				elif self.board[r][c] == 0:
					break
				elif self.board[r][c] == -self.player:
					to_flip.append((r,c))
			if flip:
				for coord in to_flip:
					self.board[coord] = -self.board[coord]

	def calculate_valid_moves(self):
		valid_moves = []
		for rr in range(8):
			for cc in range(8):
				if not self.board[rr][cc] == 0:
					continue
				isValid = False
				for direction in range(8):
					if isValid:
						break
					r = rr
					c = cc
					hasOppositeColor = False
					for i in range(7):
						r,c = move_in_direction(r,c,direction)
						if r>7 or r<0 or c>7 or c<0:
							#print(0)
							break
						elif self.board[r][c] == 0:
							break
						elif self.board[r][c] == -self.player:
							hasOppositeColor = True
						elif self.board[r][c] == self.player:
							if hasOppositeColor:
								isValid = True
							break
						else:
							print("wtf")
				if isValid:
					valid_moves.append((rr,cc))
		return valid_moves

	def get_children(self):
		children = []
		for move in self.valid_moves:
			newPos = deepcopy(self)
			newPos.place_piece(move)
			newPos.print_board()
			children.append(newPos)
		return children

	def evaluate_position(self):
		return np.sum(self.board)

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
		pos.place_piece(text_to_coord(move))
		pos.print_board()
		print("Children")
		children = pos.get_children()
		main(read())
	elif msg == "your move\n":
		move = "d6"
		write(move)
		pos.place_piece(text_to_coord(move))
		pos.print_board()
		print("Children")
		children = pos.get_children()
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


