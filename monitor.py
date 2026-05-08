import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Analizador de Surtos", layout="wide")

st.title("📊 Monitor de Surtos")
st.markdown("Carregue sua planilha para filtrar e analisar informações rapidamente.")

# 1. Upload do Arquivo
uploaded_file = st.file_uploader("Escolha um arquivo (CSV ou XLSX)", type=['csv', 'xlsx'])

if uploaded_file is not None:
    # Lógica para ler diferentes formatos
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.success("Arquivo carregado com sucesso!")

        # 2. Barra Lateral para Filtros
        st.sidebar.header("Filtros de Pesquisa")
        
        # Seleção de Colunas para filtrar (Dinâmico)
        colunas = df.columns.tolist()
        filtro_coluna = st.sidebar.selectbox("Selecione a coluna principal para filtrar (ex: Doença ou Cidade):", colunas)
        
        # Opções únicas baseadas na coluna selecionada
        opcoes = df[filtro_coluna].unique().tolist()
        selecionados = st.sidebar.multiselect(f"Selecione os valores de '{filtro_coluna}':", opcoes, default=opcoes)

        # 3. Processamento do Filtro
        df_filtrado = df[df[filtro_coluna].isin(selecionados)]

        # 4. Exibição de Métricas Simples
        col1, col2 = st.columns(2)
        col1.metric("Total de Registros", len(df))
        col2.metric("Registros Filtrados", len(df_filtrado))

        # 5. Visualização dos Dados
        st.subheader("📋 Dados Filtrados")
        st.dataframe(df_filtrado, use_container_width=True)

        # 6. Botão para Download dos Dados Filtrados
        csv = df_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar resultado filtrado como CSV",
            data=csv,
            file_name='surto_filtrado.csv',
            mime='text/csv',
        )

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")

else:
    st.info("Aguardando upload de planilha para começar...")