import openmath.config
from openmath import Symbol
from openmath.latex import eval

openmath.config.addKeyVal("DIVIDE_AS_FRACTION", ["YES", "NO"], "YES")
openmath.config.addKeyVal("HIDE_SQRT", ["YES", "NO"], "YES")

priority = [
    Symbol("unary_minus", "arith1"),    
    Symbol("power", "arith1"),    
    Symbol("divide", "arith1"),    
    Symbol("times", "arith1"),    
    Symbol("minus", "arith1"),    
    Symbol("plus", "arith1"),    
]

lcm = ("lcm", "call")

gcm = ("gcm", "call")

plus = ("+", "infix")

def unary_minus(x): 
    return "- "+x

minus = ("-", "infix")

times  = ("\\times", "infix")

def divide(a,b):
    if openmath.config.get("DIVIDE_AS_FRACTION") == "YES":
        return "\\frac{%s}{%s}" % (a,b)
    return "%s / %s" % (a,b)

def power(a,b):
    return "%s^{%s}" % (a,b)

abs = ("abs", "call")

def root(a,b):
    if b == 2 and openmath.config.get("HIDE_SQRT") == "YES":
        return "\\sqrt{%s}" % a
    return "\\sqrt[%s]{%s}" % (b,a)

def sum(a,b):
    "http://www.openmath.org/cd/arith1#sum"
    return "\\sum_{%s=%s}^{%s} %s" % (eval(b.variables[0]),eval(a.arguments[0]), eval(a.arguments[1]), eval(b.object))

def product(a,b):
    return "\\prod_{%s=%s}^{%s} %s" % (eval(b.variables[0]),eval(a.arguments[0]), eval(a.arguments[1]), eval(b.object))

special = [
    "sum",
    "product"
]