<div align="center">

# 🎬 Site Definitivo

**Aplicação web em Flask para autenticação, gestão de usuários e compartilhamento de vídeos.**

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1.3-000000?style=for-the-badge&logo=flask&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

[Visão Geral](#-visão-geral) • [Funcionalidades](#-funcionalidades) • [Instalação](#-instalação) • [Rotas](#-rotas-da-aplicação) • [Avisos](#-avisos-importantes)

---

</div>

## 📌 Visão Geral

O **Site Definitivo** é uma plataforma web leve desenvolvida em **Flask (Python)** que gerencia contas de usuários e permite a publicação de links de vídeos em um painel compartilhado.

> 💾 **Sem necessidade de banco de dados externo:** Toda a persistência de dados é gerenciada nativamente via arquivos **JSON** estruturados.

---

## ✨ Funcionalidades

- **👤 Autenticação de Usuários:** Cadastro, login e controle de sessão (`flask.session`).
- **🛡️ Segurança de Senha:** Validação de formato (mínimo 8 caracteres e ao menos um número).
- **📹 Dashboard do Usuário:** Inclusão e remoção de links de vídeos em um feed compartilhado.
- **👑 Painel Administrativo (`/admin`):** Listagem, edição completa de credenciais e exclusão de contas.
- **⚡ Feedback Visual:** Mensagens dinâmicas de erro e sucesso diretamente na interface.
- **🚪 Logout Seguro:** Encerramento imediato de sessão ativa.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Função |
| :--- | :---: | :--- |
| **[Python](https://www.python.org/)** | `3.13` | Linguagem principal |
| **[Flask](https://flask.palletsprojects.com/)** | `3.1.3` | Microframework web |
| **[Werkzeug](https://werkzeug.palletsprojects.com/)** | `3.1.8` | Utilitários WSGI e roteamento |
| **[Jinja2](https://jinja.palletsprojects.com/)** | `3.1.6` | Template Engine para renderização HTML |
| **HTML5 / CSS3** | — | Interface do usuário e estilização |
| **JSON** | — | Persistência leve de dados |

---

## 📂 Estrutura do Projeto

```text
Site Definitivo/
├── main.py                 # Ponto de entrada da aplicação
├── views.py                 # Rotas da aplicação (Login, Admin, Dashboard)
├── db/
│   ├── functions.py         # Leitura e escrita nos arquivos JSON
│   ├── cadastros.json        # Base de dados de usuários
│   └── videos.json           # Base de dados de vídeos
├── static/
│   └── styles.css            # Folha de estilos CSS
├── templates/
│   ├── login.html            # Interface de Login
│   ├── cadaster.html         # Interface de Cadastro
│   ├── dashboard.html        # Painel do Usuário
│   ├── admin.html             # Painel Administrativo
│   └── edit_user.html         # Edição de Usuário (Admin)
└── requirements.txt          # Dependências do projeto
