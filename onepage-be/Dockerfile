FROM python:3.14-slim

WORKDIR /app

# Instalar uv
RUN pip install uv

# Copiar primero los ficheros de dependencias
COPY pyproject.toml uv.lock ./

# Instalar dependencias
RUN uv sync --frozen --no-dev

# Copiar código
COPY . .

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]