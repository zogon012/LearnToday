# 📝 Todo List Backend API

A simple and modern Todo List backend built with **FastAPI** and **SQLAlchemy**.  
Easily manage your todos with a clean RESTful API.

---

## 🚀 Features

- Create, read, update, and delete todos
- Mark todos as done or undone
- Fast and async API with FastAPI
- PostgreSQL database support
- Streamlit frontend included

---

## 📦 Project Structure

```
.
├── app/
│   ├── main.py          # FastAPI entrypoint
│   ├── models.py        # SQLAlchemy models
│   ├── crud.py          # Database CRUD logic
│   ├── schemas.py       # Pydantic schemas
│   ├── routers/
│   │   └── todo.py      # Todo API endpoints
│   └── streamlit_app.py # Streamlit frontend
├── alembic/             # Database migrations
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🛠️ Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the server

```bash
uvicorn app.main:app --reload
```

### 3. Health Check

Visit [http://localhost:8000/health](http://localhost:8000/health)  
You should see:  
```json
{"status": "ok"}
```

---

## 📚 API Endpoints

| Method | Endpoint           | Description            |
|--------|--------------------|------------------------|
| GET    | /todos/            | List all todos         |
| POST   | /todos/            | Create a new todo      |
| GET    | /todos/{todo_id}   | Get a specific todo    |
| PUT    | /todos/{todo_id}   | Update a todo          |
| DELETE | /todos/{todo_id}   | Delete a todo          |
| GET    | /health            | Health check           |

---

## 🖥️ Frontend

A beautiful Streamlit frontend is included!  
To run it:

```bash
streamlit run app/streamlit_app.py
```

---

## 📝 License

This project is licensed under the MIT License.
