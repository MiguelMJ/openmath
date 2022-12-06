import requests
import xml.etree.ElementTree as ET
import re

import openmath as OM

cdbase_default = "http://www.openmath.org/cd"
CDs = {}


def getUri(oms, ocd=True):
    cdbase = oms.getCDBase()
    if cdbase is None:
        cdbase = cdbase_default
    cd = getattr(oms, "cd", None)
    if cdbase is None or cd is None:
        return None
    id = "#" + getattr(oms, "name", "")
    return cdbase.rstrip("/") + "/" + cd + (".ocd" if ocd else id)


def buildCD(ocdxml):
    # get namespace
    if ocdxml.tag[0] == "{":
        [ns, _] = ocdxml.tag[1:].split("}")
    else:
        ns = None
    # single method to get tag with no ns
    def qname(t):
        return t if ns is None else ("{%s}%s" % (ns, t))

    cd = {"meta": {}, "entries": {}}
    for child in ocdxml:
        tag = child.tag.split("}")[-1]
        if tag == "CDDefinition":
            name = child.find(qname("Name")).text.strip()
            desc = child.find(qname("Description")).text.strip()
            role = child.find(qname("Role")).text.strip()
            cd["entries"][name] = {
                "desc": desc,
                "role": role,
            }
        elif tag[0:2] == "CD":
            cd["meta"][tag[2:]] = child.text
    return cd


def getDictionary(arg1):
    if isinstance(arg1, OM.Symbol):
        ocd_uri = re.sub("#.*$", "", getUri(arg1))
    else:
        ocd_uri = arg1

    if ocd_uri not in CDs:
        ocdtext = requests.get(ocd_uri).text
        ocdxml = ET.fromstring(ocdtext)
        CDs[ocd_uri] = buildCD(ocdxml)

    return CDs[ocd_uri]


def help(oms):
    cd = getDictionary(getUri(oms, ocd=True))
    entry = cd["entries"][oms.name]
    return (entry["role"], entry["desc"])
