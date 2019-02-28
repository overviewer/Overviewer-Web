from random import SystemRandom
import string

def random_string(length):
    """Return a random string using the system's RNG."""
    rng = SystemRandom()
    return ''.join(rng.choice(string.printable) for i in range(length))
