# Honeypot Multi-Superfície com Defesa Ativa

**Disciplina:** Projeto Final  
**Autor:** Mabila Mateus  
**Ano Letivo:** 2026/27



## Objetivo do Projeto
O objetivo deste Projeto Final foi desenvolver e implementar um **Honeypot de Defesa Ativa** em ambiente Linux (Ubuntu). Ao contrário de um honeypot tradicional que apenas regista intrusões de forma passiva, este sistema reage de forma autónoma a ameaças. 

O script em Python simula três serviços vulneráveis comuns (FTP, SSH e HTTP) e, ao detetar qualquer interação não autorizada, alerta o administrador em tempo real via Discord e aciona automaticamente a firewall do sistema (Iptables) para banir o endereço IP do atacante permanentemente.

##  Arquitetura e Ambiente de Laboratório
Para garantir o isolamento e a segurança dos testes, o projeto foi desenvolvido num ambiente de laboratório virtualizado utilizando o **VMware Workstation** com configuração de rede NAT.

* **Máquina Vítima (Honeypot):** Ubuntu Linux
  * Hospeda o script Python em background utilizando o `systemd`.
  * Utiliza o `iptables` nativo para a aplicação das regras de bloqueio.
* **Máquina Atacante:** Kali Linux
  * Utilizada para simular varrimentos de reconhecimento (Nmap).
  * Utilizada para simular ataques de Força Bruta / Dicionário (Hydra).

## Funcionalidades Principais
1. **Monitorização Multi-Porta:** Escuta em simultâneo nas portas 21 (FTP), 22 (SSH) e 80 (HTTP) sem bloqueios entre processos, utilizando a biblioteca `threading` do Python.
2. **Engano de Reconhecimento:** Envio de banners forjados (ex: *vsFTPd 3.0.3*, *OpenSSH 8.2p1*, *Apache 2.4.41*) para enganar ferramentas de scanning como o Nmap.
3. **Alertas em Tempo Real:** Integração com Webhooks do Discord, enviando notificações instantâneas com o IP do atacante, a porta alvejada e a ação tomada.
4. **Defesa Ativa Autónoma:** Execução imediata de comandos Iptables (`iptables -A INPUT -s [IP] -j DROP`) via `subprocess`, mitigando ataques de força bruta no primeiro milissegundo.

## Dificuldades Encontradas e Soluções
Durante o desenvolvimento do projeto, surgiram alguns desafios técnicos que foram ultrapassados com sucesso:
* **Transição de Comunicação:** Inicialmente considerou-se a API do Telegram para os alertas, mas optou-se pela transição para Webhooks do Discord devido à maior simplicidade de integração e menor latência na entrega das mensagens JSON.
* **Bloqueio Inadvertido do Host:** Durante os testes de Defesa Ativa, o IP da máquina Host (Windows) foi bloqueado pela firewall, cortando o acesso. A solução passou por implementar uma VM isolada (Kali Linux) exclusivamente para ataques e a utilização do comando `sudo iptables -F` para libertar IPs banidos durante a fase de testes.
* **Concorrência de Portas:** O script inicial parava na primeira ligação (SSH). Foi necessário redesenhar a arquitetura de software para incluir *Threads*, permitindo que cada serviço (FTP, SSH, HTTP) corresse de forma independente.

## Como Testar
Para simular a Defesa Ativa, deve-se utilizar a máquina Kali Linux:

1. **Varrimento Inicial:** `nmap -sV -F [IP_DO_UBUNTU]`
   * *Resultado:* O Nmap deteta os serviços falsos, o Honeypot regista a intrusão, envia o alerta para o Discord e bloqueia o IP.
2. **Prova do Bloqueio:** Repetir `nmap -sV -F [IP_DO_UBUNTU]`
   * *Resultado:* O Nmap falha e reporta todas as portas como "Filtered" (ignoradas pela firewall).
3. **Ataque de Força Bruta:** `hydra -l admin -p 123456 ftp://[IP_DO_UBUNTU]`
   * *Resultado:* O Hydra não consegue iniciar o ataque porque a ligação é terminada imediatamente pela firewall.

## 🏁 Conclusão
O projeto demonstrou com sucesso que a transição de uma postura de cibersegurança passiva para uma **Defesa Ativa** reduz drasticamente a janela de oportunidade de um atacante. Ao integrar a deteção em tempo real com a automação de firewall, o sistema conseguiu neutralizar ferramentas de reconhecimento e ataques de força bruta logo na primeira interação, cumprindo na íntegra os requisitos propostos para o Projeto Final.

