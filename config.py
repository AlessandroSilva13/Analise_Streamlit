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

# --- CORES FIXAS (INTACTAS) ---
COR_VERDE_ESCURO = '#1aad95'
COR_VERDE_CLARO = "#76dba9"
COR_BRANCO = '#ffffff'

# --- CORES DOS PROCEDIMENTOS (Tons Pastéis) ---
MAPA_CORES_PROCEDIMENTO = {
    'Fisioterapia': '#a1c9f4',        
    'Psicomotricidade': '#b2dfdb',    
    'Psicopedagogia': '#c8e6c9',     
    'Fonoaudiologia': '#90caf9',      
    'Psicologia': '#80cbc4',          
    'Terapia Ocupacional': '#e0f2f1' 
}

# --- CORES DAS OPERADORAS ---
MAPA_CORES_OPERADORAS = {
    'Unimed Fortaleza': COR_VERDE_ESCURO,  
    'Unimed Ceará': '#4db6ac',           
    'Unimed Florianópolis': "#5ed263",     
    'Unimed Natal': "#7cad44",            
    'Unimed Belém': "#acff4e",             
    'Unimed Fesp': "#5dae00",            
    'Central Nacional': "#41ff8d",        
    'Particular': "#00752f",               
    'Assefaz - Ceara': "#0769ea",         
    'Fusex': "#0a6793",                    
    'Marinha': '#29b6f6',                  
    'Camed': "#00e1ff",                    
    'Casembrapa': "#006d7c"              
}