from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

menu = '''
[u] Criar Usuário
[c] Criar Conta Corrente
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
'''

# Lista de usuários
usuarios = []

# Lista de contasu
contas = []

# Dados da conta corrente
conta_corrente = {
    'agencia': '0001',
    'numero_conta': 0,
    'saldo': 0,
    'depositos': 0,
    'saques': 0,
    'valores_saques': 0,
    'extrato': ''
}

def criar_usuario():
    nome = input('Digite o nome do usuário: ')
    data_nascimento = input('Digite a data de nascimento (DD/MM/AAAA): ')
    cpf = input('Digite o CPF: ')
    endereco = input('Digite o endereço (logradouro, numero, bairro, cidade, estado): ')
    cpf = ''.join(c for c in cpf if c.isdigit())  # Remove caracteres não numéricos do CPF

    # Verifica se já existe um usuário com o mesmo CPF
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            print('CPF já cadastrado. Tente novamente.')
            return

    novo_usuario = {
        'nome': nome,
        'data_nascimento': data_nascimento,
        'cpf': cpf,
        'endereco': endereco,
        'contas': []
    }

    usuarios.append(novo_usuario)
    print('Usuário criado com sucesso!')

def criar_conta_corrente():
    cpf_usuario = input('Digite o CPF do usuário para vincular a conta: ')

    # Verifica se o CPF do usuário está cadastrado
    usuario_existente = None
    for usuario in usuarios:
        if usuario['cpf'] == cpf_usuario:
            usuario_existente = usuario
            break

    if usuario_existente is None:
        print('Usuário não encontrado. Tente novamente.')
        return

    # Verifica se o usuário já possui uma conta corrente
    for conta in contas:
        if conta['usuario'] == usuario_existente:
            print('O usuário já possui uma conta corrente.')
            return

    numero_conta = len(contas) + 1

    nova_conta = {
        'agencia': conta_corrente['agencia'],
        'numero_conta': numero_conta,
        'usuario': usuario_existente
    }

    contas.append(nova_conta)
    usuario_existente['contas'].append(nova_conta)
    print(f'Conta corrente {numero_conta} criada para o usuário {usuario_existente["nome"]}.')

def depositar(valor):
    if valor >= 1:
        conta_corrente['depositos'] += valor
        conta_corrente['saldo'] += valor
        conta_corrente['extrato'] += f'Depósito: R$ {valor:.2f}\n'
        print(f'R$ {valor:.2f} depositado com sucesso!')
    else:
        print('Depósito inválido.')

def sacar(valor):
    limite_saques = 3
    limite_valor_saque = 500
    if conta_corrente['saques'] < limite_saques:
        if valor > limite_valor_saque:
            print('Saque indisponível.')
        elif valor > conta_corrente['saldo']:
            print('Saldo insuficiente.')
        else:
            conta_corrente['saques'] += 1
            conta_corrente['valores_saques'] += valor
            conta_corrente['saldo'] -= valor
            conta_corrente['extrato'] += f'Saque: R$ {valor:.2f}\n'
            print(f'Saque no valor de R$ {valor:.2f} realizado com sucesso!')
    else:
        print('Limite de saques diários atingidos.')

def visualizar_extrato():
    print(f'Depósitos: R$ {conta_corrente["depositos"]:.2f}')
    print(f'Saques: {conta_corrente["saques"]}/3')
    print(f'Valores sacados: R$ {conta_corrente["valores_saques"]:.2f}')
    print(f'Saldo: R$ {conta_corrente["saldo"]:.2f}')
    print('Extrato:')
    print(conta_corrente['extrato'])

# Função principal
def main():
    while True:
        opcao = input(menu)

        if opcao == 'u':
            criar_usuario()

        elif opcao == 'c':
            criar_conta_corrente()

        elif opcao == 'd':
            valor_deposito = int(input('Digite o valor que irá depositar: '))
            depositar(valor_deposito)

        elif opcao == 's':
            valor_saque = int(input('Digite o valor para sacar: '))
            sacar(valor_saque)

        elif opcao == 'e':
            visualizar_extrato()

        elif opcao == 'q':
            break

        else:
            print('Operação inválida. Selecione as opções disponíveis apenas.')

if __name__ == '__main__':
    main()





