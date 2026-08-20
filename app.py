import streamlit as st
import pandas as pd
import datetime

import config
import data_loader
import data_processor
import plots

st.set_page_config(page_title="Dashboard de Financeiro", layout="wide")
pd.options.display.float_format = '{:.2f}'.format

# --- Header ---
col1, col2 = st.columns([3, 1])
with col1:
    st.header('Relatório Financeiro NPC')
    st.caption('Relatório feito com dados de 2024 a 2026')
with col2:
    st.image('imagens/NPC.jpg', width=120)
st.divider()

# --- Sidebar ---
with st.sidebar:
    st.header("Dados")
    st.write("Use esta área para visualizar a base de dados.")
    if st.button('🔄 Atualizar dados'):
        st.cache_data.clear() # Limpa o cache se o usuário pedir
    st.header("Unidade")
    unidade_selecionada = st.selectbox(
                            'Selecione a Unidade',
                            ['Todas', 'MATRIZ', 'LIFE', 'SUL']
)
    
    st.header("Período")
    col_inicio, col_fim = st.columns(2)
    with col_inicio:
        data_inicio = st.date_input('Data inicial', value=datetime.date(2024, 1, 1))
    with col_fim:
        data_fim = st.date_input('Data final', value=datetime.date(2028, 12, 31))
    
# Converter para datetime para o pandas
    dt_inicio = pd.to_datetime(data_inicio)
    dt_fim = pd.to_datetime(data_fim)

    Dados = st.sidebar.radio('Selecione a análise', ('Faturamento', 'Profissionais'))

# --- Carregamento de Dados ---
df_fat_raw = data_loader.carregar_dados_faturamento(config.URL_FATURAMENTO)
df_unimed_raw = data_loader.carregar_dados_unimed(config.URL_UNIMED)
df_ind_raw = data_loader.carregar_dados_indicadores(config.URL_INDICADORES)
df_prof_raw = data_loader.carregar_dados_profissionais(config.PATH_PROFISSIONAIS)

# Processamento base
df_faturamento = data_processor.processar_faturamento_base(df_fat_raw)
df_unimed = data_processor.processar_unimed_base(df_unimed_raw)

# --- Renderização da Interface ---
if Dados == 'Faturamento':
# Obter dados filtrados
        df_evo, df_evolucao_operadoras = data_processor.obter_dados_faturamento(df_faturamento, dt_inicio, dt_fim, unidade_selecionada)
        df_fig4, dados_julho = data_processor.obter_dados_indicadores(df_ind_raw, dt_inicio, dt_fim)
        df_proc_barras, df_proc_pizza = data_processor.obter_dados_procedimentos(df_unimed)
        
# Criar Gráficos
        fig1 = plots.plot_evolucao_por_operadora(df_evolucao_operadoras)
        fig2 = plots.plot_pizza_outros(df_evolucao_operadoras)
        fig4 = plots.plot_pacientes_mes(df_fig4)
        fig5 = plots.plot_distribuicao_julho(dados_julho)
        fig6 = plots.plot_procedimentos_mes(df_proc_barras)
        fig7 = plots.plot_procedimentos_pizza(df_proc_pizza)

        c1, c2 = st.columns(2)
        c1.plotly_chart(fig1, use_container_width=True)
        c2.plotly_chart(fig2, use_container_width=True)

        c4, c5 = st.columns(2)
        c4.plotly_chart(fig4, use_container_width=True)
        c5.plotly_chart(fig5, use_container_width=True)

        c6, c7 = st.columns(2)
        c6.plotly_chart(fig6, use_container_width=True)
        c7.plotly_chart(fig7, use_container_width=True)

elif Dados == 'Profissionais':
        df_vinculo, df_reasons = data_processor.obter_dados_profissionais(df_prof_raw, dt_inicio, dt_fim)
        
        figP1 = plots.plot_profissionais_vinculo(df_vinculo)
        figP2 = plots.plot_profissionais_reason(df_reasons)
        
        cP1, cP2 = st.columns(2)
        cP1.plotly_chart(figP1, use_container_width=True)
        cP2.plotly_chart(figP2, use_container_width=True)