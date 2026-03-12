# 📋 AGENDA DE PRUEBAS — FASE 3 (Sistema Apollo + Emojis + Modelos)

**Fecha:** 2026-03-10 (Mañana)
**Prioridad:** ALTA — Validación antes de continuar con CRM

---

## 🕐 BLOQUE 1: Emojis y Term-Image (30 min)

### 1.1 Verificar assets
```bash
# Verificar que existen los archivos
ls -la /home/daniel/tron/programas/TR/assets/ares/ares-emoji.png
ls -la /home/daniel/tron/programas/TR/assets/user/user-emoji.png
```

### 1.2 Probar emoji_manager.py
```bash
cd /home/daniel/tron/programas/TR
source .venv/bin/activate

# Probar en Python
python3 -c "
from modules.ia.apollo.emoji_manager import show_emoji, format_output_with_emoji

# Mostrar emoji ARES
print(show_emoji('ares', width=4, height=1))

# Mostrar emoji USER
print(show_emoji('user', width=2, height=1))

# Formatear texto con emoji
print(format_output_with_emoji('Hola desde ARES', 'ares', prefix=True, width=4, height=1))
"
```

**Resultado esperado:** Imágenes PNG mostradas en terminal (protocolo Kitty)

### 1.3 Probar ares i con emojis
```bash
ares i
# Verificar:
# - Emoji de ARES en encabezado
# - Emoji de USER en prompt "🧑 Tú"
# - Respuestas con emoji de ARES
```

---

## 🕐 BLOQUE 2: Post-procesamiento (30 min)

### 2.1 Verificar config.yaml
```bash
# Verificar sección post_processing
grep -A 20 "post_processing:" /home/daniel/tron/programas/TR/config/config.yaml
```

**Debe mostrar:**
```yaml
post_processing:
  ares:
    strip_think_tags: true
  ares-think:
    strip_think_tags: false
  smollm3:
    strip_think_tags: true
```

### 2.2 Probar generation.py
```bash
cd /home/daniel/tron/programas/TR
source .venv/bin/activate

python3 -c "
from modules.ia.apollo.generation import apply_post_process, strip_think_tags

# Texto con think tags
text = '<think>Esto es razonamiento</think>Esta es la respuesta'

# Probar sin post-procesamiento
print('Sin post-process:', text)

# Probar con post-procesamiento (ares)
result = apply_post_process(text, 'ares')
print('Con post-process (ares):', result)

# Probar strip_think_tags directo
result2 = strip_think_tags(text)
print('strip_think_tags:', result2)
"
```

**Resultado esperado:**
```
Sin post-process: <think>Esto es razonamiento</think>Esta es la respuesta
Con post-process (ares): Esta es la respuesta
strip_think_tags: Esta es la respuesta
```

---

## 🕐 BLOQUE 3: ares i --think (30 min)

### 3.1 Probar modo interactivo normal
```bash
ares i
# Comandos dentro de la sesión:
/model ares
# Preguntar: "quien eres"
# Verificar: Respuesta SIN etiquetas <think></think>
```

### 3.2 Probar modo interactivo con --think
```bash
ares i --think
# Verificar en encabezado: "Think Mode: ON (usa ares-think)"
# Comandos dentro de la sesión:
/think status
# Preguntar: "quien eres"
# Verificar: Respuesta CON etiquetas <think></think> (si ares-think está configurado)
```

### 3.3 Probar comando /think en sesión
```bash
ares i
# Dentro de la sesión:
/think on
# Verificar: Cambia a ares-think:latest
/think off
# Verificar: Cambia a ares:latest
```

---

## 🕐 BLOQUE 4: ares p --rag --think (30 min)

### 4.1 Probar consulta con RAG
```bash
ares p "¿Qué es Apollo?" --rag docs
# Verificar:
# - Recuperación de chunks relevantes
# - Respuesta con contexto
# - Fuentes al final
```

### 4.2 Probar consulta con RAG + think
```bash
ares p "¿Qué es Apollo?" --rag docs --think
# Verificar:
# - Usa ares-think:latest
# - Mantiene etiquetas <think></think> (si el modelo las genera)
```

### 4.3 Probar diferentes datasets
```bash
ares p "skills disponibles" --rag skills
ares p "código Python" --rag codigo
ares p "configuración" --rag config
```

---

## 🕐 BLOQUE 5: mcat (15 min)

### 5.1 Instalar mcat
```bash
bash /home/daniel/tron/programas/TR/scripts/install_mcat.sh
# O manualmente:
# 1. Visitar https://github.com/Skardyy/mcat/releases/latest
# 2. Descargar .tar.gz para Linux
# 3. tar xzf mcat*.tar.gz
# 4. sudo mv mcat /usr/local/bin/
```

### 5.2 Probar mcat
```bash
mcat --version
mcat /home/daniel/tron/programas/TR/docs/FASE0-COMPLETADA-APOLLO-DB.md
```

---

## 🕐 BLOQUE 6: model_creator y modelfile_creator (PENDIENTE)

**NOTA:** Estos módulos aún no están implementados. Se crearán después de validar lo anterior.

---

## ✅ CRITERIOS DE ÉXITO

- [ ] Emojis se muestran como imágenes PNG en terminal (no caracteres Unicode)
- [ ] `ares i` muestra emojis en encabezado y prompt
- [ ] `ares i --think` activa modo pensante correctamente
- [ ] `ares p --think` usa ares-think:latest
- [ ] Post-procesamiento elimina think tags en modelo `ares`
- [ ] Post-procesamiento MANTIENE think tags en modelo `ares-think`
- [ ] RAG funciona con datasets (docs, skills, codigo, config)
- [ ] mcat instalado y funcional

---

## 🐛 POSIBLES ISSUES

| Issue | Solución |
|-------|----------|
| Emojis no se muestran | Verificar que Kitty soporta protocolo de imágenes |
| `show_emoji()` retorna fallback | Verificar rutas de archivos PNG |
| `ares i` no reconoce --think | Actualizar main.py (ya está actualizado) |
| Post-procesamiento no funciona | Verificar config.yaml (sección post_processing) |
| mcat no se instala | Usar script install_mcat.sh o binario manual |

---

## 📝 NOTAS

- **Aviso programado:** Mañana 7:00 AM (ya configurado)
- **Documentación actualizada:** INDEX.md, LEEME.md, MODELOS-ARES.md
- **TODO actualizado:** TODO-RAG-GRAFICO-SQLITE-VECTORIAL.md

---

*Esta agenda debe completarse antes de continuar con model_creator.py y modelfile_creator.py*
