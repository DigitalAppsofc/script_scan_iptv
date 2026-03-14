#!/bin/bash

# ==========================================
# 🎨 CORES DO INSTALADOR
# ==========================================
C="\033[1;36m"  # Ciano
G="\033[1;32m"  # Verde
R="\033[1;31m"  # Vermelho
Y="\033[1;33m"  # Amarelo
P="\033[1;35m"  # Roxo
W="\033[0m"     # Reset

# ==========================================
# 🔗 CONFIGURAÇÕES DO REPOSITÓRIO
# ==========================================
# Cole aqui o link RAW da pasta raiz do seu GitHub onde estão os arquivos .py
LINK_GITHUB="https://raw.githubusercontent.com/SEU_USUARIO/SEU_REPO/main"

# Nome dos arquivos que serão baixados
ARQUIVOS=(
    "config.py"
    "gerador_combos.py"
    "scanner_hosts.py"
    "server_analyzer.py"
    "leitor_grade.py"
    "main.py"
)

clear
echo -e "${C}================================================${W}"
echo -e "${G}       🚀 INSTALADOR DIGITAL SCANNER 🚀       ${W}"
echo -e "${C}================================================${W}"
echo -e "${P}            Criado por @Digital_Apps            ${W}"
echo -e "${C}================================================${W}\n"

sleep 1

# 1. DETECÇÃO DE SISTEMA (TERMUX OU VPS)
echo -e "${Y}[*] Analisando o sistema operacional...${W}"
if [ -n "$PREFIX" ] && [ -d "$PREFIX/bin" ]; then
    echo -e "${G}[+] Sistema Android (Termux) Detectado!${W}"
    IS_TERMUX=true
    BIN_DIR="$PREFIX/bin"
    
    echo -e "\n${Y}[*] Configurando armazenamento interno...${W}"
    echo -e "${C}--> Aceite a permissão na tela do seu celular se aparecer!${W}"
    termux-setup-storage
    sleep 2
else
    echo -e "${G}[+] Sistema Linux/VPS Detectado!${W}"
    IS_TERMUX=false
    BIN_DIR="/usr/local/bin"
    # Fallback se não tiver root
    if [ ! -w "$BIN_DIR" ]; then
        BIN_DIR="$HOME/.local/bin"
        mkdir -p "$BIN_DIR"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    fi
fi

# 2. ATUALIZAÇÃO E DEPENDÊNCIAS DO SISTEMA
echo -e "\n${Y}[*] Instalando pacotes base e dependências...${W}"
if [ "$IS_TERMUX" = true ]; then
    pkg update -y && pkg upgrade -y
    pkg install python clang libffi openssl curl wget -y
else
    sudo apt update -y
    sudo apt install python3 python3-pip curl wget build-essential libffi-dev libssl-dev -y
fi

# 3. DEPENDÊNCIAS PYTHON
echo -e "\n${Y}[*] Configurando o ambiente Python (Isso pode demorar um pouco)...${W}"
if [ "$IS_TERMUX" = true ]; then
    pip install --upgrade pip
    pip install curl_cffi==0.7.3 requests urllib3==2.2.1
else
    pip3 install --upgrade pip
    pip3 install curl_cffi==0.7.3 requests urllib3==2.2.1
fi

# 4. CRIANDO PASTA DE TRABALHO E BAIXANDO ARQUIVOS
DIR_INSTALACAO="$HOME/DigitalScanner"
echo -e "\n${Y}[*] Criando ambiente na pasta ${C}$DIR_INSTALACAO${W}..."
mkdir -p "$DIR_INSTALACAO"
cd "$DIR_INSTALACAO" || exit

echo -e "\n${Y}[*] Baixando arquivos oficiais do GitHub...${W}"
for arquivo in "${ARQUIVOS[@]}"; do
    echo -e "${C} ⬇️ Baixando: ${W}$arquivo..."
    curl -s -O "$LINK_GITHUB/$arquivo"
    
    # Checa se o download deu certo
    if [ -f "$arquivo" ]; then
        echo -e "${G}    ✅ Concluído!${W}"
    else
        echo -e "${R}    ❌ Falha ao baixar $arquivo! Verifique o link do GitHub.${W}"
    fi
    sleep 0.5
done

# 5. CRIANDO O COMANDO GLOBAL (scanner)
echo -e "\n${Y}[*] Criando o atalho mágico 'scanner'...${W}"

# Define se vai rodar com python ou python3
PY_CMD="python"
if ! command -v python &> /dev/null; then
    PY_CMD="python3"
fi

cat <<EOF > "$BIN_DIR/scanner"
#!/bin/bash
cd "$DIR_INSTALACAO"
$PY_CMD main.py "\$@"
EOF

chmod +x "$BIN_DIR/scanner"

# ==========================================
# 🏁 FINALIZAÇÃO
# ==========================================
clear
echo -e "${C}================================================${W}"
echo -e "${G}         🎉 INSTALAÇÃO CONCLUÍDA! 🎉            ${W}"
echo -e "${C}================================================${W}"
echo -e "${P}          Ferramenta por @Digital_Apps          ${W}"
echo -e "${C}================================================${W}\n"
echo -e "${Y}Tudo pronto! Seu ambiente foi configurado com sucesso.${W}"
echo -e "${Y}Os arquivos originais estão em:${W} ${C}$DIR_INSTALACAO${W}\n"
echo -e "👉 ${G}Sempre que quiser iniciar o painel, digite apenas o comando abaixo:${W}"
echo -e "\n   ${C}scanner${W}\n"
