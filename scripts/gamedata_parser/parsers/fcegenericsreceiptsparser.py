import os

from gamedata_parser.model.fceitem import FCEItem
from gamedata_parser.model.fceitemcarftreceipt import FCEItemCraftReceipt
from gamedata_parser.parsers.fcereceiptsparser import FCEReceiptsParser


class FCEGenericReceiptsParser(FCEReceiptsParser):
    def __init__(self, gamedata_dir, media_dir):
        super(FCEGenericReceiptsParser, self).__init__(gamedata_dir, media_dir)
        self._directory = "GenericAutoCrafter"

    def parse(self):
        for reciept_file in os.listdir('%s/%s' % (self._gamedata_dir, self._directory)):
            if reciept_file.endswith('xml'):
                xml_root = self.load_xml('%s/%s' % (self._directory, reciept_file.split('.')[0]))
                with FCEItem(self._media_dir, xml_root.find('Value').text) as assembler_item:
                    for receipt_xml_key in xml_root:
                        if receipt_xml_key.tag == 'Recipe':
                            crafted_item_name = self._find_one_of(receipt_xml_key, ['CraftedKey', 'CraftedName', 'Key']).text
                            with FCEItemCraftReceipt(self._media_dir, crafted_item_name) as item_craft_receipt:
                                for recipe_key in receipt_xml_key:
                                    if recipe_key.tag == 'Costs':
                                        self.parse_costs(assembler_item, item_craft_receipt, recipe_key.findall('CraftCost'))
                                    else:
                                        item_craft_receipt.set_simple_key(recipe_key.tag, recipe_key.text)
                                with FCEItem(self._media_dir, crafted_item_name) as item:
                                    item.append_craft_receipt(item_craft_receipt)
                        else:
                            assembler_item.set_simple_key(receipt_xml_key.tag, receipt_xml_key.text)
