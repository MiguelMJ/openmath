import openmath.latex as latex
import latex2mathml.converter

def eval(om):
    return latex2mathml.converter.convert(latex.eval(om))