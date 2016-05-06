import random
import sys

f = open("utkarsh-to-label.txt")
d = f.readlines()
s = set(d)
l = list(s)
random.shuffle(l)
for x in l:
    sys.stdout.write(x)

