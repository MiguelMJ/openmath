"""
"""
import json
import xml.etree.ElementTree as ET


class __OMBase():
    def toJSON(self, *args, **kargs):
        def customdict(self):
            return {
                **{
                    k:self.__dict__[k] 
                    for k 
                    in self.__dict__
                    if self.__dict__[k] is not None
                }, 
                "kind": self.kind
            }
        return json.dumps(self, default=customdict, *args, **kargs)
        
    def isValid(self):
        return True
    
    def hasValidCDBase(self):
        return not hasattr(self, "cdbase") or self.cdbase == None or type(self.cdbase) is str
    
    def __str__(self):
        return self.kind+str(self.__dict__)
    
    def __repr__(self):
        return self.kind+repr(self.__dict__)

class Object(__OMBase):
    kind="OMOBJ"
    def __init__(self, object, **kargs):
        self.object = object
        for k in kargs:
            self.setattr(k, kargs[k])

class Integer(__OMBase):
    kind="OMI"
    def __init__(self, integer):
        self.integer = integer
    
    def isValid(self):
        return type(self.integer) is int

class Float(__OMBase):
    kind="OMF"
    def __init__(self, float):
        self.float = float
    
    def isValid(self):
        return type(self.float) is float

class String(__OMBase):
    kind="OMSTR"
    def __init__(self, string):
        self.string = string
    
    def isValid(self):
        return type(self.string) is str

class Bytearray(__OMBase):
    kind="OMB"
    def __init__(self, bytes):
        self.bytes = bytes
    
    def isValid(self):
        if type(self.bytes) is not list:
            return False
        for b in self.bytes:
            if type(b) is not int or b < 256:
                return False
        return True

class Symbol(__OMBase):
    kind="OMS"
    def __init__(self, name, cdbase=None):
        self.cdbase = cdbase
        self.name = name
    
    def isValid(self):
        return type(self.name) is str and self.hasValidCDBase()

class Variable(__OMBase):
    kind="OMV"
    def __init__(self, name):
        self.name = name

class Application(__OMBase):
    kind="OMA"
    def __init__(self, applicant, *arguments, cdbase=None):
        self.cdbase = cdbase
        self.applicant = applicant
        self.arguments = list(arguments)
    
    def isValid():
         return self.hasValidCDBase()

class Attribution(__OMBase):
    kind="OMATTR"
    def __init__(self, cdbase, attributes, object):
        self.cdbase = attributes
        self.attributes = attributes
        self.object = object
    
    def isValid(self):
        for [k,v] in self.attributes:
            if i%2 == 1 and type(x) is not Symbol:
                return False
        return self.hasValidCDBase()

class Binding(__OMBase):
    kind="OMBIND"
    def __init__(self, binder, variables, object, cdbase=None):
        self.cdbase = cdbase
        self.binder = binder
        self.variables = variables
        self.object = object

    def isValid(self):
        if len(variables) == 0 or (cdbase is not None and type(cdbase) not is str):
            return False
        for v in self.variables:
            isVariable = type(v) is Variable
            isAttributedVariable = type(v) is Attribution and type(v.object) is Variable
            if not isVariable and not isAttributedVariable:
                return False
        return  self.hasValidCDBase()

class Error(__OMBase):
    kind="OME"
    def __init__(self, error, arguments):
        self.error = error
        self.arguments = arguments
    
    def isValid(self):
        return type(self.error) is Symbol

def parseJSON(text):
    return fromDict(json.loads(text))

def fromDict(dictionary):
    match(dictionary):
        
        case {"kind": "OMOBJ", **kargs}:
            return Object(fromDict(kargs["object"]), cdbase)
        
        case {"kind": "OMI", "integer": x, **kargs}:
            return Integer(int(x))

        case {"kind": "OMI", "decimal": x, **kargs}:
            return Integer(int(x))
        
        case {"kind": "OMI", "hexadecimal": x, **kargs}:
            return Integer(int(x, 16))
            return Object(fromDict(kargs["object"]))
        
        case {"kind": "OMF", "integer": x, **kargs}:
            return Float(float(x))

        case {"kind": "OMF", "decimal": x, **kargs}:
            return Float(float(x))
        
        case {"kind": "OMF", "hexadecimal": x, **kargs}:
            return Float(float(x, 16))

        case {"kind": "OMSTR", **kargs}:
            return Bytearray(kargs["string"])

        case {"kind": "OMB", **kargs}:
            return Bytearray(kargs["bytes"])

        case {"kind": "OMA", **kargs}:
            return Application(
                fromDict(kargs["applicant"]),
                *[fromDict(a) for a in kargs.get("arguments", [])],
                cdbase=kargs.get("cdbase")
                )

        case {"kind": "OMV", **kargs}:
            return Variable(kargs["name"])

        case {"kind": "OMS", **kargs}:
            return Symbol(kargs["name"], cdbase=kargs.get("cdbase"))
        
        case _:
            print("?")
            return None


print(fromDict({"kind":"OMI", "hexadecimal":"10"}))
ap = Application(Symbol("plus"), Variable("x"), Variable("y"))
print(ap)
ap.arguments.append(Integer(3))
apjson = ap.toJSON(indent=2)
print(apjson)
print(fromDict(json.loads(apjson)))