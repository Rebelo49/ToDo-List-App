# ✅ To-Do List App

> App de gestão de tarefas com interface web, desenvolvida em Python puro — sem dependências externas.

![Python](https://img.shields.io/badge/Python-3.6+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![HTML](https://img.shields.io/badge/HTML5-Interface-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Concluído-7c6af7?style=for-the-badge)

---

## 📸 Preview

> _Adiciona aqui um screenshot da app (arrasta a imagem para esta pasta e substitui o caminho abaixo)_

![Preview da App](screenshot.png)

---

## 🚀 Funcionalidades

- ✅ **Criar tarefas** com título e categoria
- 🏷️ **5 categorias** com cores distintas — Pessoal, Trabalho, Estudo, Saúde, Outro
- ✔️ **Marcar como concluída** (e desfazer)
- ✏️ **Editar** o título de qualquer tarefa
- 🗑️ **Apagar** com confirmação
- 🔍 **Pesquisa** em tempo real
- 🎛️ **Filtros** por categoria e por estado
- 📊 **Estatísticas** — concluídas, pendentes e total
- 💾 **Persistência** em JSON — os dados são guardados entre sessões
- 🌐 **Interface web** — abre automaticamente no browser

---

## 🛠️ Tecnologias

| Tecnologia | Utilização |
|---|---|
| Python 3 | Lógica da aplicação e servidor HTTP |
| HTML + CSS + JS | Interface web (dark mode) |
| JSON | Persistência de dados |
| `http.server` | Servidor local nativo do Python |

> Sem instalação de bibliotecas externas — corre com o Python padrão.

---

## ⚡ Como executar

### Pré-requisitos
- Python 3.6 ou superior

### Passos

```bash
# 1. Clona o repositório
git clone https://github.com/Rebelo49/todo-list-app.git
cd todo-list-app

# 2. Corre a app
python3 todo_app.py
```

O browser abre automaticamente em `http://localhost:8765` 🎉

Para parar a app: **Ctrl + C** no terminal.

---

## 🗂️ Estrutura do projeto

```
todo-list-app/
├── todo_app.py     # Servidor HTTP + interface web
├── tasks.json      # Dados guardados (criado automaticamente)
└── README.md
```

---

## 👤 Autor

**Pedro Rebelo**
- GitHub: [@Rebelo49](https://github.com/Rebelo49)

---

## 📄 Licença

Pedro Rebelo © 2026 
