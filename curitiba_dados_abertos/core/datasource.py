import re
from xml.dom import minidom

import requests

from .utils import download_file 


class Datasource(object):
    data_root_url = None
    metadata_file = None
    file_pattern = None

    _xml_handler = None

    latest_csv_url = None
    download_folder = None
    force_overwrite_file = False

    def __init__(self, download_folder=None, force_overwrite_file=False):
        self._metadata_xml_handler = self._load_metadata_xml_handler()
        self.latest_csv_url = self._fetch_latest_csv_file()
        self.download_folder = download_folder
        self.force_overwrite_file = force_overwrite_file

    def _load_metadata_xml_handler(self):
        """This fuction connects to website of dados abertos, fetches and loads XML handler;
        returns:
            minidom object
        """

        metadata_url = f'{self.data_root_url}/{self.metadata_file}'
        xml_index_get_request = requests.get(metadata_url)

        xml_index = None
        if xml_index_get_request.status_code == 200:
            xml_index = minidom.parseString(xml_index_get_request.text)
        else:
            raise SystemError(f'Unable to load the metadata url \'{metadata_url}\'')

        return xml_index

    def _fetch_latest_csv_file(self):
        dados = self._metadata_xml_handler.getElementsByTagName('dado')
        csv_file_url = None
        for dado in dados:
            name = dado.attributes['arquivo'].value
            if self.file_pattern in name:
                csv_file_url = name
                break

        latest_csv_url = f'{self.data_root_url}/{csv_file_url}' if csv_file_url else None

        return latest_csv_url

    def get_info(self):

        title = self._metadata_xml_handler.getElementsByTagName('titulo')[0].firstChild.nodeValue
        responsible_organization = self._metadata_xml_handler.getElementsByTagName('orgaoresponsavel')[0].firstChild.nodeValue

        data = {
            'title': title,
            'responsible_organization': responsible_organization,
            'latest_csv_url': self.latest_csv_url
        }

        return data

    def download(self, date_prefix=None):
        download_url = f'{self.data_root_url}/{date_prefix}{self.file_pattern}' if date_prefix else self.latest_csv_url

        return download_file(url=download_url, 
                             folder=self.download_folder, 
                             force_overwrite=self.force_overwrite_file)

    def get_pandas_dataframe(self, date_prefix=None):
        raise NotImplementedError()

    def list_available_items(self):
        request_index = requests.get(url=f'{self.data_root_url}/')

        if request_index.status_code != 200:
            raise OSError('Unable to fetch text index')

        urls = re.findall(
            rf'href=\"(.+){self.file_pattern}\"',
            request_index.text)

        return urls
