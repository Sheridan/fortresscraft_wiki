
from gamedata_parser.model.fceitem import FCEItem
from gamedata_parser.model.fceresearch import FCEResearch
from gamedata_parser.jsonbase import JsonBase

class JsonMixer(JsonBase):
    def __init__(self, media_dir):
        super(JsonMixer, self).__init__(media_dir)
        self._mixins = self._load_json("/data/home/sheridan/development/fortresscraft/fortresscraft.info/media/json/mixins.json")

    def mix(self):
        for place in ['items', 'research']:
            for processing_file in self._get_json_list(place):
                processing_data = self._load_json(processing_file)
                if processing_data['index_name'] in self._mixins:
                    processing_data['mixin'] = self._mixins[processing_data['index_name']]
                self._save_json(processing_file, processing_data)

