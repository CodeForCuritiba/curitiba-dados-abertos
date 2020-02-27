import os, re

import pytest

from curitiba_dados_abertos.datasources import DS156

@pytest.fixture
def ds156():
    return DS156()

def test_provision_dataset(ds156):
    ds_info = ds156.get_info()

    assert ds_info['title'] == '156'
    assert ds_info['responsible_organization'] == 'Governo Municipal'

def test_dataset_latest_csv_url(ds156):
    assert 'csv' in ds156.latest_csv_url

def test_ds_download_latest_csv_on_current_dir(ds156):
    filename, encoding = ds156.download()

    assert type(filename) == str
    assert type(encoding) == str

    assert os.path.isfile(filename)
    assert ds156.file_pattern in filename

def test_ds_download_old_on_current_dir(ds156):
    list_items = ds156.list_available_items()
    date_prefix_item = list_items[0]

    filename, encoding = ds156.download(date_prefix=date_prefix_item)

    assert type(filename) == str
    assert type(encoding) == str

    assert os.path.isfile(filename)
    assert ds156.file_pattern in filename
    assert date_prefix_item in filename

def test_ds_get_available_list(ds156):

    list_items = ds156.list_available_items()

    assert type(list_items) == list
    assert len(list_items) > 0

    for item in list_items:
        assert bool(re.match(r'(2[0-9]{3}-[0-9]{2}-[0-9]{2})', item)) == True

def test_ds_get_pandas_dataframe_latest(ds156):
    pd_ds156 = ds156.get_pandas_dataframe()

    assert pd_ds156 is not None
    assert type(pd_ds156['ASSUNTO'].to_list()) == list

def test_ds_get_pandas_dataframe_clean_data(ds156):
    pd_ds156 = ds156.get_pandas_dataframe(apply_cleanup=False)

    clean_data = ds156.clean_data(pd_ds156)

    assert clean_data is not None
    assert 'pandas.core.frame.DataFrame' in str(type(clean_data))

def test_ds_get_pandas_dataframe_dated(ds156):
    list_items = ds156.list_available_items()
    date_prefix_item = list_items[0]

    pd_ds156 = ds156.get_pandas_dataframe(date_prefix=date_prefix_item)

    assert pd_ds156 is not None
    assert type(pd_ds156['ASSUNTO'].to_list()) == list
