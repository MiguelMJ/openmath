import openmath as OM

def asOM(x):
    if type(x) is int:
        return OM.Integer(x)
    if type(x) is float:
        return OM.Float(x)
    if type(x) is str:
        return OM.String(x)
    raise NotImplementedError("asOM " + str(x))
    
def visualize(om):
    assert isinstance(om, OM._OMBase) or type(om) is list
    if type(om) is list:
        return ", ".join(visualize(x) for x in om)
    match (om.kind):
        case "OMOBJ":
            return visualize(om.object)
        case "OMI":
            return str(om.integer)
        case "OMF":
            return str(om.float)
        case "OMSTR":
            return om.string
        case "OMV":
            return om.name
        case "OMS":
            return "%s.%s" % (om.cd, om.name)
        case "OMB":
            raise NotImplementedError("visualize OMB")
        case "OMA":
            return "%s( %s )" % (visualize(om.applicant), visualize(om.arguments))
        case "OMBIND":
            return "%s %s: %s" % (
                visualize(om.binder),
                visualize(om.variables),
                visualize(om.object),
            )
        case "OMATTR":
            return "%s[%s]" % (
                visualize(om.obj),
                "; ".join(visualize(x) for x in om.attributes),
            )
        case _:
            return "ERR"


def replace(om, x, y):
    def singleReplace(obj, x, y):
        if obj.parent is None:
            return
        if obj == x:
            obj.parent.replace(obj, y)

    om.apply(lambda o: singleReplace(o, x, y))


def getVars(om):
    bound = []
    free = []
    allvars = []

    def subGetVars(om):
        if om.kind == "OMV":
            if om.name not in allvars:
                allvars.append(om.name)
            if om.name not in bound and om.name not in free:
                free.append(om.name)
        elif om.kind == "OMBIND":
            for v in om.variables:
                bound.append(v.name)

    om.apply(subGetVars)
    return (allvars, bound, free)
