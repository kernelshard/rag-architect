FROM python:3.11-slim

# avoid writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app:/app/app
ENV DEBIAN_FRONTEND=noninteractive



# set work directory
WORKDIR /app

# system dependencies (if any needed for prometheus or other libs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

# install dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

# copy project
COPY . /app/


# non-root user
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

# --proxy-headers tells Uvicorn to respect certain HTTP
# headers that are set by reverse proxies like X-Forwarded-For, X-Forwarded-Proto
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
