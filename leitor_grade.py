import time
import random
from curl_cffi import requests

def get_iptv_info(server_url, username, password, proxies_list=None):
    server_url = server_url.strip().rstrip('/')
    if not server_url.startswith('http'):
        server_url = 'http://' + server_url
        
    base_api = f"{server_url}/player_api.php?username={username}&password={password}"
    headers = {"User-Agent": "IPTVSmartersPro", "Accept": "*/*"}
    
    result = {"status": False, "live": 0, "vod": 0, "series": 0, "error": ""}
    
    #  SISTEMA ROTATIVO DE PROXIES
    # Começa sempre tentando CONEXÃO DIRETA (None)
    tentativas = [None]
    
    # Se o usuário tem proxies salvos, embaralha e pega 3 para tentar caso a conexão direta falhe
    if proxies_list:
        proxies_embaralhados = list(proxies_list)
        random.shuffle(proxies_embaralhados) 
        tentativas.extend(proxies_embaralhados[:3]) 
        
    for px in tentativas:
        px_dict = {"http": f"http://{px}", "https": f"http://{px}"} if px else None
        
        try:
            with requests.Session(impersonate="chrome110") as session:
                session.headers.update(headers)
                
                # Tenta fazer o login
                auth_resp = session.get(base_api, proxies=px_dict, timeout=15, verify=False)
                
                if auth_resp.status_code == 200:
                    try:
                        auth_data = auth_resp.json()
                    except:
                        result["error"] = "Resposta do servidor bloqueada (Falso Positivo)."
                        continue # Falhou, tenta o próximo proxy!
                        
                    user_info = auth_data.get('user_info', {})
                    if not user_info:
                        result["error"] = "Usuário ou Senha incorretos."
                        return result # Se a senha ta errada, o proxy não vai salvar. Interrompe aqui.
                        
                    status_conta = str(user_info.get('status', '')).strip().lower()
                    if user_info.get('auth') == 0 or status_conta in ['expired', 'disabled', 'banned', 'inativo']:
                        result["error"] = f"Conta Expirada ou Banida ({status_conta.upper()})"
                        return result # Conta ruim. Interrompe aqui.
                        
                    result["status"] = True
                    
                    # Conexão aprovada! Agora baixa a grade de canais e filmes
                    try:
                        r_live = session.get(f"{base_api}&action=get_live_streams", proxies=px_dict, timeout=15, verify=False)
                        if r_live.status_code == 200: result["live"] = len(r_live.json())
                    except: pass
                    
                    try:
                        r_vod = session.get(f"{base_api}&action=get_vod_streams", proxies=px_dict, timeout=15, verify=False)
                        if r_vod.status_code == 200: result["vod"] = len(r_vod.json())
                    except: pass
                    
                    try:
                        r_series = session.get(f"{base_api}&action=get_series", proxies=px_dict, timeout=15, verify=False)
                        if r_series.status_code == 200: result["series"] = len(r_series.json())
                    except: pass
                    
                    return result # Tudo certo, devolve a grade!
                    
                else:
                    result["error"] = f"IP Bloqueado (Erro HTTP {auth_resp.status_code})"
                    continue # Se tomou erro 403, 503, tenta o próximo proxy da lista!
                    
        except Exception as e:
            result["error"] = "Timeout ou Host Offline."
            continue # Se o site demorou muito pra responder, tenta outro proxy!
            
    # Se testar a direta e os 3 proxies e nenhum for, devolve o último erro.
    return result
