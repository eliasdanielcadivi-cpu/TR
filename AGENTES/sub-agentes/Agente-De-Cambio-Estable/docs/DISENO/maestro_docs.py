#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################################################################################
#                                                                              #
#                              maestro_docs.py                                 #
#                                                                              #
#  Script para consolididar archivos clave de diseño e interfaz en un único    #
#  documento Maestro.md. Basado en la lógica del script 'maestro' original.    #
#                                                                              #
#  Uso: python maestro_docs.py                                                 #
#  Salida: /home/daniel/tron/programas/Agente-De-Cambio-STABLE/docs/DISENO/Maestro.md
#                                                                              #
################################################################################

import os
import sys
from typing import List, Tuple

# Ruta base del proyecto
PROYECTO_RAIZ = "/home/daniel/tron/programas/Agente-De-Cambio-STABLE"
SALIDA_DIR = os.path.join(PROYECTO_RAIZ, "docs", "DISENO")
SALIDA_ARCHIVO = os.path.join(SALIDA_DIR, "Maestro.md")

# Lista de archivos clave (extraídos de la respuesta anterior)
# Cada tupla: (ruta_relativa, descripción)
ARCHIVOS_CLAVE = [
    # Documentación principal (Jerarquía 1)
    ("README.md", "Visión general, stack tecnológico, filosofía de diseño"),
    ("docs/proyecto.md", "Arquitectura completa, etapas, sistema de diseño"),
    ("docs/ListaRequerimientos.md", "27 requerimientos con filosofía Google Lens"),
    ("docs/METODOLOGIA-MODULAR.md", "Patrones arquitectónicos, optimización contexto IA"),
    ("docs/AUDITORIA-CAPACIDADES.md", "Capacidades discretas, estructura modular"),
    ("docs/estado.md", "Estado de implementación, problemas conocidos"),
    
    # Diseño y estilo (Jerarquía 2)
    ("apps/web/tailwind.config.js", "Tokens de diseño, colores, animaciones"),
    ("apps/web/app/globals.css", "Glassmorphism CSS, scrollbar, animaciones"),
    ("apps/web/app/store/chatStore.ts", "Estado global: modos, mensajes, prompt, métricas"),
    ("apps/server/src/types/socket.ts", "Tipos compartidos, eventos Socket.IO"),
    
    # Layout Components (Jerarquía 3)
    ("apps/web/components/layout/Header.tsx", "Cabecera con logo y controles"),
    ("apps/web/components/layout/ModeSwitcher.tsx", "Toggle chat/cuestionario"),
    ("apps/web/components/layout/ReasoningToggle.tsx", "Activar modo reasoning"),
    
    # Chat Components
    ("apps/web/components/chat/ChatContainer.tsx", "Contenedor principal"),
    ("apps/web/components/chat/ChatMessage.tsx", "Burbuja de mensaje animada"),
    ("apps/web/components/chat/ChatInput.tsx", "Input de texto modo chat"),
    ("apps/web/components/chat/Questionnaire.tsx", "Renderizado de preguntas"),
    
    # Métricas y Prompt
    ("apps/web/components/prompt/PromptEditor.tsx", "Editor de system prompt"),
    ("apps/web/components/metrics/DeltaMeter.tsx", "Visualización de deriva"),
    ("apps/web/components/objectives/ObjectivesPanel.tsx", "Panel de objetivos"),
]


def leer_contenido_archivo(ruta_archivo: str) -> str:
    """
    Lee y devuelve el contenido de un archivo de texto.
    Maneja posibles errores de decodificación.

    Args:
        ruta_archivo (str): Ruta absoluta del archivo a leer.

    Returns:
        str: Contenido del archivo o mensaje de error.
    """
    codificaciones = ['utf-8', 'latin-1', 'iso-8859-1']
    for codificacion in codificaciones:
        try:
            with open(ruta_archivo, 'r', encoding=codificacion) as f:
                return f.read()
        except UnicodeDecodeError:
            continue
        except (IOError, PermissionError) as e:
            return f"Error al leer el archivo: {e}"
    return f"Error: No se pudo decodificar '{ruta_archivo}'"


def verificar_rutas(archivos: List[Tuple[str, str]]) -> List[Tuple[str, str, bool]]:
    """
    Verifica que las rutas existan en el sistema de archivos.

    Args:
        archivos: Lista de tuplas (ruta_relativa, descripción)

    Returns:
        Lista de tuplas (ruta_relativa, descripción, existe)
    """
    resultados = []
    for ruta, descripcion in archivos:
        ruta_absoluta = os.path.join(PROYECTO_RAIZ, ruta)
        existe = os.path.isfile(ruta_absoluta)
        resultados.append((ruta, descripcion, existe))
        if not existe:
            print(f"⚠️  Archivo no encontrado: {ruta}")
    return resultados


