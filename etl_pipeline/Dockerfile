FROM python:3.11-slim

COPY . /etl_pipeline/

WORKDIR /etl_pipeline

RUN apt-get update \
    && apt-get install -y curl gnupg2 unixodbc-dev \
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && curl https://packages.microsoft.com/config/debian/12/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql18

RUN pip install -r requirements.txt

CMD ["python","main.py"]