import subwrap
from .mountutils import MountTable
from .utils import ensure_directories, random_name


class AlreadyMounted(Exception):
    pass


class InvalidOverlayFS(Exception):
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
        subwrap.run(['mount', '-t', 'overlayfs', '-o', options,
            'olyfs%s' % random_name(), mount_point])
        return cls(mount_point, lower_dir, upper_dir)

    @classmethod
    def from_entry(cls, entry):
        options = entry.options
        # FIXME make options an object. This works for now.
        lower_dir = None
        upper_dir = None
        for option in options:
            key = None
            if len(option) == 2:
                key, value = option
            elif len(option) == 1:
                key = option[0]
            if key == 'lowerdir':
                lower_dir = value
            elif key == 'upperdir':
                upper_dir = value
        if not (lower_dir and upper_dir):
            raise InvalidOverlayFS('Upper and lower directories '
                    'do not seem to be defined')
        return cls(entry.mount_point, lower_dir, upper_dir)

    def unmount(self):
        subwrap.run(['umount', self.mount_point])

    def __init__(self, mount_point, lower_dir, upper_dir):
        self.mount_point = mount_point
        self.lower_dir = lower_dir
        self.upper_dir = upper_dir

    def __repr__(self):
        return '<OverlayFS "%s">' % self.mount_point


class OverlayFSDoesNotExist(Exception):
    pass


class OverlayFSManager(object):
    @classmethod
    def list(cls, mount_table=None):
        if not mount_table:
            mount_table = MountTable.load()
        mount_entries = mount_table.as_list(fs_type='overlayfs')
        overlay_entries = []
        for entry in mount_entries:
            overlay_entries.append(OverlayFS.from_entry(entry))
        return overlay_entries

    @classmethod
    def get(cls, mount_point, mount_table=None):
        overlayfs_list = cls.list(mount_table=mount_table)
        for overlayfs in overlayfs_list:
            if overlayfs.mount_point == mount_point:
                return overlayfs
        raise OverlayFSDoesNotExist('Overlay with mount point, '
                '"%s", does not exist' % mount_point)
