#!/usr/bin/env python

from subprocess import Popen, PIPE

process = Popen("./othello", stdout=PIPE, stderr=PIPE, shell=True)
stdout, stderr = process.communicate()
print("this far")
print(stdout)
