import pandas as pd
import plotly.express as px
import streamlit as st
import datetime

st.set_page_config(
page_title="Dashboard de Financeiro", 
layout="wide"
)

pd.options.display.float_format = '{:.2f}'.format

# Leitura e Limpeza de dados
df = pd.read_excel(
'https://docs.google.com/spreadsheets/d/e/2PACX-1vTcbATCsLy6oktlxeb6R73G1OYH27bgDnI5LeB9W4j_oQYzYgFW14e5CxxUbr9pkeAN6Ha-EWZXiva4/pub?output=xlsx',
sheet_name=1
)

df_pax = pd.read_excel(2026 INDICADORES NPC DRE (Versão 1).xlsx,sheet_name=0)

df.rename(columns={'VALOR BRUTO': 'Valor bruto'}, inplace=True)
df_faturamento = df.dropna(axis=1, how= 'all')
df_faturamento['Data'] = pd.to_datetime(dict(year=df_faturamento['ANO'], month=df_faturamento['COMPETÊNCIA'], day=1))
df_filtro= df_faturamento[df_faturamento['SITUAÇÃO'] != 'CANCELADA']
df_evolucao = df_filtro.groupby(['ANO', 'COMPETÊNCIA'])[['Valor bruto','Valor líquido']].sum().reset_index()
df_evolucao['Data'] = pd.to_datetime(dict(year=df_evolucao['ANO'], month=df_evolucao['COMPETÊNCIA'], day=1))

cor_verde_escuro = '#1aad95'
cor_verde_claro = "#76dba9"
cor_branco = '#ffffff'

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

data_inicio = pd.to_datetime(data_inicio)
data_fim = pd.to_datetime(data_fim)

# Filtrar df_evolucao pelas datas
mascara1 = (df_evolucao['Data'] >= data_inicio) & (df_evolucao['Data'] <= data_fim)
df_evolucao_filtrado = df_evolucao.loc[mascara1]

# Criar fig1 com dados filtrados
fig1 = px.bar(df_evolucao_filtrado,
        x='Data',
        y=['Valor bruto','Valor líquido'],
        title= 'Evolução do Faturamento',
        barmode='group',
        opacity=1,
        color_discrete_sequence=[cor_verde_escuro, cor_verde_claro]
)

df_filtro2= df_faturamento[df_faturamento['OPERADORA'] != 'Unimed Fortaleza']
df_evolucao_filtro = df_filtro2.groupby(['ANO', 'COMPETÊNCIA','OPERADORA'])[['Valor bruto','Valor líquido']].sum().reset_index()
df_evolucao_filtro['Data'] = pd.to_datetime(dict(year=df_evolucao_filtro['ANO'], month=df_evolucao_filtro['COMPETÊNCIA'], day=1))

# Filtrar df_evolucao_filtro pelas datas
mascara2 = (df_evolucao_filtro['Data'] >= data_inicio) & (df_evolucao_filtro['Data'] <= data_fim)
df_evolucao_filtro_por_data = df_evolucao_filtro.loc[mascara2]

# Criar fig2 com dados filtrados
fig2 = px.bar(df_evolucao_filtro_por_data,
        x='Data',
        y=['Valor bruto'],
        title= 'Evolução do Faturamento - Outros Planos',
        color='OPERADORA',
)

df_filtro3= df_faturamento[df_faturamento['OPERADORA'] == 'Unimed Fortaleza']
df_evolucao_unimed = df_filtro3.groupby(['ANO', 'COMPETÊNCIA','OPERADORA'])[['Valor bruto','Valor líquido']].sum().reset_index()
df_evolucao_unimed['Data'] = pd.to_datetime(dict(year=df_evolucao_unimed['ANO'], month=df_evolucao_unimed['COMPETÊNCIA'], day=1))

mascara3 = (df_evolucao_unimed['Data'] >= data_inicio) & (df_evolucao_unimed['Data'] <= data_fim)
df_evolucao_unimed_por_data = df_evolucao_unimed.loc[mascara3]

fig3 = px.bar(df_evolucao_unimed_por_data,
        x='Data',
        y=['Valor bruto','Valor líquido'],
        title= 'Evolução do Faturamento - Unimed',
        barmode='overlay',
        opacity=1,
        color_discrete_sequence= [cor_verde_escuro, cor_verde_claro]
)

Dados = st.sidebar.radio(
        'Selecione os dados a serem analisados',
        ('Faturamento','Profissionais')
)
if Dados == 'Faturamento':
        # 1ª linha de gráficos
        col1, col2, col3 = st.columns(3)
        with col1:
                st.plotly_chart(fig1, use_container_width=True)
        with col2:
                st.plotly_chart(fig2, use_container_width=True)
        with col3:
                st.plotly_chart(fig3, use_container_width=True)
        # 2ª linha de gráficos
        col4, col5 = st.columns(2)
        
        with col4:
                st.write("Espaço para outro gráfico")
        with col5:
                st.write("Espaço para outro gráfico")
                
elif Dados == 'Profissionais':
        st.info('Módulo de Profissionais em construção...')
