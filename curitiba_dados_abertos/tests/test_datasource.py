import pytest

from curitiba_dados_abertos.core.datasource import Datasource


def test_datasource_abstract_on_get_pandas_dataframe():
    ds = Datasource()

    with pytest.raises(NotImplementedError, match('Implementation of method would be performed on inherited classes')):
        ds.get_pandas_dataframe()
