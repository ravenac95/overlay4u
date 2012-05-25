from overlay import OverlayFS, AlreadyMounted

def mount(directory, lower_dir, upper_dir, mount_verify=None):
    """Creates a mount"""
    return OverlayFS.mount(directory, lower_dir, upper_dir, mount_verify=mount_verify)
