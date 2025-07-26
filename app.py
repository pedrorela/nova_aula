# app.py  •  Dashboard Gapminder (simples)
import streamlit as st
import pip.express as px

# ------------------------------------------------
# Configurações da página
# ------------------------------------------------
st.set_page_config(
    page_title="🌍 Dashboard Gapminder",
    layout="wide",         # usa a largura total da tela
    initial_sidebar_state="expanded"
)

# ------------------------------------------------
# Carregamento do conjunto de dados
# ------------------------------------------------
df = px.data.gapminder()   # dataset já vem dentro do plotly

# ------------------------------------------------
# Barra lateral – filtros
# ------------------------------------------------
st.sidebar.header("Filtros")

anos = sorted(df["year"].unique())
ano_escolhido = st.sidebar.selectbox("Ano", anos, index=len(anos)-1)  # último ano como defaultpi

continentes = df["continent"].unique().tolist()
cont_escolhidos = st.sidebar.multiselect("Continente", continentes, default=continentes)

# DataFrame filtrado
df_sel = df[(df["year"] == ano_escolhido) & (df["continent"].isin(cont_escolhidos))]

# ------------------------------------------------
# Título principal
# ------------------------------------------------
st.title("🌍 Dashboard Gapminder – versão simples")

# ------------------------------------------------
# Gráficos lado a lado
# ------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("PIB per capita vs. Expectativa de Vida")
    fig_disp = px.scatter(
        df_sel,
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="continent",
        hover_name="country",
        log_x=True,
        size_max=60,
        labels={
            "gdpPercap": "PIB per Capita (US$)",
            "lifeExp": "Expectativa de Vida (anos)"
        },
        title=f"{ano_escolhido}"
    )
    st.plotly_chart(fig_disp, use_container_width=True)

with col2:
    st.subheader("Mapa – Expectativa de Vida")
    fig_mapa = px.choropleth(
        df_sel,
        locations="iso_alpha",
        color="lifeExp",
        hover_name="country",
        color_continuous_scale="Viridis",
        labels={"lifeExp": "Expectativa de Vida (anos)"},
        title=f"{ano_escolhido}"
    )
    st.plotly_chart(fig_mapa, use_container_width=True)

# ------------------------------------------------
# Tabela de dados
# ------------------------------------------------
st.subheader("Tabela de Dados Filtrados")
st.dataframe(df_sel.reset_index(drop=True), use_container_width=True)

st.caption("Fonte: gapminder (via plotly.express)")