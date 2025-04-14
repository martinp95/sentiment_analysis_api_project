# 🧠 Sentiment Analysis API

![Tests](https://github.com/martinp95/sentiment_analysis_api_project/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/martinp95/sentiment_analysis_api_project/graph/badge.svg?token=JXLM4P5IYL)](https://codecov.io/gh/martinp95/sentiment_analysis_api_project)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
[![License](https://img.shields.io/github/license/martinp95/sentiment_analysis_api_project.svg)](https://github.com/martinp95/sentiment_analysis_api_project/blob/main/LICENSE)

A FastAPI-based REST API for performing sentiment analysis on user reviews, storing results in MongoDB, and providing statistical insights per product.

---

## 📚 Project Overview

This project offers a clean, production-grade sentiment analysis API using modern Python tooling and design principles:

- ⚙️ **FastAPI** for performant async API
- 🧠 **Transformers (DistilBERT)** for pre-trained NLP
- 🧪 **Pytest with full E2E tests**, mocking with `unittest.mock`
- 🧱 **MongoDB** as data store, abstracted via repository pattern
- 🔐 **API Key security layer**
- 🏗️ **Factory pattern** and **context-based configuration**
- 🚀 **CI/CD**, **coverage reports**, **pre-commit hooks**

---

## 📦 Features

- ✅ Analyze sentiment of review texts (`positive`, `neutral`, `negative`)
- 📈 Return aggregated statistics per `product_id`
- 💾 Store classified reviews in MongoDB
- 🔐 Secure endpoints with API Key header
- 🧪 Robust unit + end-to-end testing strategy
- 🧹 Linting, formatting, typing, security checks
- 📦 Docker-ready and CI/CD enabled via GitHub Actions

---

## 🧠 Architecture Highlights

### 🔧 Design Patterns and Structure

- **Factory Pattern** via `app.core.context` to centralize configuration access (settings, DB)
- **Repository Pattern** for MongoDB access, keeping logic independent of persistence
- **Service Layer** in `app.services` encapsulates business rules (aggregation, validation, etc.)
- **Modular structure** with clear domain boundaries: `api/`, `models/`, `db/`, `services/`

### 🧪 Testing

- **Unit and E2E tests** with `pytest`, full mocking with `AsyncMock` and custom async cursors
- **Real server testing** using `multiprocessing.Process` to boot Uvicorn and `httpx.AsyncClient`
- **Test isolation**: mocks MongoDB and environment settings per test
- **Custom test utilities** (e.g., `get_open_port`, `wait_for_port`) to handle async server boot

---

## 📁 Project Structure

```
sentiment_analysis_api_project/
├── LICENSE
├── Makefile
├── README.md
├── app
│   ├── __init__.py
│   ├── api
│   │   ├── health.py
│   │   ├── sentiment.py
│   │   └── stats.py
│   ├── core
│   │   ├── config.py
│   │   ├── context.py
│   │   ├── exceptions.py
│   │   ├── logger.py
│   │   └── security.py
│   ├── db
│   │   └── mongo.py
│   ├── main.py
│   ├── models
│   │   ├── health.py
│   │   ├── review.py
│   │   └── stats.py
│   ├── repositories
│   │   ├── review_repository.py
│   │   └── stats_repository.py
│   └── services
│       ├── sentiment.py
│       └── stats.py
├── codecov.yml
├── docker
│   ├── Dockerfile
│   └── docker-compose.yaml
├── pyproject.toml
├── requirements-dev.txt
├── requirements.txt
└── tests
    ├── __init__.py
    ├── api
    │   ├── test_health.py
    │   └── test_stats.py
    └── utils.py
```
---

## 🔧 Setup & Usage

### 🔸 1. Clone the repository

```bash
git clone https://github.com/martinp95/sentiment_analysis_api_project.git
cd sentiment_analysis_api_project
```

### 🔸 2. Setup env

```bash
cp .env.example .env
```

Edit to fit your MongoDB URI and API Key:

```
# MongoDB settings
MONGO_URI=mongodb://admin:admin123@mongo:27017
DB_NAME=sentimentdb

# API security settings
API_KEY=secret123

# ML model
MODEL_NAME=distilbert-base-uncased-finetuned-sst-2-english

# Logging settings
# Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=DEBUG
```
### 🔸 3. Start the app with Docker
```bash
make build
make up
```
This will build and run the app using `docker-compose`.

- ✅ API Base: [http://localhost:8080/health](http://localhost:8080/health)
- ✅ Swagger UI: [http://localhost:8080/docs](http://localhost:8080/docs)

## 📚 API Endpoints (Sample)

### ✅ GET `/health`
Ensure de app is running by health check

```json
{"status": "healthy"}
```

### 🔍 POST `/reviews/sentiment`
Analyze the sentiment of a product review and store the result in the database.

Header:
```
X-API-Key: your_api_key
```

Body:
```json
{
    "review": "Great product, really love it!",
    "product_id": "SKU-98765"
}
```

Response:
```json
{
  "sentiment": "positive",
  "confidence": 1
}
```

### 📊 GET /reviews/stats/{product_id}

Return stats for a product.

Header:
```
X-API-Key: your_api_key
```

Response:

```json
{
  "product_id": "SKU-98765",
  "positive": 0.75,
  "neutral": 0.25,
  "negative": 0.0
}
```

## 🧪 Running Tests

### 🔹 Run all tests

```bash
make test
```

### 🔹 Run coverage

```bash
make coverage
```

Coverage report is also available in `htmlcov/index.html`.

---

## 🧹 Code Quality

Run pre-commit on all files
```bash
make precommit
````
Security scans:
```bash
make security
```
---

## 🚀 CI/CD & Coverage
- GitHub Actions runs `make ci` on every push to `main`

- Codecov publishes coverage from `coverage.xml`

- Pre-commit hooks auto-run formatting and lint checks before commit


## 🧪 Testing Philosophy
- End-to-end tests run against live HTTP endpoints

- MongoDB is mocked using `AsyncMock` + custom cursor (`AsyncCursorMock`)

- No external dependency is needed to run tests (Mongo is patched)

- Ports are dynamically allocated using `get_open_port()` and `wait_for_port()`
---

## 🛠 Makefile Commands

```bash
  build                Build Docker containers
  ci                   Run full CI check locally
  clean                Clean cache, coverage, pyc files
  coverage             Run test suite with coverage reports (html, xml, terminal)
  down                 Stop Docker containers
  help                 Show this help message
  install              Install dev requirements
  precommit            Run pre-commit hooks on all files
  restart              Restart Docker containers
  security             Run static security checks (safety + bandit)
  test                 Run all test with verbose output
  up                   Start Docker containers
  ```

  ## 🐍 Dependencies

Install with:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For testing & development
```

---

## 🔍 Swagger API Docs

Accessible without authentication at:

```
http://localhost:8080/docs/
```
---

## 👥 Author
Maintained by [@martinp95](https://github.com/martinp95) – built with ❤️ and caffeine ☕️.

---

## 📝 License

Licensed under the [MIT License](LICENSE).