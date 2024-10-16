from datetime import date
from sqlite3 import IntegrityError
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from db import SessionLocal, engine
import models
import schemas
from fastapi.staticfiles import StaticFiles
import crud
import httpx
from fastapi.middleware.cors import CORSMiddleware


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# alterar de acordo com necessidades CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,  
    allow_methods=["*"],
    allow_headers=["*"],
)




# Criação das tabelas no banco de dados, caso ainda não existam
models.Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Instanciação da aplicação FastAPI

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.post("/cadastro/", response_model=schemas.UserResponse)
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        print(f"Dados recebidos para cadastro: {user.dict()}")
        
        
        db_user = crud.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        
        new_user = crud.create_user(db=db, user=user)
        return schemas.UserResponse(
            id=new_user.id,
            name=new_user.name,
            role=new_user.role,
            email=new_user.email
        )
    except IntegrityError as e:
        
        if "UNIQUE constraint failed: users.voterID" in str(e):
            raise HTTPException(status_code=400, detail="VoterID already registered")
        elif "UNIQUE constraint failed: users.email" in str(e):
            raise HTTPException(status_code=400, detail="Email already registered")
        else:
            
            raise
    except Exception as e:
        
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@app.post("/login/")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    print(f"Dados recebidos para login: {user.model_dump()}")
    db_user = crud.authenticate_user(db, user.email, user.password )
    if not db_user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not db_user.is_active:
        raise HTTPException(status_code=403, detail="Account not activated")
    
    return {"success": True, "message": "Login successful", "user": {"id": db_user.id, "nome": db_user.name, "email": db_user.email}}


@app.get("/usuarios/", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return [schemas.UserResponse.model_validate(user) for user in users]

# Rota para criar uma nova ocorrência
@app.post("/ocorrencia/", response_model=schemas.OcorrenciaResponse)
def create_new_ocorrencia(ocorrencia: schemas.OcorrenciaCreate, db: Session = Depends(get_db)):
    print(f"Dados recebidos para nova ocorrência: {ocorrencia.model_dump()}")
    
    # Cria e retorna a nova ocorrência
    return crud.create_ocorrencia(db=db, ocorrencia=ocorrencia)

# Rota para listar todas as ocorrências, com paginação
@app.get("/ocorrencias/", response_model=list[schemas.OcorrenciaResponse])
def read_ocorrencias(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    print(f"Parâmetros recebidos para listagem de ocorrências: skip={skip}, limit={limit}")
    
    # Retorna uma lista de ocorrências
    return crud.get_ocorrencias(db=db, skip=skip, limit=limit)

# Rota para obter uma ocorrência específica pelo ID
@app.get("/ocorrencia/{ocorrencia_id}", response_model=schemas.OcorrenciaResponse)
def read_ocorrencia(ocorrencia_id: int, db: Session = Depends(get_db)):
    print(f"ID da ocorrência solicitada: {ocorrencia_id}")
    
    # Busca a ocorrência pelo ID
    db_ocorrencia = crud.get_ocorrencia(db=db, ocorrencia_id=ocorrencia_id)
    if not db_ocorrencia:
        raise HTTPException(status_code=404, detail="Ocorrência não encontrada")
    
    # Retorna a ocorrência encontrada
    return db_ocorrencia

# Rota para logout
@app.post("/logout")
def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Rota de logout que efetivamente não faz muito no lado do servidor, 
    mas pode ser expandida para adicionar o token a uma blacklist.
    """
    
    
    return {"message": "Logout successful"}

@app.get("/teste")
def test_api():
    return {"message": "API funcionando!"}

def create_test_user():
    db = SessionLocal()
    print("creating user...")
    
    date_of_birth = date(1990, 1, 1)

    
    user_data = schemas.UserCreate(
        name="Teste",
        role="Administrador",
        dateOfBirth=date_of_birth,
        voterID="123456789",
        email="teste@example.com",
        password="Senha1234!"
    )

    try:
        print(f"Attempting to create user with email: {user_data.email}")
        user = crud.create_user(db, user_data)
        print(f"Usuário de teste criado: {user.email}")
    except IntegrityError:
        print(f"Erro: O usuário com o email {user_data.email} já existe.")
    except Exception as e:
        print(f"Erro ao criar usuário: {str(e)}")
    finally:
        db.close()



IBGE_URL = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/mt/distritos"

@app.get("/municipios")
async def get_municipios():
    async with httpx.AsyncClient() as client:
        response = await client.get(IBGE_URL)
        if response.status_code == 200:
            dados = response.json()
            
            # Usando um dicionário para remover duplicados com base no ID do município
            municipios_unicos = {}
            for distrito in dados:
                municipio_id = distrito["municipio"]["id"]
                municipio_nome = distrito["municipio"]["nome"]

                # Adiciona ao dicionário somente se o município ainda não estiver presente
                if municipio_id not in municipios_unicos:
                    municipios_unicos[municipio_id] = {
                        "id": municipio_id,
                        "nome": municipio_nome
                    }

            # Converte de volta para uma lista de municípios únicos
            return list(municipios_unicos.values())
        else:
            return {"error": "Não foi possível obter os dados"}


@app.post("/admin/login/")
def login_admin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    print(f"Dados recebidos para login de administrador: {form_data.username}")
    
    # Autentica o usuário com o email (que será `form_data.username`) e a senha
    db_user = crud.authenticate_user(db, form_data.username, form_data.password)
    
    if not db_user:
        raise HTTPException(status_code=400, detail="Email ou senha incorretos")
    
    # Verifica se o usuário é administrador
    if db_user.role not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Acesso negado. Apenas administradores podem fazer login.")
    
    # Verifica se a conta está ativa
    if not db_user.is_active:
        raise HTTPException(status_code=403, detail="Conta não está ativa")
    
    return {
        "success": True,
        "message": "Login de administrador realizado com sucesso",
        "user": {
            "id": db_user.id,
            "name": db_user.name,
            "email": db_user.email,
            "role": db_user.role
        }
    }