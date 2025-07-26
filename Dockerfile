# Use a Debian base image compatible with Microsoft ODBC 18 driver
FROM python:3.13-slim-bullseye

# Install system dependencies and ODBC 18 driver with updated key handling
RUN apt-get update && \
    apt-get install -y curl gnupg apt-transport-https && \
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc -o /usr/share/keyrings/microsoft.gpg && \
    curl -fsSL https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    sed -i 's|deb https://packages.microsoft.com|deb [signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com|g' /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev

# Set workdir
WORKDIR /app

# Install git (needed for pip to install git repos)
RUN apt-get update && apt-get install -y git

# Copy requirements and install python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Collect static files, run migrations, and start server
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py makemigrations && python manage.py migrate && gunicorn syafiqkay.wsgi:application --bind 0.0.0.0:8000"]
