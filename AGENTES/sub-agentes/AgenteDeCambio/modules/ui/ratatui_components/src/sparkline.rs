//! Módulo de Sparkline para visualización de métricas
//! 
//! Proporciona funciones para renderizar sparklines
//! que muestran historial de deriva en el tiempo

use ratatui::{
    layout::Rect,
    style::Style,
    widgets::{Sparkline, Block, Borders},
    buffer::Buffer,
};
use ratatui::prelude::Widget;
use crate::buffer_to_string;

/// Renderiza un sparkline de métricas
/// 
/// # Argumentos
/// 
/// * `data` - Slice de valores f64 para graficar
/// * `width` - Ancho del sparkline
/// * `height` - Alto del sparkline
/// * `title` - Título opcional
/// 
/// # Retorna
/// 
/// String formateado con sparkline Unicode
#[no_mangle]
pub extern "C" fn render_sparkline(
    data: *const f64,
    data_len: usize,
    width: usize,
    height: usize,
    title: *const std::os::raw::c_char,
) -> *mut std::os::raw::c_char {
    // Convertir slice de Python
    let data_slice = unsafe {
        std::slice::from_raw_parts(data, data_len)
    };
    
    // Convertir a u64 para Ratatui
    let data_u64: Vec<u64> = data_slice
        .iter()
        .map(|&x| (x * 100.0) as u64)
        .collect();
    
    // Crear área
    let area = Rect::new(0, 0, width as u16, height as u16);
    let mut buffer = Buffer::empty(area);
    
    // Crear sparkline
    let mut sparkline = Sparkline::default()
        .style(Style::new().blue().on_black())
        .data(&data_u64);
    
    // Añadir título si existe
    if !title.is_null() {
        unsafe {
            let title_str = std::ffi::CStr::from_ptr(title).to_string_lossy();
            sparkline = sparkline.block(
                Block::default()
                    .title(format!(" {} ", title_str))
                    .borders(Borders::ALL)
                    .style(Style::new().white().on_black())
            );
        }
    }
    
    // Renderizar
    sparkline.render(area, &mut buffer);
    
    // Convertir a string C
    let result = buffer_to_string(&buffer);
    crate::rust_string_to_c(result)
}

/// Renderiza un sparkline simplificado (sin título)
#[no_mangle]
pub extern "C" fn render_simple_sparkline(
    data: *const f64,
    data_len: usize,
    width: usize,
    height: usize,
) -> *mut std::os::raw::c_char {
    render_sparkline(data, data_len, width, height, std::ptr::null())
}

/// Renderiza historial de delta como sparkline
#[no_mangle]
pub extern "C" fn render_delta_history(
    delta_history: *const f64,
    history_len: usize,
    width: usize,
) -> *mut std::os::raw::c_char {
    // Limitar a últimos 50 valores
    let actual_len = history_len.min(50);
    
    render_sparkline(
        delta_history,
        actual_len,
        width,
        5,
        std::ptr::null(),
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_sparkline_render() {
        let data = vec![0.1, 0.3, 0.5, 0.7, 0.9];
        let result = render_simple_sparkline(
            data.as_ptr(),
            data.len(),
            40,
            5
        );
        
        unsafe {
            let c_str = std::ffi::CStr::from_ptr(result);
            let str_slice = c_str.to_str().unwrap();
            // El sparkline debería contener caracteres Unicode
            assert!(!str_slice.is_empty());
            crate::free_c_string(result);
        }
    }
}
