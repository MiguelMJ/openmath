import openmath.latex as latex
import openmath.config
import latex2mathml.converter

openmath.config.addKeyVal("MATHML_DISPLAY", ["INLINE", "BLOCK"], "INLINE")

def eval(om):
    return latex2mathml.converter.convert(latex.eval(om), display=openmath.config.get("MATHML_DISPLAY").lower())