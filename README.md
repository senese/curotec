# Curotec Python Full Stack Assessment

**Full Stack project for Curotec Assessment using Python and React.**

## 🔖 Version requirements:
- Python 3.11
- FastAPI v0.109
- Pytest v7.3.1
- SQLAlchemy v2.0.15
- React 18
- PostgreSQL 15

## 🚀 Quick Start

To run the project, make sure that you have Docker (with Docker Compose embedded) installed and run `docker compose up` on the top-level directory.

## 🧪 Testing
To test the backend, ensure that you have installed all dependencies and activated the virtual environment.

This repository uses Poetry as Dependency Manager, so make sure that you have already installed. If it's not install already, check the [official documentantion](https://python-poetry.org/docs/#installing-with-pipx).

If you're familiar with Poetry, you can use the virtual environement created by it or create one yourself:
`cd backend && python3.11 -m venv .venv`

Still in the `backend` directory, install the dependencies with `poetry install`.

Run the tests:
`pytest` or `poetry run pytest`

## ✅ Best Practices
The project is well structured, so that any external components is dependent of internal ones and not the other way around. For big projects, concepts like Domain Driven Design (DDD) and Clean Architecture has to be taken into consideration. For this repository some simplifications were made. Check the [Controller Explanation](backend/app/controllers/README.md).