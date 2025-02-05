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
    ```
    uvicorn main:app --reload
    ```

## Test Project 🧑‍💻

 **Run tests using pytest**:
    ```
    pytest .
    ```

## Alembic Migrations 📜

### Generating Migrations

 **Generate a new migration script**:
    ```
    alembic revision --autogenerate -m "Initial migration"
    ```

### Applying Migrations 

 **Apply migrations to the database**:
    ```
    alembic upgrade head
    ```

## API Endpoints 🎯

**Endpoints for users**
- `POST /user/signup/` - Register a new user
- `POST /user/login/` - User login
- `GET /user/{user_id}` - Retrieving user information
- `PUT /user/{user_id}` - Updating user information
- `DELETE /user/{user_id}` - Deleting a user
**Endpoints for posts**
- `GET /posts/` - Getting the list of posts
- `GET /posts/{post_id}` - Retrieving a post by ID
- `PUT /posts/{post_id}` - Update post
- `DELETE /posts/{post_id}` - Deleting a post
**Endpoints for comments**
- `GET /comments/` - Getting the list of comments
- `POST /comments/{post_id}` - Creating a comment
- `GET /comments-daily-breakdown/` - Getting analytics on comments

## License 📝

This project is licensed under the MIT License.
