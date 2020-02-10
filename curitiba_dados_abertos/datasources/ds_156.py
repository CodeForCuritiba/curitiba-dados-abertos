from ..core.datasource import Datasource


class DS156(Datasource):
    data_root_url = 'http://dadosabertos.c3sl.ufpr.br/curitiba/156/'
    metadata_file = '156.xml'
    file_pattern = '_156_-_Base_de_Dados.csv'
