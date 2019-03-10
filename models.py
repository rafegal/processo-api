__author__ = 'galleani'
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, Date, DateTime, func, exists
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://gestaoprocesso:gestaoprocesso123@localhost:5432/gestaoprocesso', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class Situacao(Base):
    __tablename__='situacao'
    id = Column(Integer, primary_key=True)
    nome = Column(String(255))
    finalizado = Column(Boolean)

    def __repr__(self):
        return '<Situacao {}>'.format(self.nome)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class Responsavel(Base):
    __tablename__='responsavel'
    id = Column(Integer, primary_key=True)
    nome = Column(String(75))
    cpf = Column(String(11))
    email = Column(String(200))
    data_nascimento = Column(Date)

    def __repr__(self):
        return '<Situacao {}>'.format(self.nome)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class Processo(Base):
    __tablename__='processo'
    id = Column(Integer, primary_key=True)
    numero_processo = Column(String(20))
    data_distribuicao = Column(Date)
    descricao = Column(String(4000))
    pasta_fisica_cliente = Column(String(75))
    segredo_justica = Column(Boolean)
    situacao_id = Column(Integer, ForeignKey('situacao.id'))
    situacao = relationship('Situacao')

    def __repr__(self):
        return '<Processo {}>'.format(self.numero_processo)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

class ProcessoResponsavel(Base):
    __tablename__='processo_responsavel'
    processo_id = Column(Integer, ForeignKey('processo.id'), primary_key=True)
    processo = relationship('Processo')
    responsavel_id = Column(Integer, ForeignKey('responsavel.id'), primary_key=True)
    responsavel = relationship('Responsavel')

    def __repr__(self):
        return '<Processo {}>'.format(self.responsavel.nome)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


def get_max_responsavel_id():
    max_id = db_session.query(func.max(Responsavel.id)).scalar()
    return max_id


def get_existing_cpf_responsavel(cpf, resp_id=None):
    q = db_session.query(Responsavel).filter(Responsavel.id != resp_id, Responsavel.cpf == cpf)
    return db_session.query(q.exists()).scalar()


def get_existing_email_responsavel(email, resp_id=None):
    q = db_session.query(Responsavel).filter(Responsavel.id != resp_id, Responsavel.email == email)
    return db_session.query(q.exists()).scalar()


def get_existing_processo_responsavel(resp_id):
    q = db_session.query(ProcessoResponsavel).filter(ProcessoResponsavel.responsavel_id == resp_id)
    return db_session.query(q.exists()).scalar()
