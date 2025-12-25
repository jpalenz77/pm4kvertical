#!/bin/bash
# Script COMPLETO para crear el addon de Plex Vertical UI
# Este script crea TODOS los archivos necesarios

set -e

echo "============================================"
echo "  Plex Vertical UI - Complete Addon Creator"
echo "============================================"
echo ""

ADDON_ID="script.plexmod.verticalui"
ADDON_DIR="$ADDON_ID"

# Verificar que no exista ya
if [ -d "$ADDON_DIR" ]; then
    echo "⚠️  El directorio $ADDON_DIR ya existe"
    read -p "¿Deseas eliminarlo y continuar? (s/n): " confirm
    if [ "$confirm" != "s" ]; then
        echo "Operación cancelada"
        exit 1
    fi
    rm -rf "$ADDON_DIR"
fi

# Crear estructura
echo "📁 Creando estructura de directorios..."
mkdir -p "$ADDON_DIR/resources/patches"
mkdir -p "$ADDON_DIR/resources/files"

# ============================================================================
# CREAR TODOS LOS ARCHIVOS
# ============================================================================

echo "📝 Creando archivos..."

# ----------------------------------------------------------------------------
# 1. addon.xml
# ----------------------------------------------------------------------------
cat > "$ADDON_DIR/addon.xml" << 'ADDONXML'
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<addon id="script.plexmod.verticalui"
       name="Plex Vertical UI Installer"
       version="1.0.0"
       provider-name="Moids">
    <requires>
        <import addon="xbmc.python" version="3.0.0"/>
        <import addon="script.module.six" />
    </requires>
    <extension point="xbmc.python.script" library="installer.py">
        <provides>executable</provides>
    </extension>
    <extension point="xbmc.addon.metadata">
        <platform>all</platform>
        <summary lang="en_GB">Vertical UI Mod installer for Plex for Kodi</summary>
        <summary lang="es_ES">Instalador de modificación UI Vertical para Plex for Kodi</summary>
        <description lang="en_GB">This addon installs a vertical navigation UI modification for Plex for Kodi (script.plexmod). Features modern design with vertical scrolling, smooth animations, and remote control optimization.</description>
        <description lang="es_ES">Este addon instala una modificación de interfaz de navegación vertical para Plex for Kodi (script.plexmod). Incluye diseño moderno con scroll vertical, animaciones suaves y optimización para mando a distancia.</description>
        <disclaimer lang="en_GB">Unofficial modification. Use at your own risk. Requires script.plexmod.</disclaimer>
        <disclaimer lang="es_ES">Modificación no oficial. Úsala bajo tu propio riesgo. Requiere script.plexmod.</disclaimer>
        <license>GPL-2.0-only</license>
        <news>
v1.0.0 (2025-12-25)
- Initial release
- Vertical navigation UI
- Modern dark theme
- Smooth animations
- One-click installer
        </news>
    </extension>
</addon>
ADDONXML

echo "  ✅ addon.xml"

# ----------------------------------------------------------------------------
# 2. README.md
# ----------------------------------------------------------------------------
cat > "$ADDON_DIR/README.md" << 'README'
# Plex Vertical UI Installer

Instalador de interfaz vertical para Plex for Kodi.

## Instalación

1. Instala este addon desde el ZIP
2. Ejecuta: Programas → Plex Vertical UI Installer
3. Selecciona "Instalar UI Vertical"
4. Ve a Configuración de Plex → Activa "Usar interfaz vertical"
5. Reinicia Plex

## Características

- Navegación vertical
- Diseño moderno
- Animaciones suaves
- Optimizado para mando

## Requisitos

- Kodi 19+
- script.plexmod instalado
README

echo "  ✅ README.md"

# ----------------------------------------------------------------------------
# 3. Patches
# ----------------------------------------------------------------------------

cat > "$ADDON_DIR/resources/patches/default_py.patch" << 'PATCH1'
                
                # ==================== VERTICAL UI INTEGRATION ====================
                import xbmcaddon
                addon = xbmcaddon.Addon()
                use_vertical_ui = addon.getSetting('use_vertical_ui')
                
                if use_vertical_ui == 'true':
                    log('Main: script.plexmod: Vertical UI mode enabled')
                    try:
                        from lib.vertical_home import VerticalHomeWindow
                        log('Main: script.plexmod: Starting Vertical UI...')
                        setGlobalProperty('running', '1', wait=True)
                        addon_path = addon.getAddonInfo('path')
                        window = VerticalHomeWindow(
                            'script-plex-vertical-home.xml',
                            addon_path,
                            'Main',
                            '1080i',
                            plex_network=None
                        )
                        window.doModal()
                        del window
                        setGlobalProperty('running', '', wait=True)
                        log('Main: script.plexmod: Vertical UI closed')
                        sys.exit(0)
                    except Exception as e:
                        log('Main: script.plexmod: Error starting Vertical UI: {}', e)
                        xbmcgui.Dialog().ok('Error', 'Error al iniciar la interfaz vertical.', str(e))
                # ==================== END VERTICAL UI INTEGRATION ====================
PATCH1

