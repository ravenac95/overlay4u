import fudge
from nose.tools import raises
from overlay4u.utils import *

@fudge.patch('os.path')
def test_ensure_directory(fake_path):
    fake_path.expects('exists').with_args('hello').returns(True)
    fake_path.expects('isdir').with_args('hello').returns(True)
    ensure_directory('hello')

@raises(PathDoesNotExist)
@fudge.patch('os.path')
def test_ensure_directory_throws_error_no_path(fake_path):
    fake_path.expects('exists').with_args('hello').returns(False)
    ensure_directory('hello')

@raises(IsNotADirectory)
@fudge.patch('os.path')
def test_ensure_directory_throws_error_not_dir(fake_path):
    fake_path.expects('exists').with_args('hello').returns(True)
    fake_path.expects('isdir').with_args('hello').returns(False)
    try:
        ensure_directory('hello')
    except PathDoesNotExist:
        pass

@fudge.patch('overlay4u.utils.ensure_directory')
def test_ensure_directories(fake_ensure):
    (fake_ensure.expects_call().with_args('hello')
            .next_call().with_args('world')
            .next_call().with_args('test'))
    ensure_directories('hello', 'world', 'test')