def generar_maestro(archivos_verificados: List[Tuple[str, str, bool]], 
                    contenido_respuesta_anterior: str) -> None:
    """
    Genera el documento Maestro.md con:
    1. Título e introducción
    2. Respuesta anterior completa (marcador)
    3. Rutas y contenido de archivos clave

    Args:
        archivos_verificados: Lista de (ruta, descripción, existe)
        contenido_respuesta_anterior: Texto de la respuesta anterior
    """
    with open(SALIDA_ARCHIVO, 'w', encoding='utf-8') as f:
        # 1. Título e introducción
        f.write("# 📋 Documento Maestro de Diseño e Interfaz\n\n")
        f.write("## Introducción\n\n")
        f.write("Este documento consolida toda la información táctica y estratégica\n")
        f.write("que una IA externa necesita para trabajar en la maquetación e interfaz\n")
        f.write("del proyecto Agente de Cambio.\n\n")
        f.write("---\n\n")
        
        # 2. Respuesta anterior completa (marcador para inserción manual)
        f.write("## 📋 Lista de Documentos de Maquetación e Interfaz para IA Externa\n\n")
        f.write("*(Nota: Este es un marcador de posición. La respuesta anterior completa\n")
        f.write("debe ser copiada y pegada aquí sin modificación alguna)*\n\n")
        f.write("<!-- INICIO_RESPUESTA_ANTERIOR -->\n")
        f.write("<!-- FIN_RESPUESTA_ANTERIOR -->\n\n")
        f.write("---\n\n")
        
        # 3. Rutas y contenido de archivos
        f.write("## 📁 Archivos Clave con Contenido Completo\n\n")
        
        archivos_existentes = [(r, d, e) for r, d, e in archivos_verificados if e]
        archivos_faltantes = [(r, d, e) for r, d, e in archivos_verificados if not e]
        
        if archivos_faltantes:
            f.write("### ⚠️ Archivos No Encontrados\n\n")
            for ruta, descripcion, _ in archivos_faltantes:
                f.write(f"- `{ruta}` - {descripcion}\n")
            f.write("\n---\n\n")
        
        f.write(f"### ✅ Archivos Incluidos ({len(archivos_existentes)})\n\n")
        
        for ruta, descripcion, _ in archivos_existentes:
            ruta_absoluta = os.path.join(PROYECTO_RAIZ, ruta)
            contenido = leer_contenido_archivo(ruta_absoluta)
            
            f.write(f"### 📄 {ruta}\n\n")
            f.write(f"**Descripción:** {descripcion}\n\n")
            f.write(f"**Ruta absoluta:** `{ruta_absoluta}`\n\n")
            f.write("```")
            
            # Detectar lenguaje para syntax highlighting
            if ruta.endswith('.md'):
                f.write("markdown\n")
            elif ruta.endswith('.ts') or ruta.endswith('.tsx'):
                f.write("typescript\n")
            elif ruta.endswith('.js'):
                f.write("javascript\n")
            elif ruta.endswith('.css'):
                f.write("css\n")
            else:
                f.write("\n")
            
            f.write(f"{contenido}\n")
            f.write("```\n\n")
            f.write("---\n\n")
        
        f.write("## 📊 Resumen\n\n")
        f.write(f"- **Total de archivos planificados:** {len(archivos_verificados)}\n")
        f.write(f"- **Archivos incluidos:** {len(archivos_existentes)}\n")
        f.write(f"- **Archivos no encontrados:** {len(archivos_faltantes)}\n")
        f.write(f"- **Fecha de generación:** {os.popen('date').read().strip()}\n")


def main():
    """Función principal."""
    print("=" * 60)
    print("  MAESTRO_DOCS.PY - Generador de Documento Maestro")
    print("=" * 60)
    print()
    
    # Crear directorio de salida si no existe
    os.makedirs(SALIDA_DIR, exist_ok=True)
    print(f"📁 Directorio de salida: {SALIDA_DIR}")
    
    # Verificar rutas
    print("\n🔍 Verificando rutas de archivos...")
    print("-" * 60)
    archivos_verificados = verificar_rutas(ARCHIVOS_CLAVE)
    
    total = len(archivos_verificados)
    existentes = sum(1 for _, _, e in archivos_verificados if e)
    faltantes = total - existentes
    
    print(f"\n✅ Archivos encontrados: {existentes}/{total}")
    print(f"⚠️  Archivos no encontrados: {faltantes}")
    print()
    
    if existentes == 0:
        print("❌ Error: No se encontró ningún archivo. Verifica las rutas.")
        sys.exit(1)
    
    # Generar documento
    print("📝 Generando documento Maestro.md...")
    print("-" * 60)
    
    # Contenido de la respuesta anterior (marcador)
    contenido_respuesta = """
*(Este espacio está reservado para la respuesta anterior completa.
Debe ser copiada y pegada manualmente sin modificación alguna)*
""".strip()
    
    generar_maestro(archivos_verificados, contenido_respuesta)
    
    print(f"\n✅ Documento generado exitosamente:")
    print(f"   📄 {SALIDA_ARCHIVO}")
    print()
    print("=" * 60)
    print("  Proceso completado")
    print("=" * 60)


if __name__ == "__main__":
    main()
