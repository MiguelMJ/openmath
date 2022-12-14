"""https://openmath.org/cd/arith1.html"""
from functools import reduce
import math

def lcm(*args):
    """http://www.openmath.org/cd/arith1#lcm"""
    x = max(args)
    while not all(x % a == 0 for a in args):
        x += 1
    return x

def gcm(*args):
    """http://www.openmath.org/cd/arith1#gcm"""
    x = min(args)
    while not all(a % x == 0 for a in args):
        x -= 1
    return x

def plus(*args):
    """http://www.openmath.org/cd/arith1#plus"""
    return reduce(lambda a,b: a+b, args, 0)

def unary_minus(x):
    """http://www.openmath.org/cd/arith1#unary_minus"""
    return -x

def minus(a,b):
    """http://www.openmath.org/cd/arith1#minus"""
    return a-b

def times(*args):
    """http://www.openmath.org/cd/arith1#times"""
    return reduce(lambda a,b: a*b, args, 1)

def divide(a,b):
    """http://www.openmath.org/cd/arith1#divide"""
    return a/b

def power(a,b):
    """http://www.openmath.org/cd/arith1#power"""
    return a**b

def abs(a):
    """http://www.openmath.org/cd/arith1#abs"""
    return math.abs(a)

def root(a,b):
    """http://www.openmath.org/cd/arith1#root"""
    return a ** (1.0/b)

def sum(a,b):
    """http://www.openmath.org/cd/arith1#sum"""
    return reduce(lambda v1,v2: v1+v2, (b(v) for v in a), 0)

def product(a,b):
    """http://www.openmath.org/cd/arith1#product"""
    return reduce(lambda v1,v2:v1*v2, (b(v) for v in a), 1)
