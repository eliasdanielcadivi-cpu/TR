#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { Client, LocalAuth } = require('whatsapp-web.js');
const express = require('express');
const qrcode = require('qrcode-terminal');

const app = express();
app.use(express.json());

const DEPURACION = process.argv.includes('--depuracion');
const LOG_DIR = path.join(__dirname, 'logs');

if (DEPURACION && !fs.existsSync(LOG_DIR)) fs.mkdirSync(LOG_DIR);

function log(tipo, mensaje) {
    const timestamp = new Date().toISOString();
    const linea = `[${timestamp}] [${tipo.toUpperCase()}] ${mensaje}\n`;
    console.log(linea.trim());
    if (DEPURACION) {
        fs.appendFileSync(path.join(LOG_DIR, `${tipo}.log`), linea);
    }
}

const client = new Client({
    authStrategy: new LocalAuth({ dataPath: './wwebjs_auth' }),
    puppeteer: {
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

client.on('qr', qr => {
    log('info', 'Escanea el QR con tu WhatsApp');
    qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
    log('info', 'Cliente listo');
});

client.on('message', async msg => {
    log('mensaje', `De: ${msg.from} | Texto: ${msg.body}`);
    // Enviar a n8n
    fetch('http://localhost:5678/webhook/whatsapp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ from: msg.from, body: msg.body })
    }).catch(err => log('error', 'Fallo al enviar a n8n: ' + err.message));
});

client.initialize();

// API: buscar contacto
app.get('/buscar', async (req, res) => {
    const numero = req.query.numero;
    if (!numero) return res.status(400).json({ error: 'Falta número' });

    try {
        const id = `${numero}@c.us`;
        const contacto = await client.getContactById(id);
        if (contacto && contacto.number) {
            log('info', `Contacto encontrado: ${contacto.number}`);
            return res.json({ encontrado: true, nombre: contacto.pushname || contacto.name });
        } else {
            log('warn', `Contacto no encontrado: ${numero}`);
            return res.json({ encontrado: false });
        }
    } catch (e) {
        log('error', 'Error al buscar: ' + e.message);
        res.status(500).json({ error: e.message });
    }
});

// API: enviar mensaje
app.post('/enviar', async (req, res) => {
    const { numero, mensaje } = req.body;
    if (!numero || !mensaje) return res.status(400).json({ error: 'Faltan datos' });

    try {
        const id = `${numero}@c.us`;
        await client.sendMessage(id, mensaje);
        log('info', `Mensaje enviado a ${numero}`);
        res.json({ enviado: true });
    } catch (e) {
        log('error', 'Error al enviar: ' + e.message);
        res.status(500).json({ error: e.message });
    }
});

const PORT = 3000;
app.listen(PORT, () => log('info', `API escuchando en http://localhost:${PORT}`));
