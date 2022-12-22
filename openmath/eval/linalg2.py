"""https://openmath.org/cd/linalg2"""


def matrix(*args):
    """https://openmath.org/cd/linalg2#matrix"""
    assert all(len(a) == 1 for a in args), "matrix needs matrixrows"
    assert len(set(len(a[0]) for a in args)) == 1, "matrixrows must be same length"
    return [a[0] for a in args]

def matrixrow(*args):
    """https://openmath.org/cd/linalg2#matrixrow"""
    return [args]

def vector(*args):
    """https://openmath.org/cd/linalg2#vector"""
    return [args]