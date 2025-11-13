# --- Estágio 1: Final (Imagem Segura) ---
FROM python:3.10-alpine

# Cria o usuário não-root
RUN addgroup -g 1002 nonroot-audit && \
    adduser -u 1002 -G nonroot-audit -D -h /app nonroot-audit

WORKDIR /app
COPY app.py .

# Cria o diretório de log e dá permissão
RUN mkdir -p /var/logs/api && \
    chown -R 1002:nonroot-audit /var/logs/api && \
    chown -R 1002:nonroot-audit /app

USER 1002

# Comando corrigido: Apenas 'python3'.
CMD [ "python3", "app.py" ]