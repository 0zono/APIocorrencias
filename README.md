# FastAPI

Este repositório contém uma aplicação backend utilizando FastAPI. O projeto faz uso de diversas bibliotecas para funcionalidades adicionais, como autenticação e manipulação de bancos de dados.

## Passo 1: Configuração do Ambiente Virtual

Antes de instalar as dependências do projeto, é recomendado criar um **ambiente virtual** para isolar as bibliotecas e garantir que elas não afetem outros projetos no seu sistema.

### Windows

1. **Instalar o Python**:
   - Certifique-se de que o Python 3.7 ou superior está instalado. Você pode baixá-lo em [python.org](https://www.python.org/downloads/).
   - Durante a instalação, marque a opção "Adicionar Python ao PATH".

2. **Criar o Ambiente Virtual**:
   - Abra o **Prompt de Comando** e navegue até o diretório do projeto:
   
   ```bash
   cd caminho/do/projeto
   python -m venv venv
3. **Ativar o ambiente virtual:**
  - Ative o ambiente virtual com o comando:
    ```bash
    venv\Scripts\activate
  
  ### Linux

1. **Instalar o Python**:
   - A maioria das distribuições Linux já vêm com o Python 3 instalado. Verifique a versão do Python com o comando:
   
   ```bash
   python3 --version

  Se necessário, instale o Python 3.7 ou superior usando o gerenciador de pacotes da sua distribuição, como:
  - No ubuntu/Debian:
    
    ```bash
    sudo apt update
    sudo apt install python3 python3-venv python3-pip

  - No fedora:
    ```bash
    sudo dnf install python3 python3-virtualenv


2. **Criar o ambiente virtual**
   - Abra o Terminal e navegue até o diretório do projeto:
      ```bash
      cd caminho/do/projeto
   - Crie o ambiente virtual com o comando:
       ```bash
      python3 -m venv venv
3. **Ativar o ambiente virtual
   - Ative o ambiente virtual com o comando:
     ```bash
      source venv/bin/activate
    Agora, o prompt de comando deve mudar para indicar que o ambiente virtual está ativo
4. **Com o ambiente virtual ativo, você pode instalar as dependências dentro dele.**
   ```bash
      pip install fastapi passlib sqlalchemy httpx python-multipart







