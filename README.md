# TaxAssistant
TaxAssistant for HackYeah 2024 


# Installation

- Docker Compose

To use docker version please use docker-compose.yml file in buld directory. Please review contents of arguments and environmental variables especially checking following variables:

- In backend section
-- API_URL=backend - this points to server where api is made visible - this settings replaces configuration of frontend to adapt to proper API source 
-- DJANGO_SUPERUSER_PASSWORD=Yarrl123 - password for admin user created during build
-- DJANGO_SUPERUSER_USERNAME=yarrl - username of admin user created during build
-- DJANGO_SUPERUSER_EMAIL=yarrl@test.com - email of admin user
-- OPENAI_API_KEY=api_key_please_edit - a key to OpenAI service.

- In postgres section
-- POSTGRES_PASSWORD=TaxAssistant123