#!/usr/bin/env python

from copy import deepcopy
import numpy as np

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

def direction_chooser(i,j):
	if i == 1 and j == 0:
		return range(8)
	if i == 1 and j == -1:
		return [1,2,3,4,5,6,7,0]
	if i == 0 and j == -1:
		return [2,3,4,5,6,7,0,1]
	if i == -1 and j == -1:
		return [3,4,5,6,7,0,1,2]
	if i == -1 and j == 0:
		return [4,5,6,7,0,1,2,3]
	if i == -1 and j == 1:
		return [5,6,7,0,1,2,3,4]
	if i == 0 and j == 1:
		return [6,7,0,1,2,3,4,5]
	if i == 1 and j == 1:
		return [7,0,1,2,3,4,5,6]

def minimax(position,depth,maximizingPlayer,pruning = True,alpha = -65,beta = 65):
	if depth == 0 or position.game_over == True:
		return position.evaluate_position(), None, 0, 0
	move = None
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
		if np.count_nonzero(self.board) == 64 or len(self.get_valid_moves()) == 0:
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
		for rr in range(8):
			for cc in range(8):
				if self.board[rr][cc] == -self.player:
					for ii in range(-1,2):
						for jj in range(-1,2):
							if ii == 0 and jj == 0:
								continue
							x = ii+rr
							y = jj+cc
							if x>7 or x<0 or y>7 or y<0 or not self.board[x][y] == 0 or (x,y) in valid_moves:
								continue
							isValid = False
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

def main():
	position = Position()
	position.print_board()
	depth = 4
	maximizingPlayer = True
	total_visited_children = 0
	total_branches_pruned = 0
	while not position.game_over:
		_, move, n_visited_children, n_pruned = minimax(position,depth,maximizingPlayer)
		total_visited_children += n_visited_children
		total_branches_pruned += n_pruned
		position.place_piece(move)
		position.print_board()
		print("Visited",n_visited_children, "children and pruned", n_pruned, "branches in previous position")
		maximizingPlayer = not maximizingPlayer
	else:
		print("\nGame is over")
		score = position.evaluate_position()
		if score>0:
			print("Black player won")
		elif score<0:
			print("White player won")
		else:
			print("It's a draw")
		print("Visited",total_visited_children,"child positions and pruned",total_branches_pruned,"branches in total")
  
if __name__== "__main__":
	main()
