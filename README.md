# FastAPI Project 🚀

This project is a simple API for managing posts and comments with AI moderation and automatic responses. It is built with FastAPI and Pydantic.

## Project Structure 📂

- `alembic/` - Alembic migration scripts
- `db/` - Database configurations and models
- `post/` - Post-related models, schemas, and routers
- `user/` - User-related models, schemas, and routers
- `tests/` - Test cases
- `main.py` - Main entry point of the application
- `requirements.txt` - Project dependencies

## Getting Started 🏁

### Prerequisites

- Python 3.8+
- SQLite

### Installation Steps

1. **Clone the repository**:
    ```bash
    git clone https://github.com/VitalyBashkiser/Test_Task_Fast-API.git
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database**:
    ```bash
    alembic upgrade head
    ```

### Running the Application

 **Start the FastAPI server**:
    ```bash
    uvicorn main:app --reload
    ```

## Test Project 🧑‍💻

 **Run tests using pytest**:
    ```bash
    pytest
    ```

## Alembic Migrations 📜

### Generating Migrations

 **Generate a new migration script**:
    ```bash
    alembic revision --autogenerate -m "Initial migration"
    ```

### Applying Migrations 

 **Apply migrations to the database**:
    ```bash
    alembic upgrade head
    ```

## API Endpoints 🎯

- `POST /register/` - Register a new user
- `POST /login/` - User login
- `POST /create/` - Create a new post

## License 📝

This project is licensed under the MIT License.
