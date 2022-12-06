import os
from pathlib import Path

import openmath as OM
import openmathcd as OMCD
import openmathutil as OMUTIL

omdir = Path("om")


def load_om(name):
    with open(omdir / name) as fh:
        return fh.read()


def parsing_tests():

    omfiles = os.listdir(omdir)

    last = None
    for omfile in omfiles:
        print("\x1b[1m%s\x1b[0m" % omfile)

        omxml = load_om(omfile)

        try:
            # parse and inequality with last example
            om = OM.parse(omxml)
            print(" Parsed")
            assert om != last, "Unexpected equality"
            assert om.isValid(), "use of isValid"
            print(" Validated")
            # JSON
            om1 = OM.parseJSON(om.toJSON())
            print(" JSON encoding")
            assert om == om1, "JSON coherence"
            print(" JSON coherence")
            # XML
            om2 = OM.parseXML(om.toXML())
            print(" XML encoding")
            assert om == om2, "XML coherence"
            print(" XML coherence")
            # XML AND JSON
            assert om1 == om2, "Interencoding    coherence"
            assert (
                om.toJSON() == om1.toJSON() == om2.toJSON()
            ), "Interencoding coherence JSON"
            assert (
                om.toXML() == om1.toXML() == om2.toXML()
            ), "Interencoding coherence XML"
            print(" Interencoding coherence")

        except NotImplementedError as err:
            print("SKIP", err)


def get_cd_test():
    om = OM.parse(load_om("sin_0.om"))
    eq_om = om.object.applicant
    print(OMCD.getUri(eq_om, ocd=False))
    print(OMCD.getUri(eq_om))
    # d = OMCD.getDictionary(eq_om)
    print(OMCD.help(eq_om))
    print(OMCD.help(OM.Symbol("plus", "arith1")))


def replacement_test():
    om = OM.parse(load_om("abs_0.om"))
    var_x = OM.Variable("x")
    int_3 = OM.Integer(333)
    sym_plus = OM.Symbol("plus", "arith1")
    sym_minus = OM.Symbol("minus", "arith1")
    # print(om.toXML(indent=2))
    print(OMUTIL.visualize(om))

    def replace(obj, x, y):
        if obj.parent is None:
            return
        if obj == x:
            obj.parent.replace(obj, y)

    om.apply(lambda o: replace(o, var_x, int_3))
    # print(om.toXML(indent=2))
    print(OMUTIL.visualize(om))

    om.apply(lambda o: replace(o, sym_plus, sym_minus))
    # print(om.toXML(indent=2))
    print(OMUTIL.visualize(om))


def bound_free_test():

    om = OM.Binding(
        OM.Symbol("forall", "quant1"),
        [OM.Variable("x")],
        OM.Application(OM.Symbol("plus", "arith1"), OM.Variable("x"), OM.Variable("y")),
    )
    oms = [om]
    # oms = os.listdir(omdir)
    for omf in oms:
        # om = OM.parse(load_om(omf))
        print(OMUTIL.visualize(om))
        print(OMUTIL.getVars(om))


if __name__ == "__main__":
    parsing_tests()
    get_cd_test()
    replacement_test()
    bound_free_test()
