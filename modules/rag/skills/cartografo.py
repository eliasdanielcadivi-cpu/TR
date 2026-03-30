#!/usr/bin/env python3
"""
Skill Cartógrafo para gestión conversacional del grafo de conocimiento.

Implementa el Anexo H: Negociación conversacional de grafos.
Se activa vía: ares rag cartografo o trigger semántico en ares i
"""

import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class GraphProposal:
    """Propuesta de cambio en el grafo."""
    action: str  # 'CONNECT', 'DISCONNECT', 'UPDATE'
    target: str
    suggested_parent: Optional[str] = None
    relation: Optional[str] = None
    criticality: str = "C1"
    requires_approval: bool = False
    reason: Optional[str] = None


class SkillCartografoRAG:
    """
    Skill conversacional para gestión del grafo de conocimiento.

    Características:
    - Diagnóstico de inconsistencias (nodos huérfanos, conflictos)
    - Propuestas de cambios con validación C1-C4
    - Negociación conversacional con confirmación explícita
    - Aplicación transaccional de cambios
    """

    SYSTEM_PROMPT = """Eres el Cartógrafo de Conocimiento de ARES.
    Modo: Negociación supervisada de relaciones C1-C4.

    Comandos disponibles:
    - "mapear [archivo/proyecto]" → Analizar y proponer entidades/relaciones
    - "validar pendientes" → Mostrar relaciones C2-C4 por aprobar
    - "conectar X con Y" → Proponer relación específica
    - "grafo de [entidad]" → Visualizar vecindad en grafo
    - "salir" → Volver a ARES normal

    Reglas:
    1. Nunca modificar el grafo sin confirmación explícita (sí/no)
    2. Relaciones C3/C4 (seguridad/integridad) requieren doble confirmación
    3. Presentar cambios como diff antes de aplicar
    4. Usar emojis ⚠️ para alertas de criticidad
    """

    def __init__(self, graph_engine, relation_guard):
        """
        Inicializar skill Cartógrafo.

        Args:
            graph_engine: Instancia de GraphEngine para acceso al grafo
            relation_guard: Instancia de RelationGuard para validación
        """
        self.graph = graph_engine
        self.guard = relation_guard

    def handle_intent(self, user_input: str, current_context: dict) -> dict:
        """
        Punto de entrada cuando el usuario entra al modo cartógrafo
        (vía trigger semántico: 'estoy perdido', 'cartografiar', etc.)

        Args:
            user_input: Texto de entrada del usuario
            current_context: Contexto actual (proyecto, sesión, etc.)

        Returns:
            Dict con diagnóstico y propuestas iniciales
        """
        logger.info(f"Cartógrafo: manejando intención: {user_input}")

        # Diagnóstico inicial
        orphan_nodes = self._find_orphan_nodes(current_context.get("project"))
        conflicts = self._detect_conflicts()

        response = {
            "mode": "CARTOGRAFO",
            "diagnosis": {
                "orphan_count": len(orphan_nodes),
                "conflicts": conflicts,
                "current_map": self._get_local_subgraph(current_context)
            },
            "proposals": []
        }

        # Generar propuestas solo si hay problemas
        if orphan_nodes:
            for node in orphan_nodes:
                proposal = self._suggest_parent_for_orphan(node)
                if proposal:
                    response["proposals"].append(asdict(proposal))

        return response

    def run_interactive(self):
        """
        Loop conversacional integrado con ares i.

        Implementación básica para demostración.
        En producción usaría el mismo sistema de streaming que ares i.
        """
        print("🧭 Entrando en modo Cartógrafo...")
        print("Escribe 'salir' para volver a ARES normal")
        print("Comandos: mapear, validar, conectar, grafo")
        print()

        context = {"project": None, "session": "interactive"}

        while True:
            try:
                user_input = input("🧭 Cartógrafo> ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ["salir", "exit", "quit"]:
                    print("Saliendo del modo Cartógrafo...")
                    break

                # Procesar comando
                result = self._process_command(user_input, context)

                # Mostrar resultado
                self._display_result(result)

            except KeyboardInterrupt:
                print("\nInterrupción detectada. Saliendo...")
                break
            except Exception as e:
                logger.error(f"Error en loop interactivo: {e}")
                print(f"⚠️ Error: {e}")

    def _process_command(self, command: str, context: dict) -> dict:
        """
        Procesar comando del usuario.

        Args:
            command: Comando/texto del usuario
            context: Contexto actual

        Returns:
            Dict con resultado del procesamiento
        """
        command_lower = command.lower()

        if command_lower.startswith("mapear"):
            return self._cmd_mapear(command, context)
        elif command_lower.startswith("validar"):
            return self._cmd_validar(command, context)
        elif command_lower.startswith("conectar"):
            return self._cmd_conectar(command, context)
        elif command_lower.startswith("grafo"):
            return self._cmd_grafo(command, context)
        else:
            # Intento de interpretación semántica
            return self._interpret_semantic(command, context)

    def _cmd_mapear(self, command: str, context: dict) -> dict:
        """Procesar comando 'mapear'."""
        target = command[7:].strip()  # Remover "mapear "

        if not target:
            return {"error": "Especifica qué quieres mapear (ej: 'mapear proyecto_x')"}

        # En un implementación real, aquí se analizaría el target
        # y se generarían propuestas de entidades/relaciones

        return {
            "action": "MAPEAR",
            "target": target,
            "message": f"Analizando '{target}' para proponer entidades y relaciones...",
            "suggestions": [
                "Identificar entidades principales",
                "Mapear dependencias",
                "Detectar nodos huérfanos"
            ]
        }

    def _cmd_validar(self, command: str, context: dict) -> dict:
        """Procesar comando 'validar pendientes'."""
        # Obtener relaciones pendientes de validación
        pending = self.guard.get_pending()

        return {
            "action": "VALIDAR",
            "pending_count": len(pending),
            "pending": pending[:10],  # Mostrar solo primeros 10
            "message": f"📋 Relaciones pendientes de validación: {len(pending)}"
        }

    def _cmd_conectar(self, command: str, context: dict) -> dict:
        """Procesar comando 'conectar X con Y'."""
        # Parsear "conectar X con Y"
        parts = command[9:].split(" con ")  # Remover "conectar "
        if len(parts) != 2:
            return {"error": "Formato: 'conectar [entidad1] con [entidad2]'"}

        entity1 = parts[0].strip()
        entity2 = parts[1].strip()

        # Generar propuesta
        proposal = GraphProposal(
            action="CONNECT",
            target=entity1,
            suggested_parent=entity2,
            relation="RELATED_TO",
            criticality="C2",
            requires_approval=True,
            reason=f"Conexión sugerida por usuario entre {entity1} y {entity2}"
        )

        return {
            "action": "CONECTAR",
            "entity1": entity1,
            "entity2": entity2,
            "proposal": asdict(proposal),
            "message": f"🔗 Propuesta: conectar '{entity1}' con '{entity2}'"
        }

    def _cmd_grafo(self, command: str, context: dict) -> dict:
        """Procesar comando 'grafo de [entidad]'."""
        entity = command[6:].strip()  # Remover "grafo "

        if not entity:
            return {"error": "Especifica una entidad (ej: 'grafo de auth_service')"}

        # Obtener vecindad del grafo (implementación simplificada)
        try:
            # Usar graph_engine para traversia
            result = self.graph.traverse(f"mostrar conexiones de {entity}", max_hops=2)

            return {
                "action": "GRAFO",
                "entity": entity,
                "connections": [
                    {
                        "from": rel.from_node,
                        "to": rel.to_node,
                        "type": rel.relation_type,
                        "weight": rel.weight
                    }
                    for rel in result.relationships[:10]  # Limitar
                ],
                "message": f"🌐 Vecindad de '{entity}' en el grafo"
            }
        except Exception as e:
            logger.error(f"Error obteniendo grafo de {entity}: {e}")
            return {"error": f"No se pudo obtener el grafo para '{entity}'"}

    def _interpret_semantic(self, command: str, context: dict) -> dict:
        """Interpretación semántica de la entrada del usuario."""
        # Detección simple de intenciones
        triggers = {
            "perdido": "estoy perdido",
            "confuso": "esto no tiene sentido",
            "organizar": "organiza mi conocimiento",
            "cartografiar": "cartografiar"
        }

        detected = None
        for key, phrase in triggers.items():
            if phrase in command.lower():
                detected = key
                break

        if detected:
            return {
                "action": "INTERPRETAR",
                "intent": detected,
                "message": f"Detectada intención: '{detected}'. ¿Necesitas ayuda para mapear el conocimiento?",
                "suggestion": "Usa 'mapear [proyecto]' para comenzar"
            }
        else:
            return {
                "action": "CHAT",
                "message": f"No reconozco el comando '{command}'. Usa: mapear, validar, conectar, grafo"
            }

    def _find_orphan_nodes(self, project: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Encontrar nodos huérfanos en el grafo.

        Args:
            project: Proyecto específico (opcional)

        Returns:
            Lista de nodos huérfanos
        """
        # Implementación simplificada
        # En producción, consultaría el grafo para nodos sin relaciones entrantes/salientes
        return []

    def _detect_conflicts(self) -> List[Dict[str, Any]]:
        """
        Detectar conflictos en el grafo.

        Returns:
            Lista de conflictos detectados
        """
        # Implementación simplificada
        # En producción, buscaría ciclos, contradicciones, etc.
        return []

    def _get_local_subgraph(self, context: dict) -> Dict[str, Any]:
        """
        Obtener subgrafo local basado en contexto.

        Args:
            context: Contexto actual

        Returns:
            Representación del subgrafo local
        """
        # Implementación simplificada
        return {
            "nodes": [],
            "edges": [],
            "project": context.get("project", "unknown")
        }

    def _suggest_parent_for_orphan(self, orphan_node: Dict[str, Any]) -> Optional[GraphProposal]:
        """
        Sugerir padre para un nodo huérfano.

        Args:
            orphan_node: Nodo huérfano

        Returns:
            Propuesta de conexión o None
        """
        # Implementación simplificada
        return None

    def _display_result(self, result: dict):
        """
        Mostrar resultado al usuario.

        Args:
            result: Resultado a mostrar
        """
        if "error" in result:
            print(f"❌ {result['error']}")
            return

        # Mostrar mensaje principal
        if "message" in result:
            print(result["message"])

        # Mostrar detalles específicos
        action = result.get("action", "")

        if action == "VALIDAR" and result.get("pending_count", 0) > 0:
            print(f"  📊 Pendientes: {result['pending_count']}")
            for i, pending in enumerate(result.get("pending", [])):
                print(f"    {i+1}. {pending.get('subject', '?')} -> {pending.get('object', '?')}")

        elif action == "GRAFO" and result.get("connections"):
            print(f"  🔗 Conexiones encontradas: {len(result['connections'])}")
            for conn in result["connections"]:
                print(f"    {conn['from']} --[{conn['type']}]--> {conn['to']} (peso: {conn['weight']})")

        elif action == "INTERPRETAR":
            print(f"  💡 Sugerencia: {result.get('suggestion', '')}")

        print()  # Línea en blanco para separar

    def apply_changes(self, approved_proposals: List[dict], user_id: str) -> dict:
        """
        Aplicación transaccional de cambios validados.

        Args:
            approved_proposals: Lista de propuestas aprobadas
            user_id: Identificador del usuario

        Returns:
            Dict con estado de aplicación
        """
        logger.info(f"Aplicando {len(approved_proposals)} cambios como usuario {user_id}")

        # En implementación real, usaríamos transacción del grafo
        applied_count = 0

        for prop in approved_proposals:
            try:
                # Verificar que el guard permita la ejecución
                # (simplificado para demostración)

                # Aplicar cambio
                # self.graph.add_relationship(...)

                applied_count += 1
                logger.info(f"Aplicado cambio: {prop.get('target', 'unknown')}")

            except Exception as e:
                logger.error(f"Error aplicando propuesta {prop}: {e}")
                continue

        return {
            "status": "APPLIED" if applied_count > 0 else "FAILED",
            "changes_count": applied_count,
            "total_proposals": len(approved_proposals)
        }


def create_cartografo_from_config(config: dict):
    """
    Factory para crear SkillCartografoRAG desde configuración.

    Args:
        config: Configuración del módulo RAG

    Returns:
        Instancia de SkillCartografoRAG o None si no se puede crear
    """
    try:
        # Importar aquí para evitar dependencias circulares
        from ..engines.graph_engine import GraphEngine
        from ..validators.relation_guard import RelationGuard

        # Obtener rutas de configuración
        graph_config = config.get("graph", {})
        guard_config = config.get("validation", {})

        db_path = graph_config.get("db_path", "rag_data/graph.db")
        guard_db_path = guard_config.get("db_path", "rag_data/validation.db")

        # Crear instancias
        graph_engine = GraphEngine(db_path)
        relation_guard = RelationGuard(guard_db_path)

        return SkillCartografoRAG(graph_engine, relation_guard)

    except Exception as e:
        logger.error(f"No se pudo crear Cartógrafo: {e}")
        return None