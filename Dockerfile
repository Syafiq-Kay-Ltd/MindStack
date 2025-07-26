FROM python:3.13-slim-bullseye

# Install system dependencies including git and tools for ODBC driver
RUN apt-get update && apt-get install -y git curl gnupg apt-transport-https msodbcsql18 unixodbc-dev && \
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft-archive-keyring.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-archive-keyring.gpg] https://packages.microsoft.com/debian/11/prod bullseye main" > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project files and requirements.txt
COPY requirements.txt .
COPY . .

# Copy the entrypoint script and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

# Default command to run gunicorn server
CMD ["gunicorn", "syafiqkay.wsgi:application", "--bind", "0.0.0.0:8000"]
