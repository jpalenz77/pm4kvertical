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
