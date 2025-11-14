запустить команду (one-liner) в консоли для локального тестирования:
```
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt -r requirements-dev.txt && mkdir -p EVIDENCE/S06 && pytest -q --junitxml=EVIDENCE/S06/test-report.xml
```
