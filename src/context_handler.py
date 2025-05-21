import sys
import os
from phishing_checker import analyze_text

def detectar_tipo(texto):
    texto = texto.strip()
    if "@" in texto and "." in texto:
        return "email"
    elif texto.startswitch("http://") or texto.startswitch("https://"):
        return "url"
    else:
        return "desconhecido"
    
def processar_entrada(texto):
    tipo = detectar_tipo(texto)
    if tipo == "desconhecido":
        return {
            "resultado": "Formato não reconhecido.",
            "suspeito": None
        }
    
    resultado = analyze_text(texto, tipo=tipo)
    return {
        "resultado": resultado.get("motivo", "Seguro"),
        "suspeito": resultado["suspeito"]
    }

def main():
    if len(sys.argv) < 2:
        print("Uso: context_handler.py \"<texto>\"")
        sys.exit(1)

    texto = sys.argv[1]
    resultado = processar_entrada(texto)

    # Exibição simples no terminal
    print("\n--- Análise ---")
    print(f"Texto: {texto}")
    print(f"Suspeito: {'Sim' if resultado['suspeito'] else 'Não'}")
    print(f"Motivo: {resultado['resultado']}")
    print("----------------")

if __name__ == "__main__":
    main()