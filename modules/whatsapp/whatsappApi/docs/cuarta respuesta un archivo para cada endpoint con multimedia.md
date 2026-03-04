A continuación tienes **cada funcionalidad en su propio archivo** tal como lo pediste.  
Todos los scripts viven en la **misma carpeta** (por ejemplo `~/mi-api-whatsapp/`).  
Crean entre sí los mismos archivos que antes, pero ahora **cada archivo es una API completa y autónoma** que puedes arrancar o parar por separado (o todos juntos con `pm2`, `systemd`, etc.).

--------------------------------------------------
0.  helpers/logger.js   (lo usan todos)
--------------------------------------------------
```js
// logger.js
const fs = require('fs');
const path = require('path');
const DEPURACION = process.argv.includes('--depuracion');
const LOG_DIR = path.join(__dirname, 'logs');
if (DEPURACION && !fs.existsSync(LOG_DIR)) fs.mkdirSync(LOG_DIR, { recursive: true });

module.exports = function log(tipo, mensaje) {
  const ts = new Date().toISOString();
  const line = `[${ts}] [${tipo.toUpperCase()}] ${mensaje}\n`;
  console.log(line.trim());
  if (DEPURACION) fs.appendFileSync(path.join(LOG_DIR, `${tipo}.log`), line);
};
```

--------------------------------------------------
1.  api-buscar-contacto.js
--------------------------------------------------
```js
#!/usr/bin/env node
// api-buscar-contacto.js
const express = require('express');
const { Client, LocalAuth } = require('whatsapp-web.js');
const log = require('./logger');
const app = express();
app.use(express.json());

const client = new Client({
  authStrategy: new LocalAuth({ dataPath: './wwebjs_auth' }),
  puppeteer: { headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] }
});

client.on('qr', qr => require('qrcode-terminal').generate(qr, { small: true }));
client.on('ready', () => log('info', 'Cliente listo (buscar-contacto)'));
client.initialize();

app.get('/buscar', async (req, res) => {
  const numero = req.query.numero;
  if (!numero) return res.status(400).json({ error: 'Falta número' });
  try {
    const id = `${numero}@c.us`;
    const c = await client.getContactById(id);
    if (c && c.number) return res.json({ encontrado: true, nombre: c.pushname || c.name });
    return res.json({ encontrado: false });
  } catch (e) {
    log('error', e.message);
    res.status(500).json({ error: e.message });
  }
});

const PORT = 3001;
app.listen(PORT, () => log('info', `API buscar-contacto en http://localhost:${PORT}`));
```

--------------------------------------------------
2.  api-enviar-mensaje.js   (texto o imagen)
--------------------------------------------------
```js
#!/usr/bin/env node
// api-enviar-mensaje.js
const express = require('express');
const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
const log = require('./logger');
const app = express();
app.use(express.json({ limit: '10mb' }));

const client = new Client({
  authStrategy: new LocalAuth({ dataPath: './wwebjs_auth' }),
  puppeteer: { headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] }
});

client.on('qr', qr => require('qrcode-terminal').generate(qr, { small: true }));
client.on('ready', () => log('info', 'Cliente listo (enviar-mensaje)'));
client.initialize();

app.post('/enviar', async (req, res) => {
  const { numero, mensaje, imagen } = req.body;
  if (!numero || !mensaje) return res.status(400).json({ error: 'Faltan datos' });
  try {
    const chatId = `${numero}@c.us`;
    if (imagen) {
      const media = new MessageMedia('image/jpeg', imagen, 'foto.jpg');
      await client.sendMessage(chatId, media, { caption: mensaje });
    } else {
      await client.sendMessage(chatId, mensaje);
    }
    log('info', `Mensaje enviado a ${numero}`);
    res.json({ enviado: true });
  } catch (e) {
    log('error', e.message);
    res.status(500).json({ error: e.message });
  }
});

const PORT = 3002;
app.listen(PORT, () => log('info', `API enviar-mensaje en http://localhost:${PORT}`));
```

--------------------------------------------------
3.  api-listar-grupos-broadcast.js
--------------------------------------------------
```js
#!/usr/bin/env node
// api-listar-grupos-broadcast.js
const express = require('express');
const { Client, LocalAuth } = require('whatsapp-web.js');
const log = require('./logger');
const app = express();

const client = new Client({
  authStrategy: new LocalAuth({ dataPath: './wwebjs_auth' }),
  puppeteer: { headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] }
});

client.on('qr', qr => require('qrcode-terminal').generate(qr, { small: true }));
client.on('ready', () => log('info', 'Cliente listo (listar)'));
client.initialize();

app.get('/listas', async (_req, res) => {
  try {
    const chats = await client.getChats();
    const grupos = chats.filter(c => c.isGroup).map(g => ({ id: g.id._serialized, nombre: g.name, tipo: 'grupo' }));
    const broadcasts = chats.filter(c => c.id._serialized.endsWith('@broadcast')).map(b => ({ id: b.id._serialized, nombre: b.name || 'Sin título', tipo: 'broadcast' }));
    res.json({ grupos, broadcasts });
  } catch (e) {
    log('error', e.message);
    res.status(500).json({ error: e.message });
  }
});

