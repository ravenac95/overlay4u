import re
import subwrap

DIR_REGEX = r'[\w\/\.-]+'
MAIN_REGEX_RAW = r'^(?P<device>%s) on (?P<point>%s) type (?P<fs_type>\w+) \((?P<raw_options>.*)\)$'
MAIN_REGEX = MAIN_REGEX_RAW % (DIR_REGEX, DIR_REGEX)
MAIN_REGEX_OBJ = re.compile(MAIN_REGEX)

def match_entry_line(str_to_match, regex_obj=MAIN_REGEX_OBJ):
    """Does a regex match of the mount entry string"""
    match_obj = regex_obj.match(str_to_match)
    if not match_obj:
        error_message = ('Line "%s" is unrecognized by overlay4u. '
                'This is only meant for use with Ubuntu Linux.')
        raise UnrecognizedMountEntry(error_message % str_to_match)
    return match_obj.groupdict()

def split_mount_options(mount_options_str):
    split_options = mount_options_str.split(',')
    return map(lambda a: a.split('='), split_options)

class UnrecognizedMountEntry(Exception):
    pass

class MountEntry(object):
    @classmethod
    def from_string(cls, entry_str):
        entry_dict = match_entry_line(entry_str)
        options = split_mount_options(entry_dict['raw_options'])
        return cls(entry_dict['point'], entry_dict['device'],
                entry_dict['fs_type'], options)

    def __init__(self, mount_point, device, fs_type, options):
        self.mount_point = mount_point
        self.device = device
        self.fs_type = fs_type
        self.options = options

class MountTable(object):
    @classmethod
    def from_string(cls, list_str, entry_class=None):
        entry_class = entry_class or MountEntry
        # Remove any trailing or preceding newlines
        list_str = list_str.strip()
        entry_list = map(entry_class.from_string, list_str.splitlines())
        return cls(entry_list)

    @classmethod
    def load(cls, entry_class=None):
        response = subwrap.run(['mount'])
        return cls.from_string(response.std_out)

    def __init__(self, entry_list):
        self._entries = entry_list

    def as_list(self, fs_type=None):
        """List mount entries"""
        entries = self._entries
        if fs_type:
            entries = filter(lambda a: a.fs_type == fs_type, entries)
        return entries

    def list_mount_points(self):
        return map(lambda a: a.mount_point, self._entries)

    def find_by_mount_point(self, mount_point):
        found = []
        for entry in self._entries:
            if entry.mount_point == mount_point:
                found.append(entry)
        return found

    def is_mounted(self, mount_point):
        results = self.find_by_mount_point(mount_point)
        return len(results) != 0
