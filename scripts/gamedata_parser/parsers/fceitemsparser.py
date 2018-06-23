from gamedata_parser.parsers.fceparserbase import FCEParserBase
from gamedata_parser.model.fceitem import FCEItem
from gamedata_parser.model.fceresearch import FCEResearch


class FCEItemsParser(FCEParserBase):
    def __init__(self, gamedata_dir, media_dir):
        super(FCEItemsParser, self).__init__(gamedata_dir, media_dir)
        self.data = self.load_xml('Items')

    def parse(self):
        for xml_item in self.data.findall('ItemEntry'):
            with FCEItem(self._media_dir, xml_item.find('Key').text) as item:
                for possible_keys in ['Key', 'Name', 'Sprite', 'Plural']:
                    xml_key = xml_item.find(possible_keys)
                    if xml_key is not None:
                        item.append_possible_name(xml_key.text)
                for xml_key in xml_item:
                    if xml_key.tag == 'ScanRequirements':
                        for scan_key in xml_key:
                            item.set_scan_requirement(scan_key.text)
                            with FCEItem(self._media_dir, scan_key.text) as scanned_item:
                                scanned_item.set_open_item_after_scan(item.name)
                    elif xml_key.tag == 'ResearchRequirements':
                        for research_key in xml_key:
                            item.set_research_requirement(research_key.text)
                            with FCEResearch(self._media_dir, research_key.text) as research:
                                research.set_open_item_after_research(item.name)
                    else:
                        item.set_simple_key(xml_key.tag, xml_key.text)
