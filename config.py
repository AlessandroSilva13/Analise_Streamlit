import streamlit as st

URL_FATURAMENTO = st.secrets["url_faturamento"]
URL_INDICADORES = st.secrets["url_indicadores"]
URL_UNIMED = st.secrets["url_unimed"]
PATH_PROFISSIONAIS = 'Resultado_Com_Faturamento.xlsx'

MAPEAMENTO_PROCEDIMENTOS = {
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

COR_VERDE_ESCURO = '#1aad95'
COR_VERDE_CLARO = "#76dba9"
COR_BRANCO = '#ffffff'

MAPA_CORES_PROCEDIMENTO = {
    'Fisioterapia': '#83c9ff',
    'Psicomotricidade': '#ffabab',
    'Psicopedagogia': '#ff2b2b',
    'Fonoaudiologia': '#0068c9',
    'Psicologia': '#29b09d',
    'Terapia Ocupacional': '#7defa1'
}