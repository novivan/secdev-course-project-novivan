# SecDev Course Template

Стартовый шаблон для студенческого репозитория (HSE SecDev 2025).

## Быстрый старт
```bash
python3.13 -m venv .venv #версия такая для нормальной работы sqlalchemy
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt
pre-commit install
python -m uvicorn app.main:app --reload
```

## Ритуал перед PR
```bash
ruff check --output-format=github . --fix
black .
isort .
pytest -q
pre-commit run --all-files
```

## Тесты
```bash
pytest -q
```

## CI
В репозитории настроен workflow **CI** (GitHub Actions) — required check для `main`.
Badge добавится автоматически после загрузки шаблона в GitHub.

## Контейнеры
```bash
docker build -t secdev-app .
docker run --rm -p 8000:8000 secdev-app
# или
docker compose up --build
```
Зайти из браузера при запущенном контейнере можно по адресу:
```
http://127.0.0.1:8000/docs
```

## Эндпойнты
- `GET /health` → `{"status": "ok"}`
- `POST /items?name=...` — демо-сущность
- `GET /items/{id}`

## Формат ошибок
Все ошибки — JSON-обёртка:
```json
{
  "error": {"code": "not_found", "message": "item not found"}
}
```

См. также: `SECURITY.md`, `.pre-commit-config.yaml`, `.github/workflows/ci.yml`.

# Для регистрации/авторизации (в рантайме)
перейдите на /auth/register и /auth/login соответственно(добавить в конце url вместо /docs)
