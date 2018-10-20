import os


class Extractor:
    def __init__(self, base_dir, config):
        self.base_dir = self._validate_dir(base_dir)
        self.config = config

    @staticmethod
    def _validate_dir(d):
        if not os.path.isdir(d):
            raise Exception('invalid directory: {}'.format(d))
        return d

    def load(file_path):
        pass
