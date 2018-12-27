import os
import re
import pandas as pd
import numpy as np
import requests
import requests_cache
import logging
import pytesseract
from pathlib import Path
from PIL import Image
from io import BytesIO

from pathlib import Path

from leventis.directory_path import DirectoryPath
from leventis.helpers import extract_number_from_string

CITATIONS_CSV_FILENAME = 'bhl_citations.csv'

requests_cache.install_cache('bhl_cache')
logger = logging.getLogger('leventis')


class BHLCitations(object):

    dir_path = DirectoryPath()

    def __init__(self, binomial=None):
        self.api = BHLAPI()

        self.df = pd.read_csv(
            os.path.join(self.dir_path.data, CITATIONS_CSV_FILENAME)
        )
        # # Page is the format Page XYZ so create a numeric column
        # self.df['PageNumber'] = self.df['Page'].apply(
        #     extract_number_from_string)
        # # Create column for the image URL data
        # self.df['ImageURL'] = np.nan
        # # Create column for the OCR text
        # self.df['OCR'] = np.nan
        # if binomial:
        #     self.df = self.df[self.df['Binomial'] == binomial]

        # self._get_bhl_image_urls()
        # # self._get_bhl_image_urls()

    def _get_processed_csv(self):
        pass

    def _get_bhl_image_urls(self):

        for binomial in list(self.df['Binomial'].unique()):
            bhl_name_result = self._bhl_api_search_name(binomial)

            if not bhl_name_result:
                logger.error("BHL name not found {}".format(binomial))
                continue

            for title in bhl_name_result['Titles']:
                publication_title = title['ShortTitle']
                for item in title['Items']:
                    publication_volume = item.get('Volume')
                    for page in item['Pages']:
                        try:
                            publication_page_number = page['PageNumbers'][0]['Number']
                        except KeyError:
                            continue

                        # Update the page URL of the matching row
                        self.df.loc[
                            (self.df['Volume'] == publication_volume)
                            &
                            (self.df['PageNumber'] == publication_page_number)
                            &
                            (self.df['Binomial'] == binomial)
                            &
                            (self.df['Title'].str.contains(
                                re.escape(publication_title), case=False)), 'ImageURL'
                        ] = page['FullSizeImageUrl']

    def _bhl_api_search_name(self, name):
        name_metadata = self.api.get_name_metadata(name)
        return name_metadata['Result'][0]

    def get_images(self):
        for _, citations in self.get_citations_with_url().iterrows():
            yield BHLImage(citations['ImageURL'])

    def get_citations_without_url(self):
        return self.df.loc[(self.df['ImageURL'].isnull())]

    def get_citations_with_url(self):
        return self.df.loc[(self.df['ImageURL'].notnull())]

    def output_citations_without_urls(self):
        columns = ['Binomial']
        return self.get_citations_without_url().to_string(columns=columns)


class BHLImage(object):

    dir_path = DirectoryPath()

    def __init__(self, url):
        self.url = url
        self._image = self._open_or_download_image()

    def _open_or_download_image(self):
        if os.path.isfile(self.file_path):
            return Image.open(self.file_path)
        else:
            return self._download_remote_image()

    @staticmethod
    def _parse_image_id_from_url(url):
        # Extract last part of url
        # https://www.biodiversitylibrary.org/pageimage/27274329 -> 27274329
        return url.split("/")[-1]

    @property
    def file_id(self):
        return self._parse_image_id_from_url(self.url)

    @property
    def file_name(self):
        return '{}.jpg'.format(self.file_id)

    @property
    def file_path(self):
        return os.path.join(self.dir_path.images, self.file_name)

    def _download_remote_image(self):
        r = requests.get(self.url)
        r.raise_for_status()
        image = Image.open(BytesIO(r.content))
        image.save(self.file_path)
        return image

    def ocr(self):
        ocr_image = BHLOCRImage(self._image)
        ocr_image.save()


class BHLOCRImage(object):

    dir_path = DirectoryPath()

    def __init__(self, image):
        self._image = image

    @property
    def file_id(self):
        # Get filename without extension
        return Path(self._image.filename).stem

    @property
    def file_name(self):
        return '{}.txt'.format(self.file_id)

    @property
    def file_path(self):
        return os.path.join(self.dir_path.ocr, self.file_name)

    def get_text(self):
        return pytesseract.image_to_string(self._image)

    def save(self):
        file = open(self.file_path, 'w')
        file.write(self.get_text())
        file.close()


class BHLAPI(object):

    api_key = '81514384-c14e-4b16-85df-ff2e6a8370e2'
    end_point = 'https://www.biodiversitylibrary.org/api3'

    def get_name_metadata(self, name):
        operation = 'GetNameMetadata'
        params = {'name': name}
        return self.call(operation, params)

    def get_publication(self, title):
        operation = 'PublicationSearch'
        params = {
            'searchterm': title,
        }
        return self.call(operation, params)

    def get_item_metadata(self, item_id):
        operation = 'GetItemMetadata'
        params = {
            'id': item_id,
            'pages': 'true'
        }
        return self.call(operation, params)

    def call(self, operation, params):
        params['op'] = operation
        params['apikey'] = self.api_key
        params['format'] = 'json'
        r = requests.get(self.end_point, params)
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            return None
        return r.json()
