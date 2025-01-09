OLD

uvicorn app:app
python celery_worker.py
npm run dev
celery -A celery_worker beat --loglevel=info
redis-server

NEW
in server dir:
uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
celery -A src.core.celery_worker worker --loglevel=info --pool=threads

<!-- celery -A src.core.celery_worker beat --loglevel=info -->

in /frontend dir:
npm run dev
