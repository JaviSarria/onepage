FROM python:3.14-slim

WORKDIR /app

# Instalar uv
RUN pip install uv

# Copiar primero los ficheros de dependencias
COPY pyproject.toml uv.lock ./

ARG BE_PORT=9910

# Instalar dependencias
RUN uv sync --frozen --no-dev

# Copiar código
COPY . .

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 9910

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${BE_PORT}"]