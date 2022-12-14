import openmath.cd as CD
import openmath.config
import importlib

openmath.config.addKeyVal("SIMPLIFY_FLOAT", ["YES", "NO"], "YES")


def __hasPriorityOver(oms1, oms2):
    if oms1.cd != oms2.cd:
        return False
    moduledict = importlib.import_module("."+oms1.cd, __package__).__dict__
    
    if "priority" not in moduledict:
        return False
    
    first_om = None
    found_oms1= False
    found_oms2= False
    
    for oms in moduledict["priority"]:
        if oms == oms1:
            found_oms1 = True
            if first_om is None:
                first_om = oms1
        if oms == oms2:
            found_oms2 = True
            if first_om is None:
                first_om = oms2
    
    if not found_oms1 or not found_oms2:
        return False
    return first_om is oms1
    
def __evalSymbol(oms):
    return importlib.import_module("."+oms.cd, __package__).__dict__[oms.name]

def __evalApplication(oma):
    moduledict = importlib.import_module("."+oma.applicant.cd, __package__).__dict__
    match moduledict[oma.applicant.name]:
        case (sym, "call"):
            return f"{sym}\\left( {', '.join(eval(x) for x in oma.arguments)} \\right)"
        
        case (sym, "infix"):
            return f" {sym} ".join(evalAndEnclose(x, oma.applicant) for x in oma.arguments)
        
        case fun:
            if callable(fun):
                if "special" in moduledict and oma.applicant.name in moduledict["special"]:
                    return fun(*oma.arguments)
                return fun(*[eval(x) for x in oma.arguments])
            else:
                raise NotImplementedError(oma)
 
def evalAndEnclose(om, parentSym):
    rep = eval(om)
    if om.kind == "OMA" and __hasPriorityOver(parentSym, om.applicant):
        return f'\\left( {rep} \\right)'
    return rep

def eval(om):
    if om.getCDBase() not in [None, CD.cdbase_official]:
        raise ValueError("CDBase must be official to evaluate")
    if om.kind == "OMOBJ":
        return eval(om.object)
    if om.kind == "OMI":
        return str(om.integer)
    if om.kind == "OMV":
        return str(om.name)
    if om.kind == "OMF":
        if openmath.config.get("SIMPLIFY_FLOAT").upper() == "YES":
            return str(om.float).rstrip(".0")
        return str(om.float)
    if om.kind == "OMSTR":
        return '"'+om.string+'"'
    if om.kind == "OMB":
        return "".join(str(om.bytes))
    if om.kind == "OMS":
        return __evalSymbol(om)
    if om.kind == "OMA":
        return __evalApplication(om)
            
