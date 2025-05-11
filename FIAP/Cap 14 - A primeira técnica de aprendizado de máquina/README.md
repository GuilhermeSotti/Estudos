
# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
  <a href="https://www.fiap.com.br/">
    <img src="../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" width="40%" />
  </a>
</p>

#  Projeto: FarmTech Solutions – Capítulo 14 - Predição de Culturas Agrícolas com Machine Learning

## Nome do grupo: --

##  Integrantes
- [Guilherme Pires de Sotti Machado](https://www.linkedin.com/in/guilherme-pires-de-sotti-machado-296a7417a/)

##  Professores

### Tutor(a)
- [Lucas Gomes Moreira](https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/)

---

## Descrição

**Prever o tipo de cultura agrícola mais adequada** com base em dados de clima e solo, aplicando técnicas de **Machine Learning (matplotlib)** conforme estudado nos capítulos 13 e 14 do curso de Desenvolvimento de Inteligência Artificial.

A solução contempla:

-  **Limpeza e pré-processamento de dados**
-  **Análise descritiva com visualizações**
-  **Treinamento de 5 modelos de Machine Learning**:
    - Decision Tree  
    - Random Forest  
    - K-Nearest Neighbors  
    - Logistic Regression  
    - Support Vector Machine
-  **Avaliação dos modelos com métricas de desempenho**
-  **Extração do “perfil ideal” de solo/clima** e comparação com culturas específicas

---

## Estrutura de Pastas

```
Cap 14 - A primeira técnica de aprendizado de máquina
├── data/ 
│   ├── Atividade_Cap_14_produtos_agricolas.csv
│   ├── exemplos_limpeza_dados.csv
│   └── HTML_Cap_14_fertilizer_prediction.csv
├── notebooks/
│   └── analise_predicao.ipynb
├── results/
│   ├── graficos/     
│   ├── metricas/     
│   └── modelos_salvos/
├── scripts/
│   ├── preprocessamento.py
│   ├── treinamento_modelos.py
│   └── visualizacoes.py
├── utils/
│   └── funcoes_auxiliares.py
└── requirements.txt 
```

---

## Como Executar

### 1. Instale as dependências

```bash
pip install -r requirements.txt
```

### 2. Rode o notebook

Abra o Jupyter e execute o notebook localizado em `notebooks/analise_predicao.ipynb`

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
