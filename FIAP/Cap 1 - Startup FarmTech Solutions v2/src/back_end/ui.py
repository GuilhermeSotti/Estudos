from src.back_end import calculations, repository, models

def menu():
    while True:
        print("\n======================================")
        print(" FarmTech Solutions – Menu Principal")
        print("======================================")
        print("1. Entrada de Dados")
        print("2. Exibição de Dados")
        print("3. Atualização de Dados")
        print("4. Deleção de Dados")
        print("5. Sair")
        opcao = input("Selecione uma opção: ").strip()

        if opcao == '1':
            entrada_dados()
        elif opcao == '2':
            exibir_dados()
        elif opcao == '3':
            atualizar_dados()
        elif opcao == '4':
            deletar_dados()
        elif opcao == '5':
            print("Encerrando o programa... Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")

def entrada_dados():
    print("\n--- Entrada de Dados ---")
    print("Culturas disponíveis: 1 - Café | 2 - Soja")
    opcao = input("Selecione a cultura (1 ou 2): ").strip()

    if opcao == '1':
        cultura = "Café"
        try:
            comprimento = float(input("Informe o comprimento do campo (m): "))
            largura = float(input("Informe a largura do campo (m): "))
            area = calculations.calcular_area_retangular(comprimento, largura)
            dose = float(input("Informe a dose de fosfato recomendada (g/m²): "))
            quantidade_insumo = calculations.calcular_insumo_cafe(area, dose)

            insumo = models.Insumo("Fosfato", dose, quantidade_insumo)
            registro = models.Cultura(cultura, 'Retangular', {'comprimento': comprimento, 'largura': largura}, area, insumo)
            repository.adicionar_registro(registro)
            print("Registro adicionado com sucesso!")
        except ValueError:
            print("Entrada inválida. Certifique-se de informar números válidos.")
    elif opcao == '2':
        cultura = "Soja"
        try:
            raio = float(input("Informe o raio do campo (m): "))
            area = calculations.calcular_area_circular(raio)
            num_ruas = int(input("Número de ruas da lavoura: "))
            comprimento_medio = float(input("Comprimento médio de cada rua (m): "))
            quantidade_insumo = calculations.calcular_insumo_soja(num_ruas, comprimento_medio)
            
            extras = {'num_ruas': num_ruas, 'comprimento_medio': comprimento_medio, 'taxa': 500}
            insumo = models.Insumo("Pulverizador", 500, quantidade_insumo, extras)
            registro = models.Cultura(cultura, 'Circular', {'raio': raio}, area, insumo)
            repository.adicionar_registro(registro)
            print("Registro adicionado com sucesso!")
        except ValueError:
            print("Entrada inválida. Certifique-se de informar números válidos.")
    else:
        print("Opção de cultura inválida. Tente novamente.")

def exibir_dados():
    print("\n--- Exibindo Dados dos Registros ---")
    registros = repository.listar_registros()
    if not registros:
        print("Nenhum registro encontrado.")
    else:
        for i, registro in enumerate(registros):
            print(f"\nRegistro [{i}]:")
            print(f"  Cultura: {registro.nome}")
            print(f"  Formato: {registro.formato}")
            if registro.nome == "Café":
                print(f"  Dimensões: Comprimento = {registro.dimensoes['comprimento']} m, Largura = {registro.dimensoes['largura']} m")
            else:
                print(f"  Dimensões: Raio = {registro.dimensoes['raio']} m")
            print(f"  Área: {registro.area:.2f} m²")
            insumo = registro.insumo
            print("  Insumo:")
            print(f"    Produto: {insumo.produto}")
            if registro.nome == "Café":
                print(f"    Dose: {insumo.dose} g/m²")
            else:
                print(f"    Número de ruas: {insumo.extras.get('num_ruas')}")
                print(f"    Comprimento médio: {insumo.extras.get('comprimento_medio')} m")
                print(f"    Taxa: {insumo.dose} mL/m")
            print(f"    Quantidade necessária: {insumo.quantidade:.2f} {'gramas' if registro.nome=='Café' else 'litros'}")

def atualizar_dados():
    print("\n--- Atualização de Dados ---")
    registros = repository.listar_registros()
    if not registros:
        print("Nenhum registro para atualizar.")
        return
    try:
        indice = int(input("Informe o índice do registro que deseja atualizar: "))
        if indice < 0 or indice >= len(registros):
            print("Índice inválido.")
            return
        print("Insira os novos dados para este registro:")
        # Simplesmente removemos o registro antigo e chamamos a entrada de dados
        repository.deletar_registro(indice)
        entrada_dados()
        print("Registro atualizado com sucesso!")
    except ValueError:
        print("Entrada inválida.")

def deletar_dados():
    print("\n--- Deleção de Dados ---")
    registros = repository.listar_registros()
    if not registros:
        print("Nenhum registro para deletar.")
        return
    try:
        indice = int(input("Informe o índice do registro que deseja deletar: "))
        if repository.deletar_registro(indice):
            print("Registro deletado com sucesso!")
        else:
            print("Índice inválido.")
    except ValueError:
        print("Entrada inválida.")
