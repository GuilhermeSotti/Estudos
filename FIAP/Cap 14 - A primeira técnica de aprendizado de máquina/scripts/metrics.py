import pandas as pd
import numpy as np

def salvar_metricas_csv(resultados, caminho='results/metricas/comparativo_modelos.csv'):
    linhas = []
    for nome, metricas in resultados.items():
        linha = {
            'Modelo': nome,
            'Acuracia': metricas['acuracia'],
            'Precision Média': np.mean([v['precision'] for k, v in metricas['relatorio_classificacao'].items() if k in metricas['relatorio_classificacao'] and isinstance(v, dict)]),
            'Recall Médio': np.mean([v['recall'] for k, v in metricas['relatorio_classificacao'].items() if k in metricas['relatorio_classificacao'] and isinstance(v, dict)])
        }
        linhas.append(linha)

    df_resultados = pd.DataFrame(linhas)
    df_resultados.to_csv(caminho, index=False)
    return df_resultados