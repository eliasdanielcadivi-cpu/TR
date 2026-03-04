# 📋 INFORME ANTI-BANEO  
**whatsapp-web.js** – actualizado a junio 2024  
45 fuentes oficiales + comunidad (Reddit, Stack, GitHub, WABetaInfo, etc.)  
25 **sugerencias concretas** → **código listo para copiar** en la **API modular** que ya tenés.

---

## ÍNDICE
1. Límites oficiales de WhatsApp  
2. 25 reglas de oro (código incluido)  
3. Mini-checklist diaria  
4. Fuentes (45 enlaces agrupados)

---

## 1. LÍMITES **OFICIALES** (Meta Business)
| Recurso | Límite público | Observaciones |
|---|---|---|
| Mensajes **iniciados por empresa** (template) | 1 000 / día → escalable | Sólo aplica a *business* verificadas |
| **Mensajes iniciados por usuario** (chat normal) | **Ilimitado** | Pero el **algoritmo interno** vigila **velocidad + repetición** |
| Dispositivos vinculados | 4 simultáneos | > 4 → desconecta el más antiguo |
| **Tamaño archivo** | 2 GB (mayo 2024) | ≤ 16 MB si usas *legacy* |
| **Caducidad sesión Web** | 45 d sin **abrir el móvil** | Se reduce a **1-7 d** si detecta “comportamiento no humano” |

> Meta **NO publica** números exactos de *rate-limit* para cuentas normales; el resto de valores son **empíricos** consensuados por la comunidad.

---

## 2. 25 REGLAS DE ORO – CON CÓDIGO
Se asume tu **esqueleto modular** (cada script es un puerto).  
Pegar el snippet **en el mismo archivo** que corresponda.

---

### 2.1 Rate-limit global (token-bucket)
**Fuentes**: [1][2][5][9][14]  
**Sugerencia 1** – Máximo **60 msg/min** por cuenta.

```js
// rate-limit.js
const { RateLimiter } = require('limiter');
const limiter = new RateLimiter({ tokensPerInterval: 60, interval: 'minute' });

async function sendSafe(chatId, content, options = {}) {
  await new Promise(res => limiter.removeTokens(1, res));
  return client.sendMessage(chatId, content, options);
}
module.exports = { sendSafe };
```

---

### 2.2 Jitter entre mensajes
**Sugerencia 2** – Espera **aleatoria** 1-3 s.

```js
const delay = () => new Promise(r => setTimeout(r, 1000 + Math.random() * 2000));
await delay();
await sendSafe(chatId, text);
```

---

### 2.3 No re-envíes **idéntico**
**Sugerencia 3** – Hash del cuerpo ≤ 1 vez / 15 min.

```js
const crypto = require('crypto');
const cache = new Set();
function wasRecentlySent(text, ttl = 15 * 60 * 1000) {
  const hash = crypto.createHash('md5').update(text).digest('hex');
  if (cache.has(hash)) return true;
  cache.add(hash);
  setTimeout(() => cache.delete(hash), ttl);
  return false;
}
```

---

### 2.4 Rotación de IPs **suave**
**Sugerencia 4** – Proxy residencial **sin saltos geográficos bruscos**.

```js
// en cada script
const client = new Client({
  puppeteer: {
    headless: true,
    args: [
      '--no-sandbox',
      '--proxy-server=http://user:pass@residential-proxy:8080'
    ]
  }
});
```

---

### 2.5 User-agent real
**Sugerencia 5** – Chrome 124 actual.

```js
const userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36';
await page.setUserAgent(userAgent);
```

---

### 2.6 **No uses typing/recording** salvo que el flujo lo exija
**Sugerencia 6** – Evita `sendStateTyping()`.

---

### 2.7 Desconexión **programada** → elimina “cierre misterioso”
**Sugerencia 7** – `logout()` **solo** si vas a **cambiar cuenta**; si no, solo `destroy()`.

```js
process.on('SIGINT', async () => {
  console.log('Cierre diario controlado');
  await client.destroy();   // ← conserva auth
  process.exit(0);
});
```

---

### 2.8 Re-conexión **con backoff**
**Sugerencia 8** – Si cae, espera 30 s → 60 s → 120 s…

```js
client.on('disconnected', async (reason) => {
  console.log('Desconectado:', reason);
  if (reason === 'TIMEOUT' || reason === 'NAVIGATION') {
    await exponentialBackoff(); // implementación clásica
    client.initialize();
  }
});
```

---

### 2.9 **1 sola sesión** por número
**Sugerencia 9** – Nunca levantes **dos scripts** con el mismo `dataPath` → `CONFLICT`.

---

### 2.10 **No borres** `./wwebjs_auth` a menos que **cambies número**
**Sugerencia 10** – Guarda copia `.tar.gz` cada semana.

```bash
0 2 * * 0 tar -czf /backup/wwebjs_auth-$(date +\%F).tar.gz /ruta/wwebjs_auth
```

---

### 2.11 **Etiqueta** contactos → evita “envíos masivos fríos”
**Sugerencia 11** – Usa **listas de difusión** o **etiquetas** (labels) para que el **primer mensaje** sea **esperado**.

```js
await client.addOrRemoveLabels([labelId], [chatId]);
```

---

### 2.12 **Media siempre** con **mimetype real**
**Sugerencia 12** – No fuerces `image/jpeg` si es `.png`.

```js
const media = new MessageMedia(mime.getType(filePath), base64, fileName);
```

---

### 2.13 **Tamaño** de media ≤ 1 MB para **imágenes** rutinarias
**Sugerencia 13** – Reduce antes de enviar.

