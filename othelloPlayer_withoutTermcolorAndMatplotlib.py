#!/usr/bin/env python
import sys
from subprocess import Popen, PIPE
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time
import random
#from termcolor import colored

rc2dir = np.array([[8,2,6],[4,3,5],[0,1,7]])
dir2rc = np.array([[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1]])
RC = np.array([[(y,x) for x in range(8)] for y in range(8)])

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

def direction_chooser(r,c,i =-1,j=0):
	l = []
	for x in range(8):
		d = (x + rc2dir[i,j])%8
		ll = []
		for k in range(1,8):
			a,b = (move_in_direction(r,c,d,k))
			if a>7 or a<0 or b>7 or b<0:
				break
			ll.append((a,b))
		l.append(ll)
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
		return minEval, move, n_visited_children, n_pruned*n_pruned_multiplier

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
		self.winner = "None"

	def print_board(self):
		player = "Black" if self.player == 1 else "White"
		text = "Playing as "+player+" minimax depth search set to " + str(depth) 
		print("# A B C D E F G H # "+text)
		for i in range(8):
			text = str(i+1)+" "
			for j in range(8):
				t = "  "
				if (i,j) in self.get_valid_moves():
					t = "* "
				if self.board[i][j] == 1:
					t = "D " #colored("D ","red")
				if self.board[i][j] == -1:
					t = "W " #colored("W ","green")
				text+=t
			text += str(i+1) + " "
			if i == 1:
				text += str(player) +" to move Move# " + str(move_counter)
			if i == 3 and self.last_move is not None:
				text += "Last move: " + str(coord_to_text(self.last_move))
				if self.player == 1 and my_color=="d" or self.player == -1 and my_color == "w":
					text += " (computation time: "+str(last_move_time)+ ")"
			if i == 5:
				text += "Valid moves (*): "
				for x in self.get_valid_moves():
					text += coord_to_text(x) + " "
			if i == 7:
				text += "Evaluation: " + str(self.evaluate_position()) + " Foresight: " + str(foresight)
			print(text)
		print("# A B C D E F G H #")

	def place_piece(self,move):
		self.last_move = move
		self.board[move] = self.player
		self.flip(move)
		self.player = -self.player
		self.valid_moves = None
		bothNoMoves = False
		if len(self.get_valid_moves()) == 0:
			self.player = -self.player
			self.valid_moves = None
			if len(self.get_valid_moves()) == 0:
				bothNoMoves = True
		if np.count_nonzero(self.board) == 64 or bothNoMoves:
			self.game_over = True
			self.winner = "Black" if self.evaluate_position()>0 else "White"
			if self.evaluate_position() == 0:
				self.winner = "Tie"

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
		t = time.time()
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
							 #skip if outside,not free or previously evaluated 
							if x>7 or x<0 or y>7 or y<0 or not self.board[x][y] == 0 or (x,y) in previously_evaluted:
								continue
							previously_evaluted.append((x,y))
							if self.flip((x,y),True) > 0:
								valid_moves.append((x,y))
								break;
							isValid = False
							for direction in direction_chooser(x,y,-ii,-jj): #start checking in direction of opponents piece
								if isValid:
									break
								hasOppositeColor = False
								for r,c in direction: #traverse along an arm
									if self.board[r][c] == 0:
										break
									elif self.board[r][c] == -self.player:
										hasOppositeColor = True
									elif self.board[r][c] == self.player:
										if hasOppositeColor:
											isValid = True
										break
							if isValid:
								valid_moves.append((x,y))
		global ftime
		ftime+=time.time()-t
		return self.sort_moves(valid_moves)

	def sort_moves(self, moves, sort = "distance"):
		sorted_moves = []
		if sort == "distance":
			while not len(moves) == 0:
				longest_dist = 0
				for x,y in moves:
					dist = np.sqrt((x-3.5)**2+(y-3.5)**2)
					if dist>longest_dist:
						longest_dist = dist
						move = (x,y)
				moves.remove(move)
				sorted_moves.append(move)
		else:
			while not len(moves) == 0:
				most_flips = 0
				for m in moves:
					flips = self.flip(m,True)
					if flips>most_flips:
						most_flips = flips
						move = m
				moves.remove(move)
				sorted_moves.append(move)
		global ftime
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

