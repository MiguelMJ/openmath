import sys
import openmath
import openmath.config
import openmath.latex as latex
import openmath.mathml as mathml

from openmath.eval import eval 
from openmath.util import asOM


openmath.config.addKeyVal("EVAL_RESULT", ["PYTHON", "LATEX", "MATHML", "OM"], "PYTHON")

def main(om):
    ret = eval(om)
    match(openmath.config.get("EVAL_RESULT")):
        case "PYTHON":
            return ret
        case "LATEX":
            return latex.eval(asOM(ret))
        case "MATHML":
            return mathml.eval(asOM(ret))
        case "OM":
            return asOM(ret)

files = [arg for arg in sys.argv[1:] if not arg.startswith("+")]
openmath.config.parseFromArgs(sys.argv)

if len(files) == 0:
    print(main(openmath.parse(sys.stdin.read())))

else:
    for arg in files:
        with open(arg) as fh:
            text = fh.read()
        print(main(openmath.parse(text)))
