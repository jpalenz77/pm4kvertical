# Guía de Configuración - Plex Vertical UI

## 🔧 Configuración Inicial

### 1. URL del Servidor Plex

La URL de tu servidor Plex local. Formato:
```
http://IP_DEL_SERVIDOR:32400
```

**Ejemplos:**
- `http://192.168.1.100:32400` (servidor en red local)
- `http://localhost:32400` (servidor en el mismo dispositivo)

### 2. Token de Autenticación

El token es necesario para conectarse a tu servidor Plex.

#### Método 1: Desde Plex Web App

1. Abre Plex Web en tu navegador
2. Ve a cualquier contenido (película, serie, etc.)
3. Haz clic en los 3 puntos (⋮) → "Get Info"
4. Ve a "View XML"
5. En la URL verás: `?X-Plex-Token=XXXXXXXXXX`
6. Copia todo lo que viene después de `=`

#### Método 2: Desde plex.tv/claim

1. Inicia sesión en https://app.plex.tv
2. Ve a https://www.plex.tv/claim/
3. Verás un código de 4 caracteres
4. Este código expira en 4 minutos - úsalo rápidamente

#### Método 3: Desde archivo de preferencias

**Windows:**
```
%LOCALAPPDATA%\Plex Media Server\Preferences.xml
```

**Linux/CoreELEC:**
```
/storage/.config/plexmediaserver/Library/Application Support/Plex Media Server/Preferences.xml
```

**Mac:**
```
~/Library/Application Support/Plex Media Server/Preferences.xml
```

Busca `PlexOnlineToken="XXXXXXXXXX"`

## 🚀 Inicio Rápido

1. Abre el addon "Plex Vertical UI"
2. Cuando pregunte, selecciona "Yes" para configurar
3. Introduce la **URL del servidor** (ej: http://192.168.1.100:32400)
4. Introduce el **Token** obtenido anteriormente
5. Guarda y cierra
6. Vuelve a abrir el addon
7. ¡Disfruta!

## ❓ Problemas Comunes

### No se puede conectar al servidor

- Verifica que la URL sea correcta
- Asegúrate de que Plex Media Server esté ejecutándose
- Prueba con `http://` en lugar de `https://`
- Verifica que el puerto 32400 esté accesible

### Token inválido

- El token debe ser una cadena alfanumérica larga (20+ caracteres)
- No incluyas espacios antes/después
- Si usaste plex.tv/claim, el código expira en 4 minutos

### El addon se cierra solo

- Verifica que hayas configurado AMBOS campos (URL + Token)
- Revisa los logs de Kodi: `/storage/.kodi/temp/kodi.log`
- Busca errores relacionados con `script.plexmod.verticalui`

## 📝 Configuración Avanzada

Una vez funcionando, puedes ajustar:

- **Velocidad de animación**: 50-200%
- **Elementos por página**: Cantidad de items a cargar
- **Ancho de barra lateral**: 300-500 px
- **Tema**: Dark/Light/Auto
- **Opacidad de fondo**: 50-100%

## 🔍 Más Ayuda

Si tienes problemas, revisa:
- Logs de Kodi
- README.md del proyecto
- GitHub: https://github.com/jpalenz77/pm4kvertical
