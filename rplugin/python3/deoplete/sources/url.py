try:
    from .base import Base
except:
    class Base:
        pass

import re
from subprocess import check_output
from urllib.parse import unquote


URL_PATTERN = r'https?\w*$'
URL_RE = re.compile(URL_PATTERN, re.IGNORECASE)


def get_urls():
    output = check_output('brotab_client.py list_tabs | cut -f3', shell=True)
    output = output.split()
    output = [unquote(line.decode('utf8').strip()) for line in output]
    #output = output.split()
    return output


class Source(Base):
    def __init__(self, vim):
        Base.__init__(self, vim)

        self.debug_enabled = False
        self.name = 'url'
        #self.kind = 'keyword'
        self.mark = '[url]'
        #self.min_pattern_length = 2

        # Use these options if you want to filter candidates yourself
        self.is_volatile = False
        self.matchers = ['matcher_cpsm']
        self.sorters = []

        # Use these options if you want to implement custom matcher
        #self.matchers = ['matcher_fuzzy', 'matcher_full_fuzzy']
        #self.sorters = ['sorter_rank']
        #self.converters = []

        self.max_menu_width = 120
        self.max_abbr_width = 120
        self.input_pattern = URL_PATTERN

    def get_complete_position(self, context):
        match = URL_RE.search(context['input'])
        return match.start() if match else -1

    def gather_candidates(self, context):
        context['is_async'] = False
        return get_urls()

