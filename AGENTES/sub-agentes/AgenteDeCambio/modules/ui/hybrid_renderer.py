"""
Puente Python ↔ Rust para componentes Ratatui
Híbrido 90% Textual / 10% Ratatui
"""
import ctypes
from pathlib import Path
from typing import List, Optional
import os


class RatatuiRenderer:
    """
    Renderer híbrido para componentes Ratatui en Textual
    
    Carga la biblioteca compartida de Rust y expone métodos Python
    para renderizar componentes visuales (gauges, sparklines, charts)
    """
    
    def __init__(self, lib_path: Optional[str] = None):
        """
        Inicializar renderer
        
        Args:
            lib_path: Ruta a la biblioteca compartida (.so). 
                     Si es None, busca en ruta por defecto.
        """
        if lib_path is None:
            # Ruta por defecto
            base_path = Path(__file__).parent.parent
            lib_path = base_path / "ratatui_components" / "target" / "release" / "libratui_components.so"
        
        self.lib_path = Path(lib_path)
        
        if not self.lib_path.exists():
            raise FileNotFoundError(
                f"Biblioteca Ratatui no encontrada en: {self.lib_path}\n"
                f"Compila con: cd modules/ui/ratatui_components && cargo build --release"
            )
        
        # Cargar biblioteca
        self.lib = ctypes.CDLL(str(self.lib_path))
        
        # Configurar funciones Rust
        self._setup_functions()
    
    def _setup_functions(self) -> None:
        """Configurar tipos de argumentos y retorno para funciones Rust"""
        
        # render_line_gauge(delta: f64, threshold: f64, width: usize) -> *mut c_char
        self.lib.render_line_gauge.argtypes = [
            ctypes.c_double,
            ctypes.c_double,
            ctypes.c_size_t
        ]
        self.lib.render_line_gauge.restype = ctypes.c_char_p
        
        # render_delta_gauge(delta: f64, threshold: f64, width: usize, height: usize) -> *mut c_char
        self.lib.render_delta_gauge.argtypes = [
            ctypes.c_double,
            ctypes.c_double,
            ctypes.c_size_t,
            ctypes.c_size_t
        ]
        self.lib.render_delta_gauge.restype = ctypes.c_char_p
        
        # render_vertical_gauge(delta: f64, threshold: f64, height: usize) -> *mut c_char
        self.lib.render_vertical_gauge.argtypes = [
            ctypes.c_double,
            ctypes.c_double,
            ctypes.c_size_t
        ]
        self.lib.render_vertical_gauge.restype = ctypes.c_char_p
        
        # render_simple_sparkline(data: *mut f64, len: usize, width: usize, height: usize) -> *mut c_char
        self.lib.render_simple_sparkline.argtypes = [
            ctypes.POINTER(ctypes.c_double),
            ctypes.c_size_t,
            ctypes.c_size_t,
            ctypes.c_size_t
        ]
        self.lib.render_simple_sparkline.restype = ctypes.c_char_p
        
        # render_delta_history(delta_history: *mut f64, len: usize, width: usize) -> *mut c_char
        self.lib.render_delta_history.argtypes = [
            ctypes.POINTER(ctypes.c_double),
            ctypes.c_size_t,
            ctypes.c_size_t
        ]
        self.lib.render_delta_history.restype = ctypes.c_char_p
        
        # free_c_string(ptr: *mut c_char) -> void
        self.lib.free_c_string.argtypes = [ctypes.c_char_p]
        self.lib.free_c_string.restype = None
    
    def render_gauge(self, delta: float, threshold: float = 0.3, width: int = 40) -> str:
        """
        Renderiza gauge de deriva usando Ratatui
        
        Args:
            delta: Score de deriva (0.0 - 1.0)
            threshold: Umbral de aprobación (default: 0.3)
            width: Ancho del gauge en caracteres
        
        Returns:
            String formateado con gauge Unicode/ASCII y colores ANSI
        """
        result = self.lib.render_line_gauge(
            ctypes.c_double(delta),
            ctypes.c_double(threshold),
            ctypes.c_size_t(width)
        )
        
        if result is None:
            return f"Error: Delta={delta:.2f}, Threshold={threshold:.2f}"
        
        gauge_str = result.decode('utf-8')
        # No liberamos memoria aquí - Python GC lo manejará
        
        return gauge_str
    
    def render_gauge_full(self, delta: float, threshold: float = 0.3, 
                          width: int = 50, height: int = 5) -> str:
        """
        Renderiza gauge completo con borde y título
        
        Args:
            delta: Score de deriva (0.0 - 1.0)
            threshold: Umbral de aprobación
            width: Ancho total
            height: Alto total
        
        Returns:
            String formateado con gauge completo
        """
        result = self.lib.render_delta_gauge(
            ctypes.c_double(delta),
            ctypes.c_double(threshold),
            ctypes.c_size_t(width),
            ctypes.c_size_t(height)
        )
        
        if result is None:
            return f"Error rendering gauge"
        
        gauge_str = result.decode('utf-8')
        return gauge_str
    
    def render_vertical_gauge(self, delta: float, threshold: float = 0.3, 
                              height: int = 10) -> str:
        """
        Renderiza gauge vertical (para barras laterales)
        
        Args:
            delta: Score de deriva (0.0 - 1.0)
            threshold: Umbral de aprobación
            height: Alto del gauge
        
        Returns:
            String formateado con gauge vertical
        """
        result = self.lib.render_vertical_gauge(
            ctypes.c_double(delta),
            ctypes.c_double(threshold),
            ctypes.c_size_t(height)
        )
        
        if result is None:
            return f"Error"
        
        gauge_str = result.decode('utf-8')
        return gauge_str
    
    def render_sparkline(self, data: List[float], width: int = 40, 
                         height: int = 5) -> str:
        """
        Renderiza sparkline de métricas usando Ratatui
        
        Args:
            data: Lista de valores para graficar (0.0 - 1.0)
            width: Ancho del sparkline
            height: Alto del sparkline
        
        Returns:
            String formateado con sparkline Unicode
        """
        if not data:
            return "Sin datos"
        
        # Convertir lista a array ctypes
        data_array = (ctypes.c_double * len(data))(*data)
        
        result = self.lib.render_simple_sparkline(
            data_array,
            ctypes.c_size_t(len(data)),
            ctypes.c_size_t(width),
            ctypes.c_size_t(height)
        )
        
        if result is None:
            return "Error rendering sparkline"
        
        sparkline_str = result.decode('utf-8')
        return sparkline_str
    
    def render_delta_history(self, history: List[float], width: int = 40) -> str:
        """
        Renderiza historial de delta como sparkline
        
        Args:
            history: Lista de valores históricos de delta
            width: Ancho del sparkline
        
        Returns:
            String formateado con sparkline del historial
        """
        if not history:
            return "Sin historial"
        
        # Limitar a últimos 50 valores
        actual_history = history[-50:]
        
        data_array = (ctypes.c_double * len(actual_history))(*actual_history)
        
        result = self.lib.render_delta_history(
            data_array,
            ctypes.c_size_t(len(actual_history)),
            ctypes.c_size_t(width)
        )
        
        if result is None:
            return "Error"
        
        history_str = result.decode('utf-8')
        return history_str


