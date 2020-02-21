#!/usr/bin/env python

from subprocess import Popen, PIPE

process = Popen("./othello", stdout=PIPE, stderr=PIPE, stdin=PIPE)
my_color = "w"

def read():
        return proc.stdout.readline().decode()

def write(msg):
        process.stdin.write(str.encode(msg + "\n"))
        process.stdin.flush()
        print(msg)

def main(msg):
        print(msg)
        if str(msg) == "hi! I am your othello server.\n":
                send('da7308ca-s')
                print(read())
                print(read())
                main(read())
        elif msg == "choose colour, 'd' for dark, 'w' for white.\n":
                send(my_color)
                print(read())
                main(read())
        elif msg == "The game is finished\n":
                print(read())
                print(read())
                print(read())
        elif msg == "my move\n":
                move = read()
                print(move)
        elif msg == "your move\n":
                send("e6")
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


