# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
  <a href="https://www.fiap.com.br/">
    <img src="../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" width="40%" />
  </a>
</p>

# Cap 1 - Automação e inteligência na FarmTech Solutions  

## Nome do grupo: --

##  Integrantes
- [Guilherme Pires de Sotti Machado](https://www.linkedin.com/in/guilherme-pires-de-sotti-machado-296a7417a/)

##  Professores

### Tutor(a)
- [Lucas Gomes Moreira](https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/)

---

## Descrição  

O projeto **FarmTech Solutions – Fase 4** tem como objetivo evoluir um sistema inteligente de irrigação agrícola. Esta fase incorpora **machine learning com Scikit-learn**, **visualização interativa via Streamlit**, **monitoramento via Serial Plotter**, **display LCD com ESP32 no Wokwi**, além de **otimizações no uso de memória**.

A solução inclui:  
- Coleta de dados via sensores de umidade e nutrientes no solo com **ESP32**  
- Exibição local de métricas em **display LCD I²C**  
- Envio de dados via **Serial JSON** para ingestão em banco de dados  
- Pipeline de **ML preditivo com Scikit-learn** baseado no histórico dos sensores  
- Interface web em **Streamlit** com gráficos, insights e previsões  
- Visualização em tempo real com o **Serial Plotter do Wokwi**

---

## Estrutura de Pastas  

```
Cap 1 - Automação e inteligência na FarmTech Solutions/
├── esp32_firmware/
│ ├── include/
│ │ ├── Config.h
│ │ ├── SensorManager.h
│ │ └── LCDManager.h
│ ├── src/
│ │ ├── main.cpp
│ │ ├── SensorManager.cpp
│ │ └── LCDManager.cpp
│ └── docs/
│ └── otimizacoes_memoria.md
├── python_pipeline/
│ ├── data/
│ │ └── dados_sensor.csv
│ ├── models/
│ │ └── modelo_treinado.pkl
│ ├── ingestao/
│ │ ├── config.yaml
│ │ └── ingestao_serial.py
│ ├── streamlit_app/
│ │ └── app.py
│ └── requirements.txt
├── images/
│ └── serial_plotter_prints/
│ ├── print_umidade1.png
│ └── print_umidade2.png
└── README.md

```

---

## Como Executar

### 1. Firmware ESP32

- Suba o código da pasta `esp32_firmware/` usando PlatformIO ou Arduino IDE
- Execute no [Wokwi Simulator](https://wokwi.com/)

### 2. Ambiente Python

```bash
pip install -r requirements.txt
```

### 3. Ingestão de Dados
```bash
python python_pipeline/ingestao/ingestao_serial.py
```

### 4. Aplicação Web com Streamlit
```bash
streamlit run python_pipeline/streamlit_app/app.py
```

Prints do Serial Plotter
As imagens abaixo mostram a variação em tempo real da umidade coletada no ESP32 e visualizada com o Serial Plotter do Wokwi:

<p align="center"> <img src="images/serial_plotter_prints/print_umidade1.png" width="400px" /> <img src="images/serial_plotter_prints/print_umidade2.png" width="400px" /> </p>
Essas visualizações auxiliam no entendimento das oscilações no solo ao longo do tempo.

## Modelagem com Machine Learning
Utilizamos o Scikit-learn para treinar um modelo de regressão que prevê a necessidade de irrigação com base em:

- Umidade atual

- Nível de nutrientes

- Tendência histórica

Modelos testados:

- Linear Regression

- Decision Tree Regressor

- Random Forest Regressor

## 🕓 Histórico de Versões

**v0.1.0** – Implementação básica de sensores no ESP32  

**v0.2.0** – Ingestão de dados + visualização no LCD

**v0.3.0** – Modelos de Machine Learning + Streamlit App 

**v1.0.0** – Integração total e otimizações com documentação completa

---

📋 **Licença**

<img src="https://mirrors.creativecommons.org/presskit/icons/cc.svg" width="22px" style="vertical-align:text-bottom; margin-right:2px;" /> <img src="https://mirrors.creativecommons.org/presskit/icons/by.svg" width="22px" style="vertical-align:text-bottom;" />  
<p xmlns:dct="http://purl.org/dc/terms/">
<a property="dct:title" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por 
<a property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sob 
<a href="http://creativecommons.org/licenses/by/4.0/" rel="license">Attribution 4.0 International</a>.
</p>
