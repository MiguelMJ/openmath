import os
from pathlib import Path

import openmath as OM

omdir = Path("om")

omfiles = os.listdir(omdir)

last = None
for omfile in omfiles:
    print("\x1b[1m%s\x1b[0m" % omfile)

    with open(omdir / omfile) as fh:
        omxml = fh.read()
    
    try:
        # parse and inequality with last example
        om = OM.parse(omxml)
        print(" Parsed")
        assert om != last, "Unexpected equality"
        # JSON
        om1 = OM.parseJSON(
            om.toJSON()
        )
        print(" JSON encoding")
        assert om == om1, "JSON coherence"
        print(" JSON coherence")
        # XML
        om2 = OM.parseXML(
            om.toXML()
        )
        print(" XML encoding")
        assert om == om2, "XML coherence"
        print(" XML coherence")
        # XML AND JSON
        assert om1 == om2, "Interencoding coherence"
        assert om.toJSON() == om1.toJSON() == om2.toJSON(), "Interencoding coherence JSON"
        assert om.toXML() == om1.toXML() == om2.toXML(), "Interencoding coherence XML"
        print(" Interencoding coherence")

    except NotImplementedError as err:
        print("SKIP",err)