#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Plex Vertical UI Installer
Instala/desinstala la modificación de UI vertical para script.plexmod
"""

from __future__ import absolute_import, unicode_literals
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
import os
import sys
import shutil
import time

# Addon info
ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_PATH = ADDON.getAddonInfo('path')
ADDON_VERSION = ADDON.getAddonInfo('version')

# Target addon
TARGET_ADDON_ID = 'script.plexmod'

# Paths
RESOURCES_PATH = os.path.join(ADDON_PATH, 'resources')
PATCHES_PATH = os.path.join(RESOURCES_PATH, 'patches')
FILES_PATH = os.path.join(RESOURCES_PATH, 'files')

class VerticalUIInstaller(object):
    """
    Instalador de Plex Vertical UI
    """
    
    def __init__(self):
        self.dialog = xbmcgui.Dialog()
        self.progress = None
        self.target_addon = None
        self.target_path = None
        self.backup_path = None
        
    def log(self, msg, level=xbmc.LOGINFO):
        """Log message"""
        xbmc.log('[{}] {}'.format(ADDON_ID, msg), level)
        
    def check_requirements(self):
        """Verifica que script.plexmod esté instalado"""
        try:
            self.target_addon = xbmcaddon.Addon(TARGET_ADDON_ID)
            self.target_path = self.target_addon.getAddonInfo('path')
            self.log('Target addon found at: {}'.format(self.target_path))
            return True
        except RuntimeError:
            self.log('Target addon not found!', xbmc.LOGERROR)
            self.dialog.ok(
                'Error',
                'script.plexmod no está instalado.',
                '',
                'Por favor, instala Plex for Kodi primero.'
            )
            return False
    
    def create_backup(self):
        """Crea backup de los archivos que se van a modificar"""
        try:
            # Directorio de backup
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            self.backup_path = os.path.join(
                xbmcvfs.translatePath('special://temp/'),
                'plexmod_backup_{}'.format(timestamp)
            )
            
            if not os.path.exists(self.backup_path):
                os.makedirs(self.backup_path)
            
            self.log('Creating backup in: {}'.format(self.backup_path))
            
            # Backup de default.py
            default_py = os.path.join(self.target_path, 'default.py')
            if os.path.exists(default_py):
                shutil.copy2(default_py, os.path.join(self.backup_path, 'default.py'))
                self.log('Backed up: default.py')
            
            # Backup de settings.xml
            settings_xml = os.path.join(self.target_path, 'resources', 'settings.xml')
            if os.path.exists(settings_xml):
                shutil.copy2(settings_xml, os.path.join(self.backup_path, 'settings.xml'))
                self.log('Backed up: settings.xml')
            
            return True
            
        except Exception as e:
            self.log('Backup error: {}'.format(e), xbmc.LOGERROR)
            return False
    
    def is_already_installed(self):
        """Verifica si ya está instalado"""
        try:
            default_py = os.path.join(self.target_path, 'default.py')
            with open(default_py, 'r', encoding='utf-8') as f:
                content = f.read()
                return 'VERTICAL UI INTEGRATION' in content
        except:
            return False
    
    def copy_files(self):
        """Copia los archivos necesarios"""
        try:
            self.progress.update(30, 'Copiando archivos...')
            
            # 1. Copiar vertical_home.py
            src_py = os.path.join(FILES_PATH, 'vertical_home.py')
            dst_py = os.path.join(self.target_path, 'lib', 'vertical_home.py')
            
            if os.path.exists(src_py):
                shutil.copy2(src_py, dst_py)
                self.log('Copied: vertical_home.py')
            else:
                self.log('Source file not found: vertical_home.py', xbmc.LOGERROR)
                return False
            
            # 2. Copiar XML de skin
            src_xml = os.path.join(FILES_PATH, 'script-plex-vertical-home.xml')
            dst_xml_dir = os.path.join(self.target_path, 'resources', 'skins', 'Main', '1080i')
            dst_xml = os.path.join(dst_xml_dir, 'script-plex-vertical-home.xml')
            
            if not os.path.exists(dst_xml_dir):
                os.makedirs(dst_xml_dir)
            
            if os.path.exists(src_xml):
                shutil.copy2(src_xml, dst_xml)
                self.log('Copied: script-plex-vertical-home.xml')
            else:
                self.log('Source file not found: script-plex-vertical-home.xml', xbmc.LOGERROR)
                return False
            
            return True
            
        except Exception as e:
            self.log('Copy files error: {}'.format(e), xbmc.LOGERROR)
            return False
    
    def patch_default_py(self):
        """Parchea default.py"""
        try:
            self.progress.update(50, 'Parcheando default.py...')
            
            default_py = os.path.join(self.target_path, 'default.py')
            patch_file = os.path.join(PATCHES_PATH, 'default_py.patch')
            
            # Leer archivo original
            with open(default_py, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Leer patch
            with open(patch_file, 'r', encoding='utf-8') as f:
                patch = f.read()
            
            # Buscar punto de inserción
            marker = '                started = True\n                skip_ensure_home = False'
            
            if marker in content:
                # Insertar patch
                parts = content.split(marker, 1)
                new_content = parts[0] + marker + '\n' + patch + parts[1]
                
                # Escribir archivo parcheado
                with open(default_py, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                self.log('default.py patched successfully')
                return True
            else:
                self.log('Marker not found in default.py', xbmc.LOGERROR)
                return False
                
        except Exception as e:
            self.log('Patch default.py error: {}'.format(e), xbmc.LOGERROR)
            import traceback
            self.log(traceback.format_exc(), xbmc.LOGERROR)
            return False
    
    def patch_settings_xml(self):
        """Parchea settings.xml"""
        try:
            self.progress.update(70, 'Parcheando settings.xml...')
            
            settings_xml = os.path.join(self.target_path, 'resources', 'settings.xml')
            patch_file = os.path.join(PATCHES_PATH, 'settings_xml.patch')
            
            # Leer archivo original
            with open(settings_xml, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Leer patch
            with open(patch_file, 'r', encoding='utf-8') as f:
                patch = f.read()
            
            # Buscar punto de inserción
            marker = '<group id="1" label="">'
            
            if marker in content:
                # Insertar patch
                parts = content.split(marker, 1)
                new_content = parts[0] + marker + '\n' + patch + parts[1]
                
                # Escribir archivo parcheado
                with open(settings_xml, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                self.log('settings.xml patched successfully')
                return True
            else:
                self.log('Marker not found in settings.xml', xbmc.LOGERROR)
                return False
                
        except Exception as e:
            self.log('Patch settings.xml error: {}'.format(e), xbmc.LOGERROR)
            import traceback
            self.log(traceback.format_exc(), xbmc.LOGERROR)
            return False
    
    def install(self):
        """Instalación principal"""
        self.log('Starting installation...')
        
        # Verificar requisitos
        if not self.check_requirements():
            return False
        
        # Verificar si ya está instalado
        if self.is_already_installed():
            if not self.dialog.yesno(
                'Ya instalado',
                'La UI Vertical ya está instalada.',
                '¿Deseas reinstalar?'
            ):
                return False
        
        # Mostrar progress dialog
        self.progress = xbmcgui.DialogProgress()
        self.progress.create('Instalando Plex Vertical UI')
        
        try:
            # Crear backup
            self.progress.update(10, 'Creando backup...')
            if not self.create_backup():
                raise Exception('Error creando backup')
            
            # Copiar archivos
            if not self.copy_files():
                raise Exception('Error copiando archivos')
            
            # Parchear default.py
            if not self.patch_default_py():
                raise Exception('Error parcheando default.py')
            
            # Parchear settings.xml
            if not self.patch_settings_xml():
                raise Exception('Error parcheando settings.xml')
            
            # Finalizar
            self.progress.update(100, 'Instalación completada')
            time.sleep(1)
            self.progress.close()
            
            # Mensaje de éxito
            self.dialog.ok(
                'Instalación Exitosa',
                'La UI Vertical se ha instalado correctamente.',
                '',
                'Ve a Configuración de Plex y activa "Usar interfaz vertical"'
            )
            
            self.log('Installation completed successfully')
            return True
            
        except Exception as e:
            self.log('Installation failed: {}'.format(e), xbmc.LOGERROR)
            if self.progress:
                self.progress.close()
            
            self.dialog.ok(
                'Error de Instalación',
                'La instalación falló.',
                '',
                'Backup guardado en: {}'.format(self.backup_path if self.backup_path else 'N/A')
            )
            return False
    
    def uninstall(self):
        """Desinstala la modificación"""
        self.log('Starting uninstallation...')
        
        if not self.check_requirements():
            return False
        
        if not self.is_already_installed():
            self.dialog.ok('Info', 'La UI Vertical no está instalada.')
            return False
        
        if not self.dialog.yesno(
            'Confirmar Desinstalación',
            '¿Seguro que deseas desinstalar la UI Vertical?',
            '',
            'Esto restaurará Plex a su estado original.'
        ):
            return False
        
        self.progress = xbmcgui.DialogProgress()
        self.progress.create('Desinstalando Plex Vertical UI')
        
        try:
            # Buscar backups
            temp_dir = xbmcvfs.translatePath('special://temp/')
            backups = [d for d in os.listdir(temp_dir) if d.startswith('plexmod_backup_')]
            
            if not backups:
                raise Exception('No se encontraron backups')
            
            # Usar el backup más reciente
            backups.sort(reverse=True)
            backup_path = os.path.join(temp_dir, backups[0])
            
            self.progress.update(30, 'Restaurando archivos...')
            
            # Restaurar default.py
            backup_default = os.path.join(backup_path, 'default.py')
            target_default = os.path.join(self.target_path, 'default.py')
            if os.path.exists(backup_default):
                shutil.copy2(backup_default, target_default)
            
            # Restaurar settings.xml
            backup_settings = os.path.join(backup_path, 'settings.xml')
            target_settings = os.path.join(self.target_path, 'resources', 'settings.xml')
            if os.path.exists(backup_settings):
                shutil.copy2(backup_settings, target_settings)
            
            self.progress.update(60, 'Eliminando archivos añadidos...')
            
            # Eliminar archivos añadidos
            files_to_remove = [
                os.path.join(self.target_path, 'lib', 'vertical_home.py'),
                os.path.join(self.target_path, 'resources', 'skins', 'Main', '1080i', 'script-plex-vertical-home.xml')
            ]
            
            for file_path in files_to_remove:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    self.log('Removed: {}'.format(file_path))
            
            self.progress.update(100, 'Desinstalación completada')
            time.sleep(1)
            self.progress.close()
            
            self.dialog.ok(
                'Desinstalación Exitosa',
                'La UI Vertical se ha desinstalado.',
                '',
                'Plex ha sido restaurado a su estado original.'
            )
            
            self.log('Uninstallation completed successfully')
            return True
            
        except Exception as e:
            self.log('Uninstallation failed: {}'.format(e), xbmc.LOGERROR)
            if self.progress:
                self.progress.close()
            
            self.dialog.ok('Error', 'La desinstalación falló.', '', str(e))
            return False
    
    def show_menu(self):
        """Muestra el menú principal"""
        options = [
            'Instalar UI Vertical',
            'Desinstalar UI Vertical',
            'Ver información',
            'Salir'
        ]
        
        selected = self.dialog.select('Plex Vertical UI v{}'.format(ADDON_VERSION), options)
        
        if selected == 0:
            self.install()
        elif selected == 1:
            self.uninstall()
        elif selected == 2:
            self.show_info()
    
    def show_info(self):
        """Muestra información del addon"""
        info_text = (
            'Plex Vertical UI v{}\n\n'
            'Modificación de interfaz vertical para Plex for Kodi.\n\n'
            'Características:\n'
            '• Navegación vertical\n'
            '• Diseño moderno\n'
            '• Animaciones suaves\n'
            '• Optimizado para mando\n\n'
            'Instalación:\n'
            '1. Ejecuta "Instalar UI Vertical"\n'
            '2. Ve a Configuración de Plex\n'
            '3. Activa "Usar interfaz vertical"\n'
            '4. Reinicia Plex\n\n'
            'Desarrollado por: Moids\n'
            'Basado en: script.plexmod by pannal'
        ).format(ADDON_VERSION)
        
        self.dialog.textviewer('Información', info_text)

def main():
    """Punto de entrada principal"""
    installer = VerticalUIInstaller()
    installer.show_menu()

if __name__ == '__main__':
    main()