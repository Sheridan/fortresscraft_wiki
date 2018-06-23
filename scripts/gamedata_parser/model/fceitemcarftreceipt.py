from gamedata_parser.model.fceitembase import FCEItemBase
from gamedata_parser.model.fceitem import FCEItem


class FCEItemCraftReceipt(FCEItemBase):
    def __init__(self, media_dir, name):
        '''
        name - имя крафтящейся шмотки
        '''
        super(FCEItemCraftReceipt, self).__init__(media_dir, name, 'receipts')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def set_craft_cost(self, assembler, ingridient_name, ingridient_amount):
        if 'receipt' not in self.data:
            self.data['receipt'] = {}
        with FCEItem(self._media_dir, ingridient_name) as ingridient_item:
            ingridient_item.set_participate_in_craft(self.name)
            self.data['receipt'][ingridient_item.name] = ingridient_amount
        if type(assembler) == FCEItem:
            self.set_simple_key('assembler', assembler.name)
            assembler.set_assemble_craft(self.name)
        else:
            self.set_simple_key('assembler', self._compact_name(assembler))
            with FCEItem(self._media_dir, assembler) as assembler_item:
                assembler_item.set_assemble_craft(self.name)
