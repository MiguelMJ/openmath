import sys
import openmath
import openmath.config
from openmath.mathml import eval 

files = [arg for arg in sys.argv[1:] if not arg.startswith("+")]
openmath.config.parseFromArgs(sys.argv)

if len(files) == 0:
    print(eval(openmath.parse(sys.stdin.read())))

else:
    for arg in files:
        with open(arg) as fh:
            text = fh.read()
        print(eval(openmath.parse(text)))