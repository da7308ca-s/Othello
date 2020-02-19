#!/usr/bin python
import numpy as np
import subprocess
import sys

def text_to_pair(text):
	s = "abcdefgh"
	return (s.index(text[0]), int(text[1]) - 1)

def pair_to_text(pair):
	s = "abcdefgh"
	return s[pair[0]] + str(pair[1] + 1)


class Node:
	def __init__(self, pair, parent, value, board, color):
		self.parent = parent
		self.pair = pair
		self.value = value
		self.children = {}
		self.board = board
		self.move_made_by = color


	def dig(self, node, padding):
		string = padding + str(node.pair) +" "+  str(node.value) + " " + str(node.move_made_by) + "\n"
		for v in node.children.values():
			string += self.dig(v, padding + "-")
		return string

	def __str__(self):
		string = str(self.pair) +" "+ str(self.value) + " " + str(self.move_made_by) + "\n"
		for v in self.children.values():
			string += self.dig(v, "-")
		return string 

 
def propagate(x, y, dx, dy, c, to_flip, b):
	if x < 0 or x > 7 or y < 0 or y > 7:
		return []

	if(b[x,y] == -c):
		to_flip.append((x,y))
		return propagate(x + dx, y + dy, dx, dy, c, to_flip, b)
	elif(b[x,y] == c):
		return to_flip
	else:
		return []

def calc_to_flip(p, c, b):
	x,y = p
	to_flip = []
	for i in range(-1,2):
		for j in range(-1,2):
			to_flip.extend(propagate(x + i, y + j, i, j, c, [], b))
	return to_flip


def set_piece(p, node, c, board, to_flip = []):
	if(board[p] != 0):
		print("IRREGAR")
		return 
	board[p] = c
	if(len(to_flip) == 0):
		to_flip = calc_to_flip(p, c, board)
	if(len(to_flip) == 0):
		print("Irregar")
		return
	for pair in to_flip:
		board[pair] = -board[pair]

	return Node(p, node, board.sum(), board, c)


def possible_moves(b,c):
	pos_moves = {}
	for x in range(8):
		for y in range(8):
			if(b[x,y] == -c):
				for i in range(-1,2):
					for j in range(-1,2):
						if(x + i > -1 and x + i < 8 and y + j > -1 and y + j < 8 and b[x + i,y + j] == 0 and (x + i, y + j) not in pos_moves):
							to_flip = calc_to_flip((x + i,y + j), c, b)
							if len(to_flip) > 0:
								pos_moves[(x + i, y + j)] = to_flip
	
	return pos_moves	

def build_branch(node, c, depth, alpha, beta):
	b = node.board
	pos_moves = possible_moves(b,c)

	if len(pos_moves) == 0 and np.count_nonzero(b) < 64:
		return build_branch(node, -c, depth, alpha, beta)

	best_value = -64 if c == 1 else 64
	value = -best_value
	for p,to_flip in pos_moves.items():
		bcopy = b.copy()
		bcopy[p] = c
		for tile in to_flip:
			bcopy[tile] = -bcopy[tile]
		
		value = bcopy.sum()
		child = Node(p, node, value, bcopy, c)
		if depth > 0:
			node.children[p] = build_branch(child, -c, depth - 1, alpha, beta)
			value = node.children[p].value	
		else:
			node.children[p] = child
				
		if c == 1:
			if value > best_value:
				best_value = value
			if value > alpha:
				alpha = value
				if beta <= alpha:
					break
		elif c == -1: 
			if value < best_value:
				best_value = value
			if value < beta:
				beta = value
				if beta <= alpha:
					break
			
	node.value = best_value
		
	return node



def choose_move(node, c, depth):
	print(node)
	node = build_branch(node, c, depth, -65, 65)
	favorite_child = None
	best_value = -65 if c == 1 else 65
	print(len(node.children))
	for pair, child in node.children.items():
		if(len(node.children) == 1):
			print(child)
		if c == 1 and child.value > best_value:
			best_value = child.value
			favorite_child = child
		elif c == -1 and child.value < best_value:
			best_value = child.value
			favorite_child = child	
		
	return favorite_child


board = np.zeros((8,8))
idstring = "gu6358br-s"
my_color = "d"


board[3,3] = 1 if my_color == "w" else -1
board[4,4] = 1 if my_color == "w" else -1
board[3,4] = 1 if my_color == "d" else -1
board[4,3] = 1 if my_color == "d" else -1

def test_loop(msg, root, board):
	p = (0,0)
	if msg[0] not in "abcdefgh":
		p = (int(msg[0]),int(msg[1]));
	else:	
		p = text_to_pair(msg)
	if root and p in root.children:
		root = root.children[p]
		board = root.board
	else:
		root = set_piece(p, root, -1, board)
	print(board)
	root = choose_move(root, 1, depth=2)
	board = root.board
	print(root)
	print(board)
	test_loop(input(), root, board)

#test_loop(input(), None, board)

proc = subprocess.Popen("./othello", shell=True,stdout=subprocess.PIPE, stdin=subprocess.PIPE)
def send(msg):
	proc.stdin.write(str.encode(msg + "\n"))
	proc.stdin.flush()
	print(msg)


def read():
	return proc.stdout.readline().decode()


def main_loop(msg, root, board):
	print(msg)
	if str(msg) == "hi! I am your othello server.\n":
		send(idstring)
		print(read())
		print(read())
		main_loop(read(), root, board)
	elif msg == "choose colour, 'd' for dark, 'w' for white.\n":
		send(my_color)
		root = Node((-1,-1), None, 0, board, -1 if my_color == 'd' else 1)
		print(read())
		main_loop(read(), root, board)
	elif msg == "The game is finished\n":
		print(read())
		print(read())
		print(read())
	elif msg == "my move\n":
		move = read()
		print(move)
		p = text_to_pair(move)
		if root and p in root.children:
			root = root.children[p]
			board = root.board
		else:
			root = set_piece(p, root, -1, board)
		main_loop(read(), root, board)
	elif msg == "your move\n":
		print(root.board)
		root = choose_move(root, 1, depth=4)
		board = root.board
		print(board)
		send(pair_to_text(root.pair))
		main_loop(read(), root, board)
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

print("Recursion limit " + str(sys.getrecursionlimit()))
main_loop(read(), None, board)