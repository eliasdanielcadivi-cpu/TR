import asyncio
from typing import List, Optional
from functools import wraps

# Decorador táctico ARES
def tactical_trace(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        print(f"--- Tactical Execution: {func.__name__} ---")
        return await func(*args, **kwargs)
    return wrapper

class McatOrchestrator:
    """Orquestador de demostración de Mcat en ARES."""

    def __init__(self, provider: str = "gemma3"):
        self.provider = provider
        self.history: List[str] = []

    @tactical_trace
    async def run_protocol(self, command: str) -> Optional[str]:
        """Ejecución de un protocolo de demo."""
        await asyncio.sleep(0.5)
        result = f"Command '{command}' executed via {self.provider}"
        self.history.append(result)
        return result

    def list_history(self):
        """Lista el historial de ejecuciones."""
        for i, entry in enumerate(self.history):
            print(f"[{i}] {entry}")

if __name__ == "__main__":
    orchestrator = McatOrchestrator()
    asyncio.run(orchestrator.run_protocol("mcat --help"))
    orchestrator.list_history()
