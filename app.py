import pandas as pd
import plotly.express as px
import streamlit as st
import datetime

# Classificação de variáveis

pd.options.display.float_format = '{:.2f}'.format

#Procedimentos 
mapeamento_procedimentos = {
        2010368: 'Fisioterapia',
        5000001: 'Psicomotricidade',
        5000050: 'Psicopedagogia',
        5000518: 'Fonoaudiologia',
        5000061: 'Fonoaudiologia',
        5000510: 'Psicologia',
        5000047: 'Psicologia',
        5000046: 'Psicologia',
        5000008: 'Terapia Ocupacional',
        5000517: 'Terapia Ocupacional',
}
#Cores
cor_verde_escuro = '#1aad95'
cor_verde_claro = "#76dba9"
cor_branco = '#ffffff'

mapa_cores_procedimento = {
        'Fisioterapia': '#83c9ff',
        'Psicomotricidade': '#ffabab',
        'Psicopedagogia': '#ff2b2b',
        'Fonoaudiologia': '#0068c9',
        'Psicologia': '#29b09d',
        'Terapia_Ocupacional': '#7defa1'
}

#Meses pacientes
meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

# Importação de dados
df = pd.read_excel(
'https://docs.google.com/spreadsheets/d/e/2PACX-1vTcbATCsLy6oktlxeb6R73G1OYH27bgDnI5LeB9W4j_oQYzYgFW14e5CxxUbr9pkeAN6Ha-EWZXiva4/pub?output=xlsx',
sheet_name=1
)
df_unimed = pd.read_excel('UNIMED_CONSOLIDADO_DATADO.xlsx', header = 3)
df_indicadores = pd.read_excel('2026 INDICADORES NPC DRE (Versão 1).xlsx',
                        sheet_name='OKRs Consolidados', 
                        skiprows=36,
                        nrows=10,
                        usecols='A:N',
                        index_col=0
)

df.rename(columns={'VALOR BRUTO': 'Valor bruto'}, inplace=True)
df_faturamento = df.dropna(axis=1, how= 'all')
df_faturamento['Data'] = pd.to_datetime(dict(year=df_faturamento['ANO'], month=df_faturamento['COMPETÊNCIA'], day=1))
df_filtro= df_faturamento[df_faturamento['SITUAÇÃO'] != 'CANCELADA']
df_evolucao = df_filtro.groupby(['ANO', 'COMPETÊNCIA'])[['Valor bruto','Valor líquido']].sum().reset_index()
df_evolucao['Data'] = pd.to_datetime(dict(year=df_evolucao['ANO'], month=df_evolucao['COMPETÊNCIA'], day=1))


df_unimed['Código'] = pd.to_numeric(df_unimed['Código'], errors='coerce').astype('Int64')
df_unimed['MES_ANO'] = pd.to_datetime(df_unimed['MES_ANO'])

st.header('Relatório Financeiro NPC')
st.caption('Relatório feito com dados de 2024 a 2026')
st.divider()

with st.sidebar:
        st.header("Dados")
        st.write("Use esta área para vizualizar a base de dados.")
        atualizacao = st.sidebar.button('🔄 Atualizar dados')

with st.sidebar:
        st.header("Periodo")
        col_inicio, col_fim= st.columns(2)
with col_inicio:
        data_inicio = st.date_input(
        label='Data inicial',
        value=datetime.date(2024,1,1))
with col_fim:
                data_fim = st.date_input(
                label='Data final',
                value=datetime.date(2028,12,31)
                )
# Dados Fig1
data_inicio = pd.to_datetime(data_inicio)
data_fim = pd.to_datetime(data_fim)
mascara1 = (df_evolucao['Data'] >= data_inicio) & (df_evolucao['Data'] <= data_fim)
df_evolucao_filtrado = df_evolucao.loc[mascara1]

# Dados Fig2
df_filtro2= df_faturamento[df_faturamento['OPERADORA'] != 'Unimed Fortaleza']
df_evolucao_filtro = df_filtro2.groupby(['ANO', 'COMPETÊNCIA','OPERADORA'])[['Valor bruto','Valor líquido']].sum().reset_index()
df_evolucao_filtro['Data'] = pd.to_datetime(dict(year=df_evolucao_filtro['ANO'], month=df_evolucao_filtro['COMPETÊNCIA'], day=1))
mascara2 = (df_evolucao_filtro['Data'] >= data_inicio) & (df_evolucao_filtro['Data'] <= data_fim)
df_evolucao_filtro_por_data = df_evolucao_filtro.loc[mascara2]

# Dados Fig3
df_filtro3= df_faturamento[df_faturamento['OPERADORA'] == 'Unimed Fortaleza']
df_evolucao_unimed = df_filtro3.groupby(['ANO', 'COMPETÊNCIA','OPERADORA'])[['Valor bruto','Valor líquido']].sum().reset_index()
df_evolucao_unimed['Data'] = pd.to_datetime(dict(year=df_evolucao_unimed['ANO'], month=df_evolucao_unimed['COMPETÊNCIA'], day=1))
mascara3 = (df_evolucao_unimed['Data'] >= data_inicio) & (df_evolucao_unimed['Data'] <= data_fim)
df_evolucao_unimed_por_data = df_evolucao_unimed.loc[mascara3]

# Dados Fig4
totais_mensais = df_indicadores.loc['Quant. de pacientes NPC', meses]
totais_mensais = pd.to_numeric(totais_mensais, errors='coerce')
totais_mensais = totais_mensais.dropna()

