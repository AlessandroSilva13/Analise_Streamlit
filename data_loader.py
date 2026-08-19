import pandas as pd
import streamlit as st
import time

@st.cache_data(ttl='1h')
def carregar_dados_faturamento(url: str):
    time.sleep(2)
    return pd.read_excel(url, sheet_name=1)

@st.cache_data(ttl='1h')
def carregar_dados_unimed(url: str):
    time.sleep(2)
    return pd.read_excel(url, sheet_name=0)

@st.cache_data(ttl='1h')
def carregar_dados_indicadores(url: str):
    time.sleep(2)
    df = pd.read_excel(url, sheet_name='OKRs Consolidados', skiprows=37, nrows=11, usecols='A:N', index_col=0)
    df.index = df.index.astype(str).str.strip()
    df.columns = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez', 'Total']
    return df

@st.cache_data(ttl='1h')
def carregar_dados_profissionais(caminho_arquivo: str):
    time.sleep(2)
    return pd.read_excel(caminho_arquivo)