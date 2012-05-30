import fudge
from nose.tools import raises
import overlay4u
from overlay4u.overlay import AlreadyMounted

@fudge.patch('subwrap.run')
def test_fake_mount(fake_run):
    from overlay4u.overlay import OverlayFS
    
    # Setup subwrap.run
    fake_run.expects_call()
    
    # Setup fake mount table
    fake_mount_table = fudge.Fake('mount_table')
    fake_mount_table.expects('is_mounted').returns(False)

    overlay = overlay4u.mount('mount_point', 'lower', 'upper',
            mount_table=fake_mount_table)

    assert isinstance(overlay, OverlayFS) == True
    assert overlay.mount_point == 'mount_point'
    assert overlay.lower_dir == 'lower'
    assert overlay.upper_dir == 'upper'

@fudge.patch('subwrap.run', 'overlay4u.overlay.MountTable')
def test_fake_mount_with_fake_table(fake_run, fake_table_class):
    fake_run.expects_call()
    fake_table = fake_table_class.expects('load').returns_fake()
    fake_table.expects('is_mounted').returns(False)

    overlay = overlay4u.mount('mount_point', 'lower', 'upper')

@raises(AlreadyMounted)
@fudge.patch('subwrap.run')
def test_fake_mount_twice(fake_run):
    # Setup fake mount table checker
    fake_mount_table = fudge.Fake('mount_table')
    (fake_mount_table.expects('is_mounted').with_args('mount_point')
            .returns(True))
    
    # Make a stub for subwrap.run. just in case it gets through
    fake_run.expects_call()

    # Use dependency injection to change mount verification technique
    overlay = overlay4u.mount('mount_point', 'lower', 'upper', 
            mount_table=fake_mount_table)

@fudge.patch('subwrap.run', 'overlay4u.overlay.MountTable')
def test_fake_unmount(fake_run, fake_table_class):
    # Tests that unmount method exists. 
    # FIXME we need to make this a bit better
    fake_run.expects_call()
    
    fake_table = fake_table_class.expects('load').returns_fake()
    fake_table.expects('is_mounted').returns(False)

    overlay = overlay4u.mount('mount_point', 'lower', 'upper')
    overlay.unmount()
