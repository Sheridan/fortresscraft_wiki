from gamedata_parser.parsers.fceparserbase import FCEParserBase
from gamedata_parser.model.fceresearch import FCEResearch
from gamedata_parser.model.fceitem import FCEItem


class FCEResearchParser(FCEParserBase):
    def __init__(self, gamedata_dir, media_dir):
        super(FCEResearchParser, self).__init__(gamedata_dir, media_dir)
        self.data = self.load_xml('Research')

    def parse(self):
        for xml_research in self.data.findall('ResearchDataEntry'):
            with FCEResearch(self._media_dir, self._find_one_of(xml_research, ['Key', 'Name']).text) as research:
                for possible_keys in ['Key', 'Name', 'IconName']:
                    xml_key = xml_research.find(possible_keys)
                    if xml_key is not None:
                        research.append_possible_name(xml_key.text)
                for xml_key in xml_research:
                    if xml_key.tag == 'ScanRequirements':
                        for scan_key in xml_key:
                            research.set_scan_requirement(scan_key.text)
                            with FCEItem(self._media_dir, scan_key.text) as scanned_item:
                                scanned_item.set_open_research_after_scan(research.name)
                    elif xml_key.tag == 'ResearchRequirements':
                        for research_key in xml_key:
                            research.set_research_requirement(research_key.text)
                            with FCEResearch(self._media_dir, research_key.text) as parent_research:
                                parent_research.set_open_research_after_research(research.name)
                    elif xml_key.tag == 'ProjectItemRequirements':
                        for pi_requirement_key in xml_key.findall('Requirement'):
                            research.set_project_requirement(self._find_one_of(pi_requirement_key, ['Key', 'Name']).text, pi_requirement_key.find('Amount').text)
                    else:
                        research.set_simple_key(xml_key.tag, xml_key.text)
