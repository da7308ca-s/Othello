#!/usr/bin/env python

from subprocess import Popen, PIPE
from time import sleep

process = Popen("./othello", stdout=PIPE, stderr=PIPE, stdin=PIPE)

def read():
        print(process.stdout.readline().decode())
        print(process.stdout.readline().decode())
        print(process.stdout.readline().decode())
        print(process.stdout.readline().decode())

def write(msg):
        process.stdin.write(str.encode(msg + "\n"))
        process.stdin.flush()
        print(msg)

def main():
        read()
        write("da7308ca-s")
        read()
        write("w")
        read()
        write("e6")
        read()
  
if __name__== "__main__":
        main()


