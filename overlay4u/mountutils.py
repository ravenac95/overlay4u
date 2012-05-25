import re

DIR_REGEX = r'[\w\/\.-]+'
MAIN_REGEX_RAW = r'^(?P<device>%s) on (?P<point>%s) type (?P<fs_type>\w+) \((?P<raw_options>.*)\)$'
MAIN_REGEX = MAIN_REGEX_RAW % (DIR_REGEX, DIR_REGEX)
MAIN_REGEX_OBJ = re.compile(MAIN_REGEX)

def match_entry_line(str_to_match, regex_obj=MAIN_REGEX_OBJ):
    """Does a regex match of the mount entry string"""
    match_obj = regex_obj.match(str_to_match)
    return match_obj.groupdict()

def split_mount_options(mount_options_str):
    split_options = mount_options_str.split(',')
    return map(lambda a: a.split('='), split_options)

class MountEntry(object):
    @classmethod
    def parse(cls, entry_str):
        entry_dict = match_entry_line(entry_str)
        options = split_mount_options(entry_dict['raw_options'])
        return cls(entry_dict['point'], entry_dict['device'],
                entry_dict['fs_type'], options)

    def __init__(self, directory, device, fs_type, options):
        self.directory = directory
        self.device = device
        self.fs_type = fs_type
        self.options = options

class MountTable(object):
    @classmethod
    def parse(cls, list_str, entry_class=None):
        entry_class = entry_class or MountEntry
        # Remove any trailing or preceding newlines
        list_str = list_str.strip()
        entry_list = map(entry_class.parse, list_str.splitlines())
        return cls(entry_list)

    def __init__(self, entry_list):
        self._entries = entry_list

    def as_list(self):
        return self._entries            
