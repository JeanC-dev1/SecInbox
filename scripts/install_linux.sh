#!/bin/bash

echo "🔧 Iniciando instalação do SecureInbox para Linux..."

# Caminho base do projeto
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$BASE_DIR/venv"
MAIN_SCRIPT="$BASE_DIR/src/main.py"

# 1. Criar ambiente virtual
echo "🧪 Criando ambiente virtual..."
python3 -m venv "$VENV_DIR"

# 2. Ativar venv e instalar dependências
echo "📦 Instalando dependências..."
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r "$BASE_DIR/requirements.txt"

# 3. Criar ícone no menu do sistema (secureinbox.desktop)
echo "📁 Criando atalho de aplicativo..."
DESKTOP_FILE="$HOME/.local/share/applications/secureinbox.desktop"

mkdir -p "$(dirname "$DESKTOP_FILE")"

cat > "$DESKTOP_FILE" <<EOL
[Desktop Entry]
Name=Analisar com SecureInbox
Comment=Análise de emails e links suspeitos
Exec=$VENV_DIR/bin/python3 $MAIN_SCRIPT %u
Terminal=true
Type=Application
MimeType=text/plain;
Categories=Utility;
EOL

chmod +x "$DESKTOP_FILE"
update-desktop-database "$HOME/.local/share/applications"

# 4. Adicionar ao menu de contexto do Nautilus
echo "🖱️ Adicionando ao menu de contexto do Nautilus..."

NAUTILUS_SCRIPT="$HOME/.local/share/nautilus/scripts/Analisar_com_SecureInbox"

mkdir -p "$(dirname "$NAUTILUS_SCRIPT")"

cat > "$NAUTILUS_SCRIPT" <<EOL
#!/bin/bash
source "$VENV_DIR/bin/activate"
python3 "$MAIN_SCRIPT" "\$NAUTILUS_SCRIPT_SELECTED_FILE_PATHS"
EOL

chmod +x "$NAUTILUS_SCRIPT"

echo "✅ Instalação concluída! Reinicie o Nautilus se necessário (ou faça logout/login)."
echo "👉 Agora você pode clicar com o botão direito em arquivos de texto e selecionar: Scripts > Analisar_com_SecureInbox"
