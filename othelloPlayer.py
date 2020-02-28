#!/usr/bin/env python

from subprocess import Popen, PIPE
from copy import deepcopy
import numpy as np

rc2dir = np.array([[8,2,6],[4,3,5],[0,1,7]])
dir2rc = np.array([[-1,0],[-1,1],[0,1],[1,1],[0,1],[1,-1],[0,-1],[-1,-1]])

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
	return s[coord[1]] + str(coord[0] + 1)

#move a coordinate on the board where up is zero and oriented clock-wise
def move_in_direction(r,c,d,i=1):
	return r + dir2rc[d][0]*i, c + dir2rc[d][1]*i

def direction_chooser(i,j):
	return [(x + rc2dir[i,j])%8 for x in range(8)]

def direction_chooser2(r,c,i,j):
	l = []
	for x in range(8):
		d = (x + rc2dir[i,j])%8
		l.append([(move_in_direction(r,c,d,k)) for k in range(1,8)])
	return l

def minimax(position,depth,maximizingPlayer,pruning = True,alpha = -65,beta = 65):
	if depth == 0 or position.game_over == True:
		return position.evaluate_position(), None, 0, 0
	move = None
	n_pruned = 0
	n_visited_children = 0
	if maximizingPlayer:
		maxEval = -65
		for c in position.get_children():
			n_visited_children+=1
			evaluation, _, _, n_pruned = minimax(c,depth-1,False,pruning,alpha,beta)
			if evaluation > maxEval:
				maxEval = evaluation
				move = c.last_move
			alpha = max(alpha,evaluation)
			if beta<=alpha and pruning:
				n_pruned +=1
				break
		return maxEval, move, n_visited_children, n_pruned
	else:
		minEval = 65
		for c in position.get_children():
			n_visited_children+=1
			evaluation, _, _, n_pruned = minimax(c,depth-1,True,pruning,alpha,beta)
			if evaluation<minEval:
				minEval = evaluation
				move = c.last_move
			beta = min(beta,evaluation)
			if beta<=alpha and pruning:
				n_pruned+=1
				break
		return minEval, move, n_visited_children, n_pruned

class Position:
	def __init__(self):
		self.player = 1
		self.board = np.zeros((8,8))
		self.board[3][3] = -1
		self.board[4][4] = -1
		self.board[3][4] = 1
		self.board[4][3] = 1
		self.valid_moves = None
		self.last_move = None
		self.game_over = False

	def print_board(self):
		player = "Black" if self.player == 1 else "White"
		print()
		print(player, "to move")
		print(self.board)
		print("Last move",self.last_move)
		print("Valid moves in position", self.get_valid_moves())
		print("Current Evaluation:", self.evaluate_position())

	def place_piece(self,move):
		self.last_move = move
		self.board[move] = self.player
		self.flip(move)
		self.player = -self.player
		self.valid_moves = None
		if len(self.get_valid_moves()) == 0:
			self.player = -self.player
			self.valid_moves = None
		if np.count_nonzero(self.board) == 64:
			self.game_over = True


	def flip(self,move,count_flips = False):
		n_flips = 0
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
					if count_flips:
						n_flips+=1
					else:
						self.board[coord] = -self.board[coord]
		if count_flips:
			return n_flips

	def get_valid_moves(self):
		if self.valid_moves is None:
			self.valid_moves = self.calculate_valid_moves()
		return self.valid_moves

	def calculate_valid_moves(self):
		valid_moves = []
		previously_evaluted = []
		for rr in range(8): #Loop over board
			for cc in range(8):
				if self.board[rr][cc] == -self.player: #only check opponents pieces
					for ii in range(-1,2): 
						for jj in range(-1,2): #check pieces surrounding opponents
							if ii == 0 and jj == 0: #skip center
								continue
							x = ii+rr
							y = jj+cc
							if x>7 or x<0 or y>7 or y<0 or not self.board[x][y] == 0 or (x,y) in previously_evaluted: #skip if outside or previously 
								continue
							previously_evaluted.append((x,y))
							isValid = False
							"""
							for direction in direction_chooser2(x,y,ii,jj): #start checking in direction of opponents piece
								if isValid:
									break
								for r,c in direction: #traverse along an arm
									if r>7 or r<0 or c>7 or c<0:
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
							"""
							for direction in direction_chooser(ii,jj):
								if isValid:
									break
								r = x
								c = y
								hasOppositeColor = False
								for i in range(7):
									r,c = move_in_direction(r,c,direction)
									if r>7 or r<0 or c>7 or c<0:
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
								valid_moves.append((x,y))
		return self.sort_moves_by_flips(valid_moves)

	def sort_moves_by_distance(self, moves):
		sorted_moves = []
		while not len(moves) == 0:
			longest_dist = 0
			for x,y in moves:
				dist = np.sqrt((x-3.5)**2+(y-3.5)**2)
				if dist>longest_dist:
					longest_dist = dist
					move = (x,y)
			moves.remove(move)
			sorted_moves.append(move)
		return sorted_moves

	def sort_moves_by_flips(self,moves):
		sorted_moves = []
		while not len(moves) == 0:
			most_flips = 0
			for m in moves:
				flips = self.flip(m,True)
				if flips>most_flips:
					most_flips = flips
					move = m
			moves.remove(move)
			sorted_moves.append(move)
		return sorted_moves

	def get_children(self):
		children = []
		for move in self.get_valid_moves():
			newPos = deepcopy(self)
			newPos.place_piece(move)
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
		main(read())
	elif msg == "your move\n":
		_, move, _, _ = minimax(pos,depth,my_color == "d")
		write(coord_to_text(move))
		pos.place_piece(move)
		pos.print_board()
		main(read())
	else:
		print("Unknown response:")
		print(read())
		print(read())
		print(read())
		print(read())
  
if __name__== "__main__":
	print("rc2dir")
	print(rc2dir)
	for i in range(-1,2):
		for j in range(-1,2):
			pass
			#print("i j", i , j, rc2dir[i,j])
			#print(direction_chooser2(0,0,i,j))
	process = Popen("./othello", stdout=PIPE, stderr=PIPE, stdin=PIPE)
	my_color = "w"
	depth = 4
	pos = Position()
	main(read())


