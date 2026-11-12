# python-ssh-honeypot
Um honeypot leve em Python para detetar e registar varrimentos de rede simulando um servidor SSH.
## Estado Atual do Projeto
O motor base está totalmente funcional. O honeypot é capaz de escutar tráfego, identificar scanners, resistir a cortes abruptos de ligação e falsificar a versão do serviço para enganar o atacante.

### Fase 1: Implementação Base (Concluída)
- [x] Criação de um servidor socket em Python a escutar na porta 22.
- [x] Envio de banner falso (Spoofing) para enganar o Nmap (`SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1`).
- [x] Blindagem contra falhas (Try-Except) para lidar com erros de *Connection reset by peer* gerados por varrimentos agressivos.
- [x] Criação de um sistema de registos local (`intrusoes.log`) com carimbo de tempo e IP do atacante.
- [x] Testes de eficácia comprovados via localhost e ataques de rede externa.

### Fase 2: Automação e Expansão
- [] **Persistência:** Transformar o script num serviço do sistema Linux para arranque automático e invisível.
- [ ] **Expansão Multi-Porta:** Adicionar monitorização simultânea para as portas 21 (FTP) e 80 (HTTP).
- [ ] **Alertas em Tempo Real:** Integração de Webhooks para notificar ataques instantaneamente via Discord ou Telegram.
- [ ] **Defesa Ativa:** Integração com a Firewall para banir os IPs detetados automaticamente.
- [ ] **Terminal Interativo Falso:** Simular um terminal real para capturar os comandos que o atacante tenta executar após um falso login.
- [ ] **Dashboard Visual:** Interface Web simples para visualizar as métricas dos ataques detetados.

## Pré-requisitos do Sistema
- Sistema Operativo: Ubuntu Linux 
- Rede: Interface configurada em modo NAT ou Bridged para exposição externa.
- Dependências Python: Python 3.x (bibliotecas nativas `socket`, `time`, `datetime`).

## Como executar a versão atual
No servidor Ubuntu, execute o seguinte comando para iniciar o honeypot em segundo plano:
```bash
sudo python3 honeypot.py & 

## Como Testar (Simulação de Ataque)
A partir de uma máquina externa na mesma rede, execute um varrimento de versão agressivo:

nmap -sV -p 22 192.168.164.130[IP_DO_SERVIDOR_HONEYPOT]

