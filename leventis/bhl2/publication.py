
import os
import pandas as pd
import requests
import requests_cache

from pathlib import Path

from leventis.lib import get_data_directory
from leventis.helpers import extract_number_from_string


class BHLPublication(object):
    def __init__(self, title, volume):
        self.title = title
        self.volume = volume
        self.api = BHLAPI()
        try:
            self._pages = self.get_publication_pages()
        except TypeError:
            pass

    def get_publication_pages(self):
        publication = self.fetch_publication_from_bhl(self.title)
        item = self._filter_items_by_volume(publication, self.volume)
        item_metadata = self.fetch_item_metadata_from_bhl(item['ItemID'])

        return {extract_number_from_string(page['PageNumbers'][0]['Number']): page['FullSizeImageUrl']
                for page in item_metadata['Pages'] if page['PageNumbers']}

    def fetch_publication_from_bhl(self, title):
        response = self.api.get_publication(title)
        try:
            return response['Result']
        except TypeError:
            print('No publication: {}'.format(title))

    def fetch_item_metadata_from_bhl(self, item_id):
        response = self.api.get_item_metadata(item_id)
        return response['Result'][0]

    @staticmethod
    def _filter_items_by_volume(items, volume):
        return next((item for item in items if item.get('Volume', None) == volume), None)

    def get_page(self, page_number):
        # print(page_number)
        # print(self._pages.keys())
        return self._pages[page_number]
