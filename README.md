# Site Web

Um sistema web interativo desenvolvido em Python para gerenciamento e cadastro de dados.

---

## Tecnologias Utilizadas

* **Linguagem:** Python
* **Framework Web:** Flask (ou módulo utilizado em `app.py`)
* **Armazenamento:** JSON (`cadastros.json`)
* **Frontend:** HTML5, CSS3, JavaScript

---

## Passo a Passo: Como Rodar o Projeto

Siga estas etapas no terminal do VS Code para executar o projeto na sua máquina:

### 1️⃣ Criar o ambiente virtual (`.venv`)
```bash
python -m venv .venv
```
###  2️⃣ Ativar o ambiente virtual
Windows (PowerShell / VS Code):

PowerShell
```bash
.\.venv\Scripts\Activate.ps1

(Se der erro de permissão no PowerShell, rode antes:
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass)
```

###  3️⃣ Instalar as dependências
```bash
pip install -r requirements.txt
```

###  4️⃣ Executar a aplicação
```bash
python app.py
```

---

## Estrutura do Projeto

```text
Site-WEB/
|── templates/          # Arquivos HTML da aplicação
├── app.py              # Script principal e rotas da aplicação
├── functions.py        # Funções auxiliares e lógica de negócios
├── cadastros.json      # Base de dados local em formato JSON
└── README.md           # Documentação do projeto