# Dados Fig5
linhas_para_remover = ['Quant. de pacientes NPC']
df_planos = df_indicadores.drop(linhas_para_remover, errors='ignore')
dados_junho = df_planos['Jun']
dados_junho = pd.to_numeric(dados_junho, errors='coerce').dropna()
dados_junho = dados_junho[dados_junho > 0]

# Dados Fig6 & Fig7
df_unimed_proc = df_unimed.groupby(['MES_ANO', 'Código']).size().reset_index(name='Quantidade')
df_unimed_proc['Procedimento'] = df_unimed_proc['Código'].map(mapeamento_procedimentos)
df_unimed_proc['Procedimento'] = df_unimed_proc['Procedimento'].fillna('Outros/Não Mapeado')
df_unimed_proc = df_unimed_proc[['MES_ANO', 'Código', 'Procedimento', 'Quantidade']]
df_unimed_proc = df_unimed_proc.groupby(['MES_ANO', 'Procedimento'], as_index=False)['Quantidade'].sum()
df_pizza = df_unimed_proc.groupby('Procedimento', as_index=False)['Quantidade'].sum()
df_pizza_consolidado = df_unimed_proc.groupby('Procedimento', as_index=False)['Quantidade'].sum()

st.set_page_config(
page_title="Dashboard de Financeiro", 
layout="wide"
)

#Criação de Figuras Faturamento

fig1 = px.bar(df_evolucao_filtrado,
        x='Data',
        y=['Valor bruto','Valor líquido'],
        title= 'Evolução do Faturamento',
        barmode='group',
        opacity=1,
        color_discrete_sequence=[cor_verde_escuro, cor_verde_claro]
)
fig1.update_layout(
xaxis_title='Data',
yaxis_title='Valores',
plot_bgcolor='white',
legend_title_text='Definição de valores'
)

fig1.update_traces(
textposition='inside',
textfont_size=10
)

fig2 = px.bar(df_evolucao_filtro_por_data,
        x='Data',
        y=['Valor bruto'],
        title= 'Evolução do Faturamento - Outros Planos',
        color='OPERADORA',
)
fig2.update_layout(
xaxis_title='Data',
yaxis_title='Valor bruto',
plot_bgcolor='white',
legend_title_text='Operadoras'
)

fig2.update_traces(
textposition='inside',
textfont_size=10
)

fig3 = px.bar(df_evolucao_unimed_por_data,
        x='Data',
        y=['Valor bruto','Valor líquido'],
        title= 'Evolução do Faturamento - Unimed',
        barmode='overlay',
        opacity=1,
        color_discrete_sequence= [cor_verde_escuro, cor_verde_claro]
)
fig3.update_layout(
xaxis_title='Data',
yaxis_title='Valores',
plot_bgcolor='white',
legend_title_text='Definição de valores'
)

fig3.update_traces(
textposition='inside',
textfont_size=10
)

fig4 = px.bar(
        x=totais_mensais.index,     
        y=totais_mensais.values,      
        title='Evolução Mensal - Total de Pacientes',
        labels={'x': 'Meses', 'y': 'Quantidade de Pacientes'},
        text_auto=True,
        color_discrete_sequence=[cor_verde_claro]              
)

fig5 = px.pie(
        names=dados_junho.index,
        values=dados_junho.values,
        title='Distribuição de Pacientes por Convênio (Exceto Unimed Fortaleza) - Junho',
        hole=0.3,
        color_discrete_map=mapa_cores_procedimento
)
fig5.update_traces(
        textposition='inside',
        textinfo='percent+label'
)

fig6 = px.bar(
        df_unimed_proc,
        x='MES_ANO',
        y='Quantidade',
        color='Procedimento',
        color_discrete_map=mapa_cores_procedimento,
        title='Procedimentos por Mês - Unimed',
        barmode='stack',
        text_auto=True
)
fig6.update_layout(
xaxis_title='Mês / Ano',
yaxis_title='Quantidade',
plot_bgcolor='white',
legend_title_text='Procedimento'
)

fig6.update_traces(
textposition='inside',
textfont_size=10
)

fig7 = px.pie(
        df_pizza,
        names='Procedimento',
        values='Quantidade',
        color_discrete_map=mapa_cores_procedimento,
        title='Distribuição total de Procedimentos da Unimed',
        hole=0.3,
)
fig7.update_traces(
        textposition='inside',
        textinfo='percent+label'
)
fig7.update_layout(legend={'traceorder':'normal'})

Dados = st.sidebar.radio(
        'Selecione os dados a serem analisados',
        ('Faturamento','Profissionais')
)
if Dados == 'Faturamento':
        col1, col2, col3 = st.columns(3)
        with col1:
                st.plotly_chart(fig1, use_container_width=True)
        with col2:
                st.plotly_chart(fig2, use_container_width=True)
        with col3:
                st.plotly_chart(fig3, use_container_width=True)

        col4, col5 = st.columns(2)
        with col4:
                st.plotly_chart(fig4, use_container_width=True)
        with col5:
                st.plotly_chart(fig5, use_container_width=True)

        col6, col7, = st.columns(2)
        with col6:
                st.plotly_chart(fig6, use_container_width=True)
        with col7:
                st.plotly_chart(fig7, use_container_width=True)

elif Dados == 'Profissionais':
        st.info('Módulo de Profissionais em construção...')

