# FastAPI Project

This is a basic FastAPI project with Docker support.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a .env file:**
    Create a file named `.env` in the root directory of the project and add your OpenAI API key:
    ```
    OPENAI_API_KEY=your_openai_api_key_here
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the application

To run the application locally, use the following command:

```bash
uvicorn app.main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

## Running with Docker

To run the application with Docker, use the following command:

```bash
docker-compose up -d --build
```

The application will be available at `http://localhost:8008`.

## Running tests

To run the tests, use the following command:

```bash
pytest
```
