import openmath as OM

def visualize(om):
    assert isinstance(om, OM._OMBase) or type(om) is list
    if type(om) is list:
        return ", ".join(visualize(x) for x in om)
    match(om.kind):
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
            return "%s %s: %s" % (visualize(om.binder), visualize(om.variables), visualize(om.object))
        case "OMATTR":
            return "%s[%s]" % (visualize(om.obj), "; ".join(visualize(x) for x in om.attributes))
        case _:
            return "ERR"