import re
import os
import json
from gamedata_parser.jsonbase import JsonBase

class FCEItemBase(JsonBase):
    def __init__(self, media_dir, name, where):
        super(FCEItemBase, self).__init__(media_dir)
        self._where = where
        self.name = self._compact_name(name)
        self.data = {'possible_names': [], 'index_name': self.name }
        self.append_possible_name(name)

    def _make_self_filename(self):
        return self._make_filename(self._where, self.name)

    def _load(self):
        print('Loading %s from %s' % (self.name, self._where))
        try:
            self.data = self._load_json(self._make_self_filename())
        except:
            for json_file in self._get_json_list(self._where):
                temp_data = self._load_json(json_file)
                if self.name in temp_data['possible_names']:
                    self.name = temp_data['index_name']
                    self.data = temp_data
                    print('loaded %s from %s' % (self.name, self._where))
                    return

    def _save(self):
        print('Saving %s to %s' % (self.name, self._where))
        self._save_json(self._make_self_filename(), self.data)

    def _full_strip(self, value):
        value = re.sub(r'(\\?\\[nt]|[\n\t]|\*)+', ' ', value)
        return re.sub(' +', ' ', value).strip()

    def append_possible_name(self, name):
        for possible_name in [self._compact_name(name), self._canonical_name(name), self._canonical_minus_name(name)]:
            if possible_name not in self.data['possible_names']:
                self.data['possible_names'].append(possible_name)

    def _canonical_minus_name(self, name):
        return re.sub(r'[^a-z0-9-]', '-', name.lower())

    def _canonical_name(self, name):
        return re.sub(r'[^a-z0-9_]', '_', name.lower())

    def delete_key(self, key):
        if key in self.data:
            self.data.pop(self._canonical_name(key))

    def set_simple_key(self, key, value):
        if value:
            self.data[self._canonical_name(key)] = self._full_strip(value)

    def _set_array_key(self, key_name, element):
        if key_name not in self.data:
            self.data[key_name] = []
        element_name = self._compact_name(element)
        if element_name not in self.data[key_name]:
            self.data[key_name].append(element_name)

    def set_multiblock_part(self, part_name):
        self._set_array_key('multiblock_part', part_name)

    def set_scan_requirement(self, scan_name):
        self._set_array_key('scan_requirement', scan_name)

    def set_research_requirement(self, research_name):
        self._set_array_key('research_requirement', research_name)

    def set_open_item_after_research(self, item_name):
        self._set_array_key('open_items_after_research', item_name)

    def set_open_research_after_research(self, research_name):
        self._set_array_key('open_researches_after_research', research_name)

    def set_open_research_after_scan(self, research_name):
        self._set_array_key('open_researches_after_scan', research_name)

    def set_open_item_after_scan(self, item_name):
        self._set_array_key('open_items_after_scan', item_name)
