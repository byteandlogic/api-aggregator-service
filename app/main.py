from fastapi import FastAPI, HTTPException
import requests

app = FastAPI(title="API Aggregator Service")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/country/{code}")
def country_by_code(code: str):
    code = code.strip().lower()
    url = f"https://restcountries.com/v3.1/alpha/{code}"

    try:
        resp = requests.get(url, timeout=10)
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Upstream request failed: {e}")

    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail="Country not found")
    if resp.status_code >= 400:
        raise HTTPException(status_code=502, detail=f"Upstream error: {resp.status_code}")

    data = resp.json()
    if not isinstance(data, list) or not data:
        raise HTTPException(status_code=502, detail="Unexpected upstream response format")

    c = data[0]

    return {
        "code": code.upper(),
        "name": (c.get("name") or {}).get("common"),
        "capital": (c.get("capital") or [None])[0],
        "region": c.get("region"),
        "population": c.get("population"),
        "source": "REST Countries",
    }
