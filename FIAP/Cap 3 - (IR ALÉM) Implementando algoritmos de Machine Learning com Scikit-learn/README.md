# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
  <a href="https://www.fiap.com.br/">
    <img src="../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" width="40%" />
  </a>
</p>

# Cap 3 - (IR ALÉM) Implementando algoritmos de Machine Learning com Scikit-learn

## Nome do grupo: --

##  Integrantes
- [Guilherme Pires de Sotti Machado](https://www.linkedin.com/in/guilherme-pires-de-sotti-machado-296a7417a/)

##  Professores

### Tutor(a)
- [Lucas Gomes Moreira](https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/)

---

## 📌 Sobre o Projeto
O FarmTech Solutions é uma aplicação voltada para cooperativas agrícolas de pequeno porte, com o objetivo de automatizar a classificação de variedades de grãos de trigo (Kama, Rosa, Canadian) a partir de características físicas. Baseado na metodologia CRISP-DM e no Seeds Dataset do UCI Machine Learning Repository, o projeto engloba desde a obtenção e pré-processamento dos dados até o deploy de um serviço de predição em produção.

## 📖 Índice
- [📌 Sobre o Projeto](#-sobre-o-projeto)
- [🎯 Objetivos](#-objetivos)
- [⚙️ Funcionalidades](#️-funcionalidades)
- [🛠️ Tecnologias Utilizadas](#️-tecnologias-utilizadas)
- [⚙️ Pré-requisitos](#️-pré-requisitos)
- [💻 Como Executar](#-como-executar)
- [👥 Contribuição](#-contribuição)
- [⚠️ Licença](#️-licença)

## 🎯 Objetivos
- **Automatizar a classificação** de grãos de trigo para reduzir tempo e erros humanos em cooperativas.
- **Desenvolver** um pipeline completo (CRISP-DM) de EDA, pré-processamento, modelagem, otimização e avaliação.
- **Construir** uma API REST para permitir predição em tempo real ou em lote a partir de novas medições.
- **Garantir** boas práticas de engenharia de software: modularidade, configuração externa, logs, testes e reprodutibilidade.
- **Possibilitar** extensões “fora da caixa”, como extração de medidas via visão computacional, explainability (SHAP/LIME), monitoramento de drift e dashboard interativo.

## ⚙️ Funcionalidades
- **Download e pré-processamento de dados**: scripts para obter o Seeds Dataset, verificar missing/outliers, split treino/teste.
- **Exploratory Data Analysis (EDA)**: notebooks com estatísticas descritivas, histogramas, boxplots, scatter matrix, correlações.
- **Feature Engineering**: cálculo de compacidade (4·π·area / perimeter²), ratios (length/width), PCA/LDA para visualização ou uso em pipeline.
- **Modelagem e comparação de algoritmos**: pipelines sklearn para KNN, SVM, Random Forest, Naive Bayes, Logistic Regression, entre outros.
- **Otimização de hiperparâmetros**: GridSearchCV/RandomizedSearchCV (e opção para otimização bayesiana) integrados a pipelines.
- **Avaliação e relatórios**: geração de classification report (JSON), matriz de confusão (PNG), métricas resumo (accuracy, precision, recall, F1, ROC AUC multiclass).
- **Explainability**: integração com SHAP (e possivelmente LIME) para interpretar importâncias e decisões do modelo.
- **Deploy de API REST**: serviço em FastAPI (ou Flask) para predição de novas amostras, calculando features necessárias (ex.: compacidade) se ausentes.
- **Scripts CLI**: orquestração de treino, avaliação e predição em lote ou interativa.
- **Monitoramento e manutenção**: sugestões para monitorar drift de dados, re-treinamento automático, logs de predições.
- **Integração opcional de Visão Computacional**: pipeline para extrair medidas de imagens de grãos via OpenCV.
- **Dashboard Interativo**: ideia de uso de Streamlit/Dash para exibir estatísticas, predições e explicações a operadores.

## 🛠️ Tecnologias Utilizadas
- **Linguagem e Bibliotecas**:
  - Python 3.8+  
  - Pandas, NumPy  
  - scikit-learn  
  - matplotlib  
  - joblib  
  - pyyaml (config)  
  - OpenCV (opcional, para pipeline de visão)  
  - SHAP (explainability)  
  - pytest (testes)  

- **Infraestrutura**:
  - GitHub
- **Ambiente de Desenvolvimento**:
  - venv para gerenciar dependências  

- **Ferramentas de Dashboard** (opcional):
  - Streamlit ou Dash para interface interativa  
- **Ferramentas de Monitoramento**:
  - Logging estruturado e rotação de logs


## ⚙️ Pré-requisitos
- Python 3.8 ou superior instalado.
- Ferramentas de ambiente virtual (venv, Poetry ou Pipenv).
- Internet (para baixar dataset via script) ou download manual do Seeds Dataset.
- Permissões para criar diretórios e salvar arquivos de saída.

## 💻 Como Executar

```bash
  cd Cap 3 - (IR ALÉM) Implementando algoritmos de Machine Learning com Scikit-learn

  pip install -r requirements.txt

  python run_all.py

```

---

📋 Licença
<img src="https://mirrors.creativecommons.org/presskit/icons/cc.svg" width="22px" style="vertical-align:text-bottom; margin-right:2px;" /> <img src="https://mirrors.creativecommons.org/presskit/icons/by.svg" width="22px" style="vertical-align:text-bottom;" /> <p xmlns:dct="http://purl.org/dc/terms/"> <a property="dct:title" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/" rel="license">Attribution 4.0 International</a>. </p>