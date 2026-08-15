# Build Stage
FROM python:3.11-slim AS build

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Run Stage
FROM python:3.11-slim

WORKDIR /app

COPY --from=build /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY backend/ ./backend/
WORKDIR /app/backend

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]</arg_value>
