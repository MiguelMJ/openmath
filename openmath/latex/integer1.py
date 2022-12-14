"""https://openmath.org/cd/integer1.html"""

factorof = ("factorof", "call")

def factorial(x):
    if " " in x:
        return f"\\left( {x}  \\right) !"
    return x + " !"

quotient = ("quotient", "call")
remainder = ("remainder", "call")