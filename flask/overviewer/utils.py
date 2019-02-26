from random import SystemRandom
import string

def random_string(length):
    """Return a random string using the system's RNG."""
    return ''.join(SystemRandom().choice(string.printable) for i in range(length))
