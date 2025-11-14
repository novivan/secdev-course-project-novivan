# Build stage
FROM python:3.11-slim AS build
WORKDIR /.
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt
COPY . /
RUN pytest -q

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
RUN useradd -m appuser
COPY --from=build /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=build /usr/local/bin /usr/local/bin
COPY . /
RUN mkdir -p /app/data \
    && chown -R appuser:appuser /app \
    && chmod -R 755 /app
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=5s --timeout=3s --start-period=5s CMD curl -f http://0.0.0.0:8000/ || exit 1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
