import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle

def salvar_modelo(modelo, nome_arquivo):
    with open(nome_arquivo, 'wb') as f:
        pickle.dump(modelo, f)

def carregar_modelo(nome_arquivo):
    with open(nome_arquivo, 'rb') as f:
        return pickle.load(f)

def gerar_radar_chart(perfil_ideal, culturas, media_culturas):
    import matplotlib.pyplot as plt

    labels = perfil_ideal.index
    num_vars = len(labels)

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    perfil_ideal_valores = perfil_ideal.tolist()
    perfil_ideal_valores += perfil_ideal_valores[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.plot(angles, perfil_ideal_valores, label='Perfil Ideal', color='black', linewidth=2)
    ax.fill(angles, perfil_ideal_valores, alpha=0.1)

    for cultura in culturas:
        valores = media_culturas.loc[cultura].tolist()
        valores += valores[:1]
        ax.plot(angles, valores, label=cultura)
        ax.fill(angles, valores, alpha=0.1)

    ax.set_title('Radar Chart: Perfil Ideal vs Culturas')
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.show()
