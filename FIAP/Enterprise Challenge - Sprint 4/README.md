# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
  <a href="https://www.fiap.com.br/">
    <img src="../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" width="40%" />
  </a>
</p>

# Projeto: Enterprise Challenge - Sprint 4

## Nome do grupo: --

## Integrantes
- [Guilherme Pires de Sotti Machado](https://www.linkedin.com/in/guilherme-pires-de-sotti-machado-296a7417a/)

## Professores

### Tutor(a)
- [Lucas Gomes Moreira](https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/)

---

## Video
Link: [VideoExplicativo](https://youtu.be/-muc-A1wRK8)

## Objetivo
Integrar as entregas anteriores (arquitetura, simulação/coleta e modelagem) em um **MVP ponta-a-ponta** para um cenário de Indústria 4.0: simular/ler sensores (ESP32) → ingestão (MQTT/HTTP) → persistência em banco relacional → processamento/ML (treino ou inferência) → visualização e alertas (dashboard). Ênfase em reprodutibilidade, observabilidade e evidências (prints, logs e vídeo).

## Requisitos Locais
- Python 3.10+ e `pip`
- PostgreSQL 12+ (recomendado 15)
- Mosquitto (opcional, para testes MQTT) ou outro broker MQTT
- Git
- Streamlit (instalado via `pip install streamlit`)
- Repositório clonado com arquivos do projeto
- (Opcional) Wokwi / VSCode + PlatformIO para simular ESP32

---

## Execução Local (sem Docker)

> Estes passos assumem que você prefere rodar serviços localmente (Postgres e Mosquitto já instalados e em execução). Se preferir o caminho containerizado, use o `docker-compose.yml`.

1. Preparar ambiente Python e dependências:
   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Linux / macOS
   .venv\Scripts\activate           # Windows (PowerShell)
   pip install -r requirements.txt
   ```

2. Criar banco e tabelas (Postgres):
   ```bash
   psql -h localhost -U postgres -c "CREATE DATABASE factorydb;"
   psql -h localhost -U postgres -d factorydb -f db/create_tables.sql
   psql -h localhost -U postgres -d factorydb -f db/seed.sql
   ```

3. Rodar endpoint HTTP de ingestão (FastAPI):
   ```bash
   uvicorn http_ingest:app --host 0.0.0.0 --port 8000
   ```

4. Simular publicação de sensores (se não usar ESP32 físico):
   ```bash
   python utils/replay.py
   ```

5. Rodar ingestor MQTT (se optar por MQTT subscriber):
   ```bash
   python ingest/mqtt_ingest.py
   ```

6. Treinar o modelo ML e salvar o artefato:
   ```bash
   python ml/train_eval.py
   ```

7. Abrir dashboard (Streamlit):
   ```bash
   streamlit run dashboard/app.py
   ```

---

## Estrutura dos Principais Arquivos

- `http_ingest.py` — FastAPI endpoint que recebe POST /ingest e grava medições no Postgres.  
- `ingest/mqtt_ingest.py` — Subscriber MQTT que persiste mensagens recebidas em `measurements`.  
- `esp32/wokwi_esp32_post_mqtt.ino` — Sketch de ESP32 (Wokwi) que publica JSON via MQTT (simulação).  
- `db/create_tables.sql` — DDL para criar as tabelas do projeto (`devices`, `measurements`, `alerts`, `ml_runs`).  
- `db/seed.sql` — Script para popular dados de exemplo (gera séries para `esp01` e `esp02`).  
- `db/sample_measurements.csv` — CSV de fallback / exemplo para o notebook.  
- `ml/train_eval.py` — Script para treinar RandomForestRegressor sobre os dados e gravar métricas/modelo.  
- `ml/notebook_ml.ipynb` — Notebook Jupyter com pipeline ML (carregamento, features, treino, avaliação, plots).  
- `dashboard/app.py` — App Streamlit que mostra KPIs, série temporal, previsões e dispara alerta simples.  
- `utils/replay.py` — Publisher MQTT para simular fluxo contínuo de sensores (útil para demonstração).  
- `docker-compose.yml` — Compose para Postgres, Mosquitto, pgAdmin e serviço opcional `ingest-http`.  
- `Dockerfile` — imagem para o serviço `ingest-http` (FastAPI + Uvicorn).  
- `Makefile` — atalhos: build, up, seed, gen-sample, run-ml, run-dashboard, run-replay, logs.  
- `requirements.txt` — dependências Python do projeto.

---

## 🕓 Histórico de Versões

**v0.1.0** – Estruturação do projeto, carregamento e análise dos dados  
**v0.2.0** – Implementação dos modelos de ML  
**v0.3.0** – Avaliação dos modelos e extração do perfil ideal  
**v1.0.0** – Entrega final com documentação completa

---

📋 **Licença**

<img src="https://mirrors.creativecommons.org/presskit/icons/cc.svg" width="22px" style="vertical-align:text-bottom; margin-right:2px;" /> <img src="https://mirrors.creativecommons.org/presskit/icons/by.svg" width="22px" style="vertical-align:text-bottom;" />  
<p xmlns:dct="http://purl.org/dc/terms/">
<a property="dct:title" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por 
<a property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sob 
<a href="http://creativecommons.org/licenses/by/4.0/" rel="license">Attribution 4.0 International</a>.
</p>
      