"""https://openmath.org/cd/relation1"""

import math
import openmath.config

openmath.config.addKeyVal("RELATIVE_TOLERANCE", None, 1e-09)
openmath.config.addKeyVal("ABSOLUTE_TOLERANCE", None, 0.0)

def approx(a, b):
    """https://openmath.org/cd/relation1#approx"""
    return math.isclose(a, b, rel_tol=float(openmath.config.get("RELATIVE_TOLERANCE")), abs_tol=float(openmath.config.get("ABSOLUTE_TOLERANCE")))

def eq(a,b):
    """https://openmath.org/cd/relation1#eq"""
    return a == b

def geq(a, b):
    """https://openmath.org/cd/relation1#geq"""
    return a >= b

def gt(a,b):
    """https://openmath.org/cd/relation1#gt"""
    return a > b

def leq(a, b):
    """https://openmath.org/cd/relation1#leq"""
    return a <= b

def lt(a,b):
    """https://openmath.org/cd/relation1#lt"""
    return a < b

def neq(a, b):
    """https://openmath.org/cd/relation1#neq"""
    return a != b
