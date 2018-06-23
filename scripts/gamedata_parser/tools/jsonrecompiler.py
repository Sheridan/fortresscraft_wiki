import json
import os
from gamedata_parser.model.fceitem import FCEItem
from gamedata_parser.model.fceresearch import FCEResearch
from gamedata_parser.jsonbase import JsonBase


class JsonRecompiler(JsonBase):
    def __init__(self, media_dir):
        super(JsonRecompiler, self).__init__(media_dir)

    def get_item_index_name(self, name):
        with FCEItem(self._media_dir, name) as item:
            if name != item.name:
                print('Found non-index item element name [%s] -> [%s]' % (name, item.name))
            return item.name

    def get_research_index_name(self, name):
        with FCEResearch(self._media_dir, name) as research:
            if name != research.name:
                print('Found non-index research element name [%s] -> [%s]' % (name, research.name))
            return research.name

    def _recompile_array(self, array_ref, class_type):
        replacement = []
        for element in array_ref:
            if class_type == 'FCEItem':
                replacement.append(self.get_item_index_name(element))
            else:
                replacement.append(self.get_research_index_name(element))
        return replacement

    def _recompile_dict(self, dict_ref, class_type):
        replacement = {}
        for element in dict_ref.keys():
            if class_type == 'FCEItem':
                replacement[self.get_item_index_name(element)] = dict_ref[element]
            else:
                replacement[self.get_research_index_name(element)] = dict_ref[element]
        return replacement

    def _recompile_in(self, dict_part):
        for what in [
            ['participate_in_craft', 'FCEItem'],
            ['scan_requirement', 'FCEItem'],
            ['research_requirement', 'FCEResearch'],
            ['assemble_craft', 'FCEItem'],
            ['multiblock_part', 'FCEItem'],
            ['open_items_after_research', 'FCEItem'],
            ['open_researches_after_research', 'FCEResearch'],
            ['open_items_after_scan', 'FCEItem'],
            ['open_researches_after_scan', 'FCEResearch'],
            ]:
            if what[0] in dict_part:
                dict_part[what[0]] = self._recompile_array(dict_part[what[0]], what[1])
        for what in [
            ['receipt', 'FCEItem'],
            ['project_item_requirements', 'FCEItem']]:
            if what[0] in dict_part:
                dict_part[what[0]] = self._recompile_dict(dict_part[what[0]], what[1])
        for what in ['part_of_multiblock_machine']:
            if what in dict_part:
                dict_part[what] = self.get_item_index_name(dict_part[what])

    def _recompile_where(self, where):
        for processing_file in self._get_json_list(where):
            processing_data = self._load_json(processing_file)
            self._recompile_in(processing_data)
            if 'craft_receipts' in processing_data:
                for craft_receipt in processing_data['craft_receipts']:
                    self._recompile_in(craft_receipt)
            self._save_json(processing_file, processing_data)

    def recompile(self):
        self._recompile_where('items')
        self._recompile_where('research')

