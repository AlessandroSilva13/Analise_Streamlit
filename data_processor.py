import pandas as pd
from config import MAPEAMENTO_PROCEDIMENTOS
from config import MESES_PT

def processar_faturamento_base(df_fat):
    df_fat.rename(columns={'VALOR BRUTO': 'Valor bruto', 'EMPRESA':'Unidade_Padrao'}, inplace=True)
    df = df_fat.dropna(axis=1, how='all')
    df['Data'] = pd.to_datetime(dict(year=df['ANO'], month=df['COMPETÊNCIA'], day=1))
    return df[df['SITUAÇÃO'] != 'CANCELADA']

def processar_unimed_base(df_unimed):
    df_unimed['Código'] = pd.to_numeric(df_unimed['Código'], errors='coerce').astype('Int64')
    df_unimed['MES_ANO'] = pd.to_datetime(df_unimed['MES_ANO'])
    df_unimed.rename(columns={'Unidade':'Unidade_Padrao'}, inplace=True)
    return df_unimed


def obter_dados_faturamento(df_faturamento, dt_inicio, dt_fim, unidade): 
    mascara = (df_faturamento['Data'] >= dt_inicio) & (df_faturamento['Data'] <= dt_fim)
    df_filtrado = df_faturamento.loc[mascara]
    
    if unidade != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['Unidade_Padrao'] == unidade]
    
    # DataFrame para gráficos gerais (se ainda usar)
    df_evolucao = df_filtrado.groupby(['Data'])[['Valor bruto','Valor líquido']].sum().reset_index()
    
    # DataFrame específico para o seu gráfico empilhado com todas as operadoras
    df_evolucao_operadoras = df_filtrado.groupby(['Data', 'OPERADORA'])[['Valor bruto']].sum().reset_index() 
    
    return df_evolucao, df_evolucao_operadoras

def mes_para_data(mes_abrev, ano):
    """Converte 'Jul' -> Timestamp(ano, 7, 1)"""
    return pd.Timestamp(year=ano, month=MESES_PT[mes_abrev], day=1)

def obter_dados_indicadores(df_indicadores, dt_inicio, dt_fim):
    ano = dt_inicio.year
    meses = df_indicadores.columns[:-1]
    
    mapa_datas = {m: mes_para_data(m, ano) for m in meses if m in MESES_PT}
    meses_filtrados = [m for m, data in mapa_datas.items() if dt_inicio <= data <= dt_fim]
    
    if not meses_filtrados:
        return pd.DataFrame(columns=['Meses', 'Quantidade']), pd.Series(dtype=float)
    
    # --- Pacientes totais (Fig4) ---
    totais = pd.to_numeric(df_indicadores.loc["Quant. de pacientes NPC", meses_filtrados], errors='coerce').dropna()
    df_fig4 = totais.reset_index()
    df_fig4.columns = ['Meses', 'Quantidade']
    
    # --- Pacientes de TODO o período filtrado (Fig5) ---
    df_planos = df_indicadores.drop(['Quant. de pacientes NPC'], errors='ignore')
    df_planos.rename(index={'Unimed Central Nacional': 'Central Nacional'}, inplace=True)
    
    # 1. Isola apenas as colunas dos meses selecionados e garante que são números
    df_planos_selecionados = df_planos[meses_filtrados].apply(pd.to_numeric, errors='coerce')
    
    # 2. Soma a linha inteira (todos os meses) para cada operadora
    dados_periodo = df_planos_selecionados.mean(axis=1).dropna()
    
    # 3. Mantém apenas quem teve mais de zero pacientes no período
    dados_periodo = dados_periodo[dados_periodo > 0]
    
    return df_fig4, dados_periodo

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

def processar_indicadores_unidades_base(df_ind_unidades):
    df = df_ind_unidades.reset_index()
    
    nome_coluna_unidade = df.columns[0]
    df.rename(columns={nome_coluna_unidade: 'Unidade_Padrao'}, inplace=True)
    
    df['Unidade_Padrao'] = df['Unidade_Padrao'].astype(str).str.replace('Quant. de pacientes ', '', regex=False)
    
    df = df[df['Unidade_Padrao'] != 'Total']
    
    return df