#!/bin/bash

# Colores para los mensajes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}[*] Iniciando instalación de dependencias...${NC}"

# Actualizar repositorios
echo -e "\n${BLUE}[*] Actualizando repositorios...${NC}"
pkg update -y &>/dev/null

# Instalar Python si no está instalado
if ! command -v python &>/dev/null; then
    echo -e "\n${BLUE}[*] Instalando Python...${NC}"
    pkg install python -y &>/dev/null
fi

# Instalar pip si no está instalado
if ! command -v pip &>/dev/null; then
    echo -e "\n${BLUE}[*] Instalando pip...${NC}"
    pkg install python-pip -y &>/dev/null
fi

# Instalar mpv
echo -e "\n${BLUE}[*] Instalando mpv...${NC}"
pkg install mpv -y &>/dev/null

# Instalar termux-api
echo -e "\n${BLUE}[*] Instalando termux-api...${NC}"
pkg install termux-api -y &>/dev/null

# Instalar readchar via pip
echo -e "\n${BLUE}[*] Instalando módulo readchar...${NC}"
pip install readchar &>/dev/null

# Verificar las instalaciones
echo -e "\n${BLUE}[*] Verificando instalaciones...${NC}"

# Array de comandos para verificar
declare -A commands=(
    ["python"]="Python"
    ["pip"]="Pip"
    ["mpv"]="MPV"
    ["termux-volume"]="Termux-API"
)

# Verificar cada comando
all_installed=true
for cmd in "${!commands[@]}"; do
    if command -v $cmd &>/dev/null; then
        echo -e "${GREEN}[✓] ${commands[$cmd]} instalado correctamente${NC}"
    else
        echo -e "${RED}[×] Error al instalar ${commands[$cmd]}${NC}"
        all_installed=false
    fi
done

# Verificar módulo readchar
if python -c "import readchar" &>/dev/null; then
    echo -e "${GREEN}[✓] Módulo readchar instalado correctamente${NC}"
else
    echo -e "${RED}[×] Error al instalar el módulo readchar${NC}"
    all_installed=false
fi

# Mensaje final
echo -e "\n${BLUE}[*] Proceso de instalación completado${NC}"
if [ "$all_installed" = true ]; then
    echo -e "${GREEN}[✓] Todas las dependencias se instalaron correctamente${NC}"
else
    echo -e "${RED}[×] Algunas dependencias no se pudieron instalar${NC}"
    echo -e "${RED}[×] Por favor, revisa los errores e intenta instalar manualmente${NC}"
fi