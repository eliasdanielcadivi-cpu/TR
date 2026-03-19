import os
import sys

def imprimir_bonito(titulo, valor):
    if not valor:
        valor = "[VACÍO/NULL]"
    # Si es una clave larga, la censuramos visualmente
    if len(valor) > 20 and "sk-" in valor:
        valor = f"{valor[:6]}...{valor[-4:]}"
    print(f"{titulo:<30}: {valor}")

print("\n" + "="*60)
print(f"REPORTANDO DESDE EL PROCESO: {sys.argv[0]}")
print("="*60)

variables_clave = [
    "ANTHROPIC_BASE_URL",
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_MODEL",
    "ANTHROPIC_DEFAULT_SONNET_MODEL",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC"
]

print("Estado de las Variables de Entorno:\n")

for var in variables_clave:
    val = os.environ.get(var)
    imprimir_bonito(var, val)

print("="*60 + "\n")