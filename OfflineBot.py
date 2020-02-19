#!/usr/bin/env python

from subprocess import Popen, PIPE
from time import sleep

process = Popen("./othello", stdout=PIPE, stderr=PIPE, stdin=PIPE)

def read():
        stdout = []
        while True:
                line = process.stdout.readline()
                stdout.append(line)
                print('The line', line)
                if line == '' and p.poll() != None:
                        break
        return ''.join(stdout)

def write(msg):
        process.stdin.write(str.encode(msg + "\n"))
        process.stdin.flush()
        print(msg)

def main():
        print(read())
        write("da7308ca-s")
        print(read())
        write("w")
        print(read())
        write("e6")
        print(read())
  
if __name__== "__main__":
        main()


