import subprocess

class AlreadyMounted(Exception):
    pass

class FakeMountVerify(object):
    def is_mounted(self, *args):
        return False

class OverlayFS(object):
    @classmethod
    def mount(cls, mount_point, lower_dir, upper_dir, mount_verify=None):
        """Execute the mount. This requires root"""
        # Calculate mount options
        mount_verify = mount_verify or FakeMountVerify()
        if mount_verify.is_mounted(mount_point):
            raise AlreadyMounted()
        options = "lowerdir=%s,upperdir=%s" % (lower_dir, upper_dir)
        # Run the actual mount
        process = subprocess.Popen(['mount', '-t', 'overlayfs', '-o', options,
            'overlayfs', mount_point])
        process.wait()
        return cls(mount_point, lower_dir, upper_dir)

    def __init__(self, mount_point, lower_dir, upper_dir):
        self.mount_point = mount_point
        self.lower_dir = lower_dir
        self.upper_dir = upper_dir