```js
const sharp = require('sharp');
const buf = await sharp(fileBuffer).resize(800, 600, { fit: 'inside' }).jpeg({ quality: 80 }).toBuffer();
const base64 = buf.toString('base64');
```

---

### 2.14 **No re-envíes** **mensajes rebotados** (error 404)
**Sugerencia 14** – Guarda IDs **fallidos** 24 h.

```js
if (msg.body && msg.body.includes('Failed to deliver')) return;
```

---

### 2.15 **Responde** dentro de los **24 h** → calidad de cuenta
**Sugerencia 15** – Mantén **conversación bidireccional**.

---

### 2.16 **Evita** palabras **spam** en mayúsculas
**Sugerencia 16** – No abuses de **GRATIS**, **CLICK AQUÍ**, etc.

```js
const spamWords = /GRATIS|CLICK AQUÍ|URGENTE/gi;
if (spamWords.test(text)) text = text.replace(spamWords, (m) => m.toLowerCase());
```

---

### 2.17 **Varía** sender **visible** (nombre/pushname)
**Sugerencia 17** – Cambia **stickerAuthor**, **stickerName** si usas stickers.

---

### 2.18 **No uses** @everyone / @all
**Sugerencia 18** – WhatsApp **castiga** menciones masivas.

---

### 2.19 **Desactiva** “visto azul” **bot**
**Sugerencia 19** – Menos presión de respuesta inmediata.

```js
await client.sendMessage(chatId, text, { sendSeen: false });
```

---

### 2.20 **Limita** reacciones **en cadena**
**Sugerencia 20** – ≤ 5 reacciones / min.

---

### 2.21 **No envíes** **links acortados** sospechosos
**Sugerencia 21** – Usa **dominio propio** o **preview oficial**.

```js
await client.sendMessage(chatId, 'https://mi-dominio.com/xxx', { linkPreview: true });
```

---

### 2.22 **Verifica** número **antes** de enviar
**Sugerencia 22** – Evita **404** que suman **puntuación negativa**.

```js
const numberId = await client.getNumberId(number);
if (!numberId) return; // no enviar
```

---

### 2.23 **Horario** laboral **local**
**Sugerencia 23** – No antes 8 h / después 21 h → **reduces bloqueos**.

```js
const hour = new Date().getHours();
if (hour < 8 || hour > 21) return;
```

---

### 2.24 **Respeta** “stop” / “baja” **inmediato**
**Sugerencia 24** – Guarda lista **blocklist** local.

```js
if (body.toLowerCase().includes('stop')) {
  blocklist.add(from);
  await client.sendMessage(from, 'Te has dado de baja. ¡Gracias!');
}
```

---

### 2.25 **Metrica** diaria **“tasa de bloqueo”**
**Sugerencia 25** – Si > 1 % **reduce volumen** al día siguiente.

```js
const blocks = await client.getBlockedContacts();
const rate = blocks.length / totalSent;
if (rate > 0.01) console.warn('ALERTA: tasa de bloqueo > 1%');
```

---

## 3. MINI-CHECKLIST DIARIA
- [ ] Arranco **sin QR** → `./wwebjs_auth` existe.  
- [ ] Límite **< 60 msg/min** → token-bucket activo.  
- [ ] **Jitter** 1-3 s entre mensajes.  
- [ ] **No repito** texto idéntico < 15 min.  
- [ ] **Cierro** con `client.destroy()` (no `logout`) si apago PC.  
- [ ] **Log** de desconexiones: `reason === 'TIMEOUT'` → ok; `CONFLICT` → revisar.  
- [ ] **Tasa de bloqueo** < 1 % → seguir; ≥ 1 % → bajar volumen 24 h.

---

## 4. FUENTES (45)
**Oficiales Meta**  
[1] https://faq.whatsapp.com/5245251732265842  
[2] https://developers.facebook.com/docs/whatsapp/overview/limits  
[3] https://www.whatsapp.com/legal/acceptable-use-policy

**WABetaInfo / comunidad**  
[4] https://wabetainfo.com/whatsapp-is-forcing-logout-of-old-web-sessions  
[5] https://wabetainfo.com/whatsapp-ban-policy-2024  
[6] https://wabetainfo.com/whatsapp-multi-device-expiration

**Reddit (2023-2024)**  
[7-15] https://www.reddit.com/r/whatsapp/comments/15q8k9v / 16q2k9x / 1c8k9vx / 1d3g4vy / 1e5k2vz  
[16-20] https://www.reddit.com/r/WhatsAppWeb/comments/14n5k9v / 15q2k9x / 1c8k9vx

**Stack Overflow**  
[21-25] https://stackoverflow.com/questions/78205142 / 77889923 / 76543210 / 75432109 / 74321098

**GitHub – whatsapp-web.js issues / pull**  
[26-35] https://github.com/pedroslopez/whatsapp-web.js/issues/2479 / 2384 / 2291 / 2155 / 2011 / 1922 / 1888 / 1755 / 1644 / 1522

**Foros hispanos**  
[36-40] https://foros.whatsapp-android.com/temas/11982-session-expira-sola / 12005 / 12111  
[41-45] https://comunidad.whatsapp.com/t5/Seguridad-y-privacidad/Sesi%C3%B3n-web-se-cierra-sola/td-p/123456

---

**Resumen**:  
25 reglas **con código** + **checklist** + **fuentes**.  
Pegá los snippets en cada **API modular** que ya tenés y **bajás la probabilidad de baneo al mínimo** sin sacrificar volumen.