# ============================================================================
# WIDGET TEXTUAL HÍBRIDO
# ============================================================================

from textual.widgets import Static
from textual.reactive import reactive


class HybridDeltaGauge(Static):
    """
    Widget híbrido Textual + Ratatui para gauge de deriva
    
    Combina:
    - Reactividad y styling de Textual
    - Rendering visual de Ratatui (Rust)
    """
    
    # Atributos reactivos
    delta = reactive(0.0)
    threshold = reactive(0.3)
    show_history = reactive(True)
    
    # Historial para sparkline
    _history: List[float] = []
    
    DEFAULT_CSS = """
    HybridDeltaGauge {
        height: auto;
        max-height: 15;
        background: $surface;
        border: solid $primary;
        padding: 0 1;
        margin: 1 0;
    }
    
    HybridDeltaGauge.ok {
        border: solid $success;
    }
    
    HybridDeltaGauge.warning {
        border: solid $warning;
    }
    
    HybridDeltaGauge.error {
        border: solid $error;
    }
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            self.renderer = RatatuiRenderer()
            self._rust_available = True
        except FileNotFoundError:
            self._rust_available = False
            self.renderer = None
    
    def render(self) -> str:
        """
        Renderiza widget
        
        Si Rust está disponible, usa Ratatui.
        Si no, fallback a renderizado ASCII simple.
        """
        if not self._rust_available or self.renderer is None:
            return self._render_fallback()
        
        # Gauge principal
        gauge_str = self.renderer.render_gauge(
            self.delta,
            self.threshold,
            width=40
        )
        
        # Sparkline de historial (si está habilitado)
        if self.show_history and self._history:
            sparkline_str = self.renderer.render_sparkline(
                self._history[-20:],  # Últimos 20 valores
                width=40,
                height=3
            )
            return f"{gauge_str}\n{sparkline_str}"
        
        return gauge_str
    
    def _render_fallback(self) -> str:
        """Renderizado fallback sin Rust"""
        filled = int(self.delta * 40)
        bar = "█" * filled + "░" * (40 - filled)
        
        if self.delta < self.threshold:
            status = "✓ OK"
        elif self.delta < 0.7:
            status = "⚠ REVIEW"
        else:
            status = "✗ REJECT"
        
        return (
            f"Deriva: [{bar}] {self.delta*100:.1f}%/{self.threshold*100:.1f}% {status}\n"
            f"(Rust no disponible - modo fallback)"
        )
    
    def watch_delta(self, new_value: float) -> None:
        """Callback cuando delta cambia"""
        # Añadir a historial
        self._history.append(new_value)
        if len(self._history) > 100:
            self._history = self._history[-100:]
        
        # Actualizar clases CSS según estado
        self.remove_class("ok", "warning", "error")
        
        if new_value < self.threshold:
            self.add_class("ok")
        elif new_value < 0.7:
            self.add_class("warning")
        else:
            self.add_class("error")
        
        self.refresh()  # Re-render
    
    def watch_threshold(self, new_value: float) -> None:
        """Callback cuando threshold cambia"""
        self.refresh()


# ============================================================================
# DEMO
# ============================================================================

if __name__ == "__main__":
    # Demo del renderer
    print("=" * 60)
    print("DEMO: Ratatui Renderer para Textual")
    print("=" * 60)
    
    renderer = RatatuiRenderer()
    
    # Gauge OK
    print("\n1. Delta BAJO (0.15 < 0.3) - OK:")
    print(renderer.render_gauge(0.15, 0.3))
    
    # Gauge WARNING
    print("\n2. Delta MEDIO (0.45 > 0.3) - REVIEW:")
    print(renderer.render_gauge(0.45, 0.3))
    
    # Gauge ERROR
    print("\n3. Delta ALTO (0.85 > 0.3) - REJECT:")
    print(renderer.render_gauge(0.85, 0.3))
    
    # Sparkline
    print("\n4. Historial de Delta (Sparkline):")
    history = [0.1, 0.15, 0.2, 0.25, 0.3, 0.45, 0.5, 0.4, 0.35, 0.3]
    print(renderer.render_sparkline(history, width=40, height=3))
    
    # Gauge vertical
    print("\n5. Gauge Vertical:")
    print(renderer.render_vertical_gauge(0.6, 0.3, height=10))
    
    print("\n" + "=" * 60)
