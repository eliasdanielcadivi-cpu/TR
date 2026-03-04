# 🔑 Configuración de DeepSeek API Key para ARES

## Problema Detectado

El error `Error: API key de DeepSeek no configurada` indica que la variable de entorno `DEEPSEEK_API_KEY` no está disponible en el shell actual.

---

## ✅ Solución: Configurar API Key

### Opción 1: Variable de Entorno Temporal (Sesión Actual)

```bash
export DEEPSEEK_API_KEY="tu-api-key-aqui"
```

**Nota:** Esta configuración solo dura mientras la terminal esté abierta.

---

### Opción 2: Variable de Entorno Permanente (~/.bashrc o ~/.zshrc)

```bash
# Añadir al final de ~/.bashrc o ~/.zshrc
echo 'export DEEPSEEK_API_KEY="tu-api-key-aqui"' >> ~/.bashrc

# Recargar configuración
source ~/.bashrc
```

**Para ZSH:**
```bash
echo 'export DEEPSEEK_API_KEY="tu-api-key-aqui"' >> ~/.zshrc
source ~/.zshrc
```

---

### Opción 3: Archivo .env en el Proyecto TR

```bash
# Crear archivo .env en TR/
cd /home/daniel/tron/programas/TR
echo "DEEPSEEK_API_KEY=tu-api-key-aqui" > .env

# Cargar automáticamente al usar ares
# (Requiere modificar bin/ares para cargar .env)
```

---

## 🔍 Verificar Configuración

```bash
# Verificar si está configurada
echo $DEEPSEEK_API_KEY

# Debería mostrar los primeros caracteres de tu key
# Ejemplo: sk-abc123...
```

---

## 📝 Obtener API Key de DeepSeek

1. Visitar [DeepSeek Platform](https://platform.deepseek.com/)
2. Iniciar sesión o crear cuenta
3. Ir a **API Keys** en el dashboard
4. Click en **"Create API Key"**
5. Copiar y guardar en lugar seguro

---

## 🧪 Probar Configuración

```bash
# Test simple
ares p "Hola, ¿cómo estás?" --model deepseek

# Si funciona, verás respuesta de DeepSeek
# Si falla, verificarás el error de API key
```

---

## ⚠️ Notas de Seguridad

- **NUNCA** compartas tu API key públicamente
- **NUNCA** la commitees a Git
- Usa `.gitignore` para excluir archivos `.env`
- Considera usar un gestor de secretos para producción

---

## 🔧 Debugging

Si el error persiste:

```bash
# 1. Verificar variable de entorno
env | grep DEEPSEEK

# 2. Verificar que bin/ares carga el entorno correcto
cd /home/daniel/tron/programas/TR
source .venv/bin/activate
echo $DEEPSEEK_API_KEY

# 3. Probar directamente con Python
python3 -c "import os; print(os.getenv('DEEPSEEK_API_KEY'))"
```

---

## 📊 Costos y Límites

DeepSeek API es de pago por token usado:

- **Input:** ~$0.14 / 1M tokens
- **Output:** ~$0.28 / 1M tokens

**Verificar uso en:** https://platform.deepseek.com/usage

---

*Documentación creada para ARES - Terminal Remote Operations Nexus*
