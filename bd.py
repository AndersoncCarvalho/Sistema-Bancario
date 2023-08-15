from sqlalchemy import Column, String, Numeric, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Cliente(Base):
    __tablename__ = 'cliente'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(Numeric)
    endereco = Column(Numeric)

    def __repr__(self):
        return f'Cliente(nome: {self.nome}, cpf: {self.cpf}, endereco: {self.endereco})'


class Conta(Base):
    __tablename__ = 'conta'

    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    agencia = Column(String)
    numero = Column(Integer)
    id_cliente = Column(Integer)
    saldo = Column(Numeric)

    def __repr__(self):
        return f'Tipo: {self.tipo}, Agencia: {self.agencia}, Numero: {self.numero}, ' \
               f'Id_cliente: {self.id_cliente}, saldo: {self.saldo}'