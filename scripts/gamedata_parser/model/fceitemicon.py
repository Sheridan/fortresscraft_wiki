import os
import requests
import time
from PIL import Image


tryed_links = []
doit = False


class FCEItemIcon:
    def __init__(self, item, icons_dir):
        self._item = item
        self._icons_dir = icons_dir

    def _make_icon_local_path(self, dimension):
        return '%s/%s/%s.png' % (self._icons_dir, dimension, self._item.name)

    def _make_icon_url(self, icon_name):
        return 'http://fcedb.com/images/sprite/%s.png' % (icon_name,)

    def _get_possible_names(self):
        return self._item.data['possible_names']

    def _check_icon_already_here(self):
        return os.path.isfile(self._make_icon_local_path(64))

    def _download_icon(self):
        icon_path = self._make_icon_local_path(64)
        for icon_name in self._get_possible_names():
            url = self._make_icon_url(icon_name)
            if url not in tryed_links:
                print('Downloading %s' % (url,), end=' ', flush=True)
                response = requests.get(url)
                print('%s [Total tryed %s]' % ('ok' if response.ok else 'nope', len(tryed_links)))
                if response.ok:
                    print('Downloaded %s' % (icon_path,))
                    with open(icon_path, 'wb') as handler:
                        handler.write(response.content)
                    return True
                else:
                    tryed_links.append(url)
                # time.sleep(1)
        return False

    def _resize_icon(self):
        icon_64_path = self._make_icon_local_path(64)
        for size in [16, 32]:
            icon_x_path = self._make_icon_local_path(size)
            im = Image.open(icon_64_path)
            im.thumbnail((size, size), Image.ANTIALIAS)
            im.save(icon_x_path, "PNG")

    def get_icon(self):
        if doit:
            if self._check_icon_already_here():
                return
            downloaded = self._download_icon()
            # self._item.set_icon_available(downloaded)
            if downloaded:
                self._resize_icon()
