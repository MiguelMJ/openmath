"""

"""
import json
import xml.etree.ElementTree as ET
from copy import deepcopy
from xml.dom import minidom


class _OMBase():
    version="2.0"
    parent=None

    def _customdict(self):
        d = self.__dict__
        return {
            "kind": self.kind,
            **{
                k: d[k] 
                for k 
                in sorted(d.keys())
                if d[k] is not None and k != "parent"
            }
        }
    
    def toJSON(self, *args, **kargs):
        return json.dumps(self, default=_OMBase._customdict, *args, **kargs)

    def toElement(self):
        raise NotImplementedError("OpenMath XML encoding")

    def toXML(self, *args, **kargs):
        tostringaccepted = ["encoding", "method", "xml_declaration", "default_namespace", "short_empty_elements"]
        tostringkargs = {k:kargs[k] for k in kargs if k in tostringaccepted}
        root = self.toElement()
        root.set("xmlns", "http://www.openmath.org/OpenMath")
        ret = ET.tostring(root, *args, **tostringkargs).decode("utf8")
        toprettyaccepted = ["indent", "newl", "encoding", "standalone"]
        toprettykargs = {k:kargs[k] for k in kargs if k in toprettyaccepted}
        if any(x in kargs for x in toprettykargs if x != "encoding"):
            if type(kargs.get("indent")) is int:
                toprettykargs["indent"] *= " "
            ret = minidom.parseString(ret).toprettyxml(**toprettykargs)
        return ret

    def isValid(self):
        return True
    
    def hasValidCDBase(self):
        return not hasattr(self, "cdbase") or self.cdbase == None or type(self.cdbase) is str
    
    applydepth = 0
    def apply(self, f, accumulator=None):
        _OMBase.applydepth += 1
        mydepth = _OMBase.applydepth
        if accumulator is None:
            accumulator = []

        if any(self is x for x in accumulator):
            return
        else:
            accumulator.append(self)
        
        f(self) 
        d = self._customdict()
        for k in list(d.keys())[::-1]: # reversed keys
            if isinstance(d[k], _OMBase):
                d[k].apply(f, accumulator)
            elif type(d[k]) is list:
                for i,a in enumerate(d[k]):
                    if isinstance(a, _OMBase):
                        a.apply(f, accumulator)
                    elif type(a) is list:
                        for j,b in enumerate(a):
                            if isinstance(b, _OMBase):
                                b.apply(f, accumulator)
        _OMBase.applydepth -= 1

    def getCDBase(self):
        if "cdbase" not in dir(self) or self.cdbase is None:
            if self.parent is None:
                return None
            return self.parent.getCDBase()
        return self.cdbase

    def replace(self, obj1, obj2):
        d = self.__dict__
        for k in d:
            if obj1 is d[k]:
                d[k] = deepcopy(obj2)
                d[k].parent = self
            elif type(d[k]) is list and not (k == "variables" and self.kind == "OMBIND"):
                for i,elem in enumerate(d[k]):
                    if obj1 is elem:
                        d[k][i] = deepcopy(obj2)
                        d[k][i].parent = self
                    elif type(elem) is list:
                        for j,subelem in enumerate(elem):
                            if subelem is obj1:
                                elem[j] = deepcopy(obj2)
                                elem[j].parent = self

    def __eq__(self, other):
        if not isinstance(other, _OMBase):
            return False
        a = self._customdict()
        b = other._customdict()
        allkeys = set([*a, *b])
        
        if "cdbase" in allkeys:
            if self.getCDBase() != self.getCDBase():
                return False
            allkeys.remove("cdbase")
        
        def compare(x,y):
            ret = None
            if type(x) is list and type(y) is list:
                ret = len(x) == len(y) and all(compare(x[i], y[i]) for i in range(len(x)))
            else:
                ret = x == y
            return ret

        return all(compare(a.get(k), b.get(k)) for k in allkeys)
             
    def __str__(self):
        return "OM"+str(self._customdict())
    
    def __repr__(self):
        return "OM"+repr(self._customdict())

