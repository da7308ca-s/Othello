import subprocess

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