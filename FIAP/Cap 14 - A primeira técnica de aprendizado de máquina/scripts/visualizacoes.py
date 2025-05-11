import matplotlib.pyplot as plt
import seaborn as sns

def plot_histograma(df):
    df.hist(bins=15, figsize=(15,10), color='teal')
    plt.suptitle("Distribuição das Variáveis")
    plt.show()

def plot_boxplot(df, coluna_x, coluna_y):
    plt.figure(figsize=(12,6))
    sns.boxplot(x=coluna_x, y=coluna_y, data=df)
    plt.title(f'{coluna_y} por {coluna_x}')
    plt.xticks(rotation=45)
    plt.show()

def plot_correlacao(df):
    df_numerico = df.select_dtypes(include=['number'])
    plt.figure(figsize=(10, 8))
    sns.heatmap(df_numerico.corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Mapa de Calor das Correlações entre Variáveis Numéricas")
    plt.tight_layout()
    plt.show()

def plot_dispersao(df, x, y, hue):
    sns.scatterplot(data=df, x=x, y=y, hue=hue)
    plt.title(f'{x} vs {y} por {hue}')
    plt.show()

def plot_violino(df, x, y):
    plt.figure(figsize=(12,6))
    sns.violinplot(x=x, y=y, data=df)
    plt.title(f'{y} por {x}')
    plt.xticks(rotation=45)
    plt.show()
