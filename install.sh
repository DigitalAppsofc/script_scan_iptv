#!/bin/bash

echo -e "\e[1;36m=== INICIANDO INSTALAÇÃO DIGITAL APPS ===\e[0m"

# Atualiza pacotes e instala Python
pkg update -y && pkg upgrade -y
pkg install python -y
pkg install clang libffi openssl -y # Necessários para o curl_cffi rodar liso no Termux

# Pede permissão da pasta (crucial no Termux para a pasta Downloads funcionar)
echo -e "\e[1;33m[*] Solicitando permissão de armazenamento...\e[0m"
termux-setup-storage
sleep 2

# Instala bibliotecas
echo -e "\e[1;32m[*] Instalando dependências Python...\e[0m"
pip install curl_cffi==0.7.3 requests urllib3==2.2.1

# Cria atalho
echo -e "\e[1;36m[*] Criando atalho...\e[0m"
pwd_dir=$(pwd)
echo "alias scan='python $pwd_dir/main.py'" >> ~/.bashrc
source ~/.bashrc

echo -e "\e[1;32m✅ Instalação Concluída!\e[0m"
echo -e "\e[1;33mPara abrir o painel, feche o termux, abra novamente e digite: \e[1;32mscan\e[0m"
