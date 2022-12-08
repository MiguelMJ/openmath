import openmath.cd as CD
import importlib

def __evalSymbol(oms):
    return importlib.import_module("."+oms.cd, __package__).__dict__[oms.name]

def __evalApplication(oma):
    match importlib.import_module("."+oma.applicant.cd, __package__).__dict__[oma.applicant.name]:
        case (sym, "application"):
            return f"{sym}\\left( {', '.join(eval(x) for x in oma.arguments)} \\right)"
        
        case (sym, "infix"):
            return f" {sym} ".join(eval(x) for x in oma.arguments)
        
        case fun:
            if callable(fun):
                return fun(*[eval(x) for x in oma.arguments])
            else:
                raise NotImplementedError(oma)
 

def eval(om):
    if om.getCDBase() not in [None, CD.cdbase_official]:
        raise ValueError("CDBase must be official to evaluate")
    if om.kind == "OMOBJ":
        return eval(om.object)
    if om.kind == "OMI":
        return str(om.integer)
    if om.kind == "OMF":
        return str(om.float)
    if om.kind == "OMSTR":
        return '"'+om.string+'"'
    if om.kind == "OMB":
        return "".join(str(om.bytes))
    if om.kind == "OMS":
        return __evalSymbol(om)
    if om.kind == "OMA":
        return __evalApplication(om)
            
