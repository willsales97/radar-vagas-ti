import sqlite3
from collections import Counter
from datetime import datetime
import pandas as pd
import requests


def buscar_vagas_tech(termo="Python"):
    print(f"🔍 Buscando vagas reais para: {termo}...")
    # API pública de vagas do GitHub / Adzuna
    url = f"https://api.github.com/repos/backend-br/vagas/issues?per_page=50&state=open"

    headers = {"User-Agent": "Mozilla/5.0"}
    resposta = requests.get(url, headers=headers)

    if resposta.status_code != 200:
        print("❌ Erro ao acessar a API de vagas.")
        return pd.DataFrame()

    vagas = resposta.json()
    lista_vagas = []

    # Lista de tecnologias para monitorar
    tecnologias_alvo = [
        "python",
        "sql",
        "excel",
        "linux",
        "aws",
        "docker",
        "javascript",
        "react",
        "java",
        "power bi",
        "redes",
        "git",
    ]

    for vaga in vagas:
        titulo = vaga.get("title", "")
        corpo = (vaga.get("body") or "").lower()
        data_criacao = vaga.get("created_at", "")[:10]

        # Contar quais tecnologias aparecem na descrição
        techs_encontradas = [tech for tech in tecnologias_alvo if tech in corpo]

        lista_vagas.append(
            {
                "id_vaga": vaga.get("id"),
                "titulo": titulo,
                "tecnologias": ", ".join(techs_encontradas),
                "total_skills": len(techs_encontradas),
                "data_postagem": data_criacao,
                "url": vaga.get("html_url"),
            }
        )

    return pd.DataFrame(lista_vagas)


def salvar_banco(df):
    conn = sqlite3.connect("mercado_ti.db")
    df.to_sql("vagas_tech", conn, if_exists="replace", index=False)
    conn.close()
    print("💾 Vagas processadas e salvas no banco de dados!")


if __name__ == "__main__":
    df_vagas = buscar_vagas_tech()

    if not df_vagas.empty:
        salvar_banco(df_vagas)

        # Análise rápida de termos mais pedidos
        todas_skills = [
            skill.strip()
            for sublist in df_vagas["tecnologias"].str.split(",")
            for skill in sublist
            if skill.strip()
        ]
        contagem = Counter(todas_skills)

        print("\n🏆 Top 5 Requisitos Mais Pedidos nas Vagas:")
        for skill, freq in contagem.most_common(5):
            print(f"- {skill.upper()}: {freq} vagas")