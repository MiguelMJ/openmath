"""http://www.openmath.org/cd/set1"""

import openmath.config
from openmath.latex import eval

openmath.config.addKeyVal("SUCHTHAT_SYMBOL", ["BAR", "COLON"], "BAR")
openmath.config.addKeyVal("SUCHTHAT_VARIABLE", ["ALONE", "SET"], "SET")

"""http://www.openmath.org/cd/set1#emptyset"""
cartesian_product = ("\\times", "infix")

"""http://www.openmath.org/cd/set1#emptyset"""
emptyset = "\\emptyset"

"""http://www.openmath.org/cd/set1#in"""
in_ = ("\\in", "infix")

"""http://www.openmath.org/cd/set1#intersect"""
intersect = ("\\cap", "infix")

"""http://www.openmath.org/cd/set1#map"""
def map(f, a):
    if openmath.config.get("SUCHTHAT_SYMBOL") == "BAR":
        sym = "\\mid"
    else:
        sym = ":"
    tup = (eval(f.object),  sym, f.variables[0].name, eval(a))
    return "\\left{ %s %s %s \\in %s \\right}" % tup
    
"""http://www.openmath.org/cd/set1#notin"""
notin = ("\\notin", "infix")

"""http://www.openmath.org/cd/set1#notprsubset"""
notprsubset = ("", "infix") 

"""http://www.openmath.org/cd/set1#notsubset"""
notsubset = ("", "infix") 

"""http://www.openmath.org/cd/set1#prsubset"""
prsubset = ("\\subset", "infix") 

"""http://www.openmath.org/cd/set1#set"""
def set_(*args):
    return "\\left{ %s \\right}" % ", ".join(args)

"""http://www.openmath.org/cd/set1#setdiff"""
setdiff = ("\\setminus", "infix")

"""http://www.openmath.org/cd/set1#size"""
def size(a):
    return len(a)

"""http://www.openmath.org/cd/set1#subset"""
subset = ("\\subseteq", "infix")

"""http://www.openmath.org/cd/set1#suchthat"""
def suchthat(a, f):
    if openmath.config.get("SUCHTHAT_SYMBOL") == "BAR":
        sym = "\\mid"
    else:
        sym = ":"
    if openmath.config.get("SUCHTHAT_VARIABLE") == "SET":
        tup = (f.variables[0].name, eval(a), sym, eval(f.object))
        return "\\left{ %s \\in %s %s %s \\right}" % tup
    else:
        tup = (f.variables[0].name, sym, f.variables[0].name, eval(a), eval(f.object))
        return "\\left{ %s %s %s \\in %s, %s \\right}" % tup

"""http://www.openmath.org/cd/set1#union"""
union = ("\\cup", "infix")

locals()["in"] = in_
locals()["set"] = set_

special = [
    "map",
    "suchthat"
]