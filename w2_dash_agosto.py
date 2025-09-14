import streamlit as st
import pandas as pd

df_relatorio = pd.read_excel('agosto_w2.xlsx')

st.set_page_config(layout="wide")
st.title("📊 Dashboard de Relatório Financeiro - Agosto")

# --- Cálculo das Métricas Totais ---
# Mapeando suas colunas para as colunas do resultado da análise do arquivo
total_qtd_notas = df_relatorio['NF'].count()
total_valor_notas = df_relatorio['Valor Nota'].sum()
total_frete_empresa = df_relatorio['Frete Empresa'].sum()
# 'Receita' no DataFrame simulado corresponde ao seu 'Frete W2'
total_faturamento = df_relatorio['Frete W2'].sum()
total_desp_barqueiros = df_relatorio['Frete Barqueiros'].sum()
df_relatorio['lucro'] = df_relatorio['Frete W2'] - \
    df_relatorio['Frete Barqueiros']
# 'Lucro' no DataFrame simulado corresponde ao seu 'Frete W2' - 'Frete Barqueiros'
total_receita_liquida = df_relatorio['lucro'].sum()

# --- Exibição das Métricas Principais ---
st.header("Resumo Geral dos Indicadores")

# Função auxiliar para formatar valores monetários em BRL


def format_currency(value):
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total de Notas Fiscais",
              f"{total_qtd_notas:,.0f}".replace(",", "."))
with col2:
    st.metric("Valor Total das Notas", format_currency(total_valor_notas))
with col3:
    st.metric("Valor Total do Frete (Empresas)",
              format_currency(total_frete_empresa))

col4, col5, col6 = st.columns(3)
with col4:
    st.metric("Faturamento (Frete W2)", format_currency(total_faturamento))
with col5:
    st.metric("Despesas com Barqueiros",
              format_currency(total_desp_barqueiros))
with col6:
    st.metric("Receita Líquida (Lucro)",
              format_currency(total_receita_liquida))

st.markdown("---")

# --- Exibição da Tabela Detalhada por Empresa ---
st.header("Detalhes por Empresa")
st.dataframe(df_relatorio.style.format({
    "Valor Total das Notas": format_currency,
    "Valor Total do Frete Empresa": format_currency,
    "Receita": format_currency,
    "Frete dos Barqueiros": format_currency,
    "Lucro": format_currency
}), use_container_width=True)

# Soma do Frete W2 por Empresa e Lucro por Empresa ---
st.header("Análise Detalhada por Empresa")

st.subheader("Soma do Frete W2 e Lucro por Empresa")

# Realizando as operações de groupby conforme você solicitou
soma_frete_w2_por_empresa = df_relatorio.groupby("Empresa")["Frete W2"].sum()
lucro_por_empresa = df_relatorio.groupby("Empresa")["lucro"].sum()

# Combinando os resultados agrupados em um novo DataFrame para melhor exibição
df_analise_por_empresa = pd.DataFrame({
    "Frete W2 por Empresa": soma_frete_w2_por_empresa,
    "Lucro por Empresa": lucro_por_empresa
})

# Exibindo a tabela de análise por empresa
st.dataframe(df_analise_por_empresa.style.format({
    "Frete W2 por Empresa": format_currency,
    "Lucro por Empresa": format_currency
}), use_container_width=True)

# Opcional: Adicionar gráficos para visualização dos dados agrupados
st.subheader("Gráfico de Frete W2 por Empresa")
st.bar_chart(df_analise_por_empresa["Frete W2 por Empresa"])

st.subheader("Gráfico de Lucro por Empresa")
st.bar_chart(df_analise_por_empresa["Lucro por Empresa"])

