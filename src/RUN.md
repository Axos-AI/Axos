in server dir:
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
celery -A src.core.async_worker worker --loglevel=info --pool=threads

create venv:
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
