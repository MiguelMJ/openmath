"""https://openmath.org/cd/list1"""

def list_(*args):
    """https://openmath.org/cd/list1#list"""
    return args

def map(f, a):
    """https://openmath.org/cd/list1#map"""
    return [f(x) for x in a]

def suchthat(a, p):
    """https://openmath.org/cd/list1#suchthat"""
    return [x for x in a if p(x)]

locals()["list"] = list_