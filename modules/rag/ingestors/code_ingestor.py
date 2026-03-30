#!/usr/bin/env python3
"""
Ingestor especializado para código fuente.

Usa AST (Abstract Syntax Tree) para análisis estructural de código.
Extrae funciones, clases, métodos, imports y relaciones entre ellos.
"""

import ast
import os
import re
import logging
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass, field
from pathlib import Path

from .file_ingestor import FileIngestor, ProcessedDocument, DocumentChunk

logger = logging.getLogger(__name__)


@dataclass
class CodeEntity:
    """Entidad de código extraída del AST."""
    name: str
    entity_type: str  # 'function', 'class', 'method', 'module', 'import'
    source_file: str
    line_start: int
    line_end: int
    docstring: Optional[str] = None
    parent: Optional[str] = None  # Para métodos dentro de clases
    dependencies: List[str] = field(default_factory=list)  # Imports/llamadas
    complexity: int = 1  # Métrica simple de complejidad


@dataclass
class CodeRelationship:
    """Relación entre entidades de código."""
    from_entity: str
    to_entity: str
    relation_type: str  # 'imports', 'calls', 'inherits', 'contains'
    line_number: Optional[int] = None
    confidence: float = 1.0


class CodeIngestor(FileIngestor):
    """
    Ingestor especializado para código fuente.

    Características:
    - Análisis AST para Python
    - Extracción estructural de entidades
    - Detección de relaciones (imports, llamadas)
    - Chunking basado en estructura lógica
    """

    # Lenguajes soportados con análisis AST
    AST_SUPPORTED_LANGUAGES = ['python']

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        super().__init__(chunk_size, chunk_overlap)

    def can_process(self, file_path: str) -> bool:
        """Determinar si este ingestor puede procesar el archivo."""
        ext = Path(file_path).suffix.lower()
        doc_type = self.SUPPORTED_EXTENSIONS.get(ext, 'unknown')
        return doc_type in self.AST_SUPPORTED_LANGUAGES

    def process(self, file_path: str, config: Dict[str, Any] = None) -> ProcessedDocument:
        """
        Procesar archivo de código con análisis AST.

        Args:
            file_path: Ruta al archivo de código
            config: Configuración adicional

        Returns:
            Documento procesado con análisis estructural
        """
        config = config or {}
        logger.info(f"Procesando código con AST: {file_path}")

        # Primero procesar como archivo normal
        base_document = super().process(file_path, config)

        # Análisis AST para Python
        if base_document.doc_type == 'python':
            ast_analysis = self._analyze_python_ast(file_path)
            base_document.entities = self._enhance_entities_with_ast(
                base_document.entities or [], ast_analysis
            )

            # Agregar relaciones de AST al metadata
            for chunk in base_document.chunks:
                if chunk.metadata is None:
                    chunk.metadata = {}
                chunk.metadata['ast_entities'] = self._get_entities_in_chunk(
                    chunk, ast_analysis.entities
                )

        return base_document

    def _analyze_python_ast(self, file_path: str) -> 'ASTAnalysisResult':
        """Analizar archivo Python usando AST."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            tree = ast.parse(content, filename=file_path)

            analyzer = PythonASTAnalyzer(file_path)
            analyzer.visit(tree)

            return ASTAnalysisResult(
                entities=analyzer.entities,
                relationships=analyzer.relationships,
                imports=analyzer.imports,
                parse_success=True
            )

        except SyntaxError as e:
            logger.warning(f"Error de sintaxis en {file_path}: {e}")
            return ASTAnalysisResult(
                entities=[],
                relationships=[],
                imports=[],
                parse_success=False,
                error_message=str(e)
            )
        except Exception as e:
            logger.error(f"Error analizando AST de {file_path}: {e}")
            return ASTAnalysisResult(
                entities=[],
                relationships=[],
                imports=[],
                parse_success=False,
                error_message=str(e)
            )

    def _enhance_entities_with_ast(self, base_entities: List[Dict[str, Any]],
                                 ast_analysis: 'ASTAnalysisResult') -> List[Dict[str, Any]]:
        """Mejorar entidades extraídas con información del AST."""
        enhanced_entities = base_entities.copy()

        for ast_entity in ast_analysis.entities:
            # Buscar entidad correspondiente en base_entities
            existing_entity = None
            for entity in enhanced_entities:
                if entity.get('name') == ast_entity.name and entity.get('entity_type') == ast_entity.entity_type:
                    existing_entity = entity
                    break

            if existing_entity:
                # Mejorar entidad existente
                existing_entity.update({
                    'line_start': ast_entity.line_start,
                    'line_end': ast_entity.line_end,
                    'docstring': ast_entity.docstring,
                    'parent': ast_entity.parent,
                    'dependencies': ast_entity.dependencies,
                    'complexity': ast_entity.complexity,
                    'ast_analyzed': True
                })
            else:
                # Agregar nueva entidad del AST
                enhanced_entities.append({
                    'name': ast_entity.name,
                    'entity_type': ast_entity.entity_type,
                    'source': ast_entity.source_file,
                    'context': f'Python {ast_entity.entity_type} (AST analyzed)',
                    'line_start': ast_entity.line_start,
                    'line_end': ast_entity.line_end,
                    'docstring': ast_entity.docstring,
                    'parent': ast_entity.parent,
                    'dependencies': ast_entity.dependencies,
                    'complexity': ast_entity.complexity,
                    'ast_analyzed': True
                })

        return enhanced_entities

    def _get_entities_in_chunk(self, chunk: DocumentChunk,
                             ast_entities: List[CodeEntity]) -> List[Dict[str, Any]]:
        """Obtener entidades AST que están dentro de un chunk."""
        entities_in_chunk = []

        for entity in ast_entities:
            # Verificar si la entidad está dentro del rango de líneas del chunk
            if (entity.line_start >= chunk.start_line and
                entity.line_end <= chunk.end_line):
                entities_in_chunk.append({
                    'name': entity.name,
                    'type': entity.entity_type,
                    'lines': f"{entity.line_start}-{entity.line_end}"
                })

        return entities_in_chunk

    def _chunk_code(self, content: str, doc_id: str, doc_type: str,
                   file_path: str) -> List[DocumentChunk]:
        """Chunking mejorado para código usando análisis estructural."""
        if doc_type == 'python':
            # Intentar usar chunking basado en AST
            try:
                ast_analysis = self._analyze_python_ast(file_path)
                if ast_analysis.parse_success and ast_analysis.entities:
                    return self._chunk_by_ast_entities(content, doc_id, file_path, ast_analysis.entities)
            except Exception as e:
                logger.warning(f"No se pudo usar chunking por AST, usando heurístico: {e}")

        # Fallback a chunking heurístico del padre
        return super()._chunk_code(content, doc_id, doc_type, file_path)

    def _chunk_by_ast_entities(self, content: str, doc_id: str, file_path: str,
                             entities: List[CodeEntity]) -> List[DocumentChunk]:
        """Crear chunks basados en entidades AST (funciones, clases)."""
        chunks = []
        lines = content.split('\n')

        # Ordenar entidades por línea de inicio
        sorted_entities = sorted(entities, key=lambda e: e.line_start)

        for i, entity in enumerate(sorted_entities):
            # Determinar rango de líneas para este chunk
            start_line = entity.line_start - 1  # AST usa 1-based, nosotros 0-based
            end_line = entity.line_end - 1

            # Incluir algunas líneas de contexto antes y después
            context_before = 3
            context_after = 3

            chunk_start = max(0, start_line - context_before)
            chunk_end = min(len(lines) - 1, end_line + context_after)

            # Si este chunk se solapa con el anterior, fusionar
            if chunks and chunk_start <= chunks[-1].end_line:
                last_chunk = chunks[-1]
                chunk_start = last_chunk.start_line
                chunk_content = '\n'.join(lines[chunk_start:chunk_end + 1])
                last_chunk.content = chunk_content
                last_chunk.end_line = chunk_end
                last_chunk.char_count = len(chunk_content)
                continue

            # Extraer contenido del chunk
            chunk_content = '\n'.join(lines[chunk_start:chunk_end + 1])
            chunk_id = f"{doc_id}_entity_{i}"

            chunks.append(DocumentChunk(
                chunk_id=chunk_id,
                doc_id=doc_id,
                content=chunk_content,
                chunk_index=i,
                start_line=chunk_start,
                end_line=chunk_end,
                char_count=len(chunk_content),
                metadata={
                    'file_path': file_path,
                    'entity_name': entity.name,
                    'entity_type': entity.entity_type,
                    'entity_lines': f"{entity.line_start}-{entity.line_end}",
                    'parent': entity.parent,
                    'ast_based': True
                }
            ))

        # Si no hay entidades AST, crear un chunk con todo el contenido
        if not chunks:
            return super()._chunk_generic_text(content, doc_id, file_path)

        return chunks


@dataclass
class ASTAnalysisResult:
    """Resultado del análisis AST."""
    entities: List[CodeEntity]
    relationships: List[CodeRelationship]
    imports: List[str]
    parse_success: bool
    error_message: Optional[str] = None


class PythonASTAnalyzer(ast.NodeVisitor):
    """Visitor de AST para análisis de código Python."""

    def __init__(self, source_file: str):
        self.source_file = source_file
        self.entities: List[CodeEntity] = []
        self.relationships: List[CodeRelationship] = []
        self.imports: List[str] = []
        self.current_class: Optional[str] = None
        self._entity_stack: List[CodeEntity] = []

    def visit_Module(self, node):
        """Visitar módulo."""
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        """Visitar definición de clase."""
        # Extraer docstring
        docstring = ast.get_docstring(node)

        class_entity = CodeEntity(
            name=node.name,
            entity_type='class',
            source_file=self.source_file,
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            docstring=docstring,
            parent=None,
            complexity=self._calculate_complexity(node)
        )

        # Relaciones de herencia
        for base in node.bases:
            if isinstance(base, ast.Name):
                self.relationships.append(CodeRelationship(
                    from_entity=node.name,
                    to_entity=base.id,
                    relation_type='inherits',
                    line_number=node.lineno
                ))

        self.entities.append(class_entity)

        # Entrar al contexto de la clase
        previous_class = self.current_class
        self.current_class = node.name
        self._entity_stack.append(class_entity)

        self.generic_visit(node)

        # Salir del contexto
        self._entity_stack.pop()
        self.current_class = previous_class

    def visit_FunctionDef(self, node):
        """Visitar definición de función/método."""
        docstring = ast.get_docstring(node)

        # Determinar si es función o método
        entity_type = 'method' if self.current_class else 'function'
        parent = self.current_class

        func_entity = CodeEntity(
            name=node.name,
            entity_type=entity_type,
            source_file=self.source_file,
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            docstring=docstring,
            parent=parent,
            complexity=self._calculate_complexity(node)
        )

        # Analizar llamadas dentro de la función
        self._analyze_function_calls(node, node.name)

        self.entities.append(func_entity)
        self._entity_stack.append(func_entity)

        self.generic_visit(node)

        self._entity_stack.pop()

    def visit_AsyncFunctionDef(self, node):
        """Visitar definición de función asíncrona."""
        self.visit_FunctionDef(node)  # Mismo tratamiento

    def visit_Import(self, node):
        """Visitar import."""
        for alias in node.names:
            self.imports.append(alias.name)

            # Relación de import
            current_entity = self._entity_stack[-1] if self._entity_stack else None
            if current_entity:
                self.relationships.append(CodeRelationship(
                    from_entity=current_entity.name,
                    to_entity=alias.name,
                    relation_type='imports',
                    line_number=node.lineno
                ))

        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """Visitar import from."""
        module = node.module or ''
        for alias in node.names:
            full_name = f"{module}.{alias.name}" if module else alias.name
            self.imports.append(full_name)

            current_entity = self._entity_stack[-1] if self._entity_stack else None
            if current_entity:
                self.relationships.append(CodeRelationship(
                    from_entity=current_entity.name,
                    to_entity=full_name,
                    relation_type='imports',
                    line_number=node.lineno
                ))

        self.generic_visit(node)

    def _analyze_function_calls(self, node: ast.AST, caller_name: str):
        """Analizar llamadas a funciones dentro de un nodo."""
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                # Extraer nombre de la función llamada
                callee_name = self._extract_callee_name(child)

                if callee_name and callee_name != caller_name:
                    self.relationships.append(CodeRelationship(
                        from_entity=caller_name,
                        to_entity=callee_name,
                        relation_type='calls',
                        line_number=child.lineno if hasattr(child, 'lineno') else None
                    ))

    def _extract_callee_name(self, call_node: ast.Call) -> Optional[str]:
        """Extraer nombre de función de un nodo Call."""
        if isinstance(call_node.func, ast.Name):
            return call_node.func.id
        elif isinstance(call_node.func, ast.Attribute):
            # Para métodos: obj.metodo
            return call_node.func.attr
        elif isinstance(call_node.func, ast.Subscript):
            # Para llamadas con subíndice: func[arg]
            return None
        return None

    def _calculate_complexity(self, node: ast.AST) -> int:
        """Calcular complejidad simple de un nodo."""
        complexity = 1

        # Contar estructuras de control
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try,
                                ast.ExceptHandler, ast.With)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
            elif isinstance(child, ast.Compare):
                complexity += len(child.ops)

        return complexity