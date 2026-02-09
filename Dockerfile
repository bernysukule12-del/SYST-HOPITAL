FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get update && apt-get install -y build-essential libpq-dev netcat && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /code/

RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /code
USER appuser

# collect static (may fail in dev builds if settings not configured; ignore)
RUN python manage.py collectstatic --noinput || true

ENTRYPOINT ["/code/entrypoint.sh"]
CMD ["gunicorn", "hospital_api.wsgi:application", "--bind", "0.0.0.0:8000"]
