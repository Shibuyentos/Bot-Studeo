FROM python:3.11-slim

WORKDIR /app

# Dependências
COPY pyproject.toml .
RUN pip install --no-cache-dir .

# Código fonte
COPY src/ src/

# Diretórios de dados
RUN mkdir -p data/materials

CMD ["python", "-m", "src.main"]
