import sys
import openmath
from openmath.latex import eval 

files = sys.argv[1:]

if len(files) == 0:
    print(eval(openmath.parse(sys.stdin.read())))

else:
    for arg in sys.argv[1:]:
        with open(arg) as fh:
            text = fh.read()
        print(eval(openmath.parse(text)))