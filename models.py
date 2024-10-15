from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, ARRAY, Date
from db import Base
import json

class Ocorrencia(Base):
    __tablename__ = "ocorrencias"

    id = Column(Integer, primary_key=True, index=True)
    municipio = Column(String)
    zona = Column(String)
    secaoMrj = Column(String)
    correspondencia = Column(String)
    patrimonioUrna = Column(String)
    dataOcorrencia = Column(String)
    horaOcorrencia = Column(String)
    tipoDeUrna = Column(String)
    modeloUrna = Column(String)
    problemas = Column(String)   
    solucoes = Column(String)  
    descricaoProblema = Column(String)
    imagem = Column(String)

    def set_problemas(self, problemas_list):
        self.problemas = json.dumps(problemas_list)

    def get_problemas(self):
        return json.loads(self.problemas) if self.problemas else []

    def set_solucoes(self, solucoes_list):
        self.solucoes = json.dumps(solucoes_list)

    def get_solucoes(self):
        return json.loads(self.solucoes) if self.solucoes else []


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(String)
    dateOfBirth = Column(Date)
    voterID = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class Admin(Base):
    __tablename__ = "administradores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    voterID = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="admin")  
    is_active = Column(Boolean, default=True)
    created_at = Column(Date)
    updated_at = Column(Date)

    
    def is_superadmin(self):
        return self.role == "superadmin"

    def activate(self):
        self.is_active = True

    def deactivate(self):
        self.is_active = False
