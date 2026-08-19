import pandas as pd
from config import MAPEAMENTO_PROCEDIMENTOS
from config import URL_FATURAMENTO
from config import URL_UNIMED
from config import URL_INDICADORES


def processar_indicadores_unidades_base(df_ind_unidades):
    # 1. Tira as unidades do índice e transforma em uma coluna de verdade
    df = df_ind_unidades.reset_index()
    
    # 2. Renomeia a PRIMEIRA coluna diretamente (mais seguro)
    nome_coluna_unidade = df.columns[0]
    df.rename(columns={nome_coluna_unidade: 'Unidade_Padrao'}, inplace=True)
    
    # 3. Força a coluna a ser texto (.astype(str)) e então faz a limpeza
    df['Unidade_Padrao'] = df['Unidade_Padrao'].astype(str).str.replace('Quant. de pacientes ', '', regex=False)
    
    # 4. Remove a linha de "Total"
    df = df[df['Unidade_Padrao'] != 'Total']
    
    return df

df_original = pd.read_excel(URL_INDICADORES, sheet_name='OKRs Consolidados')
df_processado = processar_indicadores_unidades_base(df_original)
print(df_processado)