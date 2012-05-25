import fudge
from nose.tools import raises
import overlay4u
from overlay4u.overlay import AlreadyMounted

@fudge.patch('subprocess.Popen')
def test_fake_mount(fake_popen):
    from overlay4u.overlay import OverlayFS
    
    # Setup Popen expectation
    fake_process = fake_popen.expects_call().returns_fake()
    fake_process.expects('wait')
    
    # Setup fake mount table
    fake_mount_table = fudge.Fake('mount_table')
    fake_mount_table.expects('is_mounted').returns(False)

    overlay = overlay4u.mount('mount_point', 'lower', 'upper',
            mount_table=fake_mount_table)

    assert isinstance(overlay, OverlayFS) == True
    assert overlay.mount_point == 'mount_point'
    assert overlay.lower_dir == 'lower'
    assert overlay.upper_dir == 'upper'

@fudge.patch('subprocess.Popen', 
    'overlay4u.overlay.MountTable')
def test_fake_mount_with_fake_table(fake_popen, fake_table_class):
    fake_popen.is_a_stub()
    fake_table = fake_table_class.expects('load').returns_fake()
    fake_table.expects('is_mounted').returns(False)

    overlay = overlay4u.mount('mount_point', 'lower', 'upper')

@raises(AlreadyMounted)
@fudge.patch('subprocess.Popen')
def test_fake_mount_twice(fake_popen):
    # Setup fake mount table checker
    fake_mount_table = fudge.Fake('mount_table')
    (fake_mount_table.expects('is_mounted').with_args('mount_point')
            .returns(True))
    
    # Make a stub for popen. just in case it gets through
    fake_popen.is_a_stub()

    # Use dependency injection to change mount verification technique
    overlay = overlay4u.mount('mount_point', 'lower', 'upper', 
            mount_table=fake_mount_table)
