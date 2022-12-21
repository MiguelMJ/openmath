"""https://openmath.org/cd/list1"""

import re 
import openmath.latex.set1
import openmath.config

openmath.config.addKeyVal("LIST_STYLE", ["BRACKETS", "CALL"], "CALL")

"""https://openmath.org/cd/list1#list"""
def list_(*args):
    if openmath.config.get("LIST_STYLE") == "BRACKETS":
        fmt = "\\left[ %s \\right]"
    else:
        fmt = "list\\left( %s \\right)"
    return fmt % ", ".join(args)

def map(f, a):
    """https://openmath.org/cd/list1#map"""
    return list_(re.sub(r"^\S* | \S*$","",openmath.latex.set1.map(f,a)))

def suchthat(a, p):
    """https://openmath.org/cd/list1#suchthat"""
    return list_(re.sub(r"^\S* | \S*$","",openmath.latex.set1.suchthat(a,p)))

special = [
    "map",
    "suchthat"
]

locals()["list"] = list_