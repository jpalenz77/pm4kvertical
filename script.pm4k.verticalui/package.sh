#!/bin/bash
# Package PM4K Vertical UI addon

ADDON_NAME="script.pm4k.verticalui"
VERSION=$(python3 -c "import re; content=open('addon.xml').read(); print(re.search(r'<addon[^>]*version=\"([^\"]+)\"', content).group(1))")
OUTPUT_ZIP="${ADDON_NAME}-${VERSION}.zip"

echo "📦 Packaging ${ADDON_NAME} v${VERSION}..."

# Clean previous builds
rm -f ../${ADDON_NAME}-*.zip
rm -rf /tmp/${ADDON_NAME}

# Copy addon to temp directory
echo "📋 Copying files..."
mkdir -p /tmp/${ADDON_NAME}
cp -r * /tmp/${ADDON_NAME}/

# Remove development files
cd /tmp/${ADDON_NAME}
rm -f package.sh
rm -f .gitignore
rm -rf .git
rm -rf __pycache__
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete
find . -name ".DS_Store" -delete

# Create ZIP
echo "🗜️  Creating ZIP..."
cd /tmp
zip -r ${OUTPUT_ZIP} ${ADDON_NAME} -x "*.pyc" "*.pyo" "*__pycache__*" > /dev/null

# Move to addon parent directory
mv ${OUTPUT_ZIP} /mnt/c/pm4k-vertical-addon/

# Cleanup
rm -rf /tmp/${ADDON_NAME}

echo "✅ Package created: /mnt/c/pm4k-vertical-addon/${OUTPUT_ZIP}"
echo ""
echo "To install:"
echo "  1. Copy ZIP to your Kodi device"
echo "  2. In Kodi: Settings > Add-ons > Install from zip file"
echo "  3. Select ${OUTPUT_ZIP}"
