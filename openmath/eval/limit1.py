"""http://www.openmath.org/cd/limit1.py"""

import math

def limit(a,b,c):
    """http://www.openmath.org/cd/limit1.py#limit"""
    if b == "above":
        if a != -math.inf:
            a = math.nextafter(a, math.inf)
        return c(a)
    if b == "below":
        if a != math.inf:
            a = math.nextafter(a, -math.inf)
        return c(a)
    if b == "both_sides":
        above = c(math.nextafter(a, math.inf))
        below = c(math.nextafter(a, -math.inf))
        if above == below:
            return above
        return math.nan
    if b == "null":
        if a >= 0:
            return limit(a, "below", c)
        else:
            return limit(a, "above", c)

"""http://www.openmath.org/cd/limit1.py#above"""
above = "above"

"""http://www.openmath.org/cd/limit1.py#below"""
below = "below"

"""http://www.openmath.org/cd/limit1.py#both_sides"""
both_sides = "both_sides"

"""http://www.openmath.org/cd/limit1.py#null"""
null = "null"
