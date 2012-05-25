"""
tests.test_mountlist
~~~~~~~~~~~~~~~~

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

def test_parse_mount_entry():
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
        yield do_parse_mount_entry, entry_str, expected

def do_parse_mount_entry(entry_str, expected):
    mount_entry = MountEntry.parse(entry_str)
    assert mount_entry.device == expected[0]
    assert mount_entry.directory == expected[1]
    assert mount_entry.fs_type == expected[2]
    assert mount_entry.options == expected[3]

def test_parse_mount_table():
    fake_entry = fudge.Fake('MountEntry')
    fake_entry.expects('parse').returns('anentry')

    mount_table = MountTable.parse(TEST_MOUNT_LIST, entry_class=fake_entry)

    assert mount_table.as_list() == ['anentry', 'anentry', 'anentry']


TEST_MOUNT_LIST = """
device1 on /somedir type fstype (opt1,opt2,opt3=val)
device2 on /somedir type fstype (opt1,opt2,opt3=val)
device3 on /somedir type fstype (opt1,opt2,opt3=val)
"""
