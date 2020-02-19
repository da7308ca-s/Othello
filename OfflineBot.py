import numpy as np
import subprocess
import sys

proc = subprocess.Popen("./othello", shell=True,stdout=subprocess.PIPE, stdin=subprocess.PIPE)

def send(msg):
        proc.stdin.write(str.encode(msg + "\n"))
        proc.stdin.flush()
        print(msg)

def read():
        return proc.stdout.readline().decode()

print(read())