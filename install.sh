#!/bin/bash

C="\033[1;36m"
G="\033[1;32m"
R="\033[1;31m"
Y="\033[1;33m"
P="\033[1;35m"
W="\033[0m"

# COLOQUE SEU LINK RAW AQUI
LINK_GITHUB="https://raw.githubusercontent.com/DigitalAppsofc/script_scan_iptv/main"

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

echo -e "${Y}[*] Analisando o sistema operacional...${W}"
if [ -n "$PREFIX" ] && [ -d "$PREFIX/bin" ]; then
    echo -e "${G}[+] Sistema Android (Termux) Detectado!${W}"
    IS_TERMUX=true
    BIN_DIR="$PREFIX/bin"
    echo -e "\n${Y}[*] Configurando armazenamento interno...${W}"
    termux-setup-storage
    sleep 2
else
    echo -e "${G}[+] Sistema Linux/VPS Detectado!${W}"
    IS_TERMUX=false
    BIN_DIR="/usr/local/bin"
    if [ ! -w "$BIN_DIR" ]; then
        BIN_DIR="$HOME/.local/bin"
        mkdir -p "$BIN_DIR"
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    fi
fi

echo -e "\n${Y}[*] Instalando pacotes base e dependências...${W}"
if [ "$IS_TERMUX" = true ]; then
    pkg update -y && pkg upgrade -y
    pkg install python clang libffi openssl curl wget -y
else
    sudo apt update -y
    sudo apt install python3 python3-pip curl wget build-essential libffi-dev libssl-dev -y
fi

echo -e "\n${Y}[*] Configurando o ambiente Python...${W}"
# 👇 AQUI FOI A MUDANÇA: APENAS REQUESTS E URLLIB3
if [ "$IS_TERMUX" = true ]; then
    pip install --upgrade pip
    pip install requests urllib3==2.2.1
else
    pip3 install --upgrade pip
    pip3 install requests urllib3==2.2.1
fi

DIR_INSTALACAO="$HOME/DigitalScanner"
echo -e "\n${Y}[*] Criando ambiente na pasta ${C}$DIR_INSTALACAO${W}..."
mkdir -p "$DIR_INSTALACAO"
cd "$DIR_INSTALACAO" || exit

echo -e "\n${Y}[*] Baixando arquivos oficiais do GitHub...${W}"
for arquivo in "${ARQUIVOS[@]}"; do
    echo -e "${C} ⬇️ Baixando: ${W}$arquivo..."
    curl -s -O "$LINK_GITHUB/$arquivo"
    if [ -f "$arquivo" ]; then
        echo -e "${G}    ✅ Concluído!${W}"
    else
        echo -e "${R}    ❌ Falha ao baixar $arquivo!${W}"
    fi
    sleep 0.5
done

echo -e "\n${Y}[*] Criando o atalho mágico 'scanner'...${W}"
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

clear
echo -e "${C}================================================${W}"
echo -e "${G}         🎉 INSTALAÇÃO CONCLUÍDA! 🎉            ${W}"
echo -e "${C}================================================${W}"
echo -e "${P}          Ferramenta por @Digital_Apps          ${W}"
echo -e "${C}================================================${W}\n"
echo -e "${Y}Tudo pronto! Seu ambiente foi configurado com sucesso.${W}"
echo -e "👉 ${G}Sempre que quiser iniciar o painel, digite apenas:${W} ${C}scanner${W}\n"
