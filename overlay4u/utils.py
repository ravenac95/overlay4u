import os
import random

LOWER_ALPHA = "abcdefghijklmnopqrstuvwxyz"
UPPER_ALPHA = LOWER_ALPHA.upper()
ALL_ALPHA = LOWER_ALPHA + UPPER_ALPHA

class PathDoesNotExist(Exception):
    def __init__(self, path):
        message = 'Path "%s" does not exist' % path
        super(PathDoesNotExist, self).__init__(message)

class IsNotADirectory(Exception):
    def __init__(self, path):
        message = 'Path "%s" is not a directory' % path
        super(IsNotADirectory, self).__init__(message)

def ensure_directory(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            return True
        else:
            raise IsNotADirectory(path)
    raise PathDoesNotExist(path)

def ensure_directories(*paths):
    for path in paths:
        ensure_directory(path)

def random_name(length=10):
    letter_list = []
    for i in range(length):
        letter_list.append(random.choice(ALL_ALPHA))
    return ''.join(letter_list)
