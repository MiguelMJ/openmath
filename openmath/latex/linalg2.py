"""https://openmath.org/cd/linalg2"""


def matrix(*args):
    """https://openmath.org/cd/linalg2#matrix"""
    return "\\begin{pmatrix} %s \\end{pmatrix}" %  " \\\\ ".join(args)

def matrixrow(*args):
    """https://openmath.org/cd/linalg2#matrixrow"""
    return " & ".join(args)

def vector(*args):
    """https://openmath.org/cd/linalg2#vector"""
    return " , ".join(args)