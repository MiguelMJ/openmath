"""http://www.openmath.org/cd/limit1.py"""

from openmath.latex import eval
import openmath.config

openmath.config.addKeyVal("LIMITS_AS_SUBSCRIPT", ["YES", "NO"], "NO")

special = [
    "limit"
]

def limit(a,b,c):
    """http://www.openmath.org/cd/limit1.py#limit"""
    tup = (c.variables[0].name, eval(a), eval(b), eval(c.object))
    if openmath.config.get("LIMITS_AS_SUBSCRIPT") == "YES":
        return "\\lim_{ %s \\to %s%s } %s" % tup
    return "\\lim\\limits_{ %s \\to %s%s } %s" % tup

"""http://www.openmath.org/cd/limit1.py#above"""
above = "^{+}"

"""http://www.openmath.org/cd/limit1.py#below"""
below = "_{-}+"

"""http://www.openmath.org/cd/limit1.py#both_sides"""
both_sides = ""

"""http://www.openmath.org/cd/limit1.py#null"""
null = ""
