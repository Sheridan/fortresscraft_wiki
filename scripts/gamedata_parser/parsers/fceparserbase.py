import xml.etree.ElementTree


class FCEParserBase:
    def __init__(self, gamedata_dir, media_dir):
        self._media_dir = media_dir
        self._gamedata_dir = gamedata_dir

    def load_xml(self, xml_name):
        print('Parsing xml %s' % (xml_name))
        return xml.etree.ElementTree.parse('%s/%s.xml' % (self._gamedata_dir, xml_name)).getroot()

    def _find_one_of(self, xml_root, keys):
        for key in keys:
            xml_key = xml_root.find(key)
            if xml_key is not None:
                return xml_key
        return None

    # def process_subkeys(self, item_data, key_name, key_root):
    #     if key_name not in item_data:
    #         item_data[key_name] = []
    #     for subkey in key_root:
    #         if subkey.text not in item_data[key_name]:
    #             item_data[key_name].append(subkey.text)
