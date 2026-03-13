import os
import time
from concurrent.futures import ThreadPoolExecutor
from curl_cffi import requests
from config import PASTA_DOWNLOADS, C, G, R, Y, W

def check_single_host(url):
    url = url.strip()
    if not url.startswith('http'): url = 'http://' + url
    url = url.rstrip('/')
    try:
        response = requests.get(url, timeout=10, verify=False, impersonate="chrome110")
        status = response.status_code
        text = response.text.lower()
        if status == 200:
            if "cloudflare" in text or "just a moment" in text: return url, "cloudflare"
            return url, "online"
        elif status in [403, 503]: return url, "cloudflare"
        else: return url, "offline"
    except Exception: return url, "offline"

def process_hosts_list(urls, threads_limit=15):
    total = len(urls)
    if total == 0:
        print(f"{R}Nenhuma URL válida.{W}")
        return

    print(f"{C}Iniciando Scanner de {total} Hosts...{W}")
    online, cloudflare, offline = [], [], []
    processados = 0

    def worker(url):
        nonlocal processados
        res_url, status = check_single_host(url)
        if status == "online": online.append(res_url)
        elif status == "cloudflare": cloudflare.append(res_url)
        else: offline.append(res_url)
        processados += 1
        print(f"\r{Y}Progresso: {processados}/{total} | {G}Online: {len(online)}{W} | {R}Offline: {len(offline)}{W}", end="")

    with ThreadPoolExecutor(max_workers=threads_limit) as executor:
        for url in urls: executor.submit(worker, url)
        
    print("\n")
    if online:
        result_path = os.path.join(PASTA_DOWNLOADS, f"hosts_online_{int(time.time())}.txt")
        with open(result_path, "w", encoding="utf-8") as f:
            for o in online: f.write(f"{o}\n")
        print(f"{G}✅ Scan Finalizado! {len(online)} Hosts salvos em: {result_path}{W}")
    else:
        print(f"{R}❌ Nenhum host online sem proteção encontrado.{W}")
