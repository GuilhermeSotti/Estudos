# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
  <a href="https://www.fiap.com.br/">
    <img src="../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" width="40%" />
  </a>
</p>

# Fase 6 — Capítulo 1: Despertar da Rede Neural

## Nome do grupo: --

## Integrantes
- [Guilherme Pires de Sotti Machado](https://www.linkedin.com/in/guilherme-pires-de-sotti-machado-296a7417a/)

## Professores

### Tutor(a)
- [Lucas Gomes Moreira](https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/)

---

## Video
Link: [VideoExplicativo](https://youtu.be/QgQF-Qi18eU)

## Objetivo
Desenvolver, treinar e comparar abordagens de visão computacional:
- Detecção: YOLO (adaptado e tradicional)
- Classificação: CNN treinada do zero

## Estrutura
- `notebooks/` — notebook Colab principal (executável).
- `src/` — scripts de preparação, treino e avaliação.
- `dataset/` — manifesto e instruções para o Google Drive.
- `results/` — métricas, artfatos e imagens de teste.

## Requisitos
- Python (3.10+ recomendado)
- GPU (Colab GPU recomendada — Tesla T4/P100/V100)
- Ver `requirements.txt` para versões exatas.

## Como reproduzir (Colab — passo a passo)
1. Abra `notebooks/01_train_yolo_cnn_colab.ipynb` no Colab.
2. Monte o Google Drive (o notebook tem uma célula automatizada).
3. Instale dependências via pip (célula pronta).
4. Execute células na ordem: preparação -> upload dataset -> rotulagem (instruções) -> treino YOLO (30 e 60 epochs) -> treino CNN -> avaliação.
5. Resultados serão salvos em `/content/drive/MyDrive/FarmTech_Fase6/Cap1_Despertar_RedeNeural/results/`.

## Como reproduzir localmente
1. Clone o repo.
2. Crie virtualenv e instale `pip install -r requirements.txt`.
3. Ajuste paths em `src/config.yaml` (ou edite variáveis nos scripts).
4. Rode `python src/data_prep.py` etc. (exemplos nas instruções abaixo e no notebook).


---

📋 **Licença**

<img src="https://mirrors.creativecommons.org/presskit/icons/cc.svg" width="22px" style="vertical-align:text-bottom; margin-right:2px;" /> <img src="https://mirrors.creativecommons.org/presskit/icons/by.svg" width="22px" style="vertical-align:text-bottom;" />  
<p xmlns:dct="http://purl.org/dc/terms/">
<a property="dct:title" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por 
<a property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sob 
<a href="http://creativecommons.org/licenses/by/4.0/" rel="license">Attribution 4.0 International</a>.
</p>
      