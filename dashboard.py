import os
import sqlite3
from collections import Counter
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Radar de Vagas T.I.", layout="wide")

st.title("🎯 Radar de Vagas & Tendências em T.I.")
st.subheader("Análise em tempo real dos requisitos mais exigidos")

DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_BANCO = os.path.join(DIRETORIO_ATUAL, "mercado_ti.db")


def carregar_dados():
    if not os.path.exists(CAMINHO_BANCO):
        return pd.DataFrame()
    conn = sqlite3.connect(CAMINHO_BANCO)
    try:
        df = pd.read_sql_query("SELECT * FROM vagas_tech", conn)
    except Exception:
        df = pd.DataFrame()
    finally:
        conn.close()
    return df


df = carregar_dados()

if df.empty:
    st.warning("⚠️ Execute 'python main.py' para carregar as vagas primeiro!")
    st.stop()

# --- MÉTRICAS ---
col1, col2 = st.columns(2)
col1.metric("Total de Vagas Analisadas", len(df))

todas_skills = [
    skill.strip()
    for sublist in df["tecnologias"].str.split(",")
    for skill in sublist
    if skill.strip()
]
contagem = Counter(todas_skills)
df_skills = pd.DataFrame(
    contagem.items(), columns=["Tecnologia", "Quantidade"]
).sort_values(by="Quantidade", ascending=False)

if not df_skills.empty:
    col2.metric("Skill Mais Demandada", df_skills.iloc[0]["Tecnologia"].upper())

st.markdown("---")

# --- GRÁFICOS ---
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("Top Tecnologias Exigidas")
    fig_barras = px.bar(
        df_skills,
        x="Tecnologia",
        y="Quantidade",
        color="Quantidade",
        title="Frequência nas Vagas",
    )
    st.plotly_chart(fig_barras, use_container_width=True)

with col_g2:
    st.subheader("Quantidade de Skills por Vaga")
    fig_hist = px.histogram(
        df,
        x="total_skills",
        nbins=10,
        labels={"total_skills": "Qtd de Skills"},
        title="Complexidade dos Requisitos",
    )
    st.plotly_chart(fig_hist, use_container_width=True)

# --- TABELA DE VAGAS ---
st.subheader("📋 Lista de Vagas Monitoradas")
st.dataframe(
    df[["titulo", "tecnologias", "data_postagem", "url"]],
    use_container_width=True,
)
