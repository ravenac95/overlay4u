"""
tests.test_as_root
~~~~~~~~~~~~~~~~~~

These are tests that must be run as root. They will be skipped by nose
automatically if you are not root.

These tests are meant to be as close to truly functional as possible. Take
extra caution when running these tests. If this is not a stable release please
do not run these tests in a production system.
"""
import os
from nose.tools import raises
from testkit import temp_directory, random_string
from tests import fixtures_path
from .utils import only_as_root
import overlay4u


def read_file_data(filepath):
    f = open(filepath)
    data = f.read()
    f.close()
    return data


@only_as_root
def test_mount():
    # Get lower directory from fixtures
    lower_dir = fixtures_path('lower_dir')
    # Read the hello.txt file in the lower_dir
    hello_orig_path = os.path.join(lower_dir, 'hello.txt')
    hello_orig_data = read_file_data(hello_orig_path)
    # Use a temp directory for the upper directory
    with temp_directory() as temp_upper_dir:
        # Use a temp directory for the mount point
        with temp_directory() as temp_mount_point:
            # Mount the overlay
            overlay = overlay4u.mount(temp_mount_point, lower_dir, temp_upper_dir)

            # Read the hello.txt file in the mount_point
            hello_overlay_path = os.path.join(temp_mount_point, 'hello.txt')
            hello_overlay_read_data = read_file_data(hello_overlay_path)

            # Assert that the text file's contents
            assert hello_orig_data == hello_overlay_read_data, ('Data '
                    'for hello.txt should be same in overlay and lower dir')

            # Write data to the overlay hello.txt
            hello_overlay_write = open(hello_overlay_path, 'w')

            # Generate a random string
            hello_overlay_write_data = random_string(50)

            # Write that string to the file
            hello_overlay_write.write(hello_overlay_write_data)

            # Save the file
            hello_overlay_write.close()

            # Unmount the overlay
            overlay.unmount()

            # Check that the file doesn't exist at the mount point now (means
            # successful unmount)
            assert os.path.exists(hello_overlay_path) == False, ('Mount '
                    'point should have nothing in it')

            # Check that the upper directory's hello.txt has the correct data
            # from the random generated string
            hello_upper_path = os.path.join(temp_upper_dir, 'hello.txt')
            hello_upper_data = read_file_data(hello_upper_path)
            assert hello_upper_data == hello_overlay_write_data

            # Check that the original file still has the same content
            current_orig_data = read_file_data(hello_orig_path)
            assert hello_orig_data == current_orig_data


@only_as_root
def test_mount_and_load():
    unmounted = False
    with temp_directory() as temp_lower_dir:
        with temp_directory() as temp_upper_dir:
            with temp_directory() as temp_mount_point:
                try:
                    overlay = overlay4u.mount(temp_mount_point,
                            temp_lower_dir, temp_upper_dir)
                    same_overlay = overlay4u.get(temp_mount_point)
                    assert overlay.mount_point == same_overlay.mount_point
                    assert overlay.lower_dir == same_overlay.lower_dir
                    assert overlay.upper_dir == same_overlay.upper_dir
                    same_overlay.unmount()
                    unmounted = True
                finally:
                    if not unmounted:
                        overlay.unmount()



@only_as_root
@raises(overlay4u.utils.PathDoesNotExist)
def test_mount_directory_does_not_exist():
    # Create and delete 3 directories
    with temp_directory() as random_mount:
        pass
    with temp_directory() as random_lower:
        pass
    with temp_directory() as random_upper:
        pass
    overlay4u.mount(random_mount, random_lower, random_upper)
