from ..core.datasource import Datasource


class DS156(Datasource):
    data_root_url = 'http://dadosabertos.c3sl.ufpr.br/curitiba/156/'
    metadata_file = '156.xml'
    file_pattern = '_156_-_Base_de_Dados.csv'

    def clean_data(self, df):
        from datetime import datetime

        df['DATA'] = df['DATA'].str.strip()
        df['DATA'] = df.apply(lambda x: datetime.strptime(x['DATA'], '%d/%m/%Y') if type(x['DATA']) is str else None, axis=1)

        return df

    def get_pandas_dataframe(self, date_prefix=None, apply_cleanup=True):
        csv_file, csv_encoding = self.download(date_prefix=date_prefix)

        import pandas as pd

        field_names = ['SOLICITACAO', 'TIPO', 'ORGAO', 'DATA',
               'HORARIO', 'ASSUNTO', 'SUBDIVISAO', 'DESCRICAO',
               'LOGRADOURO_ASS', 'BAIRRO_ASS', 'REGIONAL_ASS',
               'MEIO_RESPOSTA', 'OBSERVACAO', 'SEXO', 'BAIRRO_CIDADAO',
               'REGIONAL_CIDADAO', 'DATA_NASC', 'TIPO_CIDADAO',
               'ORGAO_RESP', 'RESPOSTA_FINAL', 'RESPOSTA_FINAL_DETALHE']

        df = pd.read_csv(csv_file, sep=';', encoding=csv_encoding,
                           error_bad_lines=False,
                           skiprows=[0,1],
                           names=field_names)

        if apply_cleanup:
            df = self.clean_data(df)

        return df
