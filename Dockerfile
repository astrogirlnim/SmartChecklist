FROM python:3.10-alpine

WORKDIR /app

RUN pip install waitress

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN ./sync_and_build.sh

RUN pip install dist/*.whl

# Create volume for database persistence
VOLUME ["/app/instance"]

# Ensure the instance directory exists with proper permissions
RUN mkdir -p /app/instance && chmod 755 /app/instance

CMD ["waitress-serve", "--port", "5000","--call", "smartchecklist:create_app()"]

