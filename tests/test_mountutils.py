"""
tests.test_mountutils
~~~~~~~~~~~~~~~~~~~~~

Tests the MountTable. This will be used to determine if a directory is
currently mounted as an overlay at this time.
"""
import fudge
from overlay4u.mountutils import *

TEST_MOUNT_LIST_ENTRY1 = 'dev on /dir type fstype (opt1,opt2,opt3=val)'
TEST_MOUNT_LIST_ENTRY2 = '/dev2 on /dir2 type fstype2 (opt1=val,opt2,opt3=val)'
TEST_MOUNT_LIST_ENTRY3 = '/dev3/.dir on /dir3/.dir type fstype2 (opt1=val,opt2,opt3=val)'
TEST_MOUNT_LIST_ENTRY4 = '/dev4/dir-with-dash on /dir4/dir-with-dash type fstype2 (opt1=val,opt2,opt3=val)'

def test_generated_match_entry_line():
    tests = [
        (TEST_MOUNT_LIST_ENTRY1, (
            'dev',
            '/dir',
            'fstype',
            'opt1,opt2,opt3=val',
        )),
        (TEST_MOUNT_LIST_ENTRY2, (
            '/dev2',
            '/dir2',
            'fstype2',
            'opt1=val,opt2,opt3=val',
        )),
        (TEST_MOUNT_LIST_ENTRY3, (
            '/dev3/.dir',
            '/dir3/.dir',
            'fstype2',
            'opt1=val,opt2,opt3=val',
        )),
        (TEST_MOUNT_LIST_ENTRY4, (
            '/dev4/dir-with-dash',
            '/dir4/dir-with-dash',
            'fstype2',
            'opt1=val,opt2,opt3=val',
        )),
    ]
    for entry_str, expected in tests:
        yield do_match_entry_line, entry_str, expected

def do_match_entry_line(entry_str, expected):
    match_dict = match_entry_line(entry_str)
    assert match_dict['device'] == expected[0]
    assert match_dict['point'] == expected[1]
    assert match_dict['fs_type'] == expected[2]
    assert match_dict['raw_options'] == expected[3]

def test_split_mount_options():
    split_options = split_mount_options('opt1,opt2,opt3')
    assert split_options == [['opt1'], ['opt2'], ['opt3']]
    
    split_options = split_mount_options('opt1=val,opt2,opt3=val')
    assert split_options == [['opt1', 'val'], ['opt2'], ['opt3', 'val']]

def test_mount_entry_from_string():
    tests = [
        # tests in the form of (entry_str, expected)
        (TEST_MOUNT_LIST_ENTRY1, (
            'dev',
            '/dir',
            'fstype',
            [['opt1'], ['opt2'], ['opt3', 'val']],
        )),
        (TEST_MOUNT_LIST_ENTRY2, (
            '/dev2',
            '/dir2',
            'fstype2',
            [['opt1', 'val'], ['opt2'], ['opt3', 'val']],
        )),
    ]
    for entry_str, expected in tests:
        yield do_mount_entry_from_string, entry_str, expected

def do_mount_entry_from_string(entry_str, expected):
    mount_entry = MountEntry.from_string(entry_str)
    assert mount_entry.device == expected[0]
    assert mount_entry.mount_point == expected[1]
    assert mount_entry.fs_type == expected[2]
    assert mount_entry.options == expected[3]

TEST_MOUNT_LIST1 = """
entry
entry
entry
"""

def test_from_string_mount_table():
    fake_entry = fudge.Fake('MountEntry')
    fake_entry.expects('from_string').returns('anentry')

    mount_table = MountTable.from_string(TEST_MOUNT_LIST1,
            entry_class=fake_entry)

    assert mount_table.as_list() == ['anentry', 'anentry', 'anentry']

TEST_MOUNT_LIST2 = """
device1 on /somedir1 type fstype (opt1,opt2,opt3=val)
device2 on /somedir2 type fstype (opt1,opt2,opt3=val)
device3 on /somedir3 type fstype (opt1,opt2,opt3=val)
device4 on /somedir1 type fstype (opt1,opt2,opt3=val)
"""

@fudge.patch('subprocess.Popen')
def test_mount_table_fake_load(fake_popen):
    fake_process = fake_popen.expects_call().returns_fake()
    fake_process.expects('communicate').returns((TEST_MOUNT_LIST2, ""))

    mount_table = MountTable.load()
    assert len(mount_table.as_list()) == 4

class TestMountTable(object):
    def setup(self):
        self.mount_table = MountTable.from_string(TEST_MOUNT_LIST2)

    def test_list_mount_points(self):
        mount_points_set = set(self.mount_table.list_mount_points())
        assert mount_points_set == set(['/somedir1', '/somedir2', '/somedir3'])

    def test_find_by_mount_point(self):
        """Test getting entries by the mount point"""
        mounts_on_dir1 = self.mount_table.find_by_mount_point('/somedir1')
        mounts_on_dir2 = self.mount_table.find_by_mount_point('/somedir2')
        
        assert len(mounts_on_dir1) == 2
        assert len(mounts_on_dir2) == 1

    def test_is_mounted(self):
        assert self.mount_table.is_mounted('/somedir1') == True
        assert self.mount_table.is_mounted('/somedir2') == True
        assert self.mount_table.is_mounted('/somedir3') == True

    def test_is_mounted_false(self):
        assert self.mount_table.is_mounted('/somedir4') == False
