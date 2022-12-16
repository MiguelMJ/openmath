"""https://openmath.org/cd/logic1"""

"""https://openmath.org/cd/logic1#true"""
true = True

"""https://openmath.org/cd/logic1#false"""
false = False

def and_(*ps):
    """https://openmath.org/cd/logic1#and"""
    return all(ps)

def equivalent(a, b):
    """https://openmath.org/cd/logic1#equivalent"""
    raise NotImplementedError("logic1.equivalent")

def implies(a, b):
    """https://openmath.org/cd/logic1#implies"""
    return not a or b

def nand(*ps):
    """https://openmath.org/cd/logic1#nand"""
    return not all(ps)

def nor(*ps):
    """https://openmath.org/cd/logic1#nor"""
    return not any(ps)

def not_(p):
    """https://openmath.org/cd/logic1#not"""
    return not p

def or_(*ps):
    """https://openmath.org/cd/logic1#or"""
    return any(ps)

def xnor(*ps):
    """https://openmath.org/cd/logic1#xnor"""
    return len([p for p in ps if p]) % 2 == 0

def xor(*ps):
    """https://openmath.org/cd/logic1#xor"""
    return len([p for p in ps if p]) % 2 == 1

locals()["not"] = not_
locals()["or"] = or_
locals()["and"] = and_