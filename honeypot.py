
import socket
import time
from datetime import datetime
import urllib.request
import json
import subprocess
import threading # NOVO: Permite correr várias portas ao mesmo tempo

# ================= CONFIGURAÇÕES DE ALERTAS =================
DISCORD_URL = "https://discord.com/api/webhooks/1570242193363308700/LpCXHXuWmsjalu5BgWJmYC6z0VpkAL5aNKeJh3zHW2QBpXmn5awhvtMzhqkShrlEweQ5"

def disparar_alertas(ip_atacante, porta, servico):
    mensagem_discord = f"🚨 **ALERTA DE INTRUSÃO (HONEYPOT)** 🚨\nVarrimento detetado!\n**Alvo:** Porta {porta} ({servico})\n**IP do Atacante:** `{ip_atacante}`\n🛡️ **Ação da Máquina:** IP banido permanentemente na Firewall!"
    
    try:
        if "COLE_AQUI" not in DISCORD_URL:
            req_disc = urllib.request.Request(DISCORD_URL, method="POST")
            req_disc.add_header('Content-Type', 'application/json')
            req_disc.add_header('User-Agent', 'Mozilla/5.0')
            urllib.request.urlopen(req_disc, data=json.dumps({"content": mensagem_discord}).encode('utf-8'), timeout=5)
            print(f"[+] Alerta Discord enviado com sucesso (Porta {porta})!")
    except Exception as e:
        print(f"[-] Falha ao enviar para Discord: {e}")

# ================= DEFESA ATIVA (FIREWALL) =================
def banir_ip(ip_atacante):
    try:
        subprocess.run(["iptables", "-A", "INPUT", "-s", ip_atacante, "-j", "DROP"], check=True)
        print(f"[🛡️] Defesa Ativa: IP {ip_atacante} bloqueado com sucesso pelo Iptables!")
    except Exception:
        pass # Se o IP já estiver bloqueado num varrimento anterior, simplesmente ignora o erro

# ================= MOTOR DO HONEYPOT MULTI-PORTA =================
def iniciar_servidor(porta, banner_falso, servico):
    host = "0.0.0.0"
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        servidor.bind((host, porta))
        servidor.listen(5)
        print(f"[*] Honeypot {servico} ativo e a escutar na porta {porta}...")
    except Exception as e:
        print(f"[-] Erro ao iniciar {servico} na porta {porta}: {e}")
        return

    while True:
        try:
            cliente, endereco = servidor.accept()
            ip_atacante = endereco[0]
            data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            mensagem_log = f"[{data_hora}] [!] {servico} (Porta {porta}) - Ligacao do IP: {ip_atacante}"
            print(mensagem_log)
            
            with open("/home/mabila-honeypot/intrusoes.log", "a") as f:
                f.write(mensagem_log + "\n")
            
            disparar_alertas(ip_atacante, porta, servico)
            banir_ip(ip_atacante)
            
            time.sleep(1) 
            cliente.send(banner_falso)
            cliente.close()
            
        except Exception:
            pass

if __name__ == "__main__":
    # Dicionário com as portas e as mensagens falsas (banners) que vamos enviar ao atacante
    servicos_falsos = [
        {"porta": 22, "banner": b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1\r\n", "nome": "SSH"},
        {"porta": 21, "banner": b"220 (vsFTPd 3.0.3)\r\n", "nome": "FTP"},
        {"porta": 80, "banner": b"HTTP/1.1 200 OK\r\nServer: Apache/2.4.41 (Ubuntu)\r\n\r\n", "nome": "HTTP"}
    ]

    print("[*] A iniciar Honeypot Multi-Superficie...")
    
    # Iniciar cada serviço numa Thread separada para correrem em simultâneo
    for servico in servicos_falsos:
        thread = threading.Thread(target=iniciar_servidor, args=(servico["porta"], servico["banner"], servico["nome"]))
        thread.daemon = True
        thread.start()

    # Manter o programa principal sempre a correr
    while True:
        time.sleep(1)
