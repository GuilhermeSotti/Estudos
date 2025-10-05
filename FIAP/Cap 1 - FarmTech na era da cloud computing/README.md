# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
  <a href="https://www.fiap.com.br/">
    <img src="../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" width="40%" />
  </a>
</p>

#  Projeto: Cap 1 - FarmTech na era da cloud computing

## Nome do grupo: --

##  Integrantes
- [Guilherme Pires de Sotti Machado](https://www.linkedin.com/in/guilherme-pires-de-sotti-machado-296a7417a/)

##  Professores

### Tutor(a)
- [Lucas Gomes Moreira](https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/)

---

## Conteúdo
- `notebooks/01_EDA_Modeling.ipynb` - notebook com EDA, clusterização e pipeline de modelagem.
- `src/` - código fonte (pré-processamento, treino, API, utilitários).
- `models/` - modelos salvos `.joblib`.
- `artifacts/` - métricas e figuras geradas.
- `iot/` - código do ESP32 (Arduino) e `mqtt_bridge.py` para integração local.
- `docker-compose.yml` - orquestra API + MQTT + MQTT-bridge para testes locais.

---

## Requisitos
- Docker + Docker Compose (opcional)
- Python 3.9/3.10
- Bibliotecas: ver `requirements.txt`

Execução rápida (local, sem Docker):
```bash
cd farmtech-fase5
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

---

## Como rodar (modo rápido)


Treine modelos:
```bash
python src/train_models.py
```

Modelos e `artifacts/metrics.csv` serão gerados.

Inicie a API local (não-Docker):
```bash
python src/serve.py
```

Para testar predição:
```bash
python src/predict_client.py
```

Para testes MQTT locais (opcional):

Suba Docker Compose:
```bash
docker-compose up --build
```

Ligue ESP32 ou publique em `farmtech/sensors` via MQTT.


---

## Gerar figure_importances.png

Se quiser gerar uma figura de importâncias real, rode:
```bash
python src/evaluate.py
```


📋 **Licença**

<img src="https://mirrors.creativecommons.org/presskit/icons/cc.svg" width="22px" style="vertical-align:text-bottom; margin-right:2px;" /> <img src="https://mirrors.creativecommons.org/presskit/icons/by.svg" width="22px" style="vertical-align:text-bottom;" />  
<p xmlns:dct="http://purl.org/dc/terms/">
<a property="dct:title" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por 
<a property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sob 
<a href="http://creativecommons.org/licenses/by/4.0/" rel="license">Attribution 4.0 International</a>.
</p>
