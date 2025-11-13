# Desafio UniFIAP Pay SPB

## Dados do Aluno
- Nome: [Seu Nome Completo]  
- RM: [Seu Registro de Matrícula]  
- Total de Pontos Deste Desafio: 9,0 pts  

---

## 1. Arquitetura da Solução e Contexto SPB

### 1.1. Descrição do Projeto
Este projeto implementa uma arquitetura de microsserviços moderna na Nuvem (Cloud Native) para a UniFIAP Pay.  
O objetivo é simular um fluxo de pagamento PIX seguindo as regras do Sistema de Pagamentos Brasileiro (SPB), que exige compensação e liquidação através do Banco Central (STR).

O desafio foca em três pilares:

- Segurança: Construir containers e redes isoladas.  
- Orquestração: Usar o Kubernetes para gerenciar a aplicação em escala.  
- Regras de Negócio: Aplicar a lógica da Reserva Bancária e Liquidação.

---

### 1.2. Papéis e Responsabilidades dos Microsserviços (Fluxo SPB)

| Microsserviço | Função Principal (Papel no SPB) | Responsabilidades de Código |
|----------------|--------------------------------|------------------------------|
| api-pagamentos | Simula o Banco Originador (UniFIAP Pay). Garante que o banco tem dinheiro suficiente no BACEN para cobrir o PIX (a Reserva Bancária). | 1. Ler Saldo: Consultar `RESERVA_BANCARIA_SALDO` (do ENV/ConfigMap).<br>2. Pré-Validar: Aplicar a regra: `SE Valor do PIX <= RESERVA_BANCARIA_SALDO`.<br>3. Registrar: Se aprovado, escrever (apendar) a instrução de pagamento no arquivo `/var/logs/api/instrucoes.log` com o status `AGUARDANDO_LIQUIDACAO`. |
| auditoria-service | Simula o Sistema de Liquidação (BACEN/STR). Atua como a autoridade central que processa os pagamentos. | 1. Monitorar: Ler novas linhas no arquivo `/var/logs/api/instrucoes.log` (o Livro-Razão).<br>2. Liquidação: Buscar transações `AGUARDANDO_LIQUIDACAO` e atualizar o status para `LIQUIDADO`.<br>3. Automação: Ser executado por um `CronJob` a cada 6h. |

---

### 1.3. Diagrama de Arquitetura
Incluir aqui o diagrama de arquitetura.  
O diagrama deve mostrar:
- Os Pods dos serviços
  <img width="1536" height="1024" alt="services" src="https://github.com/user-attachments/assets/da38336e-13d9-4eb0-8262-3fb2555e3c24" />
- O Volume Compartilhado (PVC), atuando como Livro-Razão
 <img width="1536" height="1024" alt="pvc" src="https://github.com/user-attachments/assets/234c2f85-29ac-46cc-acb1-99f8eb896f22" />
- ConfigMap e Secrets
  <img width="1536" height="1024" alt="configmap" src="https://github.com/user-attachments/assets/618ee716-d992-4d53-a3a1-dbbd7d8b6e23" />
- Rede Docker customizada (subnet isolada)
 <img width="1536" height="1024" alt="network" src="https://github.com/user-attachments/assets/186a33bc-5b7a-4d0e-9ac8-e96bbe3ec05e" />

---

## 2. Passos de Execução

### 2.1. Configuração Local (Docker)
1. Criar Rede Docker Segmentada (Isolamento) exemplo unifiap_net: 172.25.0.0/24

2. Preparar Variáveis:
- Preencher o arquivo ./docker/.env com o valor de RESERVA_BANCARIA_SALDO.
- Adicionar o arquivo pix.key com uma chave de simulação.

### 2.2. Build e Publicação das Imagens com versão e RM do aluno ex:v1.<RM_do_aluno>  
- Build com Multi-Stage (para imagens menores e seguras)
- Varredura de Vulnerabilidades (incluir o output nas evidências)
- Publicação das Imagens no Docker Hub
 
### 2.3. Subindo o Rancher (Gerenciamento de Containers)   
- Para gerenciar os containers e clusters de forma visual, suba o Rancher localmente.
- Use o painel do Rancher para monitorar Pods, Jobs e CronJobs do namespace unifiapay

### 2.4. Deploy no Kubernetes (Minikube/Kind)
- Verifique os YAMLs: Certifique-se de que os arquivos em ./k8s apontam para suas imagens do Docker Hub (com seu RM).
- Aplique os manifests

## 3. Evidências e Resultados
3.1. Etapa 1: Docker e Imagem Segura (1,5 pts)
- Print do comando docker build mostrando multi-stage.
- Saída do docker push com a tag v1.<RM_do_aluno>.
- Saída do docker scout comprovando ausência de vulnerabilidades críticas.

3.2. Etapa 2: Rede, Comunicação e Segmentação (2,5 pts)
- Saída de docker inspect unifiap_net mostrando o bloco IP customizado.
- Saída de curl ou ping entre containers.
- Logs da API lendo RESERVA_BANCARIA_SALDO do arquivo .env.
  
3.3. Etapa 3: Kubernetes – Estrutura, Escala e Deploy (3,0 pts)
- Saída de kubectl get pods -n unifiapay mostrando a API com 2 réplicas e o Auditoria rodando.
- Saída do kubectl scale e subsequente kubectl get pods mostrando o aumento de réplicas.
- Logs de dois Pods da API e do Pod da Auditoria, provando leitura/escrita no mesmo arquivo instrucoes.log.
- Saída de kubectl get cronjob e kubectl get job após a execução do cronjob-fechamento-reserva.

3.4. Etapa 4: Kubernetes – Segurança, Observação e Operação (2,0 pts)
- Saída do comando kubectl top pods -n unifiapay mostrando limites de CPU/Memória aplicados.
- Trecho do manifest YAML mostrando a configuração do securityContext (runAsNonRoot: true, etc.).
- Comando de tentativa de deploy insegura seguido do kubectl describe pod, provando bloqueio por regra de segurança.
- Saída do kubectl auth can-i ... provando que a ServiceAccount tem permissão restrita.
