"""https://openmath.org/cd/complex1"""

import math
import cmath

def argument(c):
    """https://openmath.org/cd/complex1#argument"""
    return math.atan2(c.imag, c.real)

def complex_cartesian(r, i):
    """https://openmath.org/cd/complex1#complex_cartesian"""
    return r + i * 1j

def complex_polar(r, a):
    """https://openmath.org/cd/complex1#complex_polar"""
    return cmath.rect(r, a)

def conjugate(c):
    """https://openmath.org/cd/complex1#conjugate"""
    return c.conjugate()

def imaginary(c):
    """https://openmath.org/cd/complex1#imaginary"""
    return c.imag

def real(c):
    """https://openmath.org/cd/complex1#real"""
    return c.real