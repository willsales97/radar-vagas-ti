# 🎯 Radar de Vagas & Tendências em T.I.

Projeto de automação e análise de dados em Python para mapear em tempo real as tecnologias e requisitos mais exigidos no mercado de trabalho de Tecnologia do Brasil.

## 📌 Visão Geral do Projeto
A aplicação realiza a coleta automatizada de anúncios de empregos de fontes públicas, processa o texto das descrições para identificar palavras-chave técnicas e apresenta um painel interativo com as tendências do mercado.

## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python 3.14
- **Extração & Coleta:** Requests / GitHub Jobs API (Mapeamento via REST)
- **Análise & Limpeza de Dados:** Pandas & Collections (NLP Básico)
- **Banco de Dados:** SQLite (Armazenamento relacional e histórico)
- **Visualização de Dados:** Streamlit & Plotly (Dashboard interativo)

## 🔄 Arquitetura do Pipeline (ETL)
1. **Extract (`main.py`):** Consome dados brutos de anúncios de vagas abertas em formato JSON.
2. **Transform (`main.py`):** Normaliza dados e varre descrições em busca de competências-chave (SQL, AWS, Git, Linux, Python, etc.).
3. **Load (`main.py`):** Persiste os dados limpos no banco relacional `mercado_ti.db`.
4. **Visualize (`dashboard.py`):** Apresenta métricas agregadas e gráficos em tempo real via interface web.

## 🚀 Como Executar o Projeto

1. **Clonar o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/radar-vagas-ti.git](https://github.com/seu-usuario/radar-vagas-ti.git)
   cd radar-vagas-ti