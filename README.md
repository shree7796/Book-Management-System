# 📚 Intelligent Book Management System (FastAPI + Llama3)

This project implements a modular, testable, and asynchronous prototype of an Intelligent Book Management System. Key features include **JWT-based Role-Based Access Control (RBAC)** and integration with a local **Llama3 AI model** via Ollama for dynamic summary and sentiment analysis.

## 🌟 Key Features

* **Modular Architecture:** Separate layers for API, Services, Database Models, and Configuration.
* **Asynchronous Operations:** All API and database (PostgreSQL) interactions are non-blocking using `asyncio` and `sqlalchemy[asyncio]`.
* **Security:** Mandatory **JWT Authentication** and **Role-Based Access Control (RBAC)** (`admin` vs. `user`).
* **AI Integration:** Use of a local Llama3 model (via **Ollama**) to:
    1.  Generate a summary for newly added books.
    2.  Generate a sentiment summary of user reviews.
* **Mandatory Unit Tests:** Comprehensive unit tests for services, authentication, and API endpoints using `pytest`.
* **Cloud-Ready:** Containerized using **Docker** and **Docker Compose** for easy setup and deployment.

---
## 🗺️ Project Structure

The code is organized into distinct, reusable modules to adhere to the modularity, reusability, and testability requirements.

book_management_system/
├── app/
│   ├── api/                      # FastAPI Routers / Endpoints
│   │   ├── endpoints/            # Auth, Books, Reviews, Recommendations endpoints
│   │   └── dependencies.py       # JWT validation and RBAC checks
│   ├── core/                     # Configuration & Security (config.py, security.py)
│   ├── db/                       # Database session + Base class
│   ├── models/                   # SQLAlchemy ORM models (book, review, user)
│   ├── schemas/                  # Pydantic schemas (validation & serialization)
│   ├── services/                 # Business logic (CRUD, independent of API layer)
│   ├── ai_models/                # LLM client for Llama3 integration
│   └── main.py                   # FastAPI application entry point
├── tests/                        # Unit tests (conftest.py, test_*.py)
├── Dockerfile                    # API service container definition
├── docker-compose.yml            # Multi-service stack (API, DB, Ollama)
├── requirements.txt              # Python dependencies
└── README.md                     # Documentation (this file)

---

## 🛠️ Prerequisites

1.  **Docker & Docker Compose:** Required to run the PostgreSQL database and the Ollama/Llama3 model.
2.  **Ollama:** It is highly recommended to have **Ollama installed on your host system** or set up correctly in the Docker Compose file to download the `llama3` model before running the API.
3.  **Python 3.11+**

---

## ⚙️ Step 1: Project Setup and Configuration

1.  **Clone the Repository:**
    ```bash
    git clone <your-repo-link>
    cd intelligent_book_management_system
    ```

2.  **Create `.env` File:**
    Create a file named `.env` in the root directory to define the necessary environment variables.

    **.env**
    ```
    # FastAPI & JWT
    SECRET_KEY="a_very_secure_secret_key_for_testing"
    API_V1_STR="/api/v1"

    # Postgres Database (using service name 'db' from docker-compose)
    POSTGRES_USER=myuser
    POSTGRES_PASSWORD=mypassword
    POSTGRES_DB=book_db
    POSTGRES_SERVER=db 

    # LLM Configuration (using service name 'ollama' from docker-compose)
    LLM_BASE_URL=http://ollama:11434
    LLM_MODEL_NAME=llama3 
    ```

---

## 🚀 Step 2: Running the Application (Docker Compose)

The entire application stack (API, PostgreSQL, and Ollama/Llama3) is managed via `docker-compose.yml`.

1.  **Build and Run Services:**
    Use the following command to build the API image, pull PostgreSQL/Ollama images, and start all services in detached mode (`-d`). This ensures the API waits for the database and Ollama to be available.
    ```bash
    docker-compose up --build -d
    ```

2.  **Verify Services:**
    Check the status of your containers. They should all show a healthy status, especially `db` and `api`.
    ```bash
    docker-compose ps
    ```

3.  **Access the API:**
    The API service is accessible on port `8000`.

---

## 🌐 Step 3: Accessing Documentation and Testing Authentication

**Documentation (Mandatory Requirement)**

* **Swagger UI (Interactive API Docs):**
    ```
    http://localhost:8000/docs
    ```
    (Use this to interact with all endpoints.)
* **ReDoc Documentation:**
    ```
    http://localhost:8000/redoc
    ```

**Testing JWT Authentication**

1.  **Register a User:** Use the `POST /api/v1/auth/register` endpoint in Swagger UI.
    * Example: `admin@example.com` / `strongpassword` (Role defaults to `user`).
2.  **Login and Get Token:** Use the `POST /api/v1/auth/login` endpoint (using form data).
    * Copy the resulting **`access_token`**.
3.  **Authorize:** Click the green **"Authorize"** button at the top of the Swagger UI and paste the token in the format: `Bearer <token>`.
4.  **Test RBAC:** Attempt to use an **Admin Only** endpoint (e.g., `POST /api/v1/books`). It should fail if you registered as a default `user`.

---

## ✅ Step 4: Running Mandatory Unit Tests

Unit tests are crucial and cover services, authentication, and core API logic.

1.  **Install Test Dependencies (locally):**
    Ensure you have `pytest`, `pytest-asyncio`, and `httpx` installed in your Python environment.
    ```bash
    pip install -r requirements.txt 
    ```
    (Note: If you run tests outside Docker, ensure the test database logic in `conftest.py` is respected.)

2.  **Execute Tests:**
    Run `pytest` from the root directory. The tests are configured to use an isolated in-memory SQLite database, guaranteeing consistency and independence.
    ```bash
    pytest tests/
    ```
