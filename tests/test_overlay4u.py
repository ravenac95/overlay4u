import fudge
from nose.tools import raises
from testkit import ContextUser
import overlay4u
from overlay4u.overlay import OverlayFS
from overlay4u.overlay import AlreadyMounted
from .utils import verify, reset

class GenericOverlay4uSetup(object):
    def base_setup(self):
        # Patch all of these objects for all tests
        context = fudge.patch('subwrap.run', 
                'overlay4u.overlay.ensure_directories',
                'overlay4u.overlay.MountTable',
                )
        self.context_user = ContextUser(context)
        self.fake_run, self.fake_ensure, self.fake_mount_table = self.context_user.enter()

    def expect_is_mounted(self, with_load=False):
        mount_table = self.fake_mount_table
        if with_load:
            mount_table = mount_table.expects('load').returns_fake()
        mount_table.expects('is_mounted').returns(True)
    
    def expect_not_is_mounted(self, with_load=False):
        mount_table = self.fake_mount_table
        if with_load:
            mount_table = mount_table.expects('load').returns_fake()
        mount_table.expects('is_mounted').returns(False)

    def base_teardown(self):
        # FIXME there's gotta be a better way to handle the patching.
        # This is a job for testkit to handle better
        reset()
        self.context_user.exit()

class TestOverlay4u(GenericOverlay4uSetup):
    def setup(self):
        self.base_setup()
        self.fake_run.expects_call()
        self.fake_ensure.expects_call()

    def teardown(self):
        self.base_teardown()

    @verify
    def test_fake_mount_using_inject(self):
        self.expect_not_is_mounted()

        overlay = overlay4u.mount('mount_point', 'lower', 'upper',
                mount_table=self.fake_mount_table)

        assert isinstance(overlay, OverlayFS) == True
        assert overlay.mount_point == 'mount_point'
        assert overlay.lower_dir == 'lower'
        assert overlay.upper_dir == 'upper'

    @verify
    def test_fake_mount_with_fake_table(self):
        self.expect_not_is_mounted(with_load=True)
    
        overlay = overlay4u.mount('mount_point', 'lower', 'upper')


    @verify
    def test_fake_unmount(self):
        # Tests that unmount method exists. 
        # FIXME we need to make this a bit better
        self.expect_not_is_mounted(with_load=True)

        overlay = overlay4u.mount('mount_point', 'lower', 'upper')
        overlay.unmount()

class TestOverlay4uMoreGeneral(GenericOverlay4uSetup):
    """This test class assumes less with each test. Add tests here that
    need more mock control
    
    """
    def setup(self):
        self.base_setup()
    
    def teardown(self):
        self.base_teardown()

    @verify
    @raises(AlreadyMounted)
    def test_fake_mount_twice(self):
        self.expect_is_mounted(with_load=True)
        self.fake_ensure.expects_call()

        overlay = overlay4u.mount('mount_point', 'lower', 'upper')

    @verify
    def test_ensure_directories_fails(self):
        self.fake_ensure.expects_call().raises(Exception('error'))
        
        exception_raised = False
        try:
            overlay4u.mount('mount_point', 'lower', 'upper')
        except Exception, e:
            assert e.message == 'error'
            exception_raised = True
        assert exception_raised == True



