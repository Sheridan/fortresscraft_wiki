
from gamedata_parser.model.fceitembase import FCEItemBase
from gamedata_parser.model.fceitemicon import FCEItemIcon


class FCEItem(FCEItemBase):
    def __init__(self, media_dir, name):
        '''
        name - имя шмотки
        '''
        super(FCEItem, self).__init__(media_dir, name, 'items')

    def __enter__(self):
        self._load()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        FCEItemIcon(self, self._icons_dir).get_icon()
        self._save()

    # def set_icon_available(self, icon_available):
    #     self.set_simple_key('icon_available', icon_available)

    def set_participate_in_craft(self, ingridient_name):
        self._set_array_key('participate_in_craft', ingridient_name)

    def set_assemble_craft(self, result_item_name):
        self._set_array_key('assemble_craft', result_item_name)

    def add_tag(self, tag_name):
        self._set_array_key('tags', tag_name)

    def append_craft_receipt(self, item_craft_receipt):
        if 'craft_receipts' not in self.data:
            self.data['craft_receipts'] = []
        # if 'category' in item_craft_receipt.data:
        #     self._set_array_key('category', item_craft_receipt.data['category'])
        if item_craft_receipt.data not in self.data['craft_receipts']:
            self.data['craft_receipts'].append(item_craft_receipt.data)
