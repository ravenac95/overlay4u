import os
import sys

TEST_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(TEST_DIR, '..'))

sys.path.insert(0, PROJECT_DIR)

def fixtures_path(file_path=''):
    return os.path.join(TEST_DIR, 'fixtures', file_path)
