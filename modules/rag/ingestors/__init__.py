"""Ingestores de documentos y constructores de grafo."""

from .file_ingestor import FileIngestor
from .code_ingestor import CodeIngestor
from .graph_builder import GraphBuilder
from typing import Dict, Any, Optional


def get_ingestor_for(file_path: str, doc_type: Optional[str] = None) -> Any:
    """
    Factory para obtener el ingestor apropiado.
    
    Args:
        file_path: Ruta del archivo a procesar
        doc_type: Tipo de documento (opcional, para override)
        
    Returns:
        Instancia del ingestor apropiado
    """
    from pathlib import Path
    
    if doc_type == 'code' or doc_type == 'python':
        return CodeIngestor()
    
    # Detectar automático por extensión
    ext = Path(file_path).suffix.lower()
    
    # Código Python usa CodeIngestor
    if ext == '.py':
        return CodeIngestor()
    
    # Todo lo demás usa FileIngestor
    return FileIngestor()


__all__ = ["FileIngestor", "CodeIngestor", "GraphBuilder", "get_ingestor_for"]