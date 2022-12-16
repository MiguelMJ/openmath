"""https://openmath.org/cd/logic1"""

import openmath.config
from openmath.latex import eval
from openmath import Application, Symbol

openmath.config.addKeyVal("TRUE_SYMBOL", None, "T")
openmath.config.addKeyVal("FALSE_SYMBOL", None, "F")
openmath.config.addKeyVal("LOGICAL_NEGATION", ["SYMBOL", "NEGATION", "BAR"], "BAR")

priority = [
    Symbol("not", "logic1"),
    Symbol("and", "logic1"),
    Symbol("xor", "logic1"),
    Symbol("or", "logic1"),
]

"""https://openmath.org/cd/logic1#true"""
true = openmath.config.get("TRUE_SYMBOL")

"""https://openmath.org/cd/logic1#false"""
false = openmath.config.get("FALSE_SYMBOL")

"""https://openmath.org/cd/logic1#and"""
and_ = ("\\wedge", "infix")

"""https://openmath.org/cd/logic1#equivalent"""
equivalent = ("\\equiv", "infix")

"""https://openmath.org/cd/logic1#implies"""
implies = ("\\Rightarrow", "infix")

"""https://openmath.org/cd/logic1#or"""
or_ = ("\\vee", "infix")

"""https://openmath.org/cd/logic1#xor"""
xor = ("\\oplus", "infix")


if openmath.config.get("LOGICAL_NEGATION") == "SYMBOL":
    """https://openmath.org/cd/logic1#not"""
    not_ = ("¬", "prefix")

    """https://openmath.org/cd/logic1#nand"""
    nand = ("\\barwedge", "infix")

    """https://openmath.org/cd/logic1#nor"""
    nor = ("\\downarrow", "infix")

    """https://openmath.org/cd/logic1#xnor"""
    xnor = ("\\leftrightarrow", "infix")

else:
    special = [
        "nand",
        "nor",
        "xnor",
    ]
    omneg = Symbol("not", "logic1")
    omand = Symbol("and", "logic1")
    omor = Symbol("or", "logic1")
    omxor = Symbol("xor", "logic1")
    nand = lambda *args: eval(Application(omneg, Application(omand, *args)))
    nor = lambda *args: eval(Application(omneg, Application(omor, *args)))
    xnor = lambda *args: eval(Application(omneg, Application(omxor, *args)))
    
    if openmath.config.get("LOGICAL_NEGATION") == "NEGATION":
        not_ = ("¬", "prefix")
    elif openmath.config.get("LOGICAL_NEGATION") == "BAR":
        not_ = lambda x: "\\bar{%s}" % x

locals()["not"] = not_
locals()["or"] = or_
locals()["and"] = and_