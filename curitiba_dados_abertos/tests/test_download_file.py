import pytest

from curitiba_dados_abertos.core.utils import download_file

SMALL_FILE_URL='https://support.oneskyapp.com/hc/en-us/article_attachments/202761727/example_2.json'

def test_download_file_from_url():
    filename, encoding = download_file(url=SMALL_FILE_URL,
                                       folder=None,
                                       force_overwrite=False,
                                       try_get_infer_encoding=True)

    assert 'example_2.json' in filename
    assert type(encoding) == str

def test_download_file_in_different_folder():
    filename, encoding = download_file(url=SMALL_FILE_URL,
                                       folder='/tmp',
                                       force_overwrite=False,
                                       try_get_infer_encoding=True)

    assert filename == '/tmp/example_2.json'
    assert type(encoding) == str

def test_download_file_with_force_overwrite():

    with open('/tmp/example_1.json', 'w') as f:
        f.write('JOEY')

    filename, encoding = download_file(
        url='https://support.oneskyapp.com/hc/en-us/' \
            'article_attachments/202761627/example_1.json',
        folder='/tmp',
        force_overwrite=True,
        try_get_infer_encoding=True)

    assert filename == '/tmp/example_1.json'
    assert type(encoding) == str

    read_text = None
    with open('/tmp/example_1.json') as f:
        read_text = f.read()

    assert read_text is not None
    assert 'JOEY' not in read_text

def test_download_file_without_force_overwrite():

    with open('/tmp/example_1.json', 'w') as f:
        f.write('JOEY')

    filename, encoding = download_file(
        url='https://support.oneskyapp.com/hc/en-us/' \
            'article_attachments/202761627/example_1.json',
        folder='/tmp',
        force_overwrite=False,
        try_get_infer_encoding=True)

    assert filename == '/tmp/example_1.json'
    assert type(encoding) == str

    read_text = None
    with open('/tmp/example_1.json') as f:
        read_text = f.read()

    assert read_text is not None
    assert 'JOEY' in read_text

