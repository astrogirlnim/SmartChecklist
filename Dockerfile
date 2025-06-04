FROM --platform=linux/amd64 python:3.10-alpine

WORKDIR /app

# Install bash and build dependencies
RUN apk add --no-cache bash
RUN pip install waitress build

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# Make the script executable and run it
RUN chmod +x sync_and_build.sh && ./sync_and_build.sh

RUN pip install dist/*.whl

# Create volume for database persistence
VOLUME ["/app/instance"]

# Ensure the instance directory exists with proper permissions
RUN mkdir -p /app/instance && chmod 755 /app/instance

CMD ["waitress-serve", "--port", "5000","--call", "smartchecklist:create_app"]

