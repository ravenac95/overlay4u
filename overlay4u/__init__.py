from overlay import OverlayFS

def mount(directory, lower_dir, upper_dir, mount_table=None):
    """Creates a mount"""
    return OverlayFS.mount(directory, lower_dir, upper_dir, mount_table=mount_table)
