# app.py  •  Dashboard Gapminder (versão com +4 gráficos)
import streamlit as st
import plotly.express as px

# --------------------------------------------------
# Config. da página
# --------------------------------------------------
st.set_page_config(page_title="🌍 Gapminder Dashboard",
                   layout="wide",
                   initial_sidebar_state="expanded")

# --------------------------------------------------
# Dados
# --------------------------------------------------
df = px.data.gapminder()

# --------------------------------------------------
# Barra lateral – filtros
# --------------------------------------------------
st.sidebar.header("Filtros")

anos          = sorted(df["year"].unique())
ano_escolhido = st.sidebar.selectbox("Ano", anos, index=len(anos)-1)

continentes           = df["continent"].unique().tolist()
cont_escolhidos       = st.sidebar.multiselect("Continente",
                                               continentes,
                                               default=continentes)

# 🔹 NOVO – seleção opcional de países (para o gráfico de linha)
todos_paises      = df["country"].unique().tolist()
paises_escolhidos = st.sidebar.multiselect(
    "País(es) (para o gráfico de evolução)",
    options=todos_paises,
    default=["Brazil", "United States"]
)

# --------------------------------------------------
# Dados filtrados (por ano + continente)
# --------------------------------------------------
df_sel = df[(df["year"] == ano_escolhido) &
            (df["continent"].isin(cont_escolhidos))]

# --------------------------------------------------
# Título
# --------------------------------------------------
st.title("🌍 Dashboard Gapminder – visualizações extras")

# ==================================================
# ABA 1 — Visão Geral (dois gráficos originais)
# ==================================================
aba1, aba2, aba3 = st.tabs(["Visão Geral", "Comparações", "Evolução temporal"])

with aba1:
    col1, col2 = st.columns(2)

    # --- Gráfico 1 (origem do seu código)
    with col1:
        st.subheader("PIB per capita × Expectativa de Vida")
        fig_disp = px.scatter(
            df_sel, x="gdpPercap", y="lifeExp",
            size="pop", color="continent", hover_name="country",
            log_x=True, size_max=60,
            labels={"gdpPercap": "PIB per Capita (US$)",
                    "lifeExp": "Expectativa de Vida (anos)"},
            title=str(ano_escolhido)
        )
        st.plotly_chart(fig_disp, use_container_width=True)

    # --- Gráfico 2 (origem do seu código)
    with col2:
        st.subheader("Mapa — Expectativa de Vida")
        fig_mapa = px.choropleth(
            df_sel, locations="iso_alpha", color="lifeExp",
            hover_name="country", color_continuous_scale="Viridis",
            labels={"lifeExp": "Expectativa de Vida (anos)"},
            title=str(ano_escolhido)
        )
        st.plotly_chart(fig_mapa, use_container_width=True)

# ==================================================
# ABA 2 — Comparações (3º e 4º gráficos)
# ==================================================
with aba2:
    # 🔹 NOVO Gráfico 3  -----------------------------
    st.subheader("Top 10 países por PIB per Capita")
    top10 = (df_sel.sort_values("gdpPercap", ascending=False)
                   .head(10)
                   .sort_values("gdpPercap"))        # ordena para o gráfico de barras
    fig_bar = px.bar(top10,
                     x="gdpPercap", y="country",
                     orientation="h",
                     color="continent",
                     labels={"gdpPercap": "PIB per Capita (US$)",
                             "country": "País"})
    st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    # 🔹 NOVO Gráfico 4  -----------------------------
    st.subheader("Distribuição da População por Continente")
    pop_cont = (df_sel.groupby("continent")["pop"]
                      .sum()
                      .reset_index())
    fig_pie = px.pie(pop_cont,
                     names="continent",
                     values="pop",
                     hole=0.4,
                     labels={"continent": "Continente", "pop": "População"})
    st.plotly_chart(fig_pie, use_container_width=True)

# ==================================================
# ABA 3 — Evolução temporal (5º gráfico)
# ==================================================
with aba3:
    st.subheader("Evolução da Expectativa de Vida")
    # 🔹 NOVO Gráfico 5  -----------------------------
    df_line = df[df["country"].isin(paises_escolhidos)]
    fig_line = px.line(df_line,
                       x="year", y="lifeExp",
                       color="country",
                       markers=True,
                       labels={"lifeExp": "Expectativa de Vida (anos)",
                               "year": "Ano",
                               "country": "País"})
    st.plotly_chart(fig_line, use_container_width=True)

# --------------------------------------------------
# Tabela (opcional — pode ficar em um expander)
# --------------------------------------------------
with st.expander("🔍 Ver tabela de dados filtrados"):
    st.dataframe(df_sel.reset_index(drop=True), use_container_width=True)

st.caption("Fonte: Gapminder (via plotly.express)")
