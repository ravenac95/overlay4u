from overlay import OverlayFS, OverlayFSManager

def mount(directory, lower_dir, upper_dir, mount_table=None):
    """Creates a mount"""
    return OverlayFS.mount(directory, lower_dir, upper_dir, mount_table=mount_table)

def list():
    return OverlayFSManager.list()
