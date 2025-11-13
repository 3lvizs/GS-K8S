import os
import time

LOG_FILE = '/var/logs/api/instrucoes.log'
CHAVE_SECRETA = os.environ.get('FAKE_PIX_KEY', 'CHAVE_NAO_ENCONTRADA')

def simular_liquidacao():
    print(f"--- [UniFIAP Pay] AUDITORIA-SERVICE INICIADO ---")
    print(f"--- Verificando chave secreta... Chave carregada: {'*' * len(CHAVE_SECRETA)}")
    print(f"--- Lendo Livro-Razão de: {LOG_FILE}")
    print("--------------------------------------------------")

    try:
        linhas_atualizadas = []
        houve_mudanca = False

        # Lê o arquivo de log
        with open(LOG_FILE, 'r') as f:
            linhas = f.readlines()

        # Processa as linhas
        for linha in linhas:
            if 'AGUARDANDO_LIQUIDACAO' in linha:
                nova_linha = linha.replace('AGUARDANDO_LIQUIDACAO', 'LIQUIDADO')
                linhas_atualizadas.append(nova_linha)
                print(f"LIQUIDANDO: {linha.strip()} -> {nova_linha.strip()}")
                houve_mudanca = True
            else:
                linhas_atualizadas.append(linha) # Mantém a linha original

        # Re-escreve o arquivo com as linhas atualizadas
        if houve_mudanca:
            with open(LOG_FILE, 'w') as f:
                f.writelines(linhas_atualizadas)
            print("--- Processamento concluído. Livro-Razão atualizado. ---")
        else:
            print("--- Nenhuma transação aguardando liquidação foi encontrada. ---")

    except FileNotFoundError:
        print(f"ERRO: Arquivo de log não encontrado em {LOG_FILE}. Verifique o volume.")
    except Exception as e:
        print(f"ERRO inesperado durante a auditoria: {e}")

    print("--- [UniFIAP Pay] AUDITORIA-SERVICE FINALIZADO ---")

if __name__ == '__main__':
    simular_liquidacao()