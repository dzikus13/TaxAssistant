# TaxAssistant
TaxAssistant for HackYeah 2024 


# Installation

## Docker Compose

To use docker version please use docker-compose.yml file in buld directory. Please review contents of arguments and environmental variables especially checking following variables:

- In backend section
-- API_URL=backend - this points to server where api is made visible - this settings replaces configuration of frontend to adapt to proper API source 
-- DJANGO_SUPERUSER_PASSWORD=Yarrl123 - password for admin user created during build
-- DJANGO_SUPERUSER_USERNAME=yarrl - username of admin user created during build
-- DJANGO_SUPERUSER_EMAIL=yarrl@test.com - email of admin user
-- OPENAI_API_KEY=api_key_please_edit - a key to OpenAI service.

- In postgres section
-- POSTGRES_PASSWORD=TaxAssistant123



## Local deployment

Please ensure that you have postgresql database installed locally and configured for access. To be able to access database you have to create it according to `DATABASES` setting in `src/tax_assistant/tax_assistant/settings/__init__.py`. Either change settings or create database and connecting user according to configuration.

Clone repository in convienient location and:

`cd TaxAssistant/src/tax_assistant`

`virtualenv tax_venv`

`. tax_env/bin/activate`

Note: you can use alternafive virtualenv management tools

`python manage.py migrate`

`pyhton manage.py loaddata sample`

`pyhton manage.py createsuperuser` - this creates admin user.

`python scripts/clean_url.py localhost:8000`

Go to: `localhost:8000` to see application or `localhost:8000/admin/` to login as superuser


## Important configuration details

Table `TaxForm` contain full configuration of PCC-3 form.
This configuration include:

- `metadata` - json containing description of all important fields in for with translations of names
- `system_prompt` - this is a text that is added as system prompt to every chatgpt request
- `xml_template` - this is template in Django internal templating language (similiar to Jinja) - allows for final template creation. Full language description is available here: https://docs.djangoproject.com/en/5.1/ref/templates/language/
In context only variables defined in metadata setup are allowed.
