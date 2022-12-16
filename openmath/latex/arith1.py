import openmath.config
from openmath import Symbol
from openmath.latex import eval, evalAndEnclose

from functools import reduce

openmath.config.addKeyVal("DIVIDE_AS_FRACTION", ["YES", "NO"], "YES")
openmath.config.addKeyVal("HIDE_SQRT", ["YES", "NO"], "YES")
openmath.config.addKeyVal("HIDE_TIMES", ["YES", "NO"], "YES")
openmath.config.addKeyVal("TIMES_SYMBOL", ["DOT", "X"], "X")

__invisible_times = Symbol("invisible_times", "arith1") # MADE UP FOR +HIDE_TIMES=YES
priority = [
    __invisible_times,
    Symbol("factorial", "integer1"),    
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

unary_minus = ("-", "prefix")

minus = ("-", "infix")

def times(*args):
    if openmath.config.get("TIMES_SYMBOL") == "X":
        sym = " \\times "
    elif openmath.config.get("TIMES_SYMBOL") == "DOT":
        sym = " \\;\\cdot\\; "
        
    if openmath.config.get("HIDE_TIMES") == "NO":
        return sym.join(evalAndEnclose(x, Symbol("times", "arith1")) for x in args)
    
    is_int_or_float = lambda om: om is not None and om.kind in ["OMF", "OMI"]
    [first, *rest] = args
    ret = evalAndEnclose(first, __invisible_times)
    last_is_num = is_int_or_float(first)
    
    '''
    while len(rest) > 1:
        [prev, curr, *nexts] = rest
        rest = rest[1:]
        is_prev_num = is_int_or_float(prev)
    '''
    for a in rest:
        is_num = a.kind in ["OMF", "OMI"]
        if is_num and last_is_num:
            ret += sym + evalAndEnclose(a, Symbol("times", "arith1"))
        else:
            ret += " " + evalAndEnclose(a, __invisible_times)
         
        last_is_num = is_num

    return ret

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
    "times",
    "sum",
    "product"
]