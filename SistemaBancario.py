menu = '''
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair 
'''
conta = 0
depositos = 0
saques = 0
valores_saques = 0
saldo = 0
extrato = ''

while True:
    opcao = input(menu)

    if opcao == 'd':
        depositado = int(input('Digite o valor que irá depositar: '))
        if depositado >= 1:
            conta += depositado
            depositos += depositado
            saldo = conta - saques
            print(f'R$ {depositado:.2f} depositado com sucesso!')
        else:
            print('Depósito inválido.')

    elif opcao == 's':
        limite_saques = 3
        limite_valor_saque = 500
        if saques < limite_saques:
            saque = int(input('Digite o valor para sacar: '))
            if saque > limite_valor_saque:
                print('Saque indisponível.')
            elif saque > saldo:
                print('Saldo insuficiente.')
            else:
                conta -= saque
                saques += 1
                valores_saques += saque
                saldo = conta - saques
                print(f'Saque no valor de R$ {saque:.2f} realizado com sucesso!')
        else:
            print('Limite de saques diários atingidos.')

    elif opcao == 'e':
        saldo = conta
        print(f'Depósitos: R${depositos:.2f}')
        print(f'Saques: {saques}/3.')
        print(f'Valores sacados: R${valores_saques:.2f}')
        print(f'Saldo: R${saldo:.2f}')

    elif opcao == 'q':
        break
    else:
        print('Operação inválida. Selecione as opções disponíveis apenas.')