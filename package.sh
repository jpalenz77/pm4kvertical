#!/bin/bash
# Script para empaquetar el addon Plex Vertical UI v2.0.0

ADDON_ID="script.plexmod.verticalui"
VERSION="2.0.0"
ZIP_NAME="$ADDON_ID-$VERSION.zip"

echo "================================================"
echo "  Empaquetando Plex Vertical UI v$VERSION"
echo "================================================"
echo ""
echo "Verificando archivos necesarios..."

# Verificar archivos críticos
MISSING=0

if [ ! -f "$ADDON_ID/default.py" ]; then
    echo "❌ Falta: default.py"
    MISSING=1
fi

if [ ! -f "$ADDON_ID/resources/lib/vertical_home.py" ]; then
    echo "❌ Falta: resources/lib/vertical_home.py"
    MISSING=1
fi

if [ ! -f "$ADDON_ID/resources/skins/Main/1080i/script-plex-vertical-home.xml" ]; then
    echo "❌ Falta: resources/skins/Main/1080i/script-plex-vertical-home.xml"
    MISSING=1
fi

if [ ! -f "$ADDON_ID/resources/settings.xml" ]; then
    echo "❌ Falta: resources/settings.xml"
    MISSING=1
fi

if [ $MISSING -eq 1 ]; then
    echo ""
    echo "❌ Faltan archivos necesarios."
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
