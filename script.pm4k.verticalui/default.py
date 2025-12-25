#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PM4K Vertical UI - Main Entry Point
Adds vertical navigation interface to PlexMod
"""

from __future__ import absolute_import, unicode_literals
import sys
import os
from kodi_six import xbmc, xbmcaddon, xbmcgui, xbmcvfs

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')

def check_pm4k_installed():
    """Check if PM4K is installed"""
    try:
        pm4k_addon = xbmcaddon.Addon('script.plexmod')
        return True
    except:
        return False

def main():
    """Main entry point"""
    xbmc.log('[{}] PM4K Vertical UI Starting'.format(ADDON_ID), xbmc.LOGINFO)
    
    # Check if PM4K is installed
    if not check_pm4k_installed():
        xbmcgui.Dialog().ok(
            'PM4K No Instalado',
            'PM4K Vertical UI requiere PlexMod (PM4K) instalado.',
            '',
            'Por favor instala PM4K primero desde https://pm4k.eu'
        )
        return
    
    # Import PM4K modules
    try:
        # Add PM4K lib to path
        pm4k_addon = xbmcaddon.Addon('script.plexmod')
        pm4k_path = pm4k_addon.getAddonInfo('path')
        try:
            # Kodi 19+
            pm4k_lib = os.path.join(xbmcvfs.translatePath(pm4k_path), 'lib')
        except:
            # Kodi 18
            pm4k_lib = os.path.join(xbmc.translatePath(pm4k_path).decode('utf-8'), 'lib')
        if pm4k_lib not in sys.path:
            sys.path.insert(0, pm4k_lib)
        
        # Import PM4K modules
        import plexnet
        from plexnet import plexapp
        from lib.windows import kodigui
        
        # Check if user is signed in
        if not plexapp.ACCOUNT or not plexapp.SERVERMANAGER.selectedServer:
            xbmcgui.Dialog().ok(
                'PM4K No Configurado',
                'Por favor configura y autentícate en PM4K primero.',
                '',
                'Abre PM4K y configura tu servidor Plex.'
            )
            return
        
        # Launch vertical UI
        from resources.lib import vertical_window
        window = vertical_window.VerticalHomeWindow.open()
        
    except ImportError as e:
        xbmc.log('[{}] Import error: {}'.format(ADDON_ID, e), xbmc.LOGERROR)
        xbmcgui.Dialog().ok(
            'Error de Importación',
            'No se pudo cargar PM4K correctamente.',
            str(e)
        )
    except Exception as e:
        xbmc.log('[{}] Error: {}'.format(ADDON_ID, e), xbmc.LOGERROR)
        xbmcgui.Dialog().ok(
            'Error',
            'Error al iniciar PM4K Vertical UI:',
            str(e)
        )

if __name__ == '__main__':
    import os
    main()