class Object(_OMBase):
    kind="OMOBJ"
    def __init__(self, object, **kargs):
        self.object = object
        object.parent = self
        self.xmlns = None
        self.version = None
        self.cdbase = None
        self.parent = kargs.get("parent")
        for k in kargs:
            setattr(self, k, kargs[k])
    
    def isValid(self):
        return self.hasValidCDBase and self.object.isValid()
    
    def toElement(self):
        el = ET.Element(self.kind)
        el.set("xmlns", self.xmlns) if self.xmlns is not None else None
        el.set("version", self.version) if self.version is not None else None
        el.set("cdbase", self.cdbase) if self.cdbase is not None else None
        el.append(self.object.toElement())
        return el
        
class Integer(_OMBase):
    kind="OMI"
    def __init__(self, integer):
        self.integer = integer
    
    def isValid(self):
        return type(self.integer) is int
    
    def toElement(self):
        el = ET.Element(self.kind)
        el.text = str(self.integer)
        return el

class Float(_OMBase):
    kind="OMF"
    def __init__(self, float):
        self.float = float
    
    def isValid(self):
        return type(self.float) is float

    def toElement(self):
        el = ET.Element(self.kind)
        el.text = str(self.float)
        return el

class String(_OMBase):
    kind="OMSTR"
    def __init__(self, string):
        self.string = string
    
    def isValid(self):
        return type(self.string) is str

    def toElement(self):
        el = ET.Element(self.kind)
        el.text = self.string
        return el

class Bytearray(_OMBase):
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

class Symbol(_OMBase):
    kind="OMS"
    def __init__(self, name, cd, cdbase=None):
        self.cdbase = cdbase
        self.cd = cd
        self.name = name

    def isValid(self):
        return type(self.cd) is str and type(self.name) is str and self.hasValidCDBase()

    def toElement(self):
        el = ET.Element(self.kind)
        el.set("name", self.name)
        el.set("cd", self.cd)
        if self.cdbase is not None:
            el.set("cdbase", self.cdbase)
        return el

class Variable(_OMBase):
    kind="OMV"
    def __init__(self, name):
        self.name = name

    def toElement(self):
        el = ET.Element(self.kind)
        el.set("name", self.name)
        return el

class Application(_OMBase):
    kind="OMA"
    def __init__(self, applicant, *arguments, cdbase=None):
        self.cdbase = cdbase
        self.applicant = applicant
        applicant.parent = self
        self.arguments = list(arguments)
        for a in self.arguments:
            a.parent = self
    
    def isValid(self):
         return self.hasValidCDBase() and self.applicant.isValid() and all(a.isValid() for a in self.arguments)

    def toElement(self):
        el = ET.Element(self.kind)
        if self.cdbase is not None:
            el.set("cdbase", self.cdbase)
        el.append(self.applicant.toElement())
        for a in self.arguments:
            el.append(a.toElement())
        return el

class Attribution(_OMBase):
    kind="OMATTR"
    def __init__(self, attributes, object, cdbase=None):
        self.cdbase = attributes
        self.attributes = attributes
        for pair in self.attributes:
            for elem in pair:
                elem.parent = self
        self.object = object
        object.parent = self
    
    def isValid(self):
        return self.hasValidCDBase() and self.object.isValid() and all(isinstance(a, Symbol) and a.isValid() and b.isValid() for [a,b] in attributes) 

    def toElement(self):
        el = ET.Element(self.kind)
        if self.cdbase is not None:
            el.set("cdbase", self.cdbase)
        attrs = ET.Element("OMATP")
        for [a, b] in self.attributes:
            attrs.append(a.toElement(), b.toElement())
        el.append(attrs)
        el.append(self.object.toElement())
        return el

class Binding(_OMBase):
    kind="OMBIND"
    def __init__(self, binder, variables, object, cdbase=None):
        self.cdbase = cdbase
        self.binder = binder
        self.variables = variables
        self.object = object
        binder.parent = self
        for v in self.variables:
            v.parent = self
        object.parent = self

    def isValid(self):
        if len(self.variables) == 0 or (self.cdbase is not None and type(self.cdbase) is not str):
            return False
        for v in self.variables:
            isVariable = type(v) is Variable
            isAttributedVariable = type(v) is Attribution and type(v.object) is Variable
            if not isVariable and not isAttributedVariable:
                return False
        return  self.hasValidCDBase()
    
    def toElement(self):
        el = ET.Element(self.kind)
        if self.cdbase is not None:
            el.set("cdbase", self.cdbase)
        el.append(self.binder.toElement())
        variables = ET.Element("OMBVAR")
        for v in self.variables:
            variables.append(v.toElement())
        el.append(variables)
        el.append(self.object.toElement())
        
        return el

