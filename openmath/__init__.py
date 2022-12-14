"""OpenMath standard implementation

This module provides class and functions to
work with OpenMath mathematical objects
"""
import json
import xml.etree.ElementTree as ET
from copy import deepcopy
from xml.dom import minidom


class _OMBase:
    """Base class for OpenMath objects"""

    parent = None

    def _customdict(self) -> dict:
        """Get a dictionary with the attributes of the math object"""
        d = self.__dict__
        return {
            "kind": self.kind,
            **{k: d[k] for k in sorted(d.keys()) if d[k] is not None and k != "parent"},
        }

    def toJSON(self, *args, **kargs) -> str:
        """Serialize the object to a JSON string

        All arguments are passed directly to the json.dumps function
        """
        return json.dumps(self, default=_OMBase._customdict, *args, **kargs)

    def toElement(self):
        """Return the object as an XML element from the xml.etree module"""
        raise NotImplementedError("OpenMath XML encoding")

    def toXML(self, *args, **kargs) -> str:
        """Serialize the object to a XML string

        The arguments can be any of those accepted by either the
        xml.etree.ElementTree.toString function or minidom.prettyxml
        """
        tostringaccepted = [
            "encoding",
            "method",
            "xml_declaration",
            "default_namespace",
            "short_empty_elements",
        ]
        tostringkargs = {k: kargs[k] for k in kargs if k in tostringaccepted}
        root = self.toElement()
        root.set("xmlns", "http://www.openmath.org/OpenMath")
        ret = ET.tostring(root, *args, **tostringkargs).decode("utf8")
        toprettyaccepted = ["indent", "newl", "encoding", "standalone"]
        toprettykargs = {k: kargs[k] for k in kargs if k in toprettyaccepted}
        if any(x in kargs for x in toprettykargs if x != "encoding"):
            if type(kargs.get("indent")) is int:
                toprettykargs["indent"] *= " "
            ret = minidom.parseString(ret).toprettyxml(**toprettykargs)
        return ret

    def isValid(self) -> bool:
        """Check wether the mathematical object is valid

        IMPORTANT: This function is susceptible of false positives.
        """
        return True

    def hasValidCDBase(self) -> bool:
        """Check wether the cdbase attribute is a string or None"""
        return (
            not hasattr(self, "cdbase")
            or self.cdbase == None
            or type(self.cdbase) is str
        )

    def apply(self, f, accumulator=None) -> None:
        """Traverse the object tree and apply a function to each node

        Arguments:
            f -- function to be applied
            accumulator -- list of visited nodes (used to prevent cycles)
        """
        if accumulator is None:
            accumulator = []

        if any(self is x for x in accumulator):
            return
        else:
            accumulator.append(self)

        f(self)
        d = self._customdict()
        for k in list(d.keys())[::-1]:  # reversed keys
            if isinstance(d[k], _OMBase):
                d[k].apply(f, accumulator)
            elif type(d[k]) is list:
                for i, a in enumerate(d[k]):
                    if isinstance(a, _OMBase):
                        a.apply(f, accumulator)
                    elif type(a) is list:
                        for j, b in enumerate(a):
                            if isinstance(b, _OMBase):
                                b.apply(f, accumulator)

    def getCDBase(self) -> str:
        """Get a valid cdbase attribute from an object or its ancestors"""
        if "cdbase" not in dir(self) or self.cdbase is None:
            if self.parent is None:
                return None
            return self.parent.getCDBase()
        return self.cdbase

    def clone(self):
        return deepcopy(self)

    def replace(self, obj1, obj2) -> None:
        """Replace the instances of an object with another one

        Arguments:
        obj1 -- reference of the object to be replaced
        obj2 -- object to replace obj1
        """
        d = self.__dict__
        for k in d:
            if obj1 is d[k]:
                d[k] = obj2.clone()
                d[k].parent = self
            elif type(d[k]) is list and not (
                k == "variables" and self.kind == "OMBIND"
            ):
                for i, elem in enumerate(d[k]):
                    if obj1 is elem:
                        d[k][i] = obj2.clone()
                        d[k][i].parent = self
                    elif type(elem) is list:
                        for j, subelem in enumerate(elem):
                            if subelem is obj1:
                                elem[j] = obj2.clone()
                                elem[j].parent = self

    def __eq__(self, other) -> bool:
        """Return true if all attributes are present and equal in both instances"""
        if not isinstance(other, _OMBase):
            return False
        a = self._customdict()
        b = other._customdict()
        allkeys = set([*a, *b])

        if "cdbase" in allkeys:
            if self.getCDBase() != self.getCDBase():
                return False
            allkeys.remove("cdbase")

        def compare(x, y):
            ret = None
            if type(x) is list and type(y) is list:
                ret = len(x) == len(y) and all(
                    compare(x[i], y[i]) for i in range(len(x))
                )
            else:
                ret = x == y
            return ret

        return all(compare(a.get(k), b.get(k)) for k in allkeys)

    def __str__(self):
        """Return the string representation of the object"""
        return "OM" + str(self._customdict())

    def __repr__(self):
        """Return repr(self)"""
        return "OM" + repr(self._customdict())


