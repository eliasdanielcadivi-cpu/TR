# 🤖 Ares Messenger - Módulo de Comunicación Atómica
# Este módulo centraliza los avisos al usuario y prepara la interfaz para la carita reactiva.

import click

def warn(message: str):
    """Aviso preventivo (ej: Ollama no corre)."""
    click.echo(click.style(f"⚠️  ARES: {message}", fg="yellow", bold=True))

def error(message: str):
    """Fallo crítico en la ejecución."""
    click.echo(click.style(f"❌ ARES ERROR: {message}", fg="red", bold=True))

def success(message: str):
    """Logro completado."""
    click.echo(click.style(f"✅ ARES: {message}", fg="green", bold=True))

def info(message: str):
    """Información de contexto o progreso."""
    click.echo(click.style(f"ℹ️  ARES: {message}", fg="cyan"))