class Error(_OMBase):
    kind="OME"
    def __init__(self, error, arguments):
        self.error = error
        error.parent = self
        self.arguments = arguments
        for a in arguments:
            a.parent = self
    
    def isValid(self):
        return type(self.error) is Symbol

    def toElement(self):
        el = ET.Element(self.kind)
        el.append(self.error.toElement())
        for a in self.arguments:
            el.append(a.toElement())
        return el

def parse(text):
    try:
        return parseJSON(text)
    except json.JSONDecodeError:
        return parseXML(text)

def parseJSON(text):
    return fromDict(json.loads(text))

def parseXML(text):
    return fromElement(ET.fromstring(text))

def fromDict(dictionary):
    match(dictionary):
        
        case {"kind": "OMOBJ", **kargs}:
            return Object(
                fromDict(kargs["object"]), 
                cdbase=kargs.get("cdbase"), 
                version=kargs.get("version"),
                xmlns=kargs.get("xmlns")
            )
        
        case {"kind": "OMI", "integer": x, **kargs}:
            return Integer(int(x))

        case {"kind": "OMI", "decimal": x, **kargs}:
            return Integer(int(x))
        
        case {"kind": "OMI", "hexadecimal": x, **kargs}:
            return Integer(int(x, 16))
        
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
            return Symbol(kargs["name"], kargs["cd"], cdbase=kargs.get("cdbase"))
        
        case {"kind": "OMBIND", **kargs}:
            return Binding(
                fromDict(kargs["binder"]),
                [fromDict(v) for v in kargs["variables"]],
                fromDict(kargs["object"]),
                cdbase=kargs.get("cdbase")
            )
        
        case {"kind": "OMATTR", **kargs}:            
            recFromDict = lambda x: fromDict(x) if type(x) is not list else [recFromDict(xx) for xx in x]
            return Attribution(
                recFromDict(kargs["attributes"]),
                fromDict(kargs["object"]), 
                kargs.get("cdbase")
            )

        case {"kind": "OME", **kargs}:
            return Error(kargs["error"], kargs.get("arguments"))

        case _:
            raise ValueError("A valid dictionary is required")

def fromElement(elem):
    # handle xml namespaces
    if elem.tag[0] == "{":
        [ns, tag] = elem.tag[1:].split("}")
    else:
        ns = None
        tag = elem.tag

    def qname(t):
        return t if ns is None else ("{%s}%s" % (ns, t))
    
    match tag:
        case "OMOBJ":
            return Object(fromElement(elem[0]), **elem.attrib)

        case "OMI":
            if elem.text.strip()[0] == "x":
                return Integer(int(elem.text.strip()[1:]))
            elif elem.text.strip()[:2] == "-x":
                return Integer(-int(elem.text.strip()[2:]))
            else:
                return Integer(int(elem.text.strip()))
        
        case "OMF":
            if "dec" in elem.attrib:
                return Float(float(elem.attrib["dec"]))
            else:
                return Float(float(elem.attrib["hex"]))
            
        case "OMS":
            return Symbol(elem.attrib["name"], elem.attrib["cd"], elem.attrib.get("cdbase"))

        case "OMV":
            return Variable(elem.attrib["name"])

        case "OMSTR":
            return String(elem.text)

        case "OMB":
            raise NotImplementedError("XML encoded OpenMath Bytearrays")

        case "OMA":
            return Application(fromElement(elem[0]), *[fromElement(x) for x in elem[1:]], cdbase=elem.attrib.get("cdbase"))
        
        case "OMATTR":
            obj = None
            attrs = []
            for child in elem:
                if child.tag == "OMATP":
                    key = None
                    for i,x in enumerate(child):
                        if i % 2 == 0 and key is not None:
                            attrs.append([fromElement(key), fromElement(x)])
                        else:
                            key = x
                else:
                    obj = fromElement(child)
            return Attribution(attrs, obj, cdbase=elem.attrib.get("cdbase"))

        case "OME":
            return Error(fromElement(elem[0]), [fromElement(x) for x in elem[1:]])
        
        case "OMBIND":
            return Binding(
                fromElement(elem[0]),
                [fromElement(x) for x in elem.find(qname("OMBVAR"))],
                fromElement(elem[2])
            )

        case _:
            raise ValueError("A valid ElementTree is required: %s" % elem)
