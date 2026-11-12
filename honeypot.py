import socket
import time
from datetime import datetime
import urllib.request
import json

# ================= CONFIGURAÇÕES DE ALERTAS =================
DISCORD_URL = "https://discord.com/api/webhooks/1570242193363308700/LpCXHXuWmsjalu5BgWJmYC6z0VpkAL5aNKeJh3zHW2QBpXmn5awhvtMzhqkShrlEweQ5"
TELEGRAM_TOKEN = "9252839116:AAGAn0BCS6gy6on7rAfpZaJ1eDEakFVjWuk"
TELEGRAM_CHAT = "9252839116"

def disparar_alertas(ip_atacante):
    mensagem_discord = f"🚨 **ALERTA DE INTRUSÃO (HONEYPOT)** 🚨\nVarrimento detetado na Porta 22!\n**IP do Atacante:** `{ip_atacante}`"
    mensagem_telegram = f"🚨 ALERTA DE INTRUSÃO (HONEYPOT) 🚨\nVarrimento detetado na Porta 22!\nIP do Atacante: {ip_atacante}"
    
    # Envio para o Discord
    try:
        if "COLE_AQUI" not in DISCORD_URL:
            req_disc = urllib.request.Request(DISCORD_URL, method="POST")
            req_disc.add_header('Content-Type', 'application/json')
            req_disc.add_header('User-Agent', 'Mozilla/5.0') # Mascara para evitar bloqueio do Discord
            urllib.request.urlopen(req_disc, data=json.dumps({"content": mensagem_discord}).encode('utf-8'), timeout=5)
            print("[+] Alerta Discord enviado com sucesso!")
    except Exception as e:
        print(f"[-] Falha ao enviar para Discord: {e}")

    # Envio para o Telegram
    try:
        if "COLE_AQUI" not in TELEGRAM_TOKEN:
            url_tele = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            req_tele = urllib.request.Request(url_tele, method="POST")
            req_tele.add_header('Content-Type', 'application/json')
            req_tele.add_header('User-Agent', 'Mozilla/5.0')
            urllib.request.urlopen(req_tele, data=json.dumps({"chat_id": TELEGRAM_CHAT, "text": mensagem_telegram}).encode('utf-8'), timeout=5)
            print("[+] Alerta Telegram enviado com sucesso!")
    except Exception as e:
        print(f"[-] Falha ao enviar para Telegram: {e}")

# ================= MOTOR DO HONEYPOT =================
def iniciar_honeypot():
    host = "0.0.0.0"
    porta = 22
    banner_falso = b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.1\r\n"

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        servidor.bind((host, porta))
        servidor.listen(5)
        print(f"[*] Honeypot ativo e a escutar na porta {porta}...")
    except Exception as e:
        print(f"[-] Erro ao iniciar o servidor: {e}")
        return

    while True:
        try:
            cliente, endereco = servidor.accept()
            ip_atacante = endereco[0]
            data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            mensagem_log = f"[{data_hora}] [!] Ligacao bloqueada do IP: {ip_atacante}"
            print(mensagem_log)
            
            with open("/home/mabila-honeypot/intrusoes.log", "a") as f:
                f.write(mensagem_log + "\n")
            
            disparar_alertas(ip_atacante)
            
            time.sleep(1) 
            cliente.send(banner_falso)
            cliente.close()
            
        except Exception as e:
            print(f"[-] Erro na ligacao com o cliente: {e}")

if __name__ == "__main__":
    iniciar_honeypot()