class Object(_OMBase):
    """Implementation of the OpenMath object constructor OMOBJ

    Arguments:
        object -- The OpenMath object

    Keyword arguments:
        xmlns -- XML namespace, usually "http://www.openmath.org/OpenMath"
        version -- OpenMath version (default="2.0")
        cdbase -- Base CD URI (default=None)
        parent -- Parent object
    """

    kind = "OMOBJ"

    def __init__(self, object, **kargs):
        self.object = object
        object.parent = self
        self.xmlns = None
        self.version = "2.0"
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
    """Implementation of the Integer object

    Reference: https://openmath.org/standard/om20-2019-07-01/omstd20.html#sec_basic
    """

    kind = "OMI"

    def __init__(self, integer):
        self.integer = integer

    def isValid(self):
        return type(self.integer) is int

    def toElement(self):
        el = ET.Element(self.kind)
        el.text = str(self.integer)
        return el


class Float(_OMBase):
    """Implementation of the Float object

    Reference: https://openmath.org/standard/om20-2019-07-01/omstd20.html#sec_basic
    """

    kind = "OMF"

    def __init__(self, float):
        self.float = float

    def isValid(self):
        return type(self.float) is float

    def toElement(self):
        el = ET.Element(self.kind)
        el.text = str(self.float)
        return el


class String(_OMBase):
    """Implementation of the String object

    Reference: https://openmath.org/standard/om20-2019-07-01/omstd20.html#sec_basic
    """

    kind = "OMSTR"

    def __init__(self, string):
        self.string = string

    def isValid(self):
        return type(self.string) is str

    def toElement(self):
        el = ET.Element(self.kind)
        el.text = self.string
        return el


class Bytearray(_OMBase):
    """Implementation of the Bytearray object

    Reference: https://openmath.org/standard/om20-2019-07-01/omstd20.html#sec_basic
    """

    kind = "OMB"

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
    """Implementation of the Symbol object

    Reference: https://openmath.org/standard/om20-2019-07-01/omstd20.html#sec_basic
    """

    kind = "OMS"

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
    """Implementation of the Variable object

    Reference: https://openmath.org/standard/om20-2019-07-01/omstd20.html#sec_basic
    """

    kind = "OMV"

    def __init__(self, name):
        self.name = name

    def toElement(self):
        el = ET.Element(self.kind)
        el.set("name", self.name)
        return el


class Application(_OMBase):
    """Implementation of the Application object

    Reference: https://openmath.org/standard/om20-2019-07-01/omstd20.html#sec_compound
    """

    kind = "OMA"

    def __init__(self, applicant, *arguments, cdbase=None):
        self.cdbase = cdbase
        self.applicant = applicant
        applicant.parent = self
        self.arguments = list(arguments)
        for a in self.arguments:
            a.parent = self

    def isValid(self):
        return (
            self.hasValidCDBase()
            and self.applicant.isValid()
            and all(a.isValid() for a in self.arguments)
        )

    def toElement(self):
        el = ET.Element(self.kind)
        if self.cdbase is not None:
            el.set("cdbase", self.cdbase)
        el.append(self.applicant.toElement())
        for a in self.arguments:
            el.append(a.toElement())
        return el


