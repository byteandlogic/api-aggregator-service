![CI](https://github.com/byteandlogic/api-aggregator-service/actions/workflows/ci.yml/badge.svg)

# API Aggregator Service

A small FastAPI service that aggregates and normalizes responses from public APIs. Built with tests and CI to demonstrate production-style engineering practices.

## Features
- Health endpoint: `GET /health`
- Aggregation endpoint: `GET /country/{code}` (REST Countries)
- Normalized JSON response (consistent fields)
- Unit tests with mocked upstream calls
- GitHub Actions CI on every push / pull request
- In-memory TTL caching to reduce upstream API calls

## Tech Stack
- Python, FastAPI
- pytest
- GitHub Actions (CI)

## Getting Started (Local)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

## Run with Docker
```bash
docker build -t api-aggregator-service .
docker run -p 8000:8000 api-aggregator-service
