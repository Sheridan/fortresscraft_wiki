import os
import numpy
import cv2
import itertools
from PIL import Image, ImageDraw
from gamedata_parser.jsonbase import JsonBase


class SpriteParser(JsonBase):
    def __init__(self, media_dir, sprite_file_name):
        super(SpriteParser, self).__init__(media_dir)
        self._sprite_file_path = '%s/%s' % (self._sprites_dir, sprite_file_name)
        print("Image: %s" % self._sprite_file_path)
        self._border = 10
        self._bounds = {'minw': 20, 'minh': 20, 'maxw': 256, 'maxh': 70}
        self._json = '%s.json' % self._sprite_file_path

    def save_dbg_img(self, name, img):
        cv2.imwrite('%s/%s.png' % (self._sprites_dir, name), img)

    def save_preview(self, rects):
        preview_img = Image.open(self._sprite_file_path)
        preview_drawer = ImageDraw.Draw(preview_img)
        for shash in rects.keys():
            rect = rects[shash]
            print("%s: [%s:%s]->[%s,%s], (%s, %s)" % (
                shash,
                rect['tl']['x'],
                rect['tl']['y'],
                rect['br']['x'],
                rect['br']['y'],
                rect['w'],
                rect['h'],))
            preview_drawer.rectangle(
                (
                    (
                        rect['tl']['x'],
                        rect['tl']['y']
                    ),
                    (
                        rect['br']['x'],
                        rect['br']['y']
                    )
                ))
            preview_drawer.text((rect['tl']['x']+2, rect['tl']['y']+1), shash, fill=(255, 0, 16, 255))
        preview_img.save('%s.preview.png' % self._sprite_file_path)

    def adjust_gamma(self, img, gamma=1.0):
        invGamma = 1.0 / gamma
        table = numpy.array([((i / 255.0) ** invGamma) * 255 for i in numpy.arange(0, 256)]).astype("uint8")
        return cv2.LUT(img, table)

    def open_and_prepare_sprites(self):
        img = cv2.imread(self._sprite_file_path, cv2.IMREAD_UNCHANGED)
        img = cv2.copyMakeBorder(img, self._border, self._border, self._border, self._border, cv2.BORDER_CONSTANT, value = [0, 0, 0, 0])
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        self.save_dbg_img('gray', img)
        return img

    def extract_cv_contours(self, img):
        im2, contours, hierarchy = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        return contours

    def make_rects_list(self, cv_contours):
        rects = {}
        for i, cnt in enumerate(cv_contours):
            x, y, w, h = cv2.boundingRect(cnt)
            x = x - self._border
            y = y - self._border
            if w >= self._bounds['minw'] and h >= self._bounds['minh'] and w < self._bounds['maxw'] and h < self._bounds['maxh']:
                shash = "%s%s" % (x, y)
                rects[shash] = {
                    'tl': {'x': x, 'y': y},
                    'br': {'x': x + w, 'y': y + h},
                    'w': w,
                    'h': h
                    }
        return rects

    def make_less_sized_string(self, shash, rect, size=64):
        factor = 1
        if size == 32:
            factor = 2
        if size == 16:
            factor = 4
        return '&.fce_icon_%s_%s { .fce_icons_%s(%s, %s, %s, %s); }\n' % (
                size,
                shash,
                size,
                round(rect['tl']['x'] / factor),
                round(rect['tl']['y'] / factor),
                round(rect['w'] / factor),
                round(rect['h'] / factor),
            )

    def make_less(self, rects):
        with open('/data/home/sheridan/development/fortresscraft/fortresscraft.info/mediawiki/extensions/fce/styles/icons.less', 'w') as less:
            less.write('@import "fce.base.less";\n\n span {\n')
            for shash in rects.keys():
                rect = rects[shash]
                for size in [64, 32, 16]:
                    less.write(self.make_less_sized_string(shash, rect, size))
            less.write('}\n')

    def parse(self):
        sprites_list_img = self.open_and_prepare_sprites()
        cv_contours = self.extract_cv_contours(sprites_list_img)
        rects = self.make_rects_list(cv_contours)
        self.save_preview(rects)
        self.make_less(rects)


