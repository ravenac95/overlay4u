import os

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
