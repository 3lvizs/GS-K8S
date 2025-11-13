import os
from flask import Flask, request, jsonify
import logging
from logging.handlers import RotatingFileHandler

# Pega o saldo do ConfigMap (injetado como variável de ambiente)
RESERVA_BANCARIA_SALDO = float(os.environ.get('RESERVA_BANCARIA_SALDO', 0.0))

# Configura o "Livro-Razão"
LOG_FILE = '/var/logs/api/instrucoes.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
# Usar um manipulador de arquivo
logger = logging.getLogger('api-pagamentos')
handler = RotatingFileHandler(LOG_FILE, maxBytes=100000, backupCount=5)
handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logger.addHandler(handler)
logger.propagate = False # Evita duplicar logs no stdout

app = Flask(__name__)

@app.route('/health')
def health_check():
    """Verifica se a API está online."""
    return jsonify({"status": "UP", "saldo_reserva": RESERVA_BANCARIA_SALDO}), 200

@app.route('/pix', methods=['POST'])
def processar_pix():
    """Simula o recebimento de um PIX."""
    data = request.json
    valor_pix = float(data.get('valor', 0.0))
    
    if valor_pix <= 0:
        return jsonify({"status": "ERRO", "motivo": "Valor inválido"}), 400

    # Regra de Negócio 1.2: Pré-Validar
    if valor_pix <= RESERVA_BANCARIA_SALDO:
        # Regra de Negócio 1.2: Registrar
        log_message = f"PIX_ID:{data.get('id', 'N/A')} - VALOR:{valor_pix} - STATUS:AGUARDANDO_LIQUIDACAO"
        logger.info(log_message)
        
        return jsonify({"status": "PROCESSANDO", "detalhe": "Pagamento aguardando liquidação"}), 202
    else:
        log_message = f"PIX_ID:{data.get('id', 'N/A')} - VALOR:{valor_pix} - STATUS:REJEITADO_SALDO_INSUFICIENTE"
        logger.warning(log_message) # Pode ser 'warning' ou 'info'
        
        return jsonify({"status": "REJEITADO", "motivo": "Saldo na reserva insuficiente"}), 400

if __name__ == '__main__':
    # Log para evidência 3.2 (Logs da API lendo RESERVA_BANCARIA_SALDO)
    print(f"--- [UniFIAP Pay] API-PAGAMENTOS INICIADA ---")
    print(f"--- Lendo Saldo da Reserva: {RESERVA_BANCARIA_SALDO}")
    print(f"--- Log (Livro-Razão) sendo escrito em: {LOG_FILE}")
    print("--------------------------------------------------")
    
    # Ouve na porta 8081 em todas as interfaces
    app.run(host='0.0.0.0', port=8081)