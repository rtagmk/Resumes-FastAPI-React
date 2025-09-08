# FastAPI+React resume app

[![Tests](https://github.com/rtagmk/Resumes-FastAPI-React/actions/workflows/python-app.yml/badge.svg)](https://github.com/rtagmk/Resumes-FastAPI-React/actions/workflows/python-app.yml)

This is a REST API built with FastAPI for managing resumes. It provides CRUD operations for users and resumes, authentication and authorization using JWT tokens, and data validation.

## Project Description

This API service allows you to manage users and their associated resumes. It provides the following functionality:

*   **User Management:** Create, read, update, and delete user accounts.
*   **Resume Management:** Create, read, update, and delete resumes.
*   **Authentication and Authorization:** Secure access to the API using JWT tokens. Only authenticated users can create, update, and delete resumes, and access is restricted to their own resumes.
*   **Data Validation:** Validate input data to ensure data integrity and prevent errors.

## Technologies Used

*   [Python 3.9+](https://www.python.org/)
*   [FastAPI](https://fastapi.tiangolo.com/) - A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
*   [Pydantic](https://pydantic-docs.github.io/): Data validation and settings management using Python type annotations.
*   [pytest](https://docs.pytest.org/en/7.1.x/): A testing framework for Python.
*   [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/): A pytest plugin for measuring test coverage.
*   [bcrypt](https://pypi.org/project/bcrypt/): For password hashing.
*   [PyJWT](https://pyjwt.readthedocs.io/en/stable/): For creating and verifying JWT tokens.
*   [uvicorn](https://www.uvicorn.org/): ASGI server for running the FastAPI application.
*   [SQLAlchemy](www.sqlalchemy.org) The Python SQL toolkit and Object Relational Mapper.
*   [React](https://react.dev/) - A JavaScript library for building user interfaces.
*   [Vite](https://vitejs.dev/) - A build tool that significantly improves the frontend development experience.
*   [Axios](https://axios-http.com/) - Promise-based HTTP client for browser and Node.js.

---

## Getting Started: Installation and Running the Application

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/rtagmk/Resumes-FastAPI-React.git
    cd Resumes-FastAPI-React
    ```

2.  **Choose your deployment method:**  You can run the application using a traditional Python environment or using Docker Compose (recommended). Choose **one** of the following options:

    ## Option A: Traditional Python Environment (pip)

    *   **Create a virtual environment (recommended):**

        ### On Linux/macOS
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```

        ### On Windows
        ```bash
        python -m venv .venv
        .venv\Scripts\activate
        ```

    *   **Install dependencies:**

        ```bash
        pip install -r requirements.txt
        ```

    *   **Configure environment variables:**

        *   Create a `.env` file by copying and adapting the `.env.example` template.
        *   Define the necessary environment variables within the `.env` file (e.g., `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`). These variables are used by the application and configured in `app/core/config.py`.
        *   Specifically, you'll need to set the connection details for your PostgreSQL database:

            ```
            DB_USER="your_db_user"
            DB_PASSWORD="your_db_password"
            DB_HOST="localhost"  # Typically "localhost" when running locally
            DB_PORT="5432"       # Standard PostgreSQL port
            DB_NAME="resumes"
            ```

            *   **Replace the placeholder values** with the actual credentials for your PostgreSQL database. Ensure PostgreSQL is running and accessible locally.

    *   **Apply database migrations:**

        ```bash
        alembic upgrade head
        ```

    *   **Start the FastAPI application:**

        ```bash
        uvicorn src.main:app --reload
        ```

        This will start the server on [http://localhost:8000](http://localhost:8000).

    ## Option B: Docker Compose (Recommended)

    *   **Ensure Docker and Docker Compose are installed:**

        *   [Install Docker](https://docs.docker.com/get-docker/)
        *   [Install Docker Compose](https://docs.docker.com/compose/install/)

    *   **Configure environment variables:**

        *   Create a `.env` file by copying and adapting the `.env.example` template.
        *   Define the necessary environment variables within the `.env` file (e.g., `SECRET_KEY`, `ACCESS_TOKEN_EXPIRE_MINUTES`). These variables are used by the application and configured in `app/core/config.py`.
        *   Specifically, you'll need to set the connection details for your PostgreSQL database:

            ```
            DB_USER="your_db_user"
            DB_PASSWORD="your_db_password"
            DB_HOST="db"  # 'db' is the name of the Docker service for the database
            DB_PORT="5432"       # Standard PostgreSQL port
            DB_NAME="resumes"
            ```

            *   **Replace the placeholder values** with the actual credentials for your PostgreSQL database. Ensure PostgreSQL is running and accessible locally.

    *   **Start the application using Docker Compose:**

        *   Run the following command:

            ```bash
            docker-compose up --build
            ```

            *   `docker-compose up`:  Starts the services defined in the `docker-compose.yml` file.
            *   `--build`:  Builds any Docker images that are defined in the `docker-compose.yml` file but haven't been built yet, or if the Dockerfile has changed since the last build. This ensures that the application is running with the latest code.

    *   **Access the application:**

        *   Once the Docker containers are running, the application will be accessible at [http://localhost:8000](http://localhost:8000).

3.  **Access the API documentation (for both options):**

    *   Open your web browser and navigate to `http://localhost:8000/docs`. This will display the automatically generated Swagger UI, which you can use to explore and test the API endpoints.

4.  **Web interface to work with api (for both options):**

    *   Open your web browser and navigate to `http://localhost:8000/`. This will display the light web interface to work with api. Register, login and manage user's resumes.


## Automated Testing with GitHub Actions

This project is configured with GitHub Actions to automatically run tests whenever changes are pushed to the repository or a pull request is created. This ensures that the codebase remains stable and that new changes don't introduce regressions.

*   **Continuous Integration (CI):** The tests are executed as part of a continuous integration workflow.
*   **Automatic Execution:**  Whenever you push new code to a branch or create/update a pull request, GitHub Actions will automatically trigger the test suite.
*   **Status Badge:** The current status of the tests is displayed on the main page of the repository using a status badge (see the top of this README). A green badge indicates that all tests have passed successfully, while a red badge indicates that some tests have failed.
*   **Workflow Definition:** The testing workflow is defined in the `.github/workflows/` directory (e.g., `.github/workflows/main.yml`). You can view the details of the workflow and the test results by navigating to the "Actions" tab in the repository.
*   **Peace of mind** Knowing that your tests are running automatically, you're going to be confident in your pushes and merges

## Running local Tests

Before deploying or contributing, it's crucial to run the tests locally to ensure your changes haven't introduced any regressions.  Follow these steps:

1.  Install the necessary dependencies, including pytest and other testing libraries:

    ```bash
    pip install -r requirements_with_tests.txt
    ```

2.  Run the test suite using the `pytest` command:

    ```bash
    pytest
    ```

This will execute all tests located in the `tests` directory.  Make sure your database is properly configured and running before running the tests, or the tests that require database access will fail.  Check the pytest output for any errors or failures.

## API Endpoints

### Users

*   `GET /users/`:  Get a list of all users.
*   `GET /users/{user_id}`:  Get information about a specific user. Requires authentication and ownership.
*   `POST /users/`:  Create a new user.
*   `PUT /users/{user_id}`:  Update information about a user. Requires authentication and ownership.
*   `DELETE /users/{user_id}`:  Delete a user. Requires authentication and ownership.

### Resumes

*   `GET /resumes/`:  Get a list of all resumes. Requires authentication and ownership.
*   `GET /resumes/{resume_id}`:  Get information about a specific resume. Requires authentication and ownership.
*   `POST /resumes/`:  Create a new resume. Requires authentication.
*   `PUT /resumes/{resume_id}`:  Update information about a resume. Requires authentication and ownership.
*   `DELETE /resumes/{resume_id}`:  Delete a resume. Requires authentication and ownership.
*   `POST /resumes/{resume_id}/improve`:  Improve a resume. Requires authentication and ownership.

## Authentication and Authorization

*   Authentication is handled using JWT tokens.
*   Endpoints requiring authentication will require a valid JWT token in the `Authorization` header (e.g., `Authorization: Bearer <token>`).
*   Resume modification endpoints require both authentication and authorization. Users can only modify resumes they own.


## Demonstration Video

![demonstration video](demo.gif)