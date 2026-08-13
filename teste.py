import pandas as pd

df_unimed = pd.read_excel('Analise_Streamlit/UNIMED_CONSOLIDADO_DATADO.xlsx', header = 3)
df_unimed['Código'] = pd.to_numeric(df_unimed['Código'], errors='coerce').astype('Int64')
df_unimed['MES_ANO'] = pd.to_datetime(df_unimed['MES_ANO'])

mapeamento_procedimentos = {
        2010368: 'Fisioterapia',
        5000001: 'Psicomotricidade',
        5000050: 'Psicopedagogia',
        5000518: 'Fonoaudiologia',
        5000510: 'Psicologia',
        5000061: 'Fonoaudiologia',
        5000008: 'Terapia Ocupacional',
        5000047: 'Psicologia',
        5000517: 'Terapia Ocupacional',
        5000046: 'Psicologia'
}

df_unimed_proc = df_unimed.groupby(['MES_ANO', 'Código']).size().reset_index(name='Quantidade')
df_unimed_proc['Procedimento'] = df_unimed_proc['Código'].map(mapeamento_procedimentos)
df_unimed_proc['Procedimento'] = df_unimed_proc['Procedimento'].fillna('Outros/Não Mapeado')
df_unimed_proc = df_unimed_proc[['MES_ANO', 'Código', 'Procedimento', 'Quantidade']]
print(df_unimed_proc)