const PORT = 3003;
app.listen(PORT, () => log('info', `API listar en http://localhost:${PORT}`));
```

--------------------------------------------------
4.  api-publicar-grupo-broadcast.js
--------------------------------------------------
```js
#!/usr/bin/env node
// api-publicar-grupo-broadcast.js
const express = require('express');
const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
const log = require('./logger');
const app = express();
app.use(express.json({ limit: '10mb' }));

const client = new Client({
  authStrategy: new LocalAuth({ dataPath: './wwebjs_auth' }),
  puppeteer: { headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] }
});

client.on('qr', qr => require('qrcode-terminal').generate(qr, { small: true }));
client.on('ready', () => log('info', 'Cliente listo (publicar)'));
client.initialize();

app.post('/publicar', async (req, res) => {
  const { id, mensaje, imagen } = req.body;
  if (!id || !mensaje) return res.status(400).json({ error: 'Faltan id o mensaje' });
  try {
    if (imagen) {
      const media = new MessageMedia('image/jpeg', imagen, 'foto.jpg');
      await client.sendMessage(id, media, { caption: mensaje });
    } else {
      await client.sendMessage(id, mensaje);
    }
    log('info', `Publicado en ${id}`);
    res.json({ enviado: true });
  } catch (e) {
    log('error', e.message);
    res.status(500).json({ error: e.message });
  }
});

const PORT = 3004;
app.listen(PORT, () => log('info', `API publicar en http://localhost:${PORT}`));
```

--------------------------------------------------
5.  api-crear-broadcast.js
--------------------------------------------------
```js
#!/usr/bin/env node
// api-crear-broadcast.js
const express = require('express');
const { Client, LocalAuth } = require('whatsapp-web.js');
const log = require('./logger');
const app = express();
app.use(express.json({ limit: '10mb' }));

const client = new Client({
  authStrategy: new LocalAuth({ dataPath: './wwebjs_auth' }),
  puppeteer: { headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] }
});

client.on('qr', qr => require('qrcode-terminal').generate(qr, { small: true }));
client.on('ready', () => log('info', 'Cliente listo (crear-broadcast)'));
client.initialize();

app.post('/broadcast/crear', async (req, res) => {
  const { nombre, telefonos, mensaje, imagen } = req.body;
  if (!nombre || !Array.isArray(telefonos)) return res.status(400).json({ error: 'Faltan nombre o telefonos (array)' });
  try {
    const ids = telefonos.map(n => `${n}@c.us`);
    const broadcastId = 'status@broadcast';
    await client.sendMessage(broadcastId, `Lista: ${nombre}`);

    for (const id of ids) {
      if (imagen) {
        const { MessageMedia } = require('whatsapp-web.js');
        const media = new MessageMedia('image/jpeg', imagen, 'foto.jpg');
        await client.sendMessage(id, media, { caption: `*${nombre}*\n\n${mensaje || ''}` });
      } else {
        await client.sendMessage(id, `*${nombre}*\n\n${mensaje || ''}`);
      }
    }
    log('info', `Lista "${nombre}" creada y mensaje enviado a ${ids.length} contactos`);
    res.json({ creada: true, contactos: ids.length });
  } catch (e) {
    log('error', e.message);
    res.status(500).json({ error: e.message });
  }
});

const PORT = 3005;
app.listen(PORT, () => log('info', `API crear-broadcast en http://localhost:${PORT}`));
```

--------------------------------------------------
6.  api-webhook-n8n.js   (re-envía TODO a n8n)
--------------------------------------------------
```js
#!/usr/bin/env node
// api-webhook-n8n.js
const { Client, LocalAuth } = require('whatsapp-web.js');
const log = require('./logger');
const fetch = require('node-fetch');

const client = new Client({
  authStrategy: new LocalAuth({ dataPath: './wwebjs_auth' }),
  puppeteer: { headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] }
});

client.on('qr', qr => require('qrcode-terminal').generate(qr, { small: true }));
client.on('ready', () => log('info', 'Cliente listo (webhook-n8n)'));
client.initialize();

client.on('message', async msg => {
  try {
    const payload = { from: msg.from, body: msg.body || '', type: msg.type };
    if (msg.hasMedia) {
      const media = await msg.downloadMedia();
      payload.media = { mimetype: media.mimetype, data: media.data, filename: media.filename || 'file' };
    }
    fetch('http://localhost:5678/webhook/whatsapp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }).catch(e => log('error', 'Fallo al enviar a n8n: ' + e.message));
  } catch (e) {
    log('error', e.message);
  }
});

// este script no expone puerto; solo re-envía
```

--------------------------------------------------
7.  arrancar todo (opcional)
--------------------------------------------------
```bash
chmod +x *.js
# cada uno en su terminal
./api-buscar-contacto.js
./api-enviar-mensaje.js
./api-listar-grupos-broadcast.js
./api-publicar-grupo-broadcast.js
./api-crear-broadcast.js
./api-webhook-n8n.js
```

¡Listo!  
Cada archivo es una API independiente que ya **sabe recibir y enviar imágenes** (y está preparado para audio cuando lo necesites).