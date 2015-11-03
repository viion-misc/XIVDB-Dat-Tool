from xivdm.patch.Patchable import Patchable, Boot

class Manager:
    def __init__(self, game_path):
        self._game_path = game_path

        self._patchables = {
            'game': Patchable(game_path, 'game'),
            'boot': Boot(game_path, 'boot')
        }

    def get_patchables(self):
        return self._patchables.keys()

    def get_patchable(self, name):
        return self._patchables[name]
