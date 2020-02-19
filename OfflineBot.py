#!/usr/bin/env python

from subprocess import Popen, PIPE

process = Popen("./othello", stdout=PIPE, stderr=PIPE)

print(process.stdout.readline().decode())
