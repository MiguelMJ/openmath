"""https://openmath.org/cd/nums1"""

import math

def based_integer(a,b):
    """https://openmath.org/cd/nums1#based_integer"""
    return int(b,a)

def based_float(a,b):
    """https://openmath.org/cd/nums1#based_float"""
    raise NotImplementedError("based_float")

def rational(a,b):
    """https://openmath.org/cd/nums1#rational"""
    return a / b

"""https://openmath.org/cd/nums1#infinity"""
infinity = math.inf

"""https://openmath.org/cd/nums1#e"""
e = math.e

"""https://openmath.org/cd/nums1#i"""
i = 1j

"""https://openmath.org/cd/nums1#pi"""
pi = math.pi

"""https://openmath.org/cd/nums1#gamma"""
gamma = 0.577215664

"""https://openmath.org/cd/nums1#NaN"""
NaN = math.nan