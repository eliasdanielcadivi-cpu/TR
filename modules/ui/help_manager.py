"""HelpManager: Gestor de ayuda y consultas a IA para ARES.

Soporta:
- Consultas a IA con templates y aliases
- Ayuda navegable con Broot
- Listado de templates y modelos disponibles

Filosofía atómica: máximo 3 funciones públicas principales.
"""

import os
import sys
import subprocess
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


class HelpManager:
    """Gestor de ayuda y consultas a IA."""

    def __init__(self, context):
        """Inicializar HelpManager.
        
        Args:
            context: Contexto de ARES con config y base_path.
        """
        self.ctx = context
        self.docs_path = os.path.join(self.ctx.base_path, "docs")
        self._ai_engine = None

    def show_help(self) -> None:
        """Muestra ayuda navegable con Broot o fallback a less."""
        help_file = os.path.join(self.docs_path, "HELP.md")

        console.print(f"[bold cyan]🛰  Ayuda Inteligente de ARES[/bold cyan]")
        console.print(f"[dim]Ubicación: {self.docs_path}[/dim]")
        console.print("")

        if subprocess.run(["which", "broot"], capture_output=True).returncode == 0:
            subprocess.run(["broot", self.docs_path])
        elif os.path.exists(help_file):
            console.print("[yellow]⚠ Broot no disponible, mostrando HELP.md[/yellow]")
            subprocess.run(["less", "-R", help_file])
        else:
            console.print("[red]✗ No se encontró HELP.md[/red]")

    def query_ai(self, prompt: str, model_alias: Optional[str] = None,
                 template: Optional[str] = None, **kwargs) -> None:
        """Consulta al motor de IA.
        
        Args:
            prompt: Prompt de entrada.
            model_alias: Alias de modelo (gemma, deepseek, etc.).
            template: Nombre de plantilla YAML.
            **kwargs: Parámetros adicionales.
        """
        ai = self._get_ai_engine()

        if not sys.stdout.isatty():
            # Modo no interactivo (pipe, script)
            response = ai.ask(prompt, model_alias=model_alias, template=template, **kwargs)
            print(response)
            return

        # Modo interactivo con status
        model_info = f" [{model_alias or 'default'}]" if model_alias else ""
        if template:
            model_info += f" --template {template}"
        
        with console.status(f"[bold blue] ARES pensando{model_info}..."):
            response = ai.ask(prompt, model_alias=model_alias, template=template, **kwargs)

        console.print(Panel(response, title="ARES", border_style="green"))

    def list_models(self) -> None:
        """Listar modelos disponibles por provider."""
        ai = self._get_ai_engine()
        models = ai.list_models()

        table = Table(title="📦 Modelos Disponibles")
        table.add_column("Provider", style="cyan")
        table.add_column("Modelos", style="green")

        for provider, model_list in models.items():
            table.add_row(provider, ", ".join(model_list))

        console.print(table)

    def list_templates(self, provider: Optional[str] = None) -> None:
        """Listar plantillas disponibles.
        
        Args:
            provider: Filtrar por provider (opcional).
        """
        ai = self._get_ai_engine()
        templates = ai.list_templates(provider)

        table = Table(title="📄 Plantillas YAML Disponibles")
        table.add_column("Plantilla", style="cyan")
        table.add_column("Provider", style="green")
        table.add_column("Descripción", style="yellow")

        for tmpl in templates:
            parts = tmpl.split("/")
            provider_name = parts[0] if len(parts) > 1 else "gemma"
            template_name = parts[1] if len(parts) > 1 else parts[0]
            
            # Obtener descripción desde config
            desc = self._get_template_description(provider_name, template_name)
            
            table.add_row(template_name, provider_name, desc)

        console.print(table)

    def list_tools(self) -> None:
        """Listar herramientas disponibles."""
        ai = self._get_ai_engine()
        tools = ai.list_tools()

        table = Table(title="🛠️  Herramientas Disponibles")
        table.add_column("Nombre", style="cyan")
        table.add_column("Descripción", style="green")

        for tool in tools:
            table.add_row(tool.get("name", ""), tool.get("description", ""))

        console.print(table)

    def show_config(self) -> None:
        """Mostrar configuración actual de IA y del sistema ARES."""
        ai_config = self.ctx.config.get("ai", {})
        kitty_config = self.ctx.config.get("kitty", {})
        identity = self.ctx.config.get("identity", {})
        
        # Panel de Identidad y Sockets
        sys_info = (
            f"[bold cyan]Identidad:[/bold cyan] {identity.get('window_title', 'ARES')}\n"
            f"[bold cyan]Socket Kitty:[/bold cyan] {self.ctx.socket}\n"
            f"[bold cyan]Socket Path:[/bold cyan] {self.ctx.socket_path}\n"
        )
        
        # Panel de IA
        ai_info = (
            f"[bold green]Provider Activo:[/bold green] {ai_config.get('default_provider', 'gemma')}\n"
            f"[bold green]Gemma (Ollama):[/bold green] {ai_config.get('gemma', {}).get('model', 'gemma3:4b')}\n"
            f"[bold green]DeepSeek API:[/bold green] {ai_config.get('deepseek', {}).get('model', 'deepseek-chat')}\n"
            f"[bold green]OpenRouter:[/bold green] {ai_config.get('openrouter', {}).get('model', 'n/a')}\n"
        )
        
        table = Table.grid(expand=True)
        table.add_column(style="dim")
        table.add_row(Panel(sys_info, title="🛰️ Sistema", border_style="cyan"))
        table.add_row(Panel(ai_info, title="🤖 Inteligencia Artificial", border_style="green"))
        
        console.print(Panel(table, title="⚙️ CONFIGURACIÓN GLOBAL ARES", border_style="white"))

    def _get_ai_engine(self):
        """Obtener instancia de AIEngine (lazy loading)."""
        if self._ai_engine is None:
            from modules.ia.ai_engine import AIEngine
            self._ai_engine = AIEngine(
                self.ctx.config.get("ai", {}),
                self.ctx.base_path
            )
        return self._ai_engine

    def _get_template_description(self, provider: str, name: str) -> str:
        """Obtener descripción de plantilla desde config.
        
        Args:
            provider: Nombre del provider.
            name: Nombre de la plantilla.
            
        Returns:
            Descripción o string por defecto.
        """
        templates_config = self.ctx.config.get("templates", {})
        provider_templates = templates_config.get(provider, [])
        
        for tmpl in provider_templates:
            if tmpl.get("name") == name:
                return tmpl.get("description", "Sin descripción")
        
        return "Plantilla personalizada"
