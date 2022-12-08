lcm=("lcm", "application")
gcm=("gcm", "application")
plus=("+", "infix")
unary_minus=("-", "prefix")
minus=("-", "infix")
times=("\\times", "infix")
def divide(a,b):
    return "\\frac{%s}{%s}" % (a,b)
def power(a,b):
    return "%s^{%s}" % (a,b)
abs=("abs", "application")
def root(a,b):
    return "\\sqrt[%s]{%s}" % (b,a)
#sum
#product