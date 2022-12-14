"""https://openmath.org/cd/interval1.html"""
import math

def integer_interval(a, b):
    """https://openmath.org/cd/interval1.html#integer_interval"""
    return range(a,b+1)

class FloatRange():
    """Class for floating point ranges

    Arguments
        a -- first end point
        b -- last end point
        mode -- a two string character where 'c' means closed and 'o' means
            open. Example: use "co" for a closed-open interval.
    """
    def __init__(self, a, b, mode):
        if mode[0] == "c":
            self.latest = a
        elif mode[0] == "o":
            self.latest = math.nextafter(a, math.inf)
        if mode[1] == "c":
            self.last = b
        elif mode[1] == "o":
            self.last = math.nextafter(b, -math.inf)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.latest > self.last:
            raise StopIteration
        ret = self.latest
        self.latest = math.nextafter(self.latest, self.last)
        return ret

def interval(a, b):
    """https://openmath.org/cd/interval1.html#interval"""
    return FloatRange(a, b, "cc")

def interval_cc(*args):
    """https://openmath.org/cd/interval1.html#interval_cc"""
    return FloatRange(a, b, "cc")
    

def interval_co(*args):
    """https://openmath.org/cd/interval1.html#interval_co"""
    return FloatRange(a, b, "co")

def interval_oc(*args):
    """https://openmath.org/cd/interval1.html#interval_oc"""
    return FloatRange(a, b, "oc")

def interval_oo(*args):
    """https://openmath.org/cd/interval1.html#interval_oo"""
    return FloatRange(a, b, "oo")

def oriented_interval(*args):
    """https://openmath.org/cd/interval1.html#oriented_interval"""
    return FloatRange(a, b, "cc")
    
