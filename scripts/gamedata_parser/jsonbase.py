import json
import os
import re


class JsonBase:
    def __init__(self, media_dir):
        self._media_dir = media_dir
        self._icons_dir = '%s/icons' % (self._media_dir)
        self._json_dir = '%s/json' % (self._media_dir)
        self._items_dir = '%s/items' % (self._json_dir)
        self._lists_dir = '%s/lists' % (self._json_dir)
        self._research_dir = '%s/research' % (self._json_dir)
        self._sprites_dir = '%s/sprites' % (self._media_dir)

    def _get_json_list(self, where):
        path = '%s/%s' % (self._json_dir, where)
        return sorted([os.path.join(path, file) for file in os.listdir(path)], key=os.path.getctime)

    def _load_json(self, filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except:
            raise

    def _save_json(self, filename, data):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4, sort_keys=True)

    def _compact_name(self, name):
        return re.sub(r'[^a-z0-9]', '', name.lower())

    def _make_filename(self, where, name):
        return '%s/%s/%s.json' % (self._json_dir, where, name)
