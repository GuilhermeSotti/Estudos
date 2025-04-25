# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href="https://www.fiap.com.br/"><img src="../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# 🌱 Projeto: FarmTech Solutions – Cap 6 - Python e além

## 👥 Nome do grupo: --

## 👨‍🎓 Integrantes:
- <a href="[Linkedin](https://www.linkedin.com/in/guilherme-pires-de-sotti-machado-296a7417a/)">Guilherme Pires de Sotti Machado</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/">Lucas Gomes Moreira</a>

---

## Descrição

Esta solução oferece uma plataforma integrada para captura, tratamento, análise e disseminação de dados do agronegócio brasileiro. Os principais componentes são:

- **Ingestão de dados** via FAOSTAT e COMEXSTAT, gravando cargas brutas em SQL Server.  
- **Pipelines de pré-processamento** para limpeza, normalização e enriquecimento, com área de staging validada.  
- **Modelagem preditiva** (rendimento de culturas e risco de perdas na colheita) em Python e R.  
- **APIs RESTful** para predições de rendimento e roteirização logística.  
- **Dashboards interativos** em R Shiny para visualização de indicadores.  
- **Data Warehouse** em SQL Server (raw_data, staging, analytics) organizado em star schema com partições por período.

---

## Estrutura de Pastas

├── python/ 

├── R/ 

├── man/ 

├── sql/

└── README.md

---

## Como executar

### Docker
Caso não tenha o SQL Server já instalado na maquina, preparei um docker com todos os requisitos para execução deste script

- **Pré-requisitos**: Docker Engine instalado e Docker daemon em execução.  
- **Construir a imagem** (no diretório raiz do projeto, onde está o `Dockerfile`):

  ```bash
  docker build -t Cap-6 .

  docker run -d \
  --name agrodata \
  -p 5000:5000 \
  agrodata-platform

---

### Python

- **Pré-requisitos**: Python 3 instalado e dependências configuradas via:

```bash
  pip install -r python/requirements.txt
  Pipeline completo:


  python python/main.py --year 2022
  Módulo específico (por exemplo, ingestão FAOSTAT):


  python -m ingestion.faostat_ingest production_crops 2022
```

---

### R

**Pré-requisitos**: R (>= 4.0.0) instalado:

```r
  shiny::runApp("app.R")
```

---

## Componentes Técnicos

### 1. Projeto Python  
Organizado segundo o padrão Data Science, com módulos de configuração, ingestão, pré-processamento, modelagem, API e testes, apoiado por um entry-point único (`main.py`).

### 2. Pacote R  
Implementado como RStudio com modelagem de perdas e helpers para dashboard Shiny. Documentação gerada via arquivos `.Rd` conforme “Writing R Extensions”.

### 3. Banco de Dados SQL Server  
Esquema em três níveis:  
- **raw_data:** tabelas de carga bruta (`payload` em CLOB).  
- **staging:** dados validados, com partições por ano e flags de validade.  
- **analytics:** modelo dimensional (fatos e dimensões) otimizado com índices e partições. 

### 4. Documentação Rd  
Arquivo `man/documentation.Rd` descreve suas funções principais.

---

## Histórico de Versões

- **v0.1.0** – Inicialização dos módulos de ingestão e pré-processamento.  
- **v0.2.0** – Modelos preditivos e APIs RESTful.  
- **v1.0.0** – Integração completa com dashboards Shiny e documentação final.

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
    