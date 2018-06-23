from gamedata_parser.parsers.fceparserbase import FCEParserBase
from gamedata_parser.model.fceitem import FCEItem


class FCETerrainParser(FCEParserBase):
    def __init__(self, gamedata_dir, media_dir):
        super(FCETerrainParser, self).__init__(gamedata_dir, media_dir)
        self.data = self.load_xml('TerrainData')

    def _parse_main_values(self, xml_key, item):
        if xml_key.tag == 'tags':
            for tag_key in xml_key:
                    item.add_tag(tag_key.text)
        elif xml_key.tag == 'Fuel':
            item.set_simple_key('fuel_energy', xml_key.find('Energy').text)
        elif xml_key.tag == 'PickReplacement':
            item.set_multiblock_part(xml_key.text)
            with FCEItem(self._media_dir, xml_key.text) as mb_machine_item:
                mb_machine_item.set_simple_key('part_of_multiblock_machine', item.name)
        else:
            item.set_simple_key(xml_key.tag, xml_key.text)

    def parse_with_item(self, xml_root, item_name, terrain_root):
        with FCEItem(self._media_dir, item_name) as item:
            for possible_keys in ['Key', 'Name', 'IconName']:
                xml_key = xml_root.find(possible_keys)
                if xml_key is not None:
                    item.append_possible_name(xml_key.text)
            if terrain_root:
                for xml_key in terrain_root:
                    if xml_key.tag in ['Key', 'Name', 'IconName', 'Values']:
                        pass
                    else:
                        self._parse_main_values(xml_key, item)
            for xml_key in xml_root:
                if xml_key.tag == 'Values':
                    pass
                else:
                    self._parse_main_values(xml_key, item)

    def parse(self):
        for xml_item in self.data.findall('TerrainDataEntry'):
            if xml_item.find('Values') is not None:
                for valued_xml_item in xml_item.find('Values').findall('ValueEntry'):
                    self.parse_with_item(valued_xml_item, valued_xml_item.find('Key').text, xml_item)
            else:
                self.parse_with_item(xml_item, xml_item.find('Key').text, None)

