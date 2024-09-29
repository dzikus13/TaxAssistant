FROM python:3.10-bookworm

ARG API_URL
ARG DJANGO_SUPERUSER_PASSWORD
ARG DJANGO_SUPERUSER_USERNAME
ARG DJANGO_SUPERUSER_EMAIL
ARG OPENAI_API_KEY

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV OPENAI_API_KEY=${OPENAI_API_KEY}} 
WORKDIR /app

RUN apt update && apt install -y --no-install-recommends python3-lxml postgresql-client sqlite3 

RUN pip install --upgrade pip setuptools wheel

# ADD requirements.txt requirements.txt


ADD tax_assistant /app
RUN pip install --requirement requirements.txt

RUN chmod u+x manage.py
RUN python scripts/clean_url.py ${API_URL}
RUN python manage.py collectstatic --noinput
CMD ['manage.py', 'migrate', '--settings=tax_assistant.settings.docker']
CMD ['manage.py', 'loaddata', 'sample', '--settings=tax_assistant.settings.docker']
CMD ['manage.py', 'createsuperuser', '--noinput', '--settings=tax_assistant.settings.docker']
ENTRYPOINT ["/app/scripts/run_app_prod.sh"]
