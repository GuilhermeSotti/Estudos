import subprocess
import sys
import os

def run_cmd(cmd, cwd=None):
    """Executa um comando via subprocess.run, repassa saída e interrompe em erro."""
    print(f"\n>>> Executando: {' '.join(cmd)}")
    result = subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr, cwd=cwd)
    if result.returncode != 0:
        raise RuntimeError(f"Comando falhou (exit {result.returncode}): {' '.join(cmd)}")

def main():
    root = os.getcwd()
    path_base = "Cap 3 - (IR ALÉM) Implementando algoritmos de Machine Learning com Scikit-learn"

    try:
        run_cmd([sys.executable, f"{path_base}/train.py"], cwd=root)

        run_cmd([sys.executable, f"{path_base}/preprocess_data.py"], cwd=root)

        run_cmd([sys.executable, f"{path_base}/evaluate.py"], cwd=root)

        run_cmd([sys.executable, f"{path_base}/predict.py"], cwd=root)

        print("\n>>> Todos os passos concluídos com sucesso.")
    except Exception as e:
        print(f"\nErro durante execução: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
