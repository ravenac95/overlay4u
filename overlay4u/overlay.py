import subwrap
from .mountutils import MountTable
from .utils import ensure_directories

class AlreadyMounted(Exception):
    pass

class FakeMountVerify(object):
    def is_mounted(self, *args):
        return False

class OverlayFS(object):
    @classmethod
    def mount(cls, mount_point, lower_dir, upper_dir, mount_table=None):
        """Execute the mount. This requires root"""
        ensure_directories(mount_point, lower_dir, upper_dir)
        # Load the mount table if it isn't given
        if not mount_table:
            mount_table = MountTable.load()
        # Check if the mount_point is in use
        if mount_table.is_mounted(mount_point):
            # Throw an error if it is
            raise AlreadyMounted()
        # Build mount options
        options = "rw,lowerdir=%s,upperdir=%s" % (lower_dir, upper_dir)
        # Run the actual mount
        response = subwrap.run(['mount', '-t', 'overlayfs', '-o', options,
            'overlayfs', mount_point])
        return cls(mount_point, lower_dir, upper_dir)

    def unmount(self):
        response = subwrap.run(['umount', self.mount_point])

    def __init__(self, mount_point, lower_dir, upper_dir):
        self.mount_point = mount_point
        self.lower_dir = lower_dir
        self.upper_dir = upper_dir
