import openmath.cd as CD
import importlib

def __evalSymbol(oms):
    return importlib.import_module("."+oms.cd, __package__).__dict__[oms.name]

def eval(om):
    if om.getCDBase() not in [None, CD.cdbase_official]:
        raise ValueError("CDBase must be official to evaluate")
    if om.kind == "OMOBJ":
        return eval(om.object)
    if om.kind == "OMI":
        return om.integer
    if om.kind == "OMF":
        return om.float
    if om.kind == "OMSTR":
        return om.string
    if om.kind == "OMB":
        return om.bytes
    if om.kind == "OMS":
        return __evalSymbol(om)
    if om.kind == "OMA":
        return eval(om.applicant)(*[eval(arg) for arg in om.arguments])
    if om.kind == "OMBIND":
        return eval(om.binder)(om.variables, om.object)
            
