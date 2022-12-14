import openmath as OM
from openmath.eval import eval
from openmath.util import asOM, replace

def lambda_(variables, om):
    def call(*args):
        omargs = [asOM(a) for a in args]
        toeval = OM.Object(om.clone())
        for i in range(len(args)):
            replace(toeval, variables[i], omargs[i])
        return eval(toeval.object)            

    return call

locals()["lambda"] = lambda_