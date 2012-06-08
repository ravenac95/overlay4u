import os
import fudge
from functools import wraps
from nose.plugins.skip import SkipTest

def only_as_root(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        euid = os.geteuid()
        if euid != 0:
            raise SkipTest("Sorry. Test requires root")
        return f(*args, **kwargs)
    return decorated_function

def verify(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
        finally:
            fudge.verify()
        return result
    return decorated_function

def reset():
    """Resets fudge expectations and calls"""
    fudge.clear_calls()
    fudge.clear_expectations()
