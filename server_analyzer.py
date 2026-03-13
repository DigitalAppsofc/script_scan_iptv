import time
from urllib.parse import urlparse
from curl_cffi import requests

def analisar_servidor_real(url):
    url = url.strip()
    if not url.startswith('http'):
        url = 'http://' + url
        
    parsed_url = urlparse(url)
    domain = parsed_url.hostname
    is_https = url.startswith('https')
    
    resultado = {
        "url": url,
        "ip": "Falha DNS",
        "country": "Desconhecido",
        "isp": "Desconhecido",
        "asn": "",
        "ping": 0,
        "system": "Desconhecido / Painel Customizado",
        "protection": "Sem Proxy (Conexão Direta)",
        "is_https": is_https,
        "status": False
    }

    try:
        r_geo = requests.get(f"http://ip-api.com/json/{domain}?fields=status,country,countryCode,city,isp,org,as,query", timeout=5)
        if r_geo.status_code == 200:
            geo_data = r_geo.json()
            if geo_data.get("status") == "success":
                resultado["ip"] = geo_data.get("query", "0.0.0.0")
                resultado["country"] = f"{geo_data.get('city', '')}, {geo_data.get('countryCode', '')}"
                resultado["isp"] = geo_data.get("isp", "")
                resultado["asn"] = geo_data.get("as", "")
    except:
        pass

    start_time = time.time()
    try:
        r_server = requests.get(url, timeout=10, verify=False, impersonate="chrome110")
        resultado["ping"] = int((time.time() - start_time) * 1000)
        resultado["status"] = True
        
        headers = r_server.headers
        text = r_server.text.lower()
        
        server_header = headers.get("Server", "").lower()
        if "cloudflare" in server_header or "just a moment" in text or r_server.status_code in [403, 503]:
            resultado["protection"] = "Cloudflare Ativo"
            
        if "xtream codes" in text or "xtream-codes" in text or "xui.pw" in text:
            resultado["system"] = "Xtream Codes / Xtream UI"
        elif "ministra" in text or "stalker" in text or "mag" in text:
            resultado["system"] = "Ministra / Stalker Portal"
        else:
            api_url = f"{url.rstrip('/')}/player_api.php"
            r_api = requests.get(api_url, timeout=5, verify=False, impersonate="chrome110")
            if r_api.status_code in [200, 401, 404, 405] and "html" not in r_api.headers.get("Content-Type", "").lower():
                resultado["system"] = "Xtream API (Confirmado)"
            elif requests.get(f"{url.rstrip('/')}/c/", timeout=5, verify=False, impersonate="chrome110").status_code == 200:
                resultado["system"] = "Ministra / Stalker (Portal /c/)"

    except Exception as e:
        resultado["ping"] = int((time.time() - start_time) * 1000)
        resultado["status"] = False
        resultado["protection"] = "Host Offline ou Recusou Conexão"

    return resultado
