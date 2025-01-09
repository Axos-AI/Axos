# Development Setup

## Run the API

```bash
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
```

## Run the Celery Worker

```bash
celery -A src.core.async_worker worker --loglevel=info --pool=threads
```

## Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Export Environment Variables

```bash
source export_env.sh
```
