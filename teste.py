import pandas as pd

df_profissionais = pd.read_excel('Resultado_Com_Faturamento.xlsx')
# 1. Cria a máscara avaliando a coluna do DataFrame ORIGINAL
mascara4 = (df_profissionais['Pagamento'] >= '2026-01-01') & (df_profissionais['Pagamento'] <= '2026-12-31')

# 2. Filtra o DataFrame original usando a máscara de mesmo tamanho
df_filtrado_por_data = df_profissionais.loc[mascara4]

# 3. Agora sim, agrupa apenas os dados que passaram pelo filtro
df_faturamento_vinculo_por_data = df_filtrado_por_data.groupby([
        'Vinculo do Período do Pagamento', 'Pagamento'
])[['Valor_Faturamento']].sum().reset_index()

df_filtrado_reasons = df_filtrado_por_data.loc[df_filtrado_por_data['reason_for_charge'].notnull()]
df_reasons = df_filtrado_reasons.groupby([
'reason_for_charge', 'Pagamento'
])[['Valor']].sum().reset_index()

print(df_reasons)