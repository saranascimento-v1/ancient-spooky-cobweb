def menu():
    return (
        "\nPor gentileza, selecione uma das opções listadas abaixo:\n"
        "[d] Depositar\n"
        "[s] Sacar\n"
        "[e] Extrato\n"
        "[nu] Novo Usuário\n"
        "[nc] Nova Conta\n"
        "[q] Sair\n\n"
        "=> "
    )


def exibir_extrato(saldo, /, *, extrato):
    print("\n=========== EXTRATO ===========")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\tR$ {saldo:.2f}")
    print("================================\n")


def criar_usuario(base_clientes):
    print("\n=== Vamos seguir com o cadastro do seu usuário, por gentileza, digite os dados abaixo ===")

    cpf = input("Digite seu CPF (somente números): ").strip()

    # Verifica se já existe CPF cadastrado
    for cliente in base_clientes.values():
        if cpf == cliente["cpf"]:
            return "Este CPF já está cadastrado."

    nome = input("Digite seu nome completo: ").strip()
    data_nascimento = input("Digite sua data de nascimento (dd-mm-aaaa): ").strip()
    endereco = input("Digite seu endereço (logradouro, nro - bairro - cidade/UF): ").strip()

    id_cliente = f"cliente_{cpf[:3]}"

    base_clientes[id_cliente] = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco,
    }

    print("\nUsuário cadastrado com sucesso!")
    return base_clientes


def criar_conta_corrente(base_clientes, numero_conta,conta):
    print("\n=== Abertura de Conta ===")
    cpf = input("Digite o CPF do titular da conta: ").strip()
    cpf_castrado= None
    for x in base_clientes.values():
        cpf_castrado = x["cpf"] == cpf
        if cpf_castrado:
            numero_conta+=1
            conta = {
            "agencia": "0001",
            "numero_conta": [numero_conta],
            "cpf_titular": cpf
            }
            print(f"\nConta criada com sucesso! Número da conta: {numero_conta}")
        else:
            return f"CPF não está vinculado a nenhum usuário cadastrado!"
    
    Cadastrar_nova_conta=input("Deseja cadastrar uma nova conta?")
    if Cadastrar_nova_conta =="sim" and cpf_castrado:
        numero_conta+=1
        conta["numero_conta"].extend([numero_conta])
        print(f"\nConta criada com sucesso! Número da conta: {numero_conta}")
    else: 
        print("Tente novamente mais tarde!")

    return conta, numero_conta


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if numero_saques >= limite_saques:
        print("Você atingiu o limite diário de saques.")
    elif valor > limite:
        print("O valor solicitado excede o limite permitido para saque.")
    elif valor > saldo:
        print("Saldo insuficiente para realizar o saque.")
    elif valor <= 0:
        print("Valor inválido para saque.")
    else:
        saldo -= valor
        numero_saques += 1
        extrato += f"Saque: R$ {valor:.2f}\n"
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
    
    return saldo, extrato, numero_saques


def main():
    LIMITE_SAQUES = 3

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    base_clientes = {}
    contas = {}
    numero_conta = 0

    while True:
        opcao = input(menu()).lower()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            base_clientes = criar_usuario(base_clientes)

        elif opcao == "nc":
            contas, numero_conta = criar_conta_corrente(base_clientes, numero_conta,contas)

        elif opcao == "q":
            print("Obrigado por utilizar nosso sistema! Até logo.")
            break

        else:
            print("Opção inválida! Por favor, tente novamente.")



main()
