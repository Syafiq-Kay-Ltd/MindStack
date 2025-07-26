# syntax=docker/dockerfile:1.2

FROM python:3.13-slim-bullseye

# Install system dependencies including git and ssh client
RUN apt-get update && apt-get install -y git ssh curl gnupg apt-transport-https && \
    # Setup Microsoft ODBC repo key
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft-archive-keyring.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-archive-keyring.gpg] https://packages.microsoft.com/debian/11/prod bullseye main" > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev

WORKDIR /app

COPY requirements.txt .

# Use SSH forwarding to allow git clone via SSH in pip
RUN --mount=type=ssh pip install --upgrade pip && pip install -r requirements.txt

COPY . .

CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py makemigrations && python manage.py migrate && gunicorn syafiqkay.wsgi:application --bind 0.0.0.0:8000"]
