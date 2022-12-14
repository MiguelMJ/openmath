"""
Module for configuring openmath submodules behaviour.
Modules named after CDs are loaded dynamically, so the parsing of the arguments
is always previous to the addition of key-value pairs.
"""
config = {}

def addKeyVal(key, vals, default):
    """Add accepted configuration key-value

    Arguments
    key -- configuration key
    vals -- list of possible string values for the key
    """

    key = key.upper()
    vals = [val.upper() for val in vals]
    default = default.upper()
    
    if vals is not None and default not in vals:
        raise RuntimeError(f'{default} as default value is not in config options')

    if key not in config:
        config[key] = default
    elif config[key] not in vals:
        raise RuntimeError(f'{v} is not a valid value for {k}')
    
def parseFromArgs(argv):
    """Set the configuration values from a list of arguments"""
    pairs = [ arg[1:].split("=") for arg in argv if arg.startswith("+") ]
    for [k, v] in pairs:
        k = k.upper()
        v = v.upper()
        config[k] = v

def get(key):
    return config[key.upper()]