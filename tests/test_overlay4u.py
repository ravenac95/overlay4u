import fudge
from nose.tools import raises
import overlay4u

@fudge.patch('subprocess.Popen')
def test_fake_mount(fake_popen):
    from overlay4u.overlay import OverlayFS
    
    # Setup Popen expectation
    fake_process = fake_popen.expects_call().returns_fake()
    fake_process.expects('wait')

    overlay = overlay4u.mount('directory', 'lower', 'upper')

    assert isinstance(overlay, OverlayFS) == True
    assert overlay.directory == 'directory'
    assert overlay.lower_dir == 'lower'
    assert overlay.upper_dir == 'upper'

@raises(overlay4u.AlreadyMounted)
@fudge.patch('subprocess.Popen')
def test_fake_mount_twice(fake_popen):
    # Setup fake mount state checker
    fake_mount_verify = fudge.Fake('mount_verify')
    (fake_mount_verify.expects('is_mounted').with_args('directory')
            .returns(True))
    
    # Make a stub for popen. just in case it gets through
    fake_popen.is_a_stub()

    # Use dependency injection to change mount verification technique
    overlay = overlay4u.mount('directory', 'lower', 'upper', 
            mount_verify=fake_mount_verify)