class Attribution(_OMBase):
    """Implementation of the Attribution object

    Reference: https://openmath.org/standard/om20-2019-07-01/omstd20.html#sec_compound
    """

    kind = "OMATTR"

    def __init__(self, attributes, object, cdbase=None):
        self.cdbase = attributes
        self.attributes = attributes
        for pair in self.attributes:
            for elem in pair:
                elem.parent = self
        self.object = object
        object.parent = self

    def isValid(self):
        return (
            self.hasValidCDBase()
            and self.object.isValid()
            and all(
                isinstance(a, Symbol) and a.isValid() and b.isValid()
                for [a, b] in attributes
            )
        )

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
    """Implementation of the Binding object

    Reference: https://openmath.org/standard/om20-2019-07-01/omstd20.html#sec_compound
    """

    kind = "OMBIND"

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
        if len(self.variables) == 0 or (
            self.cdbase is not None and type(self.cdbase) is not str
        ):
            return False
        for v in self.variables:
            isVariable = type(v) is Variable
            isAttributedVariable = type(v) is Attribution and type(v.object) is Variable
            if not isVariable and not isAttributedVariable:
                return False
        return self.hasValidCDBase()

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
    """Implementation of the Error object

    Reference: https://openmath.org/standard/om20-2019-07-01/omstd20.html#sec_compound
    """

    kind = "OME"

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
    """Parse either JSON or XML strings into a mathematical object

    See parseJSON and parseXML
    """
    try:
        return parseJSON(text)
    except json.JSONDecodeError:
        return parseXML(text)


def parseJSON(text):
    """Parse a JSON string into a mathematical object

    Reference: https://openmath.org/standard/om20-2019-07-01/omstd20.html#sec_json-the-json-encoding
    """
    return fromDict(json.loads(text))


def parseXML(text):
    """Parse a XML string into a mathematical object

    Reference: https://openmath.org/standard/om20-2019-07-01/omstd20.html#sec_xml
    """
    return fromElement(ET.fromstring(text))


def fromDict(dictionary):
    """Build a mathematical object from a python dictionary

    Reference: https://openmath.org/standard/om20-2019-07-01/omstd20.html#sec_json-the-json-encoding
    """
    match (dictionary):

        case {"kind": "OMOBJ", **kargs}:
            return Object(
                fromDict(kargs["object"]),
                cdbase=kargs.get("cdbase"),
                version=kargs.get("version"),
                xmlns=kargs.get("xmlns"),
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
                cdbase=kargs.get("cdbase"),
            )

        case {"kind": "OMATTR", **kargs}:
            recFromDict = (
                lambda x: fromDict(x)
                if type(x) is not list
                else [recFromDict(xx) for xx in x]
            )
            return Attribution(
                recFromDict(kargs["attributes"]),
                fromDict(kargs["object"]),
                kargs.get("cdbase"),
            )

        case {"kind": "OME", **kargs}:
            return Error(kargs["error"], kargs.get("arguments"))

        case _:
            raise ValueError("A valid dictionary is required")


def fromElement(elem):
    """Build a mathematical object from a xml.etree.Element

    Reference: https://openmath.org/standard/om20-2019-07-01/omstd20.html#sec_xml
    """
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
            return Symbol(
                elem.attrib["name"], elem.attrib["cd"], elem.attrib.get("cdbase")
            )

        case "OMV":
            return Variable(elem.attrib["name"])

        case "OMSTR":
            return String(elem.text)

        case "OMB":
            raise NotImplementedError("XML encoded OpenMath Bytearrays")

        case "OMA":
            return Application(
                fromElement(elem[0]),
                *[fromElement(x) for x in elem[1:]],
                cdbase=elem.attrib.get("cdbase")
            )

        case "OMATTR":
            obj = None
            attrs = []
            for child in elem:
                if child.tag == "OMATP":
                    key = None
                    for i, x in enumerate(child):
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
                fromElement(elem[2]),
            )

        case _:
            raise ValueError("A valid ElementTree is required: %s" % elem)
