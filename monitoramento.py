import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração da Página
st.set_page_config(page_title="Dashboard de Surtos", layout="wide")

# Estilo CSS para melhorar o visual
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Monitor de Surtos")
st.markdown("Carregue a sua planilha para analisar dados e gerar indicadores em tempo real.")

# 2. Upload do Arquivo (CSV ou Excel)
uploaded_file = st.file_uploader("Escolha o ficheiro (CSV ou XLSX)", type=['csv', 'xlsx'])

if uploaded_file is not None:
    try:
        # Leitura dos dados
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        # 3. Barra Lateral (Filtros)
        st.sidebar.header("🎯 Filtros de Análise")
        
        # Seleção da coluna para filtrar
        colunas = df.columns.tolist()
        filtro_coluna = st.sidebar.selectbox("Filtrar dados por:", colunas)
        
        # Seleção de valores específicos
        opcoes = df[filtro_coluna].unique().tolist()
        selecionados = st.sidebar.multiselect(f"Selecionar {filtro_coluna}:", opcoes, default=opcoes)

        # Processamento do Filtro
        df_filtrado = df[df[filtro_coluna].isin(selecionados)]

        # 4. Métricas de Resumo (Cards)
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Total de Registos", len(df))
        col_m2.metric("Registos Filtrados", len(df_filtrado))
        percentagem = (len(df_filtrado) / len(df)) * 100
        col_m3.metric("Representatividade", f"{percentagem:.1f}%")

        # 5. Organização por Abas
        tab_tabela, tab_graficos = st.tabs(["📋 Tabela de Dados", "📈 Análise Visual"])

        with tab_tabela:
            st.subheader("Dados Filtrados")
            st.dataframe(df_filtrado, use_container_width=True)
            
            # Botão para exportar
            csv_data = df_filtrado.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descarregar Tabela Filtrada (CSV)",
                data=csv_data,
                file_name='dados_filtrados_surto.csv',
                mime='text/csv',
            )

        with tab_graficos:
            st.subheader("Indicadores Visuais")
            
            # Preparação dos dados para gráficos (Correção do erro de 'index')
            contagem = df_filtrado[filtro_coluna].value_counts().reset_index()
            contagem.columns = [filtro_coluna, 'Contagem'] # Nomes fixos para evitar erros

            c1, c2 = st.columns(2)

            with c1:
                st.write(f"**Distribuição por {filtro_coluna}**")
                fig_bar = px.bar(contagem, 
                                 x=filtro_coluna, 
                                 y='Contagem',
                                 color='Contagem',
                                 color_continuous_scale='Viridis',
                                 labels={'Contagem': 'Qtd. de Casos'})
                st.plotly_chart(fig_bar, use_container_width=True)

            with c2:
                st.write(f"**Proporção Relativa**")
                fig_pie = px.pie(contagem, 
                                 names=filtro_coluna, 
                                 values='Contagem',
                                 hole=0.4,
                                 color_discrete_sequence=px.colors.qualitative.Set3)
                st.plotly_chart(fig_pie, use_container_width=True)

            # Extra: Gráfico de Linha (se houver coluna de data)
            colunas_data = [c for c in colunas if 'data' in c.lower() or 'ano' in c.lower()]
            if colunas_data:
                st.markdown("---")
                st.write("**Evolução Temporal**")
                # Agrupa por data/ano e conta ocorrências
                timeline = df_filtrado.groupby(colunas_data[0]).size().reset_index(name='Casos')
                fig_line = px.line(timeline, x=colunas_data[0], y='Casos', markers=True)
                st.plotly_chart(fig_line, use_container_width=True)

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar a planilha: {e}")
else:
    st.info("Suba a sua planilha (CSV ou Excel) para começar a análise.")