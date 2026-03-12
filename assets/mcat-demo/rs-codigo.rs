use std::io::prelude::*;
use std::net::{TcpListener, TcpStream};

/// Server Táctico para la demo de Mcat.
fn main() -> std::io::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:8080")?;
    println!("ARES Protocol: Server Listening on Port 8080...");

    for stream in listener.incoming() {
        match stream {
            Ok(s) => handle_connection(s),
            Err(e) => eprintln!("Error handling connection: {}", e),
        }
    }
    Ok(())
}

fn handle_connection(mut stream: TcpStream) {
    let mut buffer = [0; 1024];
    if stream.read(&mut buffer).is_ok() {
        let response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello from Mcat Demo!";
        let _ = stream.write(response.as_bytes());
        let _ = stream.flush();
    }
}