def main(msg,d=0):
	global move_counter
	if d>5:
		print("Error")
		return
	if msg == "hi! I am your othello server.\n":
		print(msg)
		write('da7308ca-s')
		print(read())
		print(read())
		main(read())
	elif msg == "choose colour, 'd' for dark, 'w' for white.\n":
		print(msg)
		write(my_color)
		print(read())
		if verbose: 
			for i in range(9):
				print(read())
		main(read())
	elif msg == "The game is finished\n":
		print(msg)
		print(read())
		print(read())
		print(read())
	elif msg == "my move\n":
		print(msg)
		move = read()
		print(move)
		pos.place_piece(text_to_coord(move))
		move_counter+=1
		pos.print_board()
		if verbose: 
			for i in range(9):
				print(read())
		main(read())
	elif msg == "your move\n":
		print(msg)
		global last_move_time, move_number, logs, foresight
		if depth == 0:
			move = random.choice(pos.get_valid_moves())
			n_visited_children = 0
			n_pruned = 0
			foresight = 0
			last_move_time=0
		else:
			t1 = time.time()
			foresight, move, n_visited_children, n_pruned = minimax(pos,depth,my_color == "d")
			t2 = time.time()
			last_move_time=t2-t1
		logs[0][game_number].append(n_visited_children)
		logs[1][game_number].append(n_pruned)
		logs[2][game_number].append(last_move_time)
		logs[3][game_number].append(foresight)
		logs[4][game_number].append(pos.evaluate_position())
		write(coord_to_text(move))
		pos.place_piece(move)
		move_counter+=1
		pos.print_board()
		if verbose: 
			for i in range(9):
				print(read())
		main(read())
	elif "The game is finished" in msg:
		print("The game is finished. White: " + read().replace("\n","") + read().replace("\n",""))
		global results
		text = "Winner:" + pos.winner + ", Final score: " + str(pos.evaluate_position())
		results.append(text)
		print(read())
	else:
		print("Unknown response:")
		print(msg)
		main(read(),d+1)

def play_game_against_computer():
	t = time.time()
	global game_number, process, pos, move_counter
	move_counter = 1
	process = Popen("./othello" if not verbose else "./verboseothello", stdout=PIPE, stderr=PIPE, stdin=PIPE)
	pos = Position()
	pos.print_board()
	main(read())
	game_number +=1
	print("Game Time:",time.time()-t)
 
if __name__== "__main__":
	n_pruned_multiplier = 3
	verbose = False
	last_move_time = 0
	colors = ["d"]
	depths = [4]
	game_number = 0
	foresight = 0
	move_counter = 1
	ftime = 0
	for i in range(1,len(sys.argv)):
		if i == 1:
			colors = [x for x in sys.argv[i]]
		if i == 2:
			depths = [int(x) for x in sys.argv[i]]
	logs = [[[] for i in range(len(depths)*len(colors))]for j in range(5)]
	results = []
	for depth in depths:
		for my_color in colors:
				play_game_against_computer()
	"""
	fig, axs = plt.subplots(len(depths),len(colors),sharex='col',sharey='row',figsize=(16,10),gridspec_kw={'hspace':0.15,'wspace':0.1})
	patches = []
	color_list=["red","blue","green","cyan","black"]
	patches.append(mpatches.Patch(color="red",label="Number of visited children"))
	patches.append(mpatches.Patch(color="blue",label="Number of pruned branches x"+str(n_pruned_multiplier)))
	patches.append(mpatches.Patch(color="green",label="Computing time"))
	patches.append(mpatches.Patch(color="cyan",label="Foresight evaluation"))
	patches.append(mpatches.Patch(color="black",label="Current Evaluation"))
	flat = [axs] if len(depths)*len(colors) == 1 else axs.flat
	for i, ax in enumerate(flat):
		if i == 0 and len(colors)==2:
			ax.set_title("Black")
		if i == 1 and len(colors)==2:
			ax.set_title("White")
		if i%len(colors) == 0:
			ax.set(ylabel="Depth = "+str(depths[i/len(colors)]))
		for j, values in enumerate(logs):
			ax.plot([k for k in range(len(values[i]))],values[i],color=color_list[j])
		ax.set(xlabel=results[i])
	if len(depths)*len(colors) == 1:
		ax.legend(handles=patches,loc="best")
	print("Time: ",ftime)	
	plt.show()
	"""



