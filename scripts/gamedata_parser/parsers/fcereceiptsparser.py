from gamedata_parser.parsers.fceparserbase import FCEParserBase
from gamedata_parser.model.fceitemcarftreceipt import FCEItemCraftReceipt
from gamedata_parser.model.fceitem import FCEItem


class FCEReceiptsParser(FCEParserBase):
    def __init__(self, gamedata_dir, media_dir):
        super(FCEReceiptsParser, self).__init__(gamedata_dir, media_dir)
        self._receipts = [
            { 'assembler': 'blastfurnace', 'library': "BlastFurnaceRecipes" },
            { 'assembler': 'coilerplant', 'library': "CoilerRecipes" },
            { 'assembler': 'extrusionplant', 'library': "ExtruderRecipes" },
            { 'assembler': 'manufacturingplant', 'library': "ManufacturerRecipes" },
            { 'assembler': 'pcbassemblingplant', 'library': "PCBAssemblerRecipes" },
            { 'assembler': 'pipeextrusionplant', 'library': "PipeExtruderRecipes" },
            { 'assembler': 'refinerycontroller', 'library': "RefineryRecipes" },
            { 'assembler': 'researchassembler', 'library': "ResearchAssemblerRecipes" },
            { 'assembler': 'standardoresmelter', 'library': "SmelterRecipes" },
            { 'assembler': 'stamperplant', 'library': "StamperRecipes" },
        ]

    def parse_costs(self, assembler, item_craft_receipt, xml_root):
        for craft_cost in xml_root:
            ingridient_name = self._find_one_of(craft_cost, ['Key', 'Name']).text
            item_craft_receipt.set_craft_cost(assembler, ingridient_name, craft_cost.find('Amount').text)

    def parse(self):
        for reciepts_library in self._receipts:
            for receipt in self.load_xml(reciepts_library['library']).findall('CraftData'):
                crafted_item_name = receipt.find('CraftedKey').text
                with FCEItemCraftReceipt(self._media_dir, crafted_item_name) as item_craft_receipt:
                    for xml_key in receipt:
                        if xml_key.tag == 'ScanRequirements':
                            for scan_key in xml_key:
                                item_craft_receipt.set_scan_requirement(scan_key.text)
                        elif xml_key.tag == 'ResearchRequirements':
                            for research_key in xml_key:
                                item_craft_receipt.set_research_requirement(research_key.text)
                        elif xml_key.tag == 'Costs':
                            self.parse_costs(reciepts_library['assembler'], item_craft_receipt, xml_key.findall('CraftCost'))
                        else:
                            item_craft_receipt.set_simple_key(xml_key.tag, xml_key.text)
                    with FCEItem(self._media_dir, crafted_item_name) as item:
                        item.append_craft_receipt(item_craft_receipt)
