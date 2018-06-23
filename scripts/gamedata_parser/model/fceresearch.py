from gamedata_parser.model.fceitembase import FCEItemBase
from gamedata_parser.model.fceitemicon import FCEItemIcon
from gamedata_parser.model.fceitem import FCEItem


class FCEResearch(FCEItemBase):
    def __init__(self, media_dir, name):
        '''
        name - имя резерча
        '''
        super(FCEResearch, self).__init__(media_dir, name, 'research')

    def __enter__(self):
        self._load()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        FCEItemIcon(self, self._icons_dir).get_icon()
        self._save()

    def set_project_requirement(self, requirement_item_name, amount):
        if 'project_item_requirements' not in self.data:
            self.data['project_item_requirements'] = {}
        with FCEItem(self._media_dir, requirement_item_name) as requirement_item:
            self.data['project_item_requirements'][requirement_item.name] = amount
