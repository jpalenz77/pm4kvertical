#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Plex Vertical UI - Standalone Edition
Modern vertical navigation interface for Plex
"""

from __future__ import absolute_import, unicode_literals
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
import json
import requests
import threading
import time
try:
    from urllib.parse import urlparse, parse_qs
except ImportError:
    from urlparse import urlparse, parse_qs

# Addon info
ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_PATH = ADDON.getAddonInfo('path')

class PlexAPI(object):
    """
    Plex API client for standalone operation
    """
    
    def __init__(self):
        self.server_url = ADDON.getSetting('plex_server')
        self.token = ADDON.getSetting('plex_token')
        self.session = requests.Session()
        self.session.headers.update({
            'X-Plex-Token': self.token,
            'X-Plex-Client-Identifier': 'plex-vertical-ui-kodi',
            'X-Plex-Product': 'Plex Vertical UI',
            'X-Plex-Version': ADDON.getAddonInfo('version'),
            'X-Plex-Platform': 'Kodi',
            'X-Plex-Device': 'PC',
            'Accept': 'application/json'
        })
    
    def get_libraries(self):
        """
        Obtiene las bibliotecas del servidor Plex
        """
        try:
            response = self.session.get("{}{}".format(self.server_url, "/library/sections"))
            data = response.json()
            return data.get('MediaContainer', {}).get('Directory', [])
        except Exception as e:
            xbmc.log('[{}] PlexAPI: Error getting libraries: {}'.format(ADDON_ID, e), xbmc.LOGERROR)
            return []
    
    def get_library_content(self, library_key, start=0, size=50):
        """
        Obtiene contenido de una biblioteca
        """
        try:
            url = "{}/library/sections/{}/all".format(self.server_url, library_key)
            params = {
                'X-Plex-Container-Start': start,
                'X-Plex-Container-Size': size
            }
            response = self.session.get(url, params=params)
            data = response.json()
            return data.get('MediaContainer', {}).get('Metadata', [])
        except Exception as e:
            xbmc.log('[{}] PlexAPI: Error getting library content: {}'.format(ADDON_ID, e), xbmc.LOGERROR)
            return []
    
    def search(self, query):
        """
        Buscar contenido en Plex
        """
        try:
            url = "{}/search".format(self.server_url)
            params = {'query': query}
            response = self.session.get(url, params=params)
            data = response.json()
            return data.get('MediaContainer', {}).get('Metadata', [])
        except Exception as e:
            xbmc.log('[{}] PlexAPI: Error searching: {}'.format(ADDON_ID, e), xbmc.LOGERROR)
            return []

class VerticalHomeWindow(xbmcgui.WindowXML):
    """
    Ventana principal con navegación vertical moderna
    """
    
    # Control IDs
    SECTION_LIST_ID = 100
    CONTENT_LIST_ID = 200
    SEARCH_BUTTON_ID = 300
    SETTINGS_BUTTON_ID = 400
    USER_BUTTON_ID = 500
    
    def __init__(self, *args, **kwargs):
        super(VerticalHomeWindow, self).__init__()
        self.plex_api = PlexAPI()
        self.current_library = None
        self.libraries = []
        self.content_items = []
        self.loading = False
        
    def onInit(self):
        """
        Inicialización de la ventana
        """
        xbmc.log('[{}] VerticalHome: Iniciando interfaz vertical'.format(ADDON_ID), xbmc.LOGINFO)
        
        # Verificar configuración
        if not self.plex_api.server_url or not self.plex_api.token:
            self.show_configuration_error()
            return
            
        self.load_libraries()
        
    def show_configuration_error(self):
        """
        Muestra error de configuración
        """
        if xbmcgui.Dialog().yesno(
            'Configuración incompleta',
            'El servidor Plex no está configurado.',
            '¿Quieres abrir la configuración ahora?'
        ):
            ADDON.openSettings()
            self.close()
        else:
            self.close()
        
    def load_libraries(self):
        """
        Carga las bibliotecas de Plex
        """
        if self.loading:
            return
            
        self.loading = True
        
        def _load_libraries():
            try:
                self.libraries = self.plex_api.get_libraries()
                
                # Si no hay bibliotecas reales, usar mock data
                if not self.libraries:
                    self.libraries = self.get_mock_libraries()
                
                xbmc.executebuiltin('Container.Refresh')
                self.populate_sections()
                
                # Cargar contenido de la primera biblioteca
                if self.libraries:
                    self.load_library_content(self.libraries[0].get('key', 'movies'))
                    
            except Exception as e:
                xbmc.log('[{}] VerticalHome: Error loading libraries: {}'.format(ADDON_ID, e), xbmc.LOGERROR)
                # Usar datos de demostración en caso de error
                self.libraries = self.get_mock_libraries()
                self.populate_sections()
                self.load_mock_content()
            finally:
                self.loading = False
        
        thread = threading.Thread(target=_load_libraries)
        thread.daemon = True
        thread.start()
    
    def get_mock_libraries(self):
        """
        Bibliotecas de demostración
        """
        return [
            {'title': 'Películas', 'type': 'movie', 'key': 'movies'},
            {'title': 'Series', 'type': 'show', 'key': 'shows'},
            {'title': 'Música', 'type': 'artist', 'key': 'music'},
            {'title': 'Fotos', 'type': 'photo', 'key': 'photos'},
            {'title': 'Documentales', 'type': 'movie', 'key': 'documentaries'}
        ]
        
    def populate_sections(self):
        """
        Poblar la lista de secciones
        """
        try:
            section_list = self.getControl(self.SECTION_LIST_ID)
            section_list.reset()
            
            for library in self.libraries:
                item = xbmcgui.ListItem()
                item.setLabel(library.get('title', 'Sin título'))
                
                # Iconos por tipo de biblioteca
                library_type = library.get('type', '')
                if library_type == 'movie':
                    icon = 'DefaultMovies.png'
                elif library_type == 'show':
                    icon = 'DefaultTVShows.png'
                elif library_type == 'artist':
                    icon = 'DefaultMusicArtists.png'
                else:
                    icon = 'DefaultFolder.png'
                    
                item.setArt({'icon': icon, 'thumb': icon})
                item.setProperty('library_key', str(library.get('key', '')))
                item.setProperty('library_type', library_type)
                
                section_list.addItem(item)
                
        except Exception as e:
            xbmc.log('[{}] VerticalHome: Error populating sections: {}'.format(ADDON_ID, e), xbmc.LOGERROR)
            
    def load_library_content(self, library_key, start=0):
        """
        Carga el contenido de una biblioteca
        """
        if self.loading:
            return
            
        self.loading = True
        self.current_library = library_key
        
        def _load_content():
            try:
                content = self.plex_api.get_library_content(library_key, start)
                
                # Si no hay contenido real, usar mock data
                if not content:
                    content = self.get_mock_content()
                
                if start == 0:
                    self.content_items = content
                else:
                    self.content_items.extend(content)
                    
                xbmc.executebuiltin('Container.Refresh')
                self.populate_content()
                
            except Exception as e:
                xbmc.log('[{}] VerticalHome: Error loading content: {}'.format(ADDON_ID, e), xbmc.LOGERROR)
                # Usar datos de demostración
                self.content_items = self.get_mock_content()
                self.populate_content()
            finally:
                self.loading = False
                
        thread = threading.Thread(target=_load_content)
        thread.daemon = True
        thread.start()
    
    def get_mock_content(self):
        """
        Contenido de demostración
        """
        return [
            {
                'title': 'Avengers: Endgame',
                'tagline': 'El final del juego',
                'summary': 'Los héroes restantes deben encontrar una manera de revertir las acciones de Thanos.',
                'year': 2019,
                'rating': 8.4,
                'duration': 10860000,  # ms
                'thumb': '/library/metadata/1/thumb',
                'art': '/library/metadata/1/art',
                'key': '/library/metadata/1',
                'type': 'movie'
            },
            {
                'title': 'The Mandalorian',
                'tagline': 'Esta es la forma',
                'summary': 'Las aventuras de un cazarrecompensas mandaloriano en los confines de la galaxia.',
                'year': 2019,
                'rating': 8.8,
                'duration': 2400000,
                'thumb': '/library/metadata/2/thumb',
                'art': '/library/metadata/2/art',
                'key': '/library/metadata/2',
                'type': 'show'
            },
            {
                'title': 'Spider-Man: No Way Home',
                'tagline': 'El multiverso se abre',
                'summary': 'Peter Parker busca ayuda del Doctor Strange cuando su identidad secreta es revelada.',
                'year': 2021,
                'rating': 8.2,
                'duration': 8880000,
                'thumb': '/library/metadata/3/thumb',
                'art': '/library/metadata/3/art',
                'key': '/library/metadata/3',
                'type': 'movie'
            }
        ]
        
    def populate_content(self):
        """
        Poblar la lista de contenido
        """
        try:
            content_list = self.getControl(self.CONTENT_LIST_ID)
            
            # Solo limpiar si es contenido nuevo
            if not hasattr(self, '_content_loaded') or not self._content_loaded:
                content_list.reset()
                self._content_loaded = True
                
            for item_data in self.content_items:
                item = xbmcgui.ListItem()
                
                # Título y metadata
                title = item_data.get('title', 'Sin título')
                item.setLabel(title)
                item.setLabel2(item_data.get('tagline', ''))
                
                # Descripción
                summary = item_data.get('summary', '')
                item.setProperty('description', summary)
                
                # Año
                year = item_data.get('year', '')
                if year:
                    item.setProperty('year', str(year))
                    
                # Rating
                rating = item_data.get('rating', '')
                if rating:
                    item.setProperty('rating', "{:.1f}".format(float(rating)))
                    
                # Duración
                duration = item_data.get('duration', '')
                if duration:
                    minutes = int(duration) // 60000  # Convert from ms
                    item.setProperty('duration', "{} min".format(minutes))
                    
                # Arte - usar placeholders si no hay servidor real
                thumb = item_data.get('thumb', '')
                if thumb and self.plex_api.server_url and not thumb.startswith('http'):
                    thumb = "{}{}?X-Plex-Token={}".format(
                        self.plex_api.server_url, thumb, self.plex_api.token
                    )
                else:
                    # Placeholder para demo
                    thumb = 'DefaultVideo.png'
                    
                art = item_data.get('art', '')
                if art and self.plex_api.server_url and not art.startswith('http'):
                    art = "{}{}?X-Plex-Token={}".format(
                        self.plex_api.server_url, art, self.plex_api.token
                    )
                else:
                    art = 'DefaultVideo.png'
                    
                item.setArt({
                    'thumb': thumb,
                    'fanart': art,
                    'poster': thumb
                })
                
                # Propiedades para reproducción
                item.setProperty('plex_key', item_data.get('key', ''))
                item.setProperty('media_type', item_data.get('type', ''))
                
                content_list.addItem(item)
                
        except Exception as e:
            xbmc.log('[{}] VerticalHome: Error populating content: {}'.format(ADDON_ID, e), xbmc.LOGERROR)
            
    def onAction(self, action):
        """
        Manejo de acciones del usuario
        """
        action_id = action.getId()
        
        if action_id in (xbmcgui.ACTION_NAV_BACK, xbmcgui.ACTION_PREVIOUS_MENU):
            self.close()
        elif action_id == xbmcgui.ACTION_CONTEXT_MENU:
            self.show_context_menu()
        elif action_id in (xbmcgui.ACTION_MOVE_UP, xbmcgui.ACTION_MOVE_DOWN):
            self.handle_vertical_navigation(action_id)
            
    def handle_vertical_navigation(self, action_id):
        """
        Maneja la navegación vertical con scroll infinito
        """
        try:
            focused_control = self.getFocusId()
            
            if focused_control == self.CONTENT_LIST_ID:
                content_list = self.getControl(self.CONTENT_LIST_ID)
                current_pos = content_list.getSelectedPosition()
                total_items = content_list.size()
                
                # Cargar más contenido si estamos cerca del final
                if action_id == xbmcgui.ACTION_MOVE_DOWN and current_pos >= total_items - 5:
                    if not self.loading and self.current_library:
                        self.load_library_content(self.current_library, total_items)
                        
        except Exception as e:
            xbmc.log('[{}] VerticalHome: Error in navigation: {}'.format(ADDON_ID, e), xbmc.LOGERROR)
            
    def onClick(self, control_id):
        """
        Manejo de clicks
        """
        if control_id == self.SECTION_LIST_ID:
            self.on_section_click()
        elif control_id == self.CONTENT_LIST_ID:
            self.on_content_click()
        elif control_id == self.SEARCH_BUTTON_ID:
            self.open_search()
        elif control_id == self.SETTINGS_BUTTON_ID:
            self.open_settings()
        elif control_id == self.USER_BUTTON_ID:
            self.open_user_menu()
            
    def on_section_click(self):
        """
        Click en sección/biblioteca
        """
        try:
            section_list = self.getControl(self.SECTION_LIST_ID)
            selected_item = section_list.getSelectedItem()
            library_key = selected_item.getProperty('library_key')
            
            if library_key:
                self._content_loaded = False  # Permitir reset de lista
                self.load_library_content(library_key)
                self.setFocusId(self.CONTENT_LIST_ID)
                
        except Exception as e:
            xbmc.log('[{}] VerticalHome: Error in section click: {}'.format(ADDON_ID, e), xbmc.LOGERROR)
            
    def on_content_click(self):
        """
        Click en contenido - reproducir
        """
        try:
            content_list = self.getControl(self.CONTENT_LIST_ID)
            selected_item = content_list.getSelectedItem()
            plex_key = selected_item.getProperty('plex_key')
            media_type = selected_item.getProperty('media_type')
            title = selected_item.getLabel()
            
            if plex_key and self.plex_api.server_url:
                self.play_item(plex_key, media_type, title)
            else:
                # Demo mode
                xbmcgui.Dialog().notification(
                    'Demo Mode',
                    'Reproduciendo: {}'.format(title),
                    xbmcgui.NOTIFICATION_INFO,
                    3000
                )
                
        except Exception as e:
            xbmc.log('[{}] VerticalHome: Error in content click: {}'.format(ADDON_ID, e), xbmc.LOGERROR)
            
    def play_item(self, plex_key, media_type, title):
        """
        Reproduce un item de Plex
        """
        try:
            # Construir URL de streaming
            stream_url = "{}{}?X-Plex-Token={}".format(
                self.plex_api.server_url, plex_key, self.plex_api.token
            )
            
            # Crear ListItem para reproducción
            play_item = xbmcgui.ListItem(title)
            play_item.setPath(stream_url)
            
            # Iniciar reproducción
            xbmc.Player().play(stream_url, play_item)
            
            xbmcgui.Dialog().notification(
                'Plex Vertical UI',
                'Reproduciendo: {}'.format(title),
                xbmcgui.NOTIFICATION_INFO,
                3000
            )
            
        except Exception as e:
            xbmc.log('[{}] VerticalHome: Error playing item: {}'.format(ADDON_ID, e), xbmc.LOGERROR)
            xbmcgui.Dialog().notification(
                'Error',
                'No se pudo reproducir el contenido',
                xbmcgui.NOTIFICATION_ERROR,
                5000
            )
            
    def open_search(self):
        """
        Abre la búsqueda
        """
        keyboard = xbmc.Keyboard('', 'Buscar en Plex')
        keyboard.doModal()
        
        if keyboard.isConfirmed():
            query = keyboard.getText()
            if query:
                self.perform_search(query)
                
    def perform_search(self, query):
        """
        Realiza una búsqueda
        """
        if self.loading:
            return
            
        self.loading = True
        
        def _search():
            try:
                results = self.plex_api.search(query)
                
                # Si no hay resultados reales, mostrar mensaje
                if not results:
                    xbmc.executebuiltin('Notification(Búsqueda,"No se encontraron resultados",3000)')
                    return
                
                self.content_items = results
                self._content_loaded = False
                xbmc.executebuiltin('Container.Refresh')
                self.populate_content()
                
            except Exception as e:
                xbmc.log('[{}] VerticalHome: Error searching: {}'.format(ADDON_ID, e), xbmc.LOGERROR)
            finally:
                self.loading = False
                
        thread = threading.Thread(target=_search)
        thread.daemon = True
        thread.start()
        
    def open_settings(self):
        """
        Abre la configuración
        """
        ADDON.openSettings()
        
    def open_user_menu(self):
        """
        Abre el menú de usuario
        """
        options = ['Cambiar servidor', 'Reconectar', 'Acerca de', 'Cancelar']
        selected = xbmcgui.Dialog().select('Usuario', options)
        
        if selected == 0:  # Cambiar servidor
            self.configure_server()
        elif selected == 1:  # Reconectar
            self.reconnect()
        elif selected == 2:  # Acerca de
            self.show_about()
            
    def configure_server(self):
        """
        Configurar servidor Plex
        """
        ADDON.openSettings()
        
    def reconnect(self):
        """
        Reconectar al servidor
        """
        self.plex_api = PlexAPI()
        self._content_loaded = False
        self.load_libraries()
        
        xbmcgui.Dialog().notification(
            'Plex Vertical UI',
            'Reconectando...',
            xbmcgui.NOTIFICATION_INFO,
            2000
        )
        
    def show_about(self):
        """
        Mostrar información del addon
        """
        about_text = (
            "Plex Vertical UI - Standalone Edition\n"
            "Version: {}\n\n"
            "Cliente independiente de Plex con navegación vertical moderna.\n"
            "Diseño inspirado en Netflix con interfaz optimizada para TV.\n\n"
            "Desarrollado por: {}".format(
                ADDON.getAddonInfo('version'),
                ADDON.getAddonInfo('author')
            )
        )
        
        xbmcgui.Dialog().textviewer('Acerca de', about_text)
        
    def show_context_menu(self):
        """
        Mostrar menú contextual
        """
        focused_control = self.getFocusId()
        
        if focused_control == self.CONTENT_LIST_ID:
            options = ['Información', 'Añadir a lista', 'Marcar como visto', 'Cancelar']
            selected = xbmcgui.Dialog().select('Opciones', options)
            
            if selected >= 0 and selected < 3:
                xbmcgui.Dialog().notification(
                    'Menú contextual',
                    options[selected],
                    xbmcgui.NOTIFICATION_INFO,
                    2000
                )
                
    def onClosed(self):
        """
        Limpieza al cerrar
        """
        xbmc.log('[{}] VerticalHome: Cerrando interfaz vertical'.format(ADDON_ID), xbmc.LOGINFO)