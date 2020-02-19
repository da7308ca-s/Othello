#!/usr/bin/env python

from subprocess import Popen, PIPE
from time import sleep

process = Popen("./othello", stdout=PIPE, stderr=PIPE, stdin=PIPE)

def read():
        msg = ""
        for i in range(5):
                msg += process.stdout.readline().decode()
        return msg

def write(msg):
        process.stdin.write(str.encode(msg + "\n"))
        process.stdin.flush()
        print(msg)

def loop(msg):
        pass

def main():
        print(read())
        sleep(0.5)
        write("da7308ca-s")
        sleep(0.5)
        print(read())
        sleep(0.5)
        write("w")
        sleep(0.5)
        print(read())
        sleep(0.5)
        write("e6")
        sleep(0.5)
        print(read())
  
if __name__== "__main__":
        main()


