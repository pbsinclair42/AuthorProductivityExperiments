
from __future__ import print_function
import sys

prev = None
sum = 0
for line in sys.stdin:
    a, b = line.strip().split()
    if prev == a:
        sum += 1
    else:
        print(a, str(sum))
        sum = 1
        prev = a

        
print(a, str(sum))
