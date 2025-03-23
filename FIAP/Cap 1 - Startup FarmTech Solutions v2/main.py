from src.back_end import ui
import os

def main():
    ui.menu()
    os.system("Rscript src/front_end/main_analysis.r")

if __name__ == "__main__":
    main()