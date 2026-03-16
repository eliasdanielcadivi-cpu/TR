//! Módulo de Gauge para métricas de deriva
//! 
//! Proporciona funciones para renderizar gauges de progreso
//! que muestran el score de deriva (0.0 - 1.0)

use ratatui::{
    layout::Rect,
    style::Style,
    widgets::{Gauge, Block, Borders},
    buffer::Buffer,
};
use ratatui::prelude::Widget;
use crate::buffer_to_string;

/// Renderiza un gauge de deriva tradicional
/// 
/// # Argumentos
/// 
/// * `delta` - Score de deriva (0.0 a 1.0)
/// * `threshold` - Umbral de aprobación (ej: 0.3)
/// * `width` - Ancho del gauge en caracteres
/// * `height` - Alto del gauge (mínimo 3)
/// 
/// # Retorna
/// 
/// String formateado con gauge Unicode/ASCII
#[no_mangle]
pub extern "C" fn render_delta_gauge(
    delta: f64,
    threshold: f64,
    width: usize,
    height: usize,
) -> *mut std::os::raw::c_char {
    // Determinar color según delta
    let (gauge_style, label) = if delta < threshold {
        (Style::new().green().on_black(), format!("Δ: {:.1}% ✓", delta * 100.0))
    } else if delta < 0.7 {
        (Style::new().yellow().on_black(), format!("Δ: {:.1}% ⚠", delta * 100.0))
    } else {
        (Style::new().red().on_black(), format!("Δ: {:.1}% ✗", delta * 100.0))
    };
    
    // Crear área
    let area = Rect::new(0, 0, width as u16, height as u16);
    let mut buffer = Buffer::empty(area);
    
    // Crear gauge con borde
    let gauge = Gauge::default()
        .block(Block::default()
            .title(" Deriva del Prompt ")
            .borders(Borders::ALL)
            .style(Style::new().white().on_black())
        )
        .gauge_style(gauge_style)
        .label(label)
        .ratio(delta.min(1.0));
    
    // Renderizar
    gauge.render(area, &mut buffer);
    
    // Convertir a string C
    let result = buffer_to_string(&buffer);
    crate::rust_string_to_c(result)
}

/// Renderiza un line gauge compacto (una sola línea)
/// 
/// # Argumentos
/// 
/// * `delta` - Score de deriva (0.0 a 1.0)
/// * `threshold` - Umbral de aprobación
/// * `width` - Ancho de la barra (sin contar texto)
/// 
/// # Retorna
/// 
/// String con gauge en línea
#[no_mangle]
pub extern "C" fn render_line_gauge(
    delta: f64,
    threshold: f64,
    width: usize,
) -> *mut std::os::raw::c_char {
    // Calcular caracteres llenos
    let filled = ((delta.min(1.0)) * width as f64) as usize;
    
    // Crear barra con caracteres Unicode
    let bar = "█".repeat(filled) + &"░".repeat(width - filled);
    
    // Determinar estado
    let (status, color_code) = if delta < threshold {
        ("✓ OK", "32")  // Verde
    } else if delta < 0.7 {
        ("⚠ REVIEW", "33")  // Amarillo
    } else {
        ("✗ REJECT", "31")  // Rojo
    };
    
    // Formatear con colores ANSI
    let result = format!(
        "\x1b[{}mDeriva: [{}] {:.1}%/{:.1}% {}\x1b[0m",
        color_code,
        bar,
        delta * 100.0,
        threshold * 100.0,
        status
    );
    
    crate::rust_string_to_c(result)
}

/// Renderiza un gauge vertical (para barras laterales)
#[no_mangle]
pub extern "C" fn render_vertical_gauge(
    delta: f64,
    threshold: f64,
    height: usize,
) -> *mut std::os::raw::c_char {
    let filled = ((delta.min(1.0)) * height as f64) as usize;
    let empty = height - filled;
    
    let (color_code, status) = if delta < threshold {
        ("32", "✓")  // Verde
    } else if delta < 0.7 {
        ("33", "⚠")  // Amarillo
    } else {
        ("31", "✗")  // Rojo
    };
    
    // Construir barra vertical
    let mut result = String::from("┌");
    for _ in 0..10 { result.push('─'); }
    result.push_str("┐\n");
    
    for _ in 0..filled {
        result.push_str(&format!("\x1b[{}m│██████████\x1b[0m\n", color_code));
    }
    for _ in 0..empty {
        result.push_str("│░░░░░░░░░░\n");
    }
    
    result.push('└');
    for _ in 0..10 { result.push('─'); }
    result.push_str(&format!("┘ {}", status));
    
    crate::rust_string_to_c(result)
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_line_gauge_ok() {
        let result = render_line_gauge(0.2, 0.3, 40);
        unsafe {
            let c_str = std::ffi::CStr::from_ptr(result);
            let str_slice = c_str.to_str().unwrap();
            assert!(str_slice.contains("✓ OK"));
            crate::free_c_string(result);
        }
    }
    
    #[test]
    fn test_line_gauge_warning() {
        let result = render_line_gauge(0.5, 0.3, 40);
        unsafe {
            let c_str = std::ffi::CStr::from_ptr(result);
            let str_slice = c_str.to_str().unwrap();
            assert!(str_slice.contains("⚠ REVIEW"));
            crate::free_c_string(result);
        }
    }
    
    #[test]
    fn test_line_gauge_error() {
        let result = render_line_gauge(0.8, 0.3, 40);
        unsafe {
            let c_str = std::ffi::CStr::from_ptr(result);
            let str_slice = c_str.to_str().unwrap();
            assert!(str_slice.contains("✗ REJECT"));
            crate::free_c_string(result);
        }
    }
}
