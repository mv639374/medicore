# What: This is a production-optimized Dockerfile. It uses a multi-stage build. The first stage (builder) installs dependencies. The second, final stage copies only the installed libraries and our application code, resulting in a smaller, more secure image.
# Why: A smaller image is faster to deploy and has a smaller attack surface. We don't need development tools in our production container, so we leave them out.


# Stage 1: Builder
FROM python:3.9-slim AS Builder

WORKDIR /app

COPY requirements/ ./requirements/

# Install dependencies to a user directory to avoid running as root
RUN pip install --user --no-cache-dir -r requirements/production.txt

# Stage 2: Runtime
FROM python:3.9-slim

WORKDIR /app

# copy installed packages from the builder stage
COPY --from=builder /root/.local /root/.local

# Copy the application code
COPY ./app ./app
COPY ./alembic ./alembic
COPY ./alembic.ini .

# Set the PATH to include the user's local bin directory
ENV PATH=/root/.local/bin:$PATH

# Expost the port on the app runs on
EXPOSE 8000

# The command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
