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
