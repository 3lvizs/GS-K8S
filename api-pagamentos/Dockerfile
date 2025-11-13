# --- Estágio 1: Builder ---
FROM python:3.10-slim-bookworm as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Estágio 2: Final (Imagem Segura) ---
FROM python:3.10-alpine

# Cria o usuário não-root
RUN addgroup -g 1001 nonroot && \
    adduser -u 1001 -G nonroot -D -h /app nonroot

WORKDIR /app
COPY app.py .
# Copia APENAS as bibliotecas, não os binários
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# Cria o diretório de log e dá permissão
RUN mkdir -p /var/logs/api && \
    chown -R 1001:nonroot /var/logs/api && \
    chown -R 1001:nonroot /app

USER 1001
EXPOSE 8081

# Comando corrigido: Apenas 'python3'. O Alpine sabe onde encontrar.
CMD [ "python3", "app.py" ]