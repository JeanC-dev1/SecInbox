#!/bin/bash

echo "Desinstalando integração do SecureInbox com o sistema..."

# Caminho do arquivo .desktop usado no menu de contexto
CONTEXT_PATH="$HOME/.local/share/file-manager/actions/secureinbox.desktop"

# Verifica e remove o arquivo
if [ -f "$CONTEXT_PATH" ]; then
    rm "$CONTEXT_PATH"
    echo "→ Atalho do menu de contexto removido: $CONTEXT_PATH"
else
    echo "→ Nenhum atalho de menu de contexto encontrado para remover."
fi

# Permissão de execução não precisa ser revertida, mas se desejar:
# chmod -x "$HOME/SecInbox/src/main.py"

echo "Desinstalação concluída."
