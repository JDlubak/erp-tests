# erp-tests

## Wymagania
Python 3.10+, uruchomiona aplikacja na Dockerze.

## Instalacja
```
python -m venv .venv
.venv\Scripts\activate          # Windows (PowerShell)
pip install -r requirements.txt
playwright install chromium     # potrzebne dla scenariuszy UI
```

## Uruchamianie
```
pytest                  # wszystkie testy
pytest -m api           # tylko API
pytest -m ui            # tylko UI
pytest -m smoke         # tylko testy o wysokim priorytecie
pytest -m bdd           # tylko BDD
pytest -v               # z nazwami testów
```

## Struktura
- `config.py` adresy i konta
- `api/client.py` klient API
- `tests/api/` testy API
- `tests/conftest.py` wspólne fixtures pytesta
