#!/usr/bin/env python3
# =============================================================================
# NOTCURSES TEST MODULE - ARES-TRON
# =============================================================================
# Propósito: Prueba encapsulada de renderizado de imágenes con notcurses
# Configuración: config/notcurses_test_config.yaml
# Uso: python -m modules.multimedia.notcurses_test
#      o: python scripts/test_notcurses.py
# =============================================================================

import sys
import os
import time
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

# =============================================================================
# CONFIGURACIÓN E IMPORTS
# =============================================================================

# Agregar raíz del proyecto al path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Imports de notcurses
try:
    from notcurses import Notcurses, NotcursesOptions, PlaneOptions, Visual
    from notcurses import NCBLIT_DEFAULT, NCBLIT_PIXEL, NCBLIT_OCTANT, NCBLIT_BRAILLE
    from notcurses import NCSCALE_SCALE, NCSCALE_STRETCH, NCSCALE_NONE
except ImportError as e:
    print(f"❌ Error: No se pudo importar notcurses")
    print(f"   Detalle: {e}")
    print(f"\n💡 Instalación requerida:")
    print(f"   sudo apt-get install libnotcurses-dev notcurses-bin")
    print(f"   pip install notcurses")
    sys.exit(1)

# Imports del proyecto
try:
    import yaml
except ImportError:
    print("❌ Error: PyYAML no está instalado")
    print("   pip install pyyaml")
    sys.exit(1)


# =============================================================================
# CONFIGURACIÓN DE LOGGING
# =============================================================================

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(PROJECT_ROOT / 'logs' / 'notcurses_test.log')
    ]
)
logger = logging.getLogger('NotcursesTest')


# =============================================================================
# CLASES DE DATOS
# =============================================================================

@dataclass
class TestConfig:
    """Configuración de prueba"""
    nombre: str
    duracion: int
    assets: Dict[str, str]
    layout: Dict[str, Any]
    notcurses_config: Dict[str, Any]
    pruebas_a_ejecutar: List[str]


@dataclass
class TestResult:
    """Resultado de una prueba"""
    nombre: str
    exito: bool
    mensaje: str
    duracion: float
    error: Optional[Exception] = None


# =============================================================================
# CARGADOR DE CONFIGURACIÓN
# =============================================================================