cat > "$ADDON_DIR/resources/patches/settings_xml.patch" << 'PATCH2'
                <!-- ==================== VERTICAL UI SETTING ==================== -->
                <setting id="use_vertical_ui" type="boolean" label="Usar interfaz vertical" help="Cambia la navegación de horizontal a vertical">
                    <level>0</level>
                    <default>false</default>
                    <control type="toggle"/>
                </setting>
                <!-- ============================================================= -->
PATCH2

echo "  ✅ Patches creados"

# ----------------------------------------------------------------------------
# 4. Nota sobre archivos que deben copiarse
# ----------------------------------------------------------------------------

cat > "$ADDON_DIR/resources/files/README.txt" << 'FILESREADME'
ARCHIVOS QUE DEBES COPIAR AQUÍ:

1. vertical_home.py
   - El archivo Python con la lógica de la UI vertical

2. script-plex-vertical-home.xml
   - El archivo XML con el diseño visual

Estos archivos deben copiarse desde donde los creaste originalmente.
FILESREADME

echo "  ✅ Nota en resources/files/"

# ----------------------------------------------------------------------------
# 5. Crear placeholder para installer.py
# ----------------------------------------------------------------------------

cat > "$ADDON_DIR/installer_placeholder.txt" << 'PLACEHOLDER'
IMPORTANTE: 

Este es un placeholder. Debes crear el archivo installer.py en la raíz
del addon con el código completo del instalador.

El código está en el artifact "installer.py" que te proporcioné.
PLACEHOLDER

echo "  ✅ Placeholder para installer.py"

# ----------------------------------------------------------------------------
# 6. Crear iconos placeholder
# ----------------------------------------------------------------------------

# Crear un PNG simple de 1x1 pixel (placeholder)
printf '\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0d\x49\x44\x41\x54\x08\x99\x63\xf8\xcf\xc0\x00\x00\x03\x01\x01\x00\x18\xdd\x8d\xb4\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82' > "$ADDON_DIR/icon.png"

echo "  ✅ icon.png (placeholder)"

# ----------------------------------------------------------------------------
# RESUMEN
# ----------------------------------------------------------------------------

echo ""
echo "============================================"
echo "✅ Estructura básica creada!"
echo "============================================"
echo ""
echo "📋 Lo que se creó:"
echo ""
echo "  ✅ addon.xml"
echo "  ✅ README.md"
echo "  ✅ resources/patches/default_py.patch"
echo "  ✅ resources/patches/settings_xml.patch"
echo "  ✅ icon.png (placeholder)"
echo ""
echo "⚠️  ARCHIVOS QUE DEBES COPIAR MANUALMENTE:"
echo ""
echo "1. installer.py → $ADDON_DIR/"
echo "   (Del artifact 'installer.py')"
echo ""
echo "2. vertical_home.py → $ADDON_DIR/resources/files/"
echo "   (Tu archivo que ya creaste)"
echo ""
echo "3. script-plex-vertical-home.xml → $ADDON_DIR/resources/files/"
echo "   (Tu archivo XML que ya creaste)"
echo ""
echo "============================================"
echo "📦 Para crear el ZIP:"
echo ""
echo "Después de copiar los archivos:"
echo "  zip -r script.plexmod.verticalui-1.0.0.zip $ADDON_DIR/"
echo ""
echo "============================================"

# Crear script helper para empaquetar
cat > "package.sh" << 'PKGSCRIPT'
#!/bin/bash
# Script para empaquetar el addon

ADDON_ID="script.plexmod.verticalui"
ZIP_NAME="$ADDON_ID-1.0.0.zip"

echo "Verificando archivos necesarios..."

# Verificar archivos críticos
MISSING=0

if [ ! -f "$ADDON_ID/installer.py" ]; then
    echo "❌ Falta: installer.py"
    MISSING=1
fi

if [ ! -f "$ADDON_ID/resources/files/vertical_home.py" ]; then
    echo "❌ Falta: vertical_home.py"
    MISSING=1
fi

if [ ! -f "$ADDON_ID/resources/files/script-plex-vertical-home.xml" ]; then
    echo "❌ Falta: script-plex-vertical-home.xml"
    MISSING=1
fi

if [ $MISSING -eq 1 ]; then
    echo ""
    echo "❌ Faltan archivos necesarios. Cópialos primero."
    exit 1
fi

# Crear ZIP
echo "📦 Creando ZIP..."
rm -f "$ZIP_NAME"
zip -r "$ZIP_NAME" "$ADDON_ID/" -x "*.DS_Store" "*/__pycache__/*" "*.pyc"

echo ""
echo "✅ ¡Addon empaquetado!"
echo "📦 Archivo: $ZIP_NAME"
echo ""
echo "Tamaño:"
ls -lh "$ZIP_NAME" | awk '{print "  " $5}'
echo ""
echo "Para instalar en Kodi:"
echo "  Settings → Add-ons → Install from zip file"
PKGSCRIPT

chmod +x package.sh

echo ""
echo "📝 Script de empaquetado creado: package.sh"
echo ""
echo "Cuando tengas todos los archivos, ejecuta:"
echo "  ./package.sh"
echo ""
echo "============================================"
