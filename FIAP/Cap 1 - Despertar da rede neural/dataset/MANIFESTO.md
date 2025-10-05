# Manifesto do dataset — Cap1_Despertar_RedeNeural

Classes:
- class0: vaca
- class1: cerca

Total de imagens: 80
- vaca: 40  -> train 32 / val 4 / test 4
- cerca: 40  -> train 32 / val 4 / test 4

Formato:
- Imagens: JPG/PNG em pastas conforme:
  /FarmTech_Fase6/Cap1_Despertar_RedeNeural/dataset/
    train/vaca/
    train/cerca/
    val/vaca/
    val/cerca/
    test/vaca/
    test/cerca/
- Labels YOLO (apenas para images de treino): train/labels/*.txt
  cada .txt: one line per bbox: <class_idx> <x_center> <y_center> <width> <height> (normalizado)

Observações:
- Os arquivos de teste e validação não devem conter .txt (para avaliar detecção/transformar para classificação).
- Privacidade: imagens não contêm pessoas identificáveis.
