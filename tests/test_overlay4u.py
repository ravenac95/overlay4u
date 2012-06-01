import fudge
from nose.tools import raises
from testkit import ContextUser
import overlay4u
from overlay4u.overlay import OverlayFS
from overlay4u.overlay import AlreadyMounted

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
        self.context_user.exit()

class TestOverlay4u(GenericOverlay4uSetup):
    def setup(self):
        self.base_setup()
        self.fake_run.expects_call()
        self.fake_ensure.expects_call()

    def teardown(self):
        self.base_teardown()

    @fudge.test
    def test_fake_mount_using_inject(self):
        self.expect_not_is_mounted()

        overlay = overlay4u.mount('mount_point', 'lower', 'upper',
                mount_table=self.fake_mount_table)

        assert isinstance(overlay, OverlayFS) == True
        assert overlay.mount_point == 'mount_point'
        assert overlay.lower_dir == 'lower'
        assert overlay.upper_dir == 'upper'

    @fudge.test
    def test_fake_mount_with_fake_table(self):
        self.expect_not_is_mounted(with_load=True)
    
        overlay = overlay4u.mount('mount_point', 'lower', 'upper')

    @raises(AlreadyMounted)
    @fudge.test
    def test_fake_mount_twice(self):
        self.expect_is_mounted(with_load=True)

        overlay = overlay4u.mount('mount_point', 'lower', 'upper')

    @fudge.test
    def test_fake_unmount(self):
        # Tests that unmount method exists. 
        # FIXME we need to make this a bit better

        self.expect_not_is_mounted(with_load=True)

        overlay = overlay4u.mount('mount_point', 'lower', 'upper')
        overlay.unmount()
