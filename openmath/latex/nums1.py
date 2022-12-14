"""https://openmath.org/cd/nums1"""

def based_integer(a,b):
    """https://openmath.org/cd/nums1#based_integer"""
    return "%s_{%s}" % (b,a)

def based_float(a,b):
    """https://openmath.org/cd/nums1#based_float"""
    return "%s_{%s}" % (b,a)
    
def rational(a,b):
    """https://openmath.org/cd/nums1#rational"""
    return "\\frac{%s}{%s}" % (a,b)
    
"""https://openmath.org/cd/nums1#infinity"""
infinity = "\\infty"

"""https://openmath.org/cd/nums1#e"""
e = "e"

"""https://openmath.org/cd/nums1#i"""
i = "i"

"""https://openmath.org/cd/nums1#pi"""
pi = "\\pi"

"""https://openmath.org/cd/nums1#gamma"""
gamma = "\\gamma"

"""https://openmath.org/cd/nums1#NaN"""
NaN = "NaN"