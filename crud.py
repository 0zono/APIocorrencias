from time import strptime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Ocorrencia, User
from schemas import OcorrenciaCreate, UserCreate
from passlib.context import CryptContext
import json

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_password_hash(password: str):
    return pwd_context.hash(password)

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        name=user.name,
        role=user.role,
        dateOfBirth=user.dateOfBirth,
        voterID=user.voterID,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user

# Ocorrencia CRUD operations

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()  
 



def create_ocorrencia(db: Session, ocorrencia: OcorrenciaCreate):
    db_ocorrencia = Ocorrencia(
        descricaoProblema=ocorrencia.descricaoProblema,
        problemas=json.dumps(ocorrencia.problemas),  # Serializa para JSON
        solucoes=json.dumps(ocorrencia.solucoes),  # Serializa as soluções para JSON
        municipio=ocorrencia.municipio,
        zona=ocorrencia.zona,
        secaoMrj=ocorrencia.secaoMrj,
        correspondencia=ocorrencia.correspondencia,
        patrimonioUrna=ocorrencia.patrimonioUrna,
        dataOcorrencia=ocorrencia.dataOcorrencia,
        horaOcorrencia=ocorrencia.horaOcorrencia,
        tipoDeUrna=ocorrencia.tipoDeUrna,
        modeloUrna=ocorrencia.modeloUrna,
        imagem=ocorrencia.imagem
    )
    db.add(db_ocorrencia)
    db.commit()
    db.refresh(db_ocorrencia)

    # Desserializa problemas e solucoes para retorno correto
    db_ocorrencia.problemas = json.loads(db_ocorrencia.problemas)
    db_ocorrencia.solucoes = json.loads(db_ocorrencia.solucoes)

    return db_ocorrencia



def get_ocorrencia(db: Session, ocorrencia_id: int):
    return db.query(Ocorrencia).filter(Ocorrencia.id == ocorrencia_id).first()

def get_ocorrencias(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Ocorrencia).offset(skip).limit(limit).all()

def delete_ocorrencia(db: Session, ocorrencia_id: int):
    db_ocorrencia = db.query(Ocorrencia).filter(Ocorrencia.id == ocorrencia_id).first()
    if db_ocorrencia:
        db.delete(db_ocorrencia)
        db.commit()
    return db_ocorrencia
