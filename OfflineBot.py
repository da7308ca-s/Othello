#!/usr/bin/env python

from subprocess import Popen, PIPE

process = Popen("./othello", stdout=PIPE, stderr=PIPE)

def read():
        return process.stdout.readline().decode()

def write(msg):
        proc.stdin.write(str.encode(msg + "\n"))
        proc.stdin.flush()

def main():
        print(read())
        write("da7308ca-s")
        print(read())
  
if __name__== "__main__":
        main()


