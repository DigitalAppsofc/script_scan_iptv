import os

# Cores do Painel
C = "\033[1;36m"  # Ciano
G = "\033[1;32m"  # Verde
R = "\033[1;31m"  # Vermelho
Y = "\033[1;33m"  # Amarelo
P = "\033[1;35m"  # Roxo
W = "\033[0m"     # Reset

# Links do GitHub (Substitua pelos links RAW do seu repositório)
URL_UPDATE = "https://raw.githubusercontent.com/SEU_USUARIO/SEU_REPO/main/update.json"
URL_PROXIES = "https://raw.githubusercontent.com/SEU_USUARIO/SEU_REPO/main/proxies.txt"
URL_FREELISTS = "https://raw.githubusercontent.com/SEU_USUARIO/SEU_REPO/main/freelists.json"

VERSAO_ATUAL = "1.0.0"

def obter_pasta_downloads():
    termux_dir = os.path.expanduser("~/storage/downloads")
    vps_dir = os.path.expanduser("~/Downloads")
    
    if os.path.exists(os.path.expanduser("~/storage")):
        return termux_dir
    elif os.path.exists(vps_dir):
        return vps_dir
    else:
        fallback_dir = os.path.join(os.getcwd(), "Downloads")
        os.makedirs(fallback_dir, exist_ok=True)
        return fallback_dir

PASTA_DOWNLOADS = obter_pasta_downloads()
