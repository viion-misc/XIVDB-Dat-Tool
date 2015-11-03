from xivdm.exd.exl import extract_categories
from xivdm.exd.Category import Category

class Manager:
    def __init__(self, dat_manager):
        self._dat_manager = dat_manager
        self._categories = {}

        try:
            self._categories = {
                category_name: Category(dat_manager, category_name)
                for category_name in extract_categories(dat_manager.get_file('exd/root.exl'))
            }
        except Exception as e:
            print('exd > manager (15) __init__ NameError: ', e)

    def get_categories(self):
        return self._categories.keys()

    def get_category(self, name):
        return self._categories[name]