import platform
hostname = platform.node()

try:
    exec "from %s import *" % (hostname,)
except ImportError:
    # default to hesperus
    from hesperus import *
