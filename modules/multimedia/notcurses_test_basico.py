#!/usr/bin/env python3
# =============================================================================
# NOTCURSES TEST - VERSIÓN BÁSICA (wrapper v3.0.7)
# =============================================================================
# Propósito: Prueba de notcurses con wrapper básico limitado
# Limitaciones: Sin imágenes, sin widgets, solo texto y colores
# =============================================================================

import sys
import os
import time
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass

# =============================================================================
# CONFIGURACIÓN E IMPORTS
# =============================================================================

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Imports de notcurses - wrapper básico v3.0.7
try:
    from notcurses import Notcurses
    print("✅ notcurses v3.0.7 (wrapper básico)")
except ImportError as e:
    print(f"❌ Error: No se pudo importar notcurses: {e}")
    sys.exit(1)


# =============================================================================
# CLASES DE DATOS
# =============================================================================

@dataclass
class TestResult:
    """Resultado de una prueba"""
    nombre: str
    exito: bool
    mensaje: str
    duracion: float
    error: Optional[Exception] = None


# =============================================================================
# MOTOR DE PRUEBAS BÁSICO
# =============================================================================

class NotcursesTestBasico:
    """Motor de pruebas para notcurses - versión básica"""

    def __init__(self):
        self.nc: Optional[Notcurses] = None
        self.resultados: List[TestResult] = []

    def inicializar(self) -> bool:
        """Inicializar notcurses"""
        try:
            print("\n📦 Inicializando notcurses...")
            self.nc = Notcurses()
            print("   ✅ Notcurses inicializado")
            return True
        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False

    def limpiar(self):
        """Limpiar recursos"""
        if self.nc:
            print("\n🧹 Limpiando recursos...")
            del self.nc
            print("   ✅ Recursos limpiados")

    def test_colores_basicos(self) -> TestResult:
        """Prueba 1: Colores básicos RGB"""
        start = time.time()
        
        try:
            print("\n🧪 Prueba: Colores Básicos RGB")
            
            stdplane = self.nc.stdplane()
            rows, cols = stdplane.getDimensions()
            
            # Escribir en diferentes colores
            colores = [
                (255, 0, 0, "ROJO"),
                (0, 255, 0, "VERDE"),
                (0, 0, 255, "AZUL"),
                (255, 255, 0, "AMARILLO"),
                (0, 255, 255, "CYAN"),
                (255, 0, 255, "MAGENTA"),
            ]
            
            y = 2
            for r, g, b, nombre in colores:
                stdplane.setFgRGB(r, g, b)
                x = (cols - len(nombre)) // 2
                for i, char in enumerate(nombre):
                    stdplane.putEGCYX(y, x + i, char)
                y += 1
            
            self.nc.render()
            print("   ✅ Colores renderizados")
            
            time.sleep(2)
            
            duracion = time.time() - start
            return TestResult(
                nombre="test_colores_basicos",
                exito=True,
                mensaje="Colores RGB OK",
                duracion=duracion
            )
            
        except Exception as e:
            duracion = time.time() - start
            print(f"   ❌ Error: {e}")
            return TestResult(
                nombre="test_colores_basicos",
                exito=False,
                mensaje=str(e),
                duracion=duracion,
                error=e
            )

    def test_caracteres_unicode(self) -> TestResult:
        """Prueba 2: Caracteres Unicode y bordes"""
        start = time.time()
        
        try:
            print("\n🧪 Prueba: Caracteres Unicode")
            
            stdplane = self.nc.stdplane()
            rows, cols = stdplane.getDimensions()
            
            # Dibujar caja con caracteres Unicode
            box_chars = {
                'tl': '╔', 'tr': '╗', 'bl': '╚', 'br': '╝',
                'h': '═', 'v': '║'
            }
            
            y1, x1 = 5, 5
            y2, x2 = 10, cols - 6
            
            # Esquinas
            stdplane.setFgRGB(0, 255, 0)
            stdplane.putEGCYX(y1, x1, box_chars['tl'])
            stdplane.putEGCYX(y1, x2, box_chars['tr'])
            stdplane.putEGCYX(y2, x1, box_chars['bl'])
            stdplane.putEGCYX(y2, x2, box_chars['br'])
            
            # Líneas horizontales
            for x in range(x1 + 1, x2):
                stdplane.putEGCYX(y1, x, box_chars['h'])
                stdplane.putEGCYX(y2, x, box_chars['h'])
            
            # Líneas verticales
            for y in range(y1 + 1, y2):
                stdplane.putEGCYX(y, x1, box_chars['v'])
                stdplane.putEGCYX(y, x2, box_chars['v'])
            
            # Texto interior
            stdplane.setFgRGB(255, 255, 255)
            mensaje = "Unicode OK"
            y_center = (y1 + y2) // 2
            x_center = (x1 + x2 - len(mensaje)) // 2
            for i, char in enumerate(mensaje):
                stdplane.putEGCYX(y_center, x_center + i, char)
            
            self.nc.render()
            print("   ✅ Unicode renderizado")
            
            time.sleep(2)
            
            duracion = time.time() - start
            return TestResult(
                nombre="test_caracteres_unicode",
                exito=True,
                mensaje="Unicode OK",
                duracion=duracion
            )
            
        except Exception as e:
            duracion = time.time() - start
            print(f"   ❌ Error: {e}")
            return TestResult(
                nombre="test_caracteres_unicode",
                exito=False,
                mensaje=str(e),
                duracion=duracion,
                error=e
            )

    def test_gradiente(self) -> TestResult:
        """Prueba 3: Gradiente de colores"""
        start = time.time()
        
        try:
            print("\n🧪 Prueba: Gradiente RGB")
            
            stdplane = self.nc.stdplane()
            rows, cols = stdplane.getDimensions()
            
            # Gradiente horizontal
            y = 12
            for x in range(min(cols, 80)):
                r = int(255 * x / min(cols, 80))
                g = int(255 * (min(cols, 80) - x) / min(cols, 80))
                b = 128
                stdplane.setFgRGB(r, g, b)
                stdplane.putEGCYX(y, x, '█')
            
            # Gradiente vertical
            x = 5
            for y in range(min(rows - 2, 20)):
                r = int(255 * y / min(rows - 2, 20))
                g = 128
                b = int(255 * (min(rows - 2, 20) - y) / min(rows - 2, 20))
                stdplane.setFgRGB(r, g, b)
                stdplane.putEGCYX(y + 14, x, '█')
                stdplane.putEGCYX(y + 14, x + 1, '█')
            
            self.nc.render()
            print("   ✅ Gradiente renderizado")
            
            time.sleep(2)
            
            duracion = time.time() - start
            return TestResult(
                nombre="test_gradiente",
                exito=True,
                mensaje="Gradiente OK",
                duracion=duracion
            )
            
        except Exception as e:
            duracion = time.time() - start
            print(f"   ❌ Error: {e}")
            return TestResult(
                nombre="test_gradiente",
                exito=False,
                mensaje=str(e),
                duracion=duracion,
                error=e
            )

    def ejecutar_todas(self) -> List[TestResult]:
        """Ejecutar todas las pruebas"""
        print("\n" + "=" * 60)
        print("EJECUTANDO PRUEBAS NOTCURSES - VERSIÓN BÁSICA")
        print("=" * 60)
        
        if not self.inicializar():
            return []
        
        try:
            # Ejecutar pruebas
            self.resultados.append(self.test_colores_basicos())
            self.resultados.append(self.test_caracteres_unicode())
            self.resultados.append(self.test_gradiente())
            
            # Resumen
            print("\n" + "=" * 60)
            print("RESUMEN DE PRUEBAS")
            print("=" * 60)
            
            exitos = sum(1 for r in self.resultados if r.exito)
            total = len(self.resultados)
            
            for r in self.resultados:
                estado = "✅" if r.exito else "❌"
                print(f"  {estado} {r.nombre}: {r.mensaje} ({r.duracion:.2f}s)")
            
            print(f"\n  Total: {exitos}/{total} pruebas exitosas")
            print("=" * 60)
            
        finally:
            self.limpiar()
        
        return self.resultados


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Función principal"""
    engine = NotcursesTestBasico()
    resultados = engine.ejecutar_todas()
    
    # Retornar código de salida
    if all(r.exito for r in resultados):
        print("\n🎉 ¡Todas las pruebas completadas!")
        return 0
    else:
        print("\n⚠️  Algunas pruebas fallaron")
        return 1


if __name__ == "__main__":
    sys.exit(main())
