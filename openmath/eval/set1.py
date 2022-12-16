"""http://www.openmath.org/cd/set1"""

import itertools

pyset = set

def cartesian_product(*sets):
    """http://www.openmath.org/cd/set1#emptyset"""
    return itertools.product(*sets)

"""http://www.openmath.org/cd/set1#emptyset"""
emptyset = pyset()

def in_(x,a):
    """http://www.openmath.org/cd/set1#in"""
    return x in a

def intersect(*sets):
    """http://www.openmath.org/cd/set1#intersect"""
    return sets[0].intersection(*sets[1:])

def map(f, a):
    """http://www.openmath.org/cd/set1#map"""
    global pyset
    return pyset(f(x) for x in a)

def notin(x, a):
    """http://www.openmath.org/cd/set1#notin"""
    return x not in a

def notprsubset(a, b):
    """http://www.openmath.org/cd/set1#notprsubset"""
    return not a < b 

def notsubset():
    """http://www.openmath.org/cd/set1#notsubset"""
    return not a <= b

def prsubset():
    """http://www.openmath.org/cd/set1#prsubset"""
    return a < b

def set_(*args):
    """http://www.openmath.org/cd/set1#set"""
    global pyset
    return pyset(args)

def setdiff(a, b):
    """http://www.openmath.org/cd/set1#setdiff"""
    return a - b

def size(a):
    """http://www.openmath.org/cd/set1#size"""
    return len(a)

def subset(a, b):
    """http://www.openmath.org/cd/set1#subset"""
    return a <= b

def suchthat(a, f):
    """http://www.openmath.org/cd/set1#suchthat"""
    global pyset
    return pyset(x for x in a if f(x))

def union(*sets): 
    """http://www.openmath.org/cd/set1#union"""
    return sets[0].union(*sets[1:])

locals()["in"] = in_
locals()["set"] = set_