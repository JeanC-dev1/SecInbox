#!/bin/bash

# Este script instala o SecureInbox em sistemas Linux.
# Ele cria um ambiente virtual, instala dependências e configura atalhos.

echo "🔧 Iniciando instalação do SecureInbox para Linux..."

# Caminho base do projeto
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$BASE_DIR/venv"
MAIN_SCRIPT="$BASE_DIR/src/main.py"
XCLIP_SCRIPT="$BASE_DIR/scripts/analisar_selecao.sh"

# 1. Instalar dependências do sistema
echo "📦 Verificando e instalando dependências do sistema (xclip)..."
if ! command -v xclip &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y xclip
fi

# 2. Criar ambiente virtual
echo "🧪 Criando ambiente virtual..."
python3 -m venv "$VENV_DIR"

# 3. Ativar venv e instalar dependências do Python
echo "📦 Instalando dependências do Python..."
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r "$BASE_DIR/requirements.txt"

# 4. Criar o script que usará o xclip para o atalho de teclado
echo "⌨️ Criando script para atalho de teclado..."
cat > "$XCLIP_SCRIPT" <<EOL
#!/bin/bash

# Pega o texto selecionado (se disponível)
SELECIONADO=\$(xclip -o -selection primary)

# Se nada for selecionado, tenta pegar da área de transferência
if [ -z "\$SELECIONADO" ]; then
    SELECIONADO=\$(xclip -o -selection clipboard)
fi

# Se ainda estiver vazio, sai do script
if [ -z "\$SELECIONADO" ]; then
    echo "Nenhum texto selecionado. A análise requer que um texto esteja sublinhado ou copiado."
    exit 1
fi

# Executa o seu script de análise com o texto
"$VENV_DIR/bin/python3" "$MAIN_SCRIPT" "\$SELECIONADO"
EOL

chmod +x "$XCLIP_SCRIPT"

# 5. Tentar configurar atalho de teclado para GNOME
echo "⌨️ Tentando configurar atalho de teclado para GNOME..."
if command -v dconf &> /dev/null && [ "$XDG_CURRENT_DESKTOP" = "GNOME" ]; then
    SHORTCUT_NAME="custom_secureinbox"
    SHORTCUT_COMMAND="$XCLIP_SCRIPT"
    SHORTCUT_KEY="<Primary><Alt>A"

    CUSTOM_SHORTCUTS_PATH="/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings"
    
    # Adiciona o novo atalho à lista
    dconf write "$CUSTOM_SHORTCUTS_PATH/$SHORTCUT_NAME/name" "'Analisar com SecureInbox'"
    dconf write "$CUSTOM_SHORTCUTS_PATH/$SHORTCUT_NAME/command" "'$SHORTCUT_COMMAND'"
    dconf write "$CUSTOM_SHORTCUTS_PATH/$SHORTCUT_NAME/binding" "'$SHORTCUT_KEY'"

    echo "✅ Atalho de teclado 'Ctrl+Alt+A' configurado para GNOME!"
    echo "⚠️ Se o atalho não funcionar, por favor configure-o manualmente em Configurações > Teclado > Atalhos de teclado."
else
    echo "❌ Não foi possível configurar o atalho automaticamente. Por favor, configure-o manualmente em Configurações > Teclado, executando:"
    echo "$XCLIP_SCRIPT"
fi

echo "✅ Instalação concluída!"
echo "👉 Agora você pode selecionar um texto em qualquer lugar e usar o atalho Ctrl+Alt+A para analisá-lo."
echo "👉 Para o Nautilus, a opção de scripts 'Analisar com SecureInbox' continuará funcionando para arquivos."