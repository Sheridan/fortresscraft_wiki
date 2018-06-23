import json
import os
import re
# from gamedata_parser.tools.toolsbase import ToolsBase
from gamedata_parser.jsonbase import JsonBase


class ListsCompiler(JsonBase):
    def __init__(self, media_dir):
        super(ListsCompiler, self).__init__(media_dir)
        self._lists = {}

    def _save_lists(self):
        for list_name in self._lists.keys():
            self._save_json(self._make_filename('lists', list_name), sorted(self._lists[list_name]))

    def _append_to_list(self, list_name, item_name):
        list_name = self._compact_name(list_name)
        if list_name not in self._lists:
            self._lists[list_name] = []
        item_name = self._compact_name(item_name)
        if item_name not in self._lists[list_name]:
            self._lists[list_name].append(item_name)

    def compile(self):
        for processing_file in self._get_json_list('items'):
            processing_data = self._load_json(processing_file)
            self._append_to_list('all', processing_data['index_name'])
            if 'category' in processing_data:
                self._append_to_list(processing_data['category'], processing_data['index_name'])
            if 'craft_receipts' in processing_data:
                self._append_to_list('crafted', processing_data['index_name'])
                for receipt in processing_data['craft_receipts']:
                    if 'category' in receipt:
                        self._append_to_list(receipt['category'], processing_data['index_name'])
                    if 'tier' in receipt:
                        self._append_to_list('tier%s' % (receipt['tier'],), receipt['index_name'])
            if 'assemble_craft' in processing_data:
                self._append_to_list('assemblers', processing_data['index_name'])
            if 'part_of_multiblock_machine' in processing_data:
                self._append_to_list('parts_of_multiblock_machines', processing_data['index_name'])
            for key in ['garbage', 'glass', 'transparent', 'passable', 'solid', 'hollow', 'paintable', 'colorised', 'reinforced', 'multiblockmachine']:
                bool_key = 'is%s' % (key, )
                if bool_key in processing_data and processing_data[bool_key] == 'true':
                    self._append_to_list(key, processing_data['index_name'])
            if 'fuel_energy' in processing_data:
                self._append_to_list('fuel', processing_data['index_name'])
            if 'powerusepersecond' in processing_data and int(float(processing_data['powerusepersecond'])) > 0 :
                self._append_to_list('powerused', processing_data['index_name'])

        self._save_lists()
