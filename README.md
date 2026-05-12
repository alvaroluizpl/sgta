# SGTA — Sistema de Gerenciamento de Tarefas Acadêmicas

API REST desenvolvida em Django para gerenciar tarefas acadêmicas e os usuários responsáveis por elas. O sistema permite cadastrar tarefas com status, prioridade e prazo de entrega, além de filtrar e buscar tarefas de diversas formas.

---

## Tecnologias utilizadas

- Python 3.x
- Django 6.0.3
- Django REST Framework 3.17.0
- SQLite (banco de dados local para desenvolvimento)

---

## Estrutura do projeto

```
sgta/
├── backend/
│   ├── config/          # Configurações do projeto Django (settings, urls, wsgi)
│   ├── tarefas/         # App de tarefas (model, views, urls)
│   ├── usuarios/        # App de usuários (model, views, urls)
│   ├── manage.py
│   └── requirements.txt
└── docker-compose.yml
```

---

## Como executar localmente

**1. Acesse a pasta do backend:**
```bash
cd backend
```

**2. Crie e ative o ambiente virtual:**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

**3. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**4. Aplique as migrations (cria o banco de dados):**
```bash
python manage.py migrate
```

**5. Inicie o servidor:**
```bash
python manage.py runserver
```

A API estará disponível em `http://127.0.0.1:8000/`.

---

## Modelos

### Usuário

| Campo         | Tipo       | Descrição                        |
|---------------|------------|----------------------------------|
| `id`          | inteiro    | Identificador único (automático) |
| `nome`        | texto      | Nome completo do usuário         |
| `email`       | e-mail     | E-mail único do usuário          |
| `ativo`       | booleano   | Se o usuário está ativo          |
| `data_criacao`| data/hora  | Preenchido automaticamente       |

### Tarefa

| Campo                  | Tipo      | Descrição                                                    |
|------------------------|-----------|--------------------------------------------------------------|
| `id`                   | inteiro   | Identificador único (automático)                             |
| `titulo`               | texto     | Título da tarefa                                             |
| `descricao`            | texto     | Descrição detalhada                                          |
| `status`               | escolha   | `ABERTA`, `EM_ANDAMENTO`, `CONCLUIDA` ou `CANCELADA`         |
| `prioridade`           | escolha   | `URGENTE` ou `NAO_URGENTE`                                   |
| `data_criacao`         | data/hora | Preenchida automaticamente                                   |
| `data_entrega`         | data      | Prazo de entrega da tarefa                                   |
| `usuario_responsavel`  | FK        | Usuário responsável (pode ser nulo)                          |

---

## Endpoints

### Tarefas

| Método | URL | Descrição |
|--------|-----|-----------|
| GET | `/tarefas/` | Lista todas as tarefas |
| GET | `/tarefas/<id>/` | Retorna uma tarefa pelo ID |
| GET | `/tarefas/status/<status>/` | Filtra tarefas por status |
| GET | `/tarefas/prioridade/<prioridade>/` | Filtra tarefas por prioridade |
| GET | `/tarefas/filtro/<status>/<prioridade>/` | Filtra por status e prioridade combinados |
| GET | `/tarefas/atrasadas/` | Lista tarefas com prazo vencido e não concluídas |
| GET | `/tarefas/busca/<termo>/` | Busca tarefas pelo título (parcial, sem distinção de maiúsculas) |

**Valores válidos para `status`:** `ABERTA`, `EM_ANDAMENTO`, `CONCLUIDA`, `CANCELADA`

**Valores válidos para `prioridade`:** `URGENTE`, `NAO_URGENTE`

**Exemplo de resposta — `/tarefas/`:**
```json
[
  {
    "id": 1,
    "titulo": "Prova de Algoritmos",
    "descricao": "Revisão dos conteúdos do semestre",
    "status": "ABERTA",
    "prioridade": "URGENTE",
    "data_criacao": "2026-03-23T14:08:26.752Z",
    "data_entrega": "2026-04-30",
    "usuario_responsavel": "Alvaro"
  }
]
```

**Exemplo de resposta — tarefa não encontrada:**
```json
{
  "erro": "Tarefa não encontrada."
}
```

---

### Usuários

| Método | URL | Descrição |
|--------|-----|-----------|
| GET | `/usuarios/` | Lista todos os usuários |
| GET | `/usuarios/<id>/` | Retorna um usuário pelo ID |

**Exemplo de resposta — `/usuarios/`:**
```json
[
  {
    "id": 1,
    "nome": "Alvaro",
    "email": "alvaro@email.com",
    "ativo": true,
    "data_criacao": "2026-03-20T10:00:00.000Z"
  }
]
```

---

## Observações

- O banco de dados padrão é **SQLite**, armazenado no arquivo `backend/db.sqlite3`. É ideal para desenvolvimento e testes locais.
- O campo `usuario_responsavel` nas respostas de tarefas exibe o **nome** do usuário, não o ID.
- Tarefas marcadas como `CONCLUIDA` não aparecem na listagem de tarefas atrasadas, mesmo que o prazo tenha vencido.

