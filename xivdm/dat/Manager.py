import zlib
from os import path, makedirs
import logging

from xivdm.dat.Category import Category

class Manager:
    CATEGORIES = {
        'common': 0x00,
        'bgcommon': 0x01,
        'bg': 0x02,
        'cut': 0x03,
        'chara': 0x04,
        'shader': 0x05,
        'ui': 0x06,
        'sound': 0x07,
        'vfx': 0x08,
        #'ui_script': 0x09,
        'exd': 0x0A,
        'game_script': 0x0B,
        'music': 0x0C
    }

    def __init__(self, game_path):
        base_path = path.join(game_path, 'game/sqpack/ffxiv')
        self._categories = {}
        for category_name, index in Manager.CATEGORIES.items():
            try:
                category = Category(category_name, base_path, '%0.6x.win32' % (index << 0x10))
                self._categories[category_name] = category
            except Exception as e:
                logging.error("Couldn't process category[%s]: %s", category_name, e)

    def get_categories(self):
        return self._categories.keys()

    def get_category(self, name):
        print('dat > manager > get_category', name)
        return self._categories[name]

    def get_file(self, name):
        print('dat > manager > get_file', name)
        logging.info('%s', name)

        dir_hash, file_hash = get_hashes(name)
        print('dat > manager > get_file > dir_hash', dir_hash, 'file_hash', file_hash)

        category = self.get_category_from_filename(name)
        print('dat > manager > get_file > category', category)

        file_data = category.get_file(dir_hash, file_hash)

        return file_data

    def check_dir_existence(self, name):
        (dir_hash, _) = get_hashes(name)
        category = self.get_category_from_filename(name)
        result = category.check_dir_existence(dir_hash)
        return result

    def check_file_existence(self, name):
        (dir_hash, file_hash) = get_hashes(name)
        category = self.get_category_from_filename(name)
        result = category.check_file_existence(dir_hash, file_hash)
        return result

    def get_category_from_filename(self, name):
        print('dat > manager > get_category_from_filename', name)
        return self.get_category(name.split('/', 1)[0].lower())


def get_hashes(name):
    print('dat > manager > get_hashes:', name)

    dir_part, file_part = name.lower().rsplit('/', 1)
    print('dat > manager > get_hashes', dir_part, file_part)

    return get_hash(dir_part), get_hash(file_part)

def get_hash(string):
    return zlib.crc32(bytes(string, 'ascii')) ^ 0xFFFFFFFF

