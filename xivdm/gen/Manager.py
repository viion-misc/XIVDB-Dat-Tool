from os import path, makedirs
import pickle
import gzip

from xivdm.gen.gens import *

class Manager:
    CACHE_PATH ='cache/%s.gz'

    def __init__(self, dat_manager):
        self._dat_manager = dat_manager
        self._categories = {
            'icons': icons,
            'maps_icons': maps_icons,
            'models': models
        }
        self._caches = {}

    def get_categories(self):
        return self._categories.keys()

    def get_category(self, name):
        return self._get_cache(name)

    def _get_cache(self, name):
        if not name in self._caches:
            cache_path = self.CACHE_PATH % name

            if not path.exists(path.dirname(cache_path)):
                makedirs(path.dirname(cache_path))

            if path.exists(cache_path):
                with gzip.open(cache_path, 'rb') as file_handle:
                    self._caches[name] = pickle.load(file_handle)
            else:
                self._caches[name] = self._categories[name](self._dat_manager)
        return self._caches[name]

    def __del__(self):
        for name, value in self._caches.items():
            cache_path = self.CACHE_PATH % name

            with gzip.open(cache_path, 'wb') as file_handle:
                pickle.dump(value, file_handle)