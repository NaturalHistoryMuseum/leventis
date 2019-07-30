
import requests
import requests_cache
from PIL import Image

from leventis.preprocess import text_preprocessor


requests_cache.install_cache('bhl.cache')


class BHLPage(object):
    def __init__(self, page_id):
        self.page_id = page_id

    @property
    def image(self):
        return self.get_image()

    @property
    def text(self):
        return self.get_text()

    def get_image(self):
        image_url = f'https://www.biodiversitylibrary.org/pageimage/{self.page_id}'
        r = self._get_request(image_url)
        return Image.open(r.raw)

    def get_text(self):
        text_url = f'https://www.biodiversitylibrary.org/pagetext/{self.page_id}'
        r = self._get_request(text_url)
        return r.text

    def get_normalised_text(self):
        return text_preprocessor(self.text)

    @staticmethod
    def _get_request(url):
        r = requests.get(url, stream=True)
        r.raise_for_status()
        return r
