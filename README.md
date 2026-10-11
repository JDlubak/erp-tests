# toolshop-tests

## Wymagania
Python 3.10+, uruchomiona aplikacja na Dockerze.

## Instalacja
```
python -m venv .venv
.venv\Scripts\activate          # Windows (PowerShell)
pip install -r requirements.txt
```

## Uruchamianie
```
pytest                  # wszystkie testy
pytest -m api           # tylko API
pytest -m smoke         # tylko testy o wysokim priorytecie
pytest -v               # z nazwami testów
```

## Struktura
- `config.py` adresy i konta
- `api/client.py` klient API
- `tests/api/` testy API
- `tests/conftest.py` wspólne fixtures pytesta
