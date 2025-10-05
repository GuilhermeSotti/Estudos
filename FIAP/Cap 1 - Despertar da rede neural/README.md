# Cap1_Despertar_RedeNeural

Repositório para a **Fase 6 — Capítulo 1: Despertar da Rede Neural** do projeto FarmTech Solutions.

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

## Notas importantes
- Seeds fixos: `seed=42` (documentado nos scripts).
- Rotulagem: Use MakeSense.ai exportando em formato YOLO e salvar em `dataset/train/labels/`.
- Entrega final: report.pdf em `/report/report.pdf` e roteiro em `/video/video_script.txt`.

## Contato
Guilherme Pires de Sotti Machado — mantenha issues no GitHub para dúvidas.
