//! Módulo de Chart para gráficos de datos
//! 
//! Proporciona funciones para renderizar gráficos
//! de líneas y barras para visualización de métricas

use ratatui::{
    layout::Rect,
    style::{Style, Color},
    widgets::{Chart, Dataset, GraphType, Axis, Block, Borders},
    buffer::Buffer,
};
use crate::buffer_to_string;

/// Renderiza un gráfico de líneas simple
#[no_mangle]
pub extern "C" fn render_line_chart(
    x_data: *const f64,
    y_data: *const f64,
    data_len: usize,
    width: usize,
    height: usize,
    title: *const std::os::raw::c_char,
    x_label: *const std::os::raw::c_char,
    y_label: *const std::os::raw::c_char,
) -> *mut std::os::raw::c_char {
    // Convertir slices de Python
    let x_slice = unsafe {
        std::slice::from_raw_parts(x_data, data_len)
    };
    let y_slice = unsafe {
        std::slice::from_raw_parts(y_data, data_len)
    };
    
    // Crear puntos
    let points: Vec<(f64, f64)> = x_slice.iter()
        .zip(y_slice.iter())
        .map(|(&x, &y)| (x, y))
        .collect();
    
    // Crear área
    let area = Rect::new(0, 0, width as u16, height as u16);
    let mut buffer = Buffer::empty(area);
    
    // Crear dataset
    let dataset = Dataset::default()
        .name("Datos")
        .marker(ratatui::symbols::Marker::Dot)
        .graph_type(GraphType::Line)
        .style(Style::new().yellow())
        .data(&points);
    
    // Crear ejes
    let x_min = x_slice.iter().cloned().fold(f64::INFINITY, f64::min);
    let x_max = x_slice.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    let y_min = y_slice.iter().cloned().fold(f64::INFINITY, f64::min);
    let y_max = y_slice.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    
    let mut chart = Chart::new(vec![dataset])
        .block(Block::default().borders(Borders::ALL).style(Style::new().white().on_black()))
        .x_axis(
            Axis::default()
                .style(Style::new().white())
                .bounds([x_min, x_max])
        )
        .y_axis(
            Axis::default()
                .style(Style::new().white())
                .bounds([y_min, y_max])
        );
    
    // Añadir títulos si existen
    if !title.is_null() {
        unsafe {
            let title_str = std::ffi::CStr::from_ptr(title).to_string_lossy();
            let block = chart.block().unwrap_or(&Block::default());
            chart = chart.block(block.clone().title(format!(" {} ", title_str)));
        }
    }
    
    // Renderizar
    chart.render(area, &mut buffer);
    
    // Convertir a string C
    let result = buffer_to_string(&buffer);
    crate::rust_string_to_c(result)
}

/// Renderiza un gráfico de barras simple
#[no_mangle]
pub extern "C" fn render_bar_chart(
    labels: *const *const std::os::raw::c_char,
    values: *const f64,
    data_len: usize,
    width: usize,
    height: usize,
) -> *mut std::os::raw::c_char {
    // Implementación simplificada usando caracteres ASCII
    let values_slice = unsafe {
        std::slice::from_raw_parts(values, data_len)
    };
    
    let mut result = String::new();
    let max_value = values_slice.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    
    for (i, &value) in values_slice.iter().enumerate() {
        let bar_length = ((value / max_value) * (width as f64 - 10.0)) as usize;
        let bar = "█".repeat(bar_length);
        
        // Obtener label si existe
        let label = unsafe {
            if labels.is_null() {
                format!("Item {}", i + 1)
            } else {
                let label_ptr = *labels.add(i);
                std::ffi::CStr::from_ptr(label_ptr).to_string_lossy().to_string()
            }
        };
        
        result.push_str(&format!("{:<8} |{} ({:.1})\n", label, bar, value));
    }
    
    crate::rust_string_to_c(result)
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[test]
    fn test_line_chart() {
        let x_data = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let y_data = vec![2.0, 4.0, 1.0, 5.0, 3.0];
        
        let result = render_line_chart(
            x_data.as_ptr(),
            y_data.as_ptr(),
            x_data.len(),
            40,
            10,
            std::ptr::null(),
            std::ptr::null(),
            std::ptr::null(),
        );
        
        unsafe {
            let c_str = std::ffi::CStr::from_ptr(result);
            let str_slice = c_str.to_str().unwrap();
            assert!(!str_slice.is_empty());
            crate::free_c_string(result);
        }
    }
}
