"""https://openmath.org/cd/complex1"""

import cmath
from openmath import Symbol, Application, Float
from openmath.latex import eval
from openmath.util import asOM
import openmath.config

openmath.config.addKeyVal("COMPLEX_NUMBER_REPRESENTATION", ["ADDITION", "TUPLE"], "ADDITION")

"""https://openmath.org/cd/complex1#argument"""
argument = ("arg", "call")

def complex_cartesian(r, i):
    """https://openmath.org/cd/complex1#complex_cartesian"""
    r = float(r)
    i = float(i)
    return eval(Application(Symbol("plus", "arith1"), asOM(r), Application(Symbol("times", "arith1"), asOM(i), Symbol("i", "nums1"))))

def complex_polar(r, a):
    """https://openmath.org/cd/complex1#complex_polar"""
    c = cmath.rect(float(r), float(a))
    return complex_cartesian(c.real, c.imag)

def conjugate(c):
    """https://openmath.org/cd/complex1#conjugate"""
    return c.conjugate()

"""https://openmath.org/cd/complex1#imaginary"""
imaginary = ("Im", "call")

"""https://openmath.org/cd/complex1#real"""
real = ("Re", "call")
