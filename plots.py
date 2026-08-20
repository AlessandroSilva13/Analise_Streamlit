import plotly.express as px
from config import COR_VERDE_ESCURO, COR_VERDE_CLARO, MAPA_CORES_PROCEDIMENTO, MAPA_CORES_OPERADORAS

def plot_evolucao_por_operadora(df_evolucao_operadoras):
    ordem_operadoras = (
        df_evolucao_operadoras.groupby('OPERADORA')['Valor bruto']
        .sum()
        .sort_values(ascending=False)
        .index.tolist()
    )
    fig = px.bar(
        df_evolucao_operadoras,
        x='Data',
        y='Valor bruto',
        color='OPERADORA',  # Isso que separa as cores
        title='Evolução do Faturamento por Operadora',
        color_discrete_map=MAPA_CORES_OPERADORAS,
        barmode='stack',
        category_orders={'OPERADORA': ordem_operadoras}# Isso que empilha as barras
    )
    
    fig.update_layout(
        xaxis_title='', 
        yaxis_title='Valor Bruto (R$)', 
        plot_bgcolor='white', 
        legend_title_text='Operadora'
    )
    
    return fig

def plot_pizza_outros(df):
    df_agregado = df.groupby('OPERADORA', as_index=False)['Valor bruto'].sum()
    
    fig = px.pie(
        df_agregado,
        values='Valor bruto',
        names='OPERADORA',
        title='Faturamento - Distribuição do Período',
        color='OPERADORA',
        color_discrete_map=MAPA_CORES_OPERADORAS,
        hole=0.3  
    )
    
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label'
    )
    
    return fig

def plot_pacientes_mes(df):
    return px.bar(df, x='Meses', y='Quantidade', title='Evolução Mensal - Pacientes', 
                text_auto='.0f', color_discrete_sequence=[COR_VERDE_CLARO])

def plot_distribuicao_julho(dados_julho):
    fig = px.pie(
        names=dados_julho.index, 
        values=dados_julho.values,
        color=dados_julho.index, 
        hole=0.3, 
        title='Distribuição Média de Pacientes no Período', 
        color_discrete_map=MAPA_CORES_OPERADORAS
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    
    return fig
def plot_procedimentos_mes(df):
    fig = px.bar(df, x='MES_ANO', y='Quantidade', color='Procedimento', barmode='stack', text_auto=True,
                color_discrete_map=MAPA_CORES_PROCEDIMENTO, title='Procedimentos por Mês - Unimed')
    fig.update_layout(xaxis_title='Mês / Ano', plot_bgcolor='white')
    return fig

def plot_procedimentos_pizza(df):
    fig = px.pie(df, names='Procedimento', values='Quantidade', hole=0.3,
                color='Procedimento', color_discrete_map=MAPA_CORES_PROCEDIMENTO, 
                title='Distribuição total de Procedimentos')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def plot_profissionais_vinculo(df):
    fig = px.bar(df, x='Pagamento', y='Valor_Faturamento', color='Vinculo do Período do Pagamento', 
                barmode='group', title='Faturamento por Vínculo')
    fig.update_layout(plot_bgcolor='white')
    return fig

def plot_profissionais_reason(df):
    fig = px.bar(df, x='Pagamento', y='Valor', color='reason_for_charge', 
                barmode='group', title='Razões de Cobrança')
    fig.update_layout(plot_bgcolor='white')
    return fig