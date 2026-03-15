//! Componentes Visuales Ratatui para AgenteDeCambio CLI
//! 
//! Esta biblioteca proporciona componentes visuales renderizados con Ratatui
//! que pueden ser incrustados en aplicaciones Textual (Python) vía FFI.
//! 
//! # Uso
//! 
//! ```rust
//! use ratatui_components::gauge::render_line_gauge;
//! 
//! let gauge_str = render_line_gauge(0.25, 0.3, 40);
//! println!("{}", gauge_str);
//! ```

pub mod gauge;
pub mod sparkline;
pub mod chart;

use std::ffi::{CStr, CString};
use std::os::raw::c_char;
use ratatui::buffer::Buffer;
use ratatui::layout::Rect;

/// Convierte un buffer de Ratatui a string C (para FFI con Python)
pub fn buffer_to_string(buffer: &Buffer) -> String {
    let mut result = String::new();
    let rect = buffer.area;
    
    for y in rect.top()..rect.bottom() {
        for x in rect.left()..rect.right() {
            let cell = buffer.get(x, y);
            result.push_str(&cell.symbol);
        }
        if y < rect.bottom() - 1 {
            result.push('\n');
        }
    }
    
    result
}

/// Función helper para convertir Rust String a C string (para Python)
fn rust_string_to_c(string: String) -> *mut c_char {
    CString::new(string).unwrap().into_raw()
}

/// Libera memoria de string C (llamado desde Python)
#[no_mangle]
pub extern "C" fn free_c_string(ptr: *mut c_char) {
    if ptr.is_null() {
        return;
    }
    unsafe {
        let _ = CString::from_raw(ptr);
    }
}
