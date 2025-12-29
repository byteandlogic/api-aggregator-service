from fastapi import FastAPI, HTTPException
from app.cache import TTLCache
from pydantic import BaseModel
from typing import Optional
import requests

app = FastAPI(title="API Aggregator Service")
country_cache = TTLCache(ttl_seconds=3600)
class CountryResponse(BaseModel):
    code: str
    name: Optional[str] = None
    capital: Optional[str] = None
    region: Optional[str] = None
    population: Optional[int] = None
    source: str
    cached: bool


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/country/{code}", response_model=CountryResponse)
def country_by_code(code: str):
    code = code.strip().lower()
    url = f"https://restcountries.com/v3.1/alpha/{code}"
    cache_key = f"country:{code}"
    cached = country_cache.get(cache_key)
    if cached is not None:
        cached_copy = dict(cached)
        cached_copy["cached"] = True
        return cached_copy

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

    result = {
        "code": code.upper(),
        "name": (c.get("name") or {}).get("common"),
        "capital": (c.get("capital") or [None])[0],
        "region": c.get("region"),
        "population": c.get("population"),
        "source": "REST Countries",
        "cached": False,
    }
    country_cache.set(cache_key, result)
    return result

