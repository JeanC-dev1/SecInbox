import sys
from phishing_checker import analyze_text
from utils import validar_email, validar_url

def main():
    if len(sys.argv) <  2:
        print("Uso: SecInbox <texto>")
        sys.exit(1)

    input_text = sys.argv[1].strip()

    print(f"[SecInbox] Analisando: {input_text}")

    # Faz a verificação se é um link ou email
    if validar_url(input_text):
        resultado = analyze_text(input_text, tipo="url")
    elif validar_email(input_text):
        resultado = analyze_text(input_text, tipo="email")
    else:
        print("[SecInbox] Entrada inválida. Forneça um link ou e-mail.")
        sys.exit(1)

    # Exibe o resultado
    if resultado["suspeito"]:
        print(f"[Alerta] Possível ameaça detectada: {resultado['motivo']}")
    else:
        print(f"[SEGURO] Nenhum sinal de phishing detectado.")

if __name__ == "__main__":
    main()