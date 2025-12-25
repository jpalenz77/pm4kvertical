#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Plex Vertical UI - Standalone Edition
Modern vertical navigation interface for Plex
Main entry point
"""

from __future__ import absolute_import, unicode_literals
import xbmc
import xbmcaddon
import xbmcgui
import os
import sys

# Addon info
ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_PATH = ADDON.getAddonInfo('path')

# Add lib directory to Python path
lib_path = os.path.join(ADDON_PATH, 'resources', 'lib')
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

def main():
    """
    Punto de entrada principal
    """
    xbmc.log('[{}] Starting Plex Vertical UI Standalone Edition'.format(ADDON_ID), xbmc.LOGINFO)
    
    try:
        # Check if server is configured
        server_url = ADDON.getSetting('plex_server')
        token = ADDON.getSetting('plex_token')
        
        if not server_url or not token:
            # First run - show configuration
            show_first_run_dialog()
            return
            
        # Import and start the vertical UI
        from vertical_home import VerticalHomeWindow
        
        window = VerticalHomeWindow(
            'script-plex-vertical-home.xml',
            ADDON_PATH,
            'Main',
            '1080i'
        )
        
        window.doModal()
        del window
        
    except ImportError as e:
        xbmc.log('[{}] Import error: {}'.format(ADDON_ID, e), xbmc.LOGERROR)
        xbmcgui.Dialog().ok(
            'Error de importación',
            'No se pudo importar el módulo vertical_home.',
            'Verifique que todos los archivos estén instalados correctamente.'
        )
        
    except Exception as e:
        xbmc.log('[{}] Error: {}'.format(ADDON_ID, e), xbmc.LOGERROR)
        xbmcgui.Dialog().ok(
            'Error',
            'Error al iniciar Plex Vertical UI:',
            str(e)
        )

def show_first_run_dialog():
    """
    Muestra el diálogo de primera ejecución para configurar Plex
    """
    dialog_text = (
        "¡Bienvenido a Plex Vertical UI!\n\n"
        "Para comenzar, necesitas configurar:\n"
        "1. URL del servidor Plex (ej: http://192.168.1.100:32400)\n"
        "2. Token de autenticación de Plex\n\n"
        "¿Abrir configuración ahora?"
    )
    
    if xbmcgui.Dialog().yesno('Primera ejecución', dialog_text):
        ADDON.openSettings()
        
        # Verificar si ahora está configurado
        server_url = ADDON.getSetting('plex_server')
        token = ADDON.getSetting('plex_token')
        
        if not server_url or not token:
            xbmcgui.Dialog().ok(
                'Configuración incompleta',
                'Necesitas configurar ambos campos:',
                '• URL del servidor Plex',
                '• Token de autenticación'
            )
        else:
            xbmcgui.Dialog().ok(
                '¡Configuración guardada!',
                'Servidor: ' + server_url,
                '',
                'Vuelve a abrir el addon para comenzar.'
            )
    else:
        xbmcgui.Dialog().ok(
            'Configuración requerida',
            'Puedes configurar el servidor más tarde desde:',
            'Complementos > Plex Vertical UI > Configurar'
        )

if __name__ == '__main__':
    main()