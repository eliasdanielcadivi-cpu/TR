#!/usr/bin/env python3
"""
Ingestor de archivos genéricos.

Procesa documentos de texto, markdown, código fuente, etc.
Extrae contenido, divide en chunks, y prepara para indexación.
"""

import os
import re
import hashlib
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import mimetypes

logger = logging.getLogger(__name__)


@dataclass
class DocumentChunk:
    """Chunk de documento procesado."""
    chunk_id: str
    doc_id: str
    content: str
    chunk_index: int
    start_line: int
    end_line: int
    char_count: int
    metadata: Dict[str, Any] = None


@dataclass
class ProcessedDocument:
    """Documento procesado completo."""
    doc_id: str
    source_path: str
    doc_type: str
    title: str
    summary: str
    total_chunks: int
    chunks: List[DocumentChunk]
    entities: List[Dict[str, Any]] = None
    processing_errors: List[str] = None


class FileIngestor:
    """
    Ingestor base para archivos de texto.

    Soporta:
    - Texto plano (.txt)
    - Markdown (.md)
    - Código fuente (.py, .js, .java, etc.)
    - Configuración (.yaml, .yml, .json)
    """

    # Extensiones soportadas
    SUPPORTED_EXTENSIONS = {
        '.txt': 'text',
        '.md': 'markdown',
        '.py': 'python',
        '.js': 'javascript',
        '.java': 'java',
        '.cpp': 'cpp',
        '.c': 'c',
        '.h': 'c_header',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.json': 'json',
        '.xml': 'xml',
        '.html': 'html',
        '.css': 'css',
        '.sql': 'sql',
        '.sh': 'shell',
        '.bash': 'shell',
        '.rs': 'rust',
        '.go': 'go',
        '.rb': 'ruby',
        '.php': 'php'
    }

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def can_process(self, file_path: str) -> bool:
        """Determinar si este ingestor puede procesar el archivo."""
        ext = Path(file_path).suffix.lower()
        return ext in self.SUPPORTED_EXTENSIONS

    def process(self, file_path: str, config: Dict[str, Any] = None) -> ProcessedDocument:
        """
        Procesar archivo completo.

        Args:
            file_path: Ruta al archivo a procesar
            config: Configuración adicional (opcional)

        Returns:
            Documento procesado con chunks y metadatos
        """
        config = config or {}
        logger.info(f"Procesando archivo: {file_path}")

        # Validar archivo
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Archivo no encontrado: {file_path}")

        # Determinar tipo de documento
        doc_type = self._detect_document_type(file_path)

        # Leer contenido
        content = self._read_file_content(file_path, doc_type)

        # Generar ID único del documento
        doc_id = self._generate_doc_id(file_path, content)

        # Extraer metadatos básicos
        title = self._extract_title(file_path, content, doc_type)
        summary = self._generate_summary(content, doc_type)

        # Dividir en chunks
        chunks = self._chunk_content(content, doc_id, doc_type, file_path)

        # Extraer entidades (si aplica)
        entities = self._extract_entities(content, doc_type, file_path)

        return ProcessedDocument(
            doc_id=doc_id,
            source_path=file_path,
            doc_type=doc_type,
            title=title,
            summary=summary,
            total_chunks=len(chunks),
            chunks=chunks,
            entities=entities,
            processing_errors=[]
        )

    def _detect_document_type(self, file_path: str) -> str:
        """Detectar tipo de documento basado en extensión."""
        ext = Path(file_path).suffix.lower()
        return self.SUPPORTED_EXTENSIONS.get(ext, 'unknown')

    def _read_file_content(self, file_path: str, doc_type: str) -> str:
        """Leer contenido del archivo con codificación apropiada."""
        try:
            # Para archivos de texto, usar UTF-8
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            # Fallback a latin-1 si UTF-8 falla
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except Exception as e:
                logger.error(f"Error leyendo archivo {file_path}: {e}")
                raise
        except Exception as e:
            logger.error(f"Error abriendo archivo {file_path}: {e}")
            raise

    def _generate_doc_id(self, file_path: str, content: str) -> str:
        """Generar ID único para el documento."""
        # Usar hash de ruta + contenido para unicidad
        file_stat = os.stat(file_path)
        unique_string = f"{file_path}:{file_stat.st_size}:{file_stat.st_mtime}:{content[:1000]}"
        return hashlib.sha256(unique_string.encode()).hexdigest()[:32]

    def _extract_title(self, file_path: str, content: str, doc_type: str) -> str:
        """Extraer título del documento."""
        # Por defecto, usar nombre del archivo
        base_name = Path(file_path).stem

        # Para markdown, buscar primer heading
        if doc_type == 'markdown':
            match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if match:
                return match.group(1).strip()

        # Para código fuente, usar nombre del archivo sin extensión
        elif doc_type in ['python', 'javascript', 'java', 'cpp', 'rust', 'go']:
            # Si hay módulo/paquete, incluirlo
            if doc_type == 'python' and '__init__.py' not in file_path:
                return f"{base_name}.py"
            return base_name

        return base_name.replace('_', ' ').replace('-', ' ').title()

    def _generate_summary(self, content: str, doc_type: str) -> str:
        """Generar resumen automático del contenido."""
        # Para documentos largos, tomar primeras líneas
        lines = content.split('\n')
        preview_lines = []

        if doc_type == 'markdown':
            # Para markdown, extraer párrafos de texto (no código, no headers)
            for line in lines[:20]:
                line_stripped = line.strip()
                if line_stripped and not line_stripped.startswith('#') and not line_stripped.startswith('```'):
                    preview_lines.append(line_stripped)
                    if len(preview_lines) >= 3:
                        break
        elif doc_type in ['python', 'javascript', 'java', 'cpp']:
            # Para código, extraer comentarios y docstrings
            for line in lines[:30]:
                line_stripped = line.strip()
                if line_stripped.startswith('#') or line_stripped.startswith('//') or line_stripped.startswith('/*'):
                    preview_lines.append(line_stripped.replace('#', '').replace('//', '').strip())
                    if len(preview_lines) >= 3:
                        break
                elif '"""' in line or "'''" in line:
                    preview_lines.append(line.replace('"""', '').replace("'''", '').strip())
        else:
            # Para texto plano, primeras líneas no vacías
            for line in lines[:10]:
                if line.strip():
                    preview_lines.append(line.strip())
                    if len(preview_lines) >= 3:
                        break

        summary = ' '.join(preview_lines[:3])
        return (summary[:200] + '...') if len(summary) > 200 else summary

    def _chunk_content(self, content: str, doc_id: str, doc_type: str,
                      file_path: str) -> List[DocumentChunk]:
        """
        Dividir contenido en chunks inteligentes.

        Estrategias por tipo de documento:
        - Texto/Markdown: Por párrafos y límites de tamaño
        - Código: Por funciones/clases/métodos
        - Configuración: Por bloques lógicos
        """
        if doc_type in ['python', 'javascript', 'java', 'cpp', 'rust', 'go']:
            return self._chunk_code(content, doc_id, doc_type, file_path)
        elif doc_type == 'markdown':
            return self._chunk_markdown(content, doc_id, file_path)
        else:
            return self._chunk_generic_text(content, doc_id, file_path)

    def _chunk_generic_text(self, content: str, doc_id: str,
                           file_path: str) -> List[DocumentChunk]:
        """Chunking para texto genérico."""
        chunks = []
        lines = content.split('\n')
        current_chunk_lines = []
        current_char_count = 0
        chunk_index = 0
        start_line = 0

        for i, line in enumerate(lines):
            line_length = len(line) + 1  # +1 por newline

            # Si agregar esta línea excede el tamaño del chunk (y ya tenemos contenido)
            if (current_char_count + line_length > self.chunk_size and
                current_char_count > 0):

                # Crear chunk actual
                chunk_content = '\n'.join(current_chunk_lines)
                chunk_id = f"{doc_id}_chunk{chunk_index}"

                chunks.append(DocumentChunk(
                    chunk_id=chunk_id,
                    doc_id=doc_id,
                    content=chunk_content,
                    chunk_index=chunk_index,
                    start_line=start_line,
                    end_line=i - 1,
                    char_count=current_char_count,
                    metadata={'file_path': file_path}
                ))

                # Preparar siguiente chunk con overlap
                chunk_index += 1
                overlap_lines = current_chunk_lines[-self._get_overlap_lines(current_chunk_lines):]
                current_chunk_lines = overlap_lines.copy()
                current_char_count = sum(len(l) + 1 for l in overlap_lines)
                start_line = i - len(overlap_lines)

            # Agregar línea al chunk actual
            current_chunk_lines.append(line)
            current_char_count += line_length

        # Agregar último chunk si hay contenido
        if current_chunk_lines:
            chunk_content = '\n'.join(current_chunk_lines)
            chunk_id = f"{doc_id}_chunk{chunk_index}"

            chunks.append(DocumentChunk(
                chunk_id=chunk_id,
                doc_id=doc_id,
                content=chunk_content,
                chunk_index=chunk_index,
                start_line=start_line,
                end_line=len(lines) - 1,
                char_count=current_char_count,
                metadata={'file_path': file_path}
            ))

        return chunks

    def _chunk_markdown(self, content: str, doc_id: str,
                       file_path: str) -> List[DocumentChunk]:
        """Chunking para markdown (respetando estructura)."""
        chunks = []
        lines = content.split('\n')
        current_chunk_lines = []
        current_char_count = 0
        chunk_index = 0
        start_line = 0
        in_code_block = False

        for i, line in enumerate(lines):
            line_length = len(line) + 1

            # Detectar bloques de código
            if line.strip().startswith('```'):
                in_code_block = not in_code_block

            # Puntos de ruptura naturales en markdown
            is_heading = line.strip().startswith('#') and not in_code_block
            is_horizontal_rule = line.strip() in ['---', '***', '___'] and not in_code_block

            # Crear chunk en puntos naturales o si excede tamaño
            should_break = (is_heading and current_char_count > self.chunk_size * 0.3 or
                          is_horizontal_rule or
                          (current_char_count + line_length > self.chunk_size and
                           current_char_count > 0 and not in_code_block))

            if should_break and current_chunk_lines:
                chunk_content = '\n'.join(current_chunk_lines)
                chunk_id = f"{doc_id}_chunk{chunk_index}"

                chunks.append(DocumentChunk(
                    chunk_id=chunk_id,
                    doc_id=doc_id,
                    content=chunk_content,
                    chunk_index=chunk_index,
                    start_line=start_line,
                    end_line=i - 1,
                    char_count=current_char_count,
                    metadata={
                        'file_path': file_path,
                        'contains_heading': any(l.strip().startswith('#') for l in current_chunk_lines),
                        'in_code_block': in_code_block
                    }
                ))

                chunk_index += 1
                # Overlap: mantener últimas líneas para contexto
                overlap_lines = current_chunk_lines[-self._get_overlap_lines(current_chunk_lines):]
                current_chunk_lines = overlap_lines.copy()
                current_char_count = sum(len(l) + 1 for l in overlap_lines)
                start_line = i - len(overlap_lines)

            current_chunk_lines.append(line)
            current_char_count += line_length

        # Último chunk
        if current_chunk_lines:
            chunk_content = '\n'.join(current_chunk_lines)
            chunk_id = f"{doc_id}_chunk{chunk_index}"

            chunks.append(DocumentChunk(
                chunk_id=chunk_id,
                doc_id=doc_id,
                content=chunk_content,
                chunk_index=chunk_index,
                start_line=start_line,
                end_line=len(lines) - 1,
                char_count=current_char_count,
                metadata={
                    'file_path': file_path,
                    'contains_heading': any(l.strip().startswith('#') for l in current_chunk_lines),
                    'in_code_block': in_code_block
                }
            ))

        return chunks

    def _chunk_code(self, content: str, doc_id: str, doc_type: str,
                   file_path: str) -> List[DocumentChunk]:
        """Chunking para código fuente (por funciones/clases)."""
        # Implementación simplificada
        # En producción, usar AST para mejores resultados
        chunks = []

        if doc_type == 'python':
            chunks = self._chunk_python_code(content, doc_id, file_path)
        else:
            # Para otros lenguajes, usar estrategia genérica con rupturas por funciones
            chunks = self._chunk_generic_code(content, doc_id, doc_type, file_path)

        return chunks

    def _chunk_python_code(self, content: str, doc_id: str,
                          file_path: str) -> List[DocumentChunk]:
        """Chunking específico para Python usando heurísticas simples."""
        chunks = []
        lines = content.split('\n')
        current_chunk_lines = []
        current_char_count = 0
        chunk_index = 0
        start_line = 0
        indent_level = 0
        in_docstring = False
        in_multiline_string = False

        for i, line in enumerate(lines):
            line_length = len(line) + 1
            stripped = line.strip()

            # Detectar docstrings y strings multilínea
            if '"""' in line or "'''" in line:
                if line.count('"""') == 1 or line.count("'''") == 1:
                    in_multiline_string = not in_multiline_string
                    if stripped.startswith('"""') or stripped.startswith("'''"):
                        in_docstring = not in_docstring

            # Puntos de ruptura naturales en Python
            is_def = stripped.startswith('def ') and not in_multiline_string
            is_class = stripped.startswith('class ') and not in_multiline_string
            is_import = stripped.startswith(('import ', 'from ')) and not in_multiline_string
            is_empty = not stripped and not in_multiline_string

            # Calcular nivel de indentación (para funciones anidadas)
            if stripped and not in_multiline_string:
                current_indent = len(line) - len(line.lstrip())
                if current_indent == 0:  # Nivel de módulo
                    indent_level = 0
                else:
                    indent_level = current_indent // 4  # Asumiendo 4 espacios por indent

            # Crear chunk en puntos naturales
            should_break = ((is_def or is_class or is_import) and
                          current_char_count > self.chunk_size * 0.2 and
                          not in_multiline_string)

            if should_break and current_chunk_lines:
                chunk_content = '\n'.join(current_chunk_lines)
                chunk_id = f"{doc_id}_chunk{chunk_index}"

                chunks.append(DocumentChunk(
                    chunk_id=chunk_id,
                    doc_id=doc_id,
                    content=chunk_content,
                    chunk_index=chunk_index,
                    start_line=start_line,
                    end_line=i - 1,
                    char_count=current_char_count,
                    metadata={
                        'file_path': file_path,
                        'contains_def': any('def ' in l for l in current_chunk_lines),
                        'contains_class': any('class ' in l for l in current_chunk_lines),
                        'indent_level': indent_level
                    }
                ))

                chunk_index += 1
                # Overlap mínimo para código
                overlap_lines = current_chunk_lines[-2:]  # Solo 2 líneas para contexto
                current_chunk_lines = overlap_lines.copy()
                current_char_count = sum(len(l) + 1 for l in overlap_lines)
                start_line = i - len(overlap_lines)

            current_chunk_lines.append(line)
            current_char_count += line_length

        # Último chunk
        if current_chunk_lines:
            chunk_content = '\n'.join(current_chunk_lines)
            chunk_id = f"{doc_id}_chunk{chunk_index}"

            chunks.append(DocumentChunk(
                chunk_id=chunk_id,
                doc_id=doc_id,
                content=chunk_content,
                chunk_index=chunk_index,
                start_line=start_line,
                end_line=len(lines) - 1,
                char_count=current_char_count,
                metadata={
                    'file_path': file_path,
                    'contains_def': any('def ' in l for l in current_chunk_lines),
                    'contains_class': any('class ' in l for l in current_chunk_lines),
                    'indent_level': indent_level
                }
            ))

        return chunks

    def _chunk_generic_code(self, content: str, doc_id: str, doc_type: str,
                           file_path: str) -> List[DocumentChunk]:
        """Chunking genérico para otros lenguajes de programación."""
        # Similar a Python pero con detección de funciones basada en llaves/parentesis
        return self._chunk_generic_text(content, doc_id, file_path)

    def _get_overlap_lines(self, lines: List[str]) -> int:
        """Calcular número de líneas para overlap basado en contenido."""
        if not lines:
            return 0

        # Calcular líneas necesarias para alcanzar overlap en caracteres
        target_chars = self.chunk_overlap
        current_chars = 0
        overlap_lines = 0

        for line in reversed(lines):
            current_chars += len(line) + 1
            overlap_lines += 1
            if current_chars >= target_chars:
                break

        return min(overlap_lines, len(lines) // 2)  # Máximo la mitad del chunk

    def _extract_entities(self, content: str, doc_type: str,
                         file_path: str) -> List[Dict[str, Any]]:
        """Extraer entidades nombradas del contenido."""
        entities = []

        # Para código Python, extraer nombres de funciones y clases
        if doc_type == 'python':
            # Patrones simples para funciones y clases
            function_pattern = r'def\s+(\w+)\s*\('
            class_pattern = r'class\s+(\w+)\s*(?:\(|:)'

            for match in re.finditer(function_pattern, content):
                entities.append({
                    'name': match.group(1),
                    'entity_type': 'function',
                    'source': file_path,
                    'context': 'Python function definition'
                })

            for match in re.finditer(class_pattern, content):
                entities.append({
                    'name': match.group(1),
                    'entity_type': 'class',
                    'source': file_path,
                    'context': 'Python class definition'
                })

        # Para markdown, extraer títulos y enlaces
        elif doc_type == 'markdown':
            heading_pattern = r'^#+\s+(.+)$'

            for match in re.finditer(heading_pattern, content, re.MULTILINE):
                entities.append({
                    'name': match.group(1).strip(),
                    'entity_type': 'heading',
                    'source': file_path,
                    'context': 'Markdown heading'
                })

        # Para otros tipos, extraer palabras en mayúsculas (potenciales acrónimos)
        else:
            acronym_pattern = r'\b[A-Z]{2,}\b'

            for match in re.finditer(acronym_pattern, content):
                entities.append({
                    'name': match.group(0),
                    'entity_type': 'acronym',
                    'source': file_path,
                    'context': 'Potential acronym'
                })

        return entities