class ConfigLoader:
    """Carga configuración desde YAML"""
    
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.config = {}
        
    def load(self) -> TestConfig:
        """Cargar configuración completa"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config no encontrada: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        logger.info(f"Configuración cargada desde {self.config_path}")
        
        return TestConfig(
            nombre=self.config['general']['nombre_prueba'],
            duracion=self.config['pruebas']['duracion_prueba'],
            assets=self.config['assets'],
            layout=self.config['layout'],
            notcurses_config=self.config['notcurses'],
            pruebas_a_ejecutar=self.config['pruebas']['ejecutar']
        )
    
    def verificar_assets(self) -> Dict[str, bool]:
        """Verificar que los archivos de assets existen"""
        resultados = {}
        
        for key, path in self.config['assets'].items():
            if isinstance(path, list):
                resultados[key] = all(Path(p).exists() for p in path)
            else:
                resultados[key] = Path(path).exists()
        
        return resultados


# =============================================================================
# MOTOR DE PRUEBAS NOTCURSES
# =============================================================================

class NotcursesTestEngine:
    """Motor de pruebas para notcurses"""
    
    def __init__(self, config: TestConfig):
        self.config = config
        self.nc: Optional[Notcurses] = None
        self.resultados: List[TestResult] = []
        
    def inicializar(self) -> bool:
        """Inicializar notcurses"""
        try:
            logger.info("Inicializando notcurses...")
            
            # Opciones de inicialización
            opts = NotcursesOptions()
            opts.log_level = self.config.notcurses_config.get('log_level', 3)
            
            if self.config.notcurses_config['flags'].get('suppress_banners', True):
                opts.flags = 0x02  # NCOPTION_SUPPRESS_BANNERS
            
            if self.config.notcurses_config['flags'].get('enable_mouse', True):
                opts.flags |= 0x01  # NCOPTION_ENABLE_MOUSE
            
            # Inicializar
            self.nc = Notcurses(opts=opts)
            
            logger.info(f"✅ Notcurses inicializado")
            logger.info(f"   Terminal: {self.nc.termname}")
            logger.info(f"   Dimensiones: {self.nc.stdplane.cols}x{self.nc.stdplane.rows}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error inicializando notcurses: {e}")
            return False
    
    def limpiar(self):
        """Limpiar recursos"""
        if self.nc:
            logger.info("Limpiando recursos de notcurses...")
            self.nc.stop()
            logger.info("✅ Recursos limpiados")
    
    # -------------------------------------------------------------------------
    # PRUEBAS
    # -------------------------------------------------------------------------
    
    def test_imagen_estatica(self) -> TestResult:
        """Prueba 1: Imagen PNG estática"""
        start = time.time()
        
        try:
            logger.info("🧪 Prueba: Imagen Estática (PNG)")
            
            stdplane = self.nc.stdplane()
            
            # Cargar avatar IA
            avatar_path = self.config.assets.get('avatar_ia_png', '')
            
            if not Path(avatar_path).exists():
                raise FileNotFoundError(f"Asset no encontrado: {avatar_path}")
            
            # Crear plano para imagen
            layout = self.config.layout['avatar_ia']
            plane_opts = PlaneOptions(
                rows=layout['filas'],
                cols=layout['columnas'],
                yoff=layout['posicion_y'],
                xoff=layout['posicion_x']
            )
            
            img_plane = stdplane.create(plane_opts)
            
            # Cargar y blitear imagen
            visual = Visual(avatar_path)
            visual.blit(img_plane)
            
            # Renderizar
            self.nc.render()
            
            # Esperar para visualización
            time.sleep(3)
            
            duracion = time.time() - start
            
            return TestResult(
                nombre="test_imagen_estatica",
                exito=True,
                mensaje=f"Imagen PNG renderizada correctamente",
                duracion=duracion
            )
            
        except Exception as e:
            duracion = time.time() - start
            logger.error(f"❌ Error en test_imagen_estatica: {e}")
            
            return TestResult(
                nombre="test_imagen_estatica",
                exito=False,
                mensaje=str(e),
                duracion=duracion,
                error=e
            )
    
    def test_imagen_con_transparencia(self) -> TestResult:
        """Prueba 2: PNG con canal alpha"""
        start = time.time()
        
        try:
            logger.info("🧪 Prueba: Imagen con Transparencia (PNG + Alpha)")
            
            stdplane = self.nc.stdplane()
            
            # Usar avatar de usuario (potencialmente con transparencia)
            avatar_path = self.config.assets.get('avatar_usuario_png', '')
            
            if not Path(avatar_path).exists():
                raise FileNotFoundError(f"Asset no encontrado: {avatar_path}")
            
            # Crear plano
            layout = self.config.layout['avatar_ia']
            plane_opts = PlaneOptions(
                rows=layout['filas'],
                cols=layout['columnas'],
                yoff=layout['posicion_y'],
                xoff=layout['posicion_x']
            )
            
            img_plane = stdplane.create(plane_opts)
            
            # Cargar y blitear
            visual = Visual(avatar_path)
            visual.blit(img_plane)
            
            self.nc.render()
            time.sleep(3)
            
            duracion = time.time() - start
            
            return TestResult(
                nombre="test_imagen_con_transparencia",
                exito=True,
                mensaje=f"PNG con transparencia renderizado correctamente",
                duracion=duracion
            )
            
        except Exception as e:
            duracion = time.time() - start
            return TestResult(
                nombre="test_imagen_con_transparencia",
                exito=False,
                mensaje=str(e),
                duracion=duracion,
                error=e
            )
    
    def test_gif_animado(self) -> TestResult:
        """Prueba 3: GIF animado (simulado por frames)"""
        start = time.time()
        
        try:
            logger.info("🧪 Prueba: GIF Animado (simulación por frames)")
            
            stdplane = self.nc.stdplane()
            
            # Obtener lista de spinners
            spinners = self.config.assets.get('spinners', [])
            
            if not spinners:
                raise ValueError("No hay spinners configurados")
            
            # Verificar que al menos uno existe
            spinner_path = None
            for path in spinners:
                if Path(path).exists():
                    spinner_path = path
                    break
            
            if not spinner_path:
                raise FileNotFoundError("Ningún spinner encontrado")
            
            # Crear plano
            layout = self.config.layout['avatar_ia']
            plane_opts = PlaneOptions(
                rows=layout['filas'],
                cols=layout['columnas'],
                yoff=layout['posicion_y'],
                xoff=layout['posicion_x']
            )
            
            img_plane = stdplane.create(plane_opts)
            
            # Simular animación (ciclar por spinners)
            for i in range(3):  # 3 ciclos
                for spinner in spinners[:3]:  # Usar primeros 3
                    if Path(spinner).exists():
                        visual = Visual(spinner)
                        visual.blit(img_plane)
                        self.nc.render()
                        time.sleep(0.1)  # 100ms por frame
            
            duracion = time.time() - start
            
            return TestResult(
                nombre="test_gif_animado",
                exito=True,
                mensaje=f"Animación GIF simulada correctamente ({len(spinners)} frames)",
                duracion=duracion
            )
            
        except Exception as e:
            duracion = time.time() - start
            return TestResult(
                nombre="test_gif_animado",
                exito=False,
                mensaje=str(e),
                duracion=duracion,
                error=e
            )
    
    def test_layout_completo(self) -> TestResult:
        """Prueba 4: Layout completo ARES"""
        start = time.time()
        
        try:
            logger.info("🧪 Prueba: Layout Completo ARES")
            
            stdplane = self.nc.stdplane()
            
            # 1. Avatar IA
            avatar_path = self.config.assets.get('avatar_ia_png', '')
            if Path(avatar_path).exists():
                layout = self.config.layout['avatar_ia']
                plane_opts = PlaneOptions(
                    rows=layout['filas'],
                    cols=layout['columnas'],
                    yoff=layout['posicion_y'],
                    xoff=layout['posicion_x']
                )
                avatar_plane = stdplane.create(plane_opts)
                visual = Visual(avatar_path)
                visual.blit(avatar_plane)
                logger.info("  ✅ Avatar IA renderizado")
            
            # 2. Banner/Cintillo
            banner_path = self.config.assets.get('header_ares_png', '')
            if Path(banner_path).exists():
                layout = self.config.layout['banner']
                plane_opts = PlaneOptions(
                    rows=layout['filas'],
                    cols=layout['columnas'],
                    yoff=layout['posicion_y'],
                    xoff=layout['posicion_x']
                )
                banner_plane = stdplane.create(plane_opts)
                visual = Visual(banner_path)
                visual.blit(banner_plane)
                logger.info("  ✅ Banner renderizado")
            
            # 3. Separador Footer
            separador_path = self.config.assets.get('separador_gif', '')
            if Path(separador_path).exists():
                layout = self.config.layout['separador']
                plane_opts = PlaneOptions(
                    rows=layout['filas'],
                    cols=layout['columnas'],
                    yoff=layout['posicion_y'],
                    xoff=layout['posicion_x']
                )
                separador_plane = stdplane.create(plane_opts)
                visual = Visual(separador_path)
                visual.blit(separador_plane)
                logger.info("  ✅ Separador renderizado")
            
            # 4. Texto en body
            body_plane = stdplane.create(PlaneOptions(
                rows=5,
                cols=40,
                yoff=5,
                xoff=0
            ))
            body_plane.set_fg_rgb8(255, 255, 255)
            body_plane.putstr_yx(0, 0, "ARES-TRON Notcurses Test")
            body_plane.putstr_yx(1, 0, "Layout completo renderizado")
            body_plane.putstr_yx(2, 0, "Presiona 'q' para salir")
            
            # Renderizar todo
            self.nc.render()
            logger.info("  ✅ Layout completo renderizado")
            
            # Esperar
            time.sleep(5)
            
            duracion = time.time() - start
            
            return TestResult(
                nombre="test_layout_completo",
                exito=True,
                mensaje="Layout completo ARES renderizado correctamente",
                duracion=duracion
            )
            
        except Exception as e:
            duracion = time.time() - start
            logger.error(f"❌ Error en test_layout_completo: {e}")
            return TestResult(
                nombre="test_layout_completo",
                exito=False,
                mensaje=str(e),
                duracion=duracion,
                error=e
            )
    
    def test_blitters(self) -> TestResult:
        """Prueba 5: Diferentes blitters"""
        start = time.time()
        
        try:
            logger.info("🧪 Prueba: Diferentes Blitters")
            
            stdplane = self.nc.stdplane()
            avatar_path = self.config.assets.get('avatar_ia_png', '')
            
            if not Path(avatar_path).exists():
                raise FileNotFoundError(f"Asset no encontrado: {avatar_path}")
            
            # Blitters a probar
            blitters = [
                (NCBLIT_PIXEL, "Pixel (KGP)"),
                (NCBLIT_OCTANT, "Octant (4x2)"),
                (NCBLIT_BRAILLE, "Braille (2x4)"),
                (NCBLIT_DEFAULT, "Default"),
            ]
            
            y_offset = 0
            for blitter, nombre in blitters:
                # Crear plano pequeño
                plane_opts = PlaneOptions(rows=4, cols=8, yoff=y_offset, xoff=0)
                img_plane = stdplane.create(plane_opts)
                
                # Cargar imagen
                visual = Visual(avatar_path)
                
                # Blitear con blitter específico
                visual.blit(img_plane, blitter=blitter)
                
                # Etiqueta
                stdplane.putstr_yx(y_offset, 10, f"{nombre}")
                
                y_offset += 5
            
            self.nc.render()
            time.sleep(5)
            
            duracion = time.time() - start
            
            return TestResult(
                nombre="test_blitters",
                exito=True,
                mensaje=f"{len(blitters)} blitters probados correctamente",
                duracion=duracion
            )
            
        except Exception as e:
            duracion = time.time() - start
            return TestResult(
                nombre="test_blitters",
                exito=False,
                mensaje=str(e),
                duracion=duracion,
                error=e
            )
    
    def test_scaling(self) -> TestResult:
        """Prueba 6: Escalado de imágenes"""
        start = time.time()
        
        try:
            logger.info("🧪 Prueba: Escalado de Imágenes")
            
            stdplane = self.nc.stdplane()
            avatar_path = self.config.assets.get('avatar_ia_png', '')
            
            if not Path(avatar_path).exists():
                raise FileNotFoundError(f"Asset no encontrado: {avatar_path}")
            
            # Escalas a probar
            escalas = [
                (2, 2, "2x2"),
                (4, 4, "4x4 (nativo)"),
                (8, 8, "8x8"),
                (12, 12, "12x12"),
            ]
            
            x_offset = 0
            for rows, cols, nombre in escalas:
                plane_opts = PlaneOptions(rows=rows, cols=cols, yoff=0, xoff=x_offset)
                img_plane = stdplane.create(plane_opts)
                
                visual = Visual(avatar_path)
                visual.blit(img_plane)
                
                # Etiqueta
                stdplane.putstr_yx(rows + 1, x_offset, nombre)
                
                x_offset += cols + 2
            
            self.nc.render()
            time.sleep(5)
            
            duracion = time.time() - start
            
            return TestResult(
                nombre="test_scaling",
                exito=True,
                mensaje=f"{len(escalas)} escalas probadas correctamente",
                duracion=duracion
            )
            
        except Exception as e:
            duracion = time.time() - start
            return TestResult(
                nombre="test_scaling",
                exito=False,
                mensaje=str(e),
                duracion=duracion,
                error=e
            )
    
    # -------------------------------------------------------------------------
    # EJECUTOR DE PRUEBAS
    # -------------------------------------------------------------------------
    
    def ejecutar_prueba(self, nombre: str) -> TestResult:
        """Ejecutar una prueba por nombre"""
        pruebas_map = {
            'test_imagen_estatica': self.test_imagen_estatica,
            'test_imagen_con_transparencia': self.test_imagen_con_transparencia,
            'test_gif_animado': self.test_gif_animado,
            'test_layout_completo': self.test_layout_completo,
            'test_blitters': self.test_blitters,
            'test_scaling': self.test_scaling,
        }
        
        if nombre not in pruebas_map:
            return TestResult(
                nombre=nombre,
                exito=False,
                mensaje=f"Prueba desconocida: {nombre}",
                duracion=0
            )
        
        return pruebas_map[nombre]()
    
    def ejecutar_todas(self) -> List[TestResult]:
        """Ejecutar todas las pruebas configuradas"""
        logger.info("=" * 60)
        logger.info(f"Iniciando batería de pruebas: {self.config.nombre}")
        logger.info("=" * 60)
        
        for nombre_prueba in self.config.pruebas_a_ejecutar:
            logger.info(f"\n{'='*60}")
            resultado = self.ejecutar_prueba(nombre_prueba)
            self.resultados.append(resultado)
            
            # Resumen
            estado = "✅ EXITO" if resultado.exito else "❌ FALLO"
            logger.info(f"{estado}: {resultado.nombre}")
            logger.info(f"   Duración: {resultado.duracion:.2f}s")
            logger.info(f"   Mensaje: {resultado.mensaje}")
        
        return self.resultados
    
    def imprimir_resumen(self):
        """Imprimir resumen de resultados"""
        print("\n" + "=" * 60)
        print("RESUMEN DE PRUEBAS")
        print("=" * 60)
        
        total = len(self.resultados)
        exitosas = sum(1 for r in self.resultados if r.exito)
        fallidas = total - exitosas
        duracion_total = sum(r.duracion for r in self.resultados)
        
        print(f"\nTotal: {total} pruebas")
        print(f"Exitosas: {exitosas} ✅")
        print(f"Fallidas: {fallidas} ❌")
        print(f"Duración total: {duracion_total:.2f}s")
        
        print("\nDetalle:")
        for r in self.resultados:
            estado = "✅" if r.exito else "❌"
            print(f"  {estado} {r.nombre}: {r.duracion:.2f}s - {r.mensaje}")
        
        print("=" * 60)


# =============================================================================
# FUNCIÓN PRINCIPAL
# =============================================================================

def main():
    """Función principal de prueba"""
    print("\n" + "=" * 60)
    print("NOTCURSES TEST MODULE - ARES-TRON")
    print("=" * 60 + "\n")
    
    # Cargar configuración
    config_path = PROJECT_ROOT / 'config' / 'notcurses_test_config.yaml'
    
    if not config_path.exists():
        logger.error(f"Configuración no encontrada: {config_path}")
        return 1
    
    loader = ConfigLoader(config_path)
    
    try:
        config = loader.load()
    except Exception as e:
        logger.error(f"Error cargando configuración: {e}")
        return 1
    
    # Verificar assets
    if config.notcurses_config.get('verificar_assets', True):
        logger.info("Verificando assets...")
        assets_ok = loader.verificar_assets()
        
        for key, existe in assets_ok.items():
            estado = "✅" if existe else "❌"
            logger.info(f"  {estado} {key}")
    
    # Inicializar motor de pruebas
    engine = NotcursesTestEngine(config)
    
    if not engine.inicializar():
        logger.error("No se pudo inicializar notcurses")
        return 1
    
    try:
        # Ejecutar pruebas
        engine.ejecutar_todas()
        
        # Imprimir resumen
        engine.imprimir_resumen()
        
        return 0
        
    except KeyboardInterrupt:
        logger.info("\n⚠️ Prueba interrumpida por usuario")
        return 130
        
    finally:
        engine.limpiar()


# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    sys.exit(main())
