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
    vals = [val.upper() for val in vals] if vals is not None else None
    default = default.upper()
    
    if vals is not None and default not in vals:
        raise RuntimeError(f'{default} as default value is not in config options')

    if key not in config:
        config[key] = default
    elif vals is not None and config[key] not in vals:
        raise RuntimeError(f'{config[key]} is not a valid value for {key}')
    
def parseFromArgs(argv):
    """Set the configuration values from a list of arguments"""
    pairs = [ arg[1:].split("=") for arg in argv if arg.startswith("+") ]
    for [k, v] in pairs:
        k = k.upper()
        v = v.upper()
        config[k] = v

def get(key):
    """Safely get a configuration value"""
    return config.get(key.upper(), None)
