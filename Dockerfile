# Use a Debian base image compatible with Microsoft ODBC 18 driver
FROM python:3.13-slim-bullseye

# Install system dependencies and ODBC 18 driver
RUN apt-get update && \
    ACCEPT_EULA=Y apt-get install -y curl gnupg apt-transport-https && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev

# Set workdir
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Collect static files, run migrations, and start server
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py makemigrations && python manage.py migrate && gunicorn syafiqkay.wsgi:application --bind 0.0.0.0:8000"]