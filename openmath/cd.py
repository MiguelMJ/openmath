import requests
import xml.etree.ElementTree as ET
import re

import openmath as OM

cdbase_official = "http://www.openmath.org/cd"
__CDs = {} # URI: dict

def _cdURI(cd, cdbase): return cdbase.rstrip("/") + "/"+ cd + ".ocd"

def _buildCD(ocdxml):
    """Translate the CD from it's XML parsed structure to a dictionary"""
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
        else:
            cd["meta"][tag] = child.text
    return cd

def loadLocalCD(cds, cdbase="./") -> bool:
    """Load a Content Dictionary from a local file
    
    Return True if it was successfully loaded
    """
    if type(cds) is str:
        cds = [cds]
    for cd in cds:
        filepath = _cdURI(cd, cdbase)
        if filepath not in __CDs:
            with open(filepath) as fh:
                text = fh.read()
            ocdxml = ET.fromstring(text)
            __CDs[ocd_uri] = _buildCD(ocdxml)
    return True

def loadRemoteCD(cds, cdbase=cdbase_official) -> bool:
    """Load a Content Dictionary from a remote file
    
    Return True if it was successfully loaded
    """
    if type(cds) is str:
        cds = [cds]
    for cd in cds:
        ocd_uri = _cdURI(cd, cdbase)
        if ocd_uri not in __CDs:
            response = requests.get(ocd_uri)
            text = response.text
            if not response:
                return False, response
            ocdxml = ET.fromstring(text)
            __CDs[ocd_uri] = _buildCD(ocdxml)
    return True

def loadCD(cd, cdbase=cdbase_official) -> bool:
    """Load a Content Dictionary

    Attempt to distinguish local and remote __CDs.

    Return True if it was successfully load
    """
    if cdbase.startswith("http"):
        return loadRemoteCD(cd, cdbase)
    return loadLocalCD(cd, cdbase)

def keys(cd, cdbase=cdbase_official) -> list:
    """Get a list of entries in a CD"""
    return list(__CDs[_cdURI(cd, cdbase)]["entries"])

def getEntry(oms, force_load=False):
    cdbase = oms.getCDBase() or cdbase_official
    cduri = cdbase.lstrip("/") + "/" + oms.cd + ".ocd"
    if force_load and cduri not in __CDs:
        loadCD(oms.cd, cdbase)
    return __CDs[cduri]["entries"][oms.name]

__all__ = ["loadLocalCD", "loadRemoteCD", "loadCD", "keys", "getEntry"]