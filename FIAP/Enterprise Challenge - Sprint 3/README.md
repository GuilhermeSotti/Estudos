# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
  <a href="https://www.fiap.com.br/">
    <img src="../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" width="40%" />
  </a>
</p>

#  Projeto: Enterprise Challenge - Sprint 3

## Nome do grupo: --

##  Integrantes
- [Guilherme Pires de Sotti Machado](https://www.linkedin.com/in/guilherme-pires-de-sotti-machado-296a7417a/)

##  Professores

### Tutor(a)
- [Lucas Gomes Moreira](https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/)

---

## Video
Link: [VideoExplicativo](https://youtu.be/-muc-A1wRK8)

## Objetivo
Solução completa para manutenção preditiva: coleta via ESP32 → MQTT → PostgreSQL → ML → Dashboard.

## Requisitos Locais
- Docker & docker-compose (recomendado)
- Python 3.10+ (para execução local de scripts)
- Broker MQTT (Mosquitto) — já incluso no docker-compose

---

## Quickstart (com Docker)

1. Copie `.env.example` para `.env` e ajuste se necessário (`MQTT_BROKER`, `PG_*`).
2. Suba a stack:
   ```bash
   docker-compose up -d --build
   ```
3. Acesse o dashboard: [http://localhost:8501](http://localhost:8501)
4. Publique mensagens MQTT (ex: ESP32) no tópico:  
   ```
   factory/machine/1/sensors
   ```

---

## Execução Local (sem Docker)

1. Crie um ambiente virtual e instale as dependências:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Execute o consumidor MQTT:
   ```bash
   python mqtt_consumer.py
   ```
3. Execute scripts de ML:
   ```bash
   python ml_improvements.py --csv simulated_readings.csv --out model_best.pkl
   python rul_regression.py --csv simulated_readings.csv --out rul_model.pkl
   ```
4. Execute o dashboard:
   ```bash
   streamlit run dashboard_app.py
   ```

---

## Estrutura dos Principais Arquivos

- `mqtt_consumer.py` — Bridge MQTT → PostgreSQL
- `ml_improvements.py` — Treino RandomForest/LightGBM + FFT + SMOTE
- `rul_regression.py` — Gera RUL e treina regressor
- `dashboard_app.py` — Streamlit demo
- `postgres_dump.sql` — DDL para Postgres
- `Dockerfiles` / `docker-compose.yml` — Infraestrutura local


## Build & Push de Imagens Docker

```bash
# mqtt_consumer
docker build -f Dockerfile.mqtt_consumer -t <yourhubuser>/pm-mqtt-consumer:latest .
docker push <yourhubuser>/pm-mqtt-consumer:latest

# dashboard
docker build -f Dockerfile.streamlit -t <yourhubuser>/pm-dashboard:latest .
docker push <yourhubuser>/pm-dashboard:latest
```

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
