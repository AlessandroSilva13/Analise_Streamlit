import pandas as pd
from config import MAPEAMENTO_PROCEDIMENTOS

def processar_faturamento_base(df_fat):
    df_fat.rename(columns={'VALOR BRUTO': 'Valor bruto'}, inplace=True)
    df = df_fat.dropna(axis=1, how='all')
    df['Data'] = pd.to_datetime(dict(year=df['ANO'], month=df['COMPETÊNCIA'], day=1))
    return df[df['SITUAÇÃO'] != 'CANCELADA']

def processar_unimed_base(df_unimed):
    df_unimed['Código'] = pd.to_numeric(df_unimed['Código'], errors='coerce').astype('Int64')
    df_unimed['MES_ANO'] = pd.to_datetime(df_unimed['MES_ANO'])
    return df_unimed

# --- Funções para gerar os dados dos gráficos baseados nas datas ---

def obter_dados_faturamento(df_faturamento, dt_inicio, dt_fim):
    mascara = (df_faturamento['Data'] >= dt_inicio) & (df_faturamento['Data'] <= dt_fim)
    df_filtrado = df_faturamento.loc[mascara]
    
    # Geral
    df_evolucao = df_filtrado.groupby(['Data'])[['Valor bruto','Valor líquido']].sum().reset_index()
    
    # Outros Planos
    df_outros = df_filtrado[df_filtrado['OPERADORA'] != 'Unimed Fortaleza']
    df_evolucao_outros = df_outros.groupby(['Data', 'OPERADORA'])[['Valor bruto']].sum().reset_index()
    
    # Unimed
    df_unimed_fat = df_filtrado[df_filtrado['OPERADORA'] == 'Unimed Fortaleza']
    df_evolucao_unimed = df_unimed_fat.groupby(['Data', 'OPERADORA'])[['Valor bruto','Valor líquido']].sum().reset_index()
    
    return df_evolucao, df_evolucao_outros, df_evolucao_unimed

def obter_dados_indicadores(df_indicadores):
    meses = df_indicadores.columns[:-1]
    
    # Pacientes totais (Fig4)
    totais = pd.to_numeric(df_indicadores.loc["Quant. de pacientes NPC", meses], errors='coerce').dropna()
    df_fig4 = totais.reset_index()
    df_fig4.columns = ['Meses', 'Quantidade']
    
    # Pacientes Julho (Fig5)
    df_planos = df_indicadores.drop(['Quant. de pacientes NPC'], errors='ignore')
    dados_julho = pd.to_numeric(df_planos['Jul'], errors='coerce').dropna()
    dados_julho = dados_julho[dados_julho > 0]
    
    return df_fig4, dados_julho

def obter_dados_procedimentos(df_unimed):
    df_proc = df_unimed.groupby(['MES_ANO', 'Código']).size().reset_index(name='Quantidade')
    df_proc['Procedimento'] = df_proc['Código'].map(MAPEAMENTO_PROCEDIMENTOS).fillna('Outros/Não Mapeado')
    
    # Para Fig6 (barras empilhadas por mês)
    df_barras = df_proc.groupby(['MES_ANO', 'Procedimento'], as_index=False)['Quantidade'].sum()
    
    # Para Fig7 (pizza total)
    df_pizza = df_proc.groupby('Procedimento', as_index=False)['Quantidade'].sum()
    
    return df_barras, df_pizza

def obter_dados_profissionais(df_profissionais, dt_inicio, dt_fim):
    mascara = (df_profissionais['Pagamento'] >= dt_inicio) & (df_profissionais['Pagamento'] <= dt_fim)
    df_filtrado = df_profissionais.loc[mascara]
    
    df_faturamento_vinculo = df_filtrado.groupby(['Vinculo do Período do Pagamento', 'Pagamento'])[['Valor_Faturamento']].sum().reset_index()
    
    df_reasons = df_filtrado.loc[df_filtrado['reason_for_charge'].notnull()]
    df_reasons = df_reasons.groupby(['reason_for_charge', 'Pagamento'])[['Valor']].sum().reset_index()
    
    return df_faturamento_vinculo, df_reasons