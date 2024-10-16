# schemas.py
from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Optional
from datetime import date


class UserCreate(BaseModel):
    name: str
    role: str
    dateOfBirth: date
    voterID: str
    email: str
    password: str

    @field_validator('password')
    def check_password(cls, v):
        if not v or len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

    class Config:
        json_encoders   = {
            date: lambda v: v.isoformat()
        }



class UserResponse(BaseModel):
    id: int
    name: str
    role: str
    email: str
    dateOfBirth: date
    voterID: str
    is_active: bool

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password : str

    @field_validator('password')
    def check_senha(cls, v):
        if not v:
            raise ValueError('Senha não pode estar vazia')
        return v

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: str
    password : str


class OcorrenciaCreate(BaseModel):
    municipio: str
    zona: str
    correspondencia: str
    dataOcorrencia: str
    tipoDeUrna: str
    secaoMrj: str
    patrimonioUrna: str
    horaOcorrencia: str
    modeloDeUrna: str

class OcorrenciaResponse(BaseModel):
    id: int
    municipio: str
    zona: str
    correspondencia: str
    dataOcorrencia: str
    tipoDeUrna: str
    secaoMrj: str
    patrimonioUrna: str
    horaOcorrencia: str
    modeloDeUrna: str

    class Config:
        from_attributes = True

class OcorrenciaBase(BaseModel):
    municipio: str
    zona: str
    secaoMrj: str
    correspondencia: str
    patrimonioUrna: str
    dataOcorrencia: date
    horaOcorrencia: str
    tipoDeUrna: str
    modeloUrna: str
    problemas: List[str]
    solucoes: List[str]
    descricaoProblema: Optional[str]
    imagem: Optional[str]

class OcorrenciaCreate(OcorrenciaBase):
    pass

class OcorrenciaResponse(OcorrenciaBase):
    id: int

    class Config:
        from_attributes = True



from pydantic import BaseModel

class AdminLogin(BaseModel):
    voterID: str
    password: str