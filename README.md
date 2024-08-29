### Flow Backend
Welcome to the backend of Flow, a Trello-like application built using FastAPI. 
This project is designed for single users to create and manage their boards, lists, and tasks. It’s a highly customizable and extendable project that can be tailored to fit individual needs.

### Features 
* Board Management: Create, update, delete, and view boards.
* List Management: Add, update, delete, and reorder lists within boards.
* Task Management: Add, update, delete, and reorder tasks (cards) within lists.
* Labels: Create, assign, and manage labels for tasks.
* Background Images: Choose or upload background images for boards, stored in S3.
* User Authentication: Secure API endpoints with JWT-based authentication.

### Project Structure

- **`app/`**: Contains the core FastAPI application code.
  - **`crud/`**: Includes files for CRUD (Create, Read, Update, Delete) operations.
  - **`models/`**: Contains database models and SQLModel schemas.
  - **`routers/`**: Defines API routes.
  - **`schemas/`**: Contains Pydantic models for request and response validation.
  - **`services/`**: Implements business logic and service classes.
  - **`tests/`**: Holds unit and integration tests.
  - **`__init__.py`**: Initialization file for the `app` module.
  - **`auth.py`**: Functions related to authentication.
  - **`database.py`**: Configures and connects to the database.
  - **`main.py`**: App and router is configured here.

- **`venv/`**: Virtual environment directory (typically excluded from version control).

- **`.env`**: Contains environment variables.

- **`.gitignore`**: Git ignore file to exclude specific files and directories from version control.

- **`main.py`**: Entry point for the FastAPI application (root level).

- **`requirements.txt`**: Lists Python dependencies for the project.

### Getting Started
#### Prerequisites
* Python 3.12
* PostgreSQL (or any preferred SQL database)

### Installation
1. Clone the repository
```
git clone https://github.com/niranjanblank/flow_backend
cd flow-backend
```
2. Create and activate the virtual environment
```commandline
python -m venv venv
```
3. Install the required dependencies
```commandline
pip install -r requirements.txt
```
4. Set up environment variables by copying the .env.example to .env and updating the values
5. Start the application
```commandline
python main.py
```

### API Documentation
Once the application is running, the interactive API documentation can be accessed at `http://127.0.0.1:8000/docs`

### Running Tests
To run the tests, use the following command:
```commandline
pytest
```