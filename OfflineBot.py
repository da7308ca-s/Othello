import numpy as np
import subprocess
import sys

proc = subprocess.Popen("./othello", shell=True,stdout=subprocess.PIPE, stdin=subprocess.PIPE)
print("test")