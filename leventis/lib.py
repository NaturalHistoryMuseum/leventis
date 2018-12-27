
import os
import leventis


class DirectoryPath(object):

    _base = os.path.dirname(os.path.dirname(
        os.path.abspath(leventis.__file__)))

    def __init__(self):
        os.makedirs(self.images, exist_ok=True)
        os.makedirs(self.ocr, exist_ok=True)

    @property
    def data(self):
        return os.path.join(self._base, 'data')

    @property
    def images(self):
        return os.path.join(self.data, 'images')

    @property
    def ocr(self):
        return os.path.join(self.data, 'ocr')
