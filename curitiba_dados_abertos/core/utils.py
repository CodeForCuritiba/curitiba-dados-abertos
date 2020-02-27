import os

import requests


def download_file(url, folder=None, force_overwrite=False, try_get_infer_encoding=False):
    """ Downloads a file from a website
    params:
        - url (mandatory)
        - folder - Destination folder; None means current directory
        - force_overwrite - if False, it will check if the dest file exists. If does, don't update
    returns:
        - local_filename - The path of downloaded file
        - file_encoding
    """
    local_filename = url.split('/')[-1]
    local_filename = local_filename if not folder \
        else f'{folder}/{local_filename}'

    file_encoding = None
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        file_encoding = r.apparent_encoding if try_get_infer_encoding else r.encoding

        if os.path.isfile(local_filename):

            if not force_overwrite:
                return local_filename, file_encoding

        with open(local_filename, 'wb') as file_handler:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    file_handler.write(chunk)

    return local_filename, file_encoding


