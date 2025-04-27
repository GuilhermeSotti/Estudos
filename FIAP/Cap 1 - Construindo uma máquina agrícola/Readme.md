# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
  <a href="https://www.fiap.com.br/">
    <img src="../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" width="40%" />
  </a>
</p>

# 🌱 Projeto: FarmTech Solutions – Cap 1 - Construindo uma máquina agrícola

## 👥 Nome do grupo: --

## 👨‍🎓 Integrantes
- [Guilherme Pires de Sotti Machado](https://www.linkedin.com/in/guilherme-pires-de-sotti-machado-296a7417a/)

## 👩‍🏫 Professores

### Tutor(a)
- [Lucas Gomes Moreira](https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/)

---

## Descrição

Esta solução implementa um **sistema de irrigação inteligente** simulado com ESP32 e sensores agrícolas, integrando:

- **Firmware em C/C++**
  - DHT22 (umidade do solo)
  - LDR (analogia de pH)
  - Dois botões (sensores de fósforo e potássio)
  - Relé (bomba de irrigação, status em LED)
- **Python**
  - Lê JSON via serial
  - Insere leituras em SQL Server (pyodbc)
  - Implementa operações CRUD
  - Integra previsão de chuva via OpenWeatherMap API
- **R Shiny** que exibe:
  - Gráficos de séries temporais (umidade, pH, P, K)
  - Status da bomba
  - Tabela de logs interativa
- **Banco de Dados** SQL Server (container Docker) modelado conforme MER da Fase 2

- **Container** via Docker Compose

---

## Estrutura de Pastas

├── firmware<br>
│   ├── src/<br>
│   │   └── main.cpp<br>
│   └── platformio.ini<br>
├── python/<br>
│   ├── main.py<br>
│   ├── requirements.txt<br>
│   └── .env<br>
├── R/<br>
│   └── app.R<br>
├── docker/<br>
│   └── docker-compose.yml<br>
├── assets<br>
└── README.md<br>

---

## Como executar

```bash
cd docker
docker-compose up -d
```

```bash
cd python
cp .env .env
```
```bash
pip install -r requirements.txt
python main.py
```
```bash
shiny::runApp("R/app.R", launch.browser = TRUE)
```

---

## Histórico de Versões
**v0.1.0** – Firmware ESP32 e simulação de sensores

**v0.2.0**  – Script Python com CRUD e integração de clima

**v0.3.0**  – Dashboard R Shiny para visualização em tempo real

**v1.0.0**  – Integração completa e documentação final

---

📋 Licença
<img src="https://mirrors.creativecommons.org/presskit/icons/cc.svg" width="22px" style="vertical-align:text-bottom; margin-right:2px;" /> <img src="https://mirrors.creativecommons.org/presskit/icons/by.svg" width="22px" style="vertical-align:text-bottom;" /> <p xmlns:dct="http://purl.org/dc/terms/"> <a property="dct:title" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/" rel="license">Attribution 4.0 International</a>. </p>