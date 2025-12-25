#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PM4K Vertical UI - Vertical Home Window
Modern vertical navigation using PM4K's backend
"""

from __future__ import absolute_import, unicode_literals
import xbmc
import xbmcgui
import xbmcaddon

# Import PM4K modules  
from plexnet import plexapp
from lib.windows import kodigui
from lib import util

ADDON = xbmcaddon.Addon('script.pm4k.verticalui')

class VerticalHomeWindow(kodigui.BaseWindow):
    xmlFile = 'script-pm4k-vertical-home.xml'
    path = ADDON.getAddonInfo('path')
    theme = 'Main'
    res = '1080i'
    width = 1920
    height = 1080

    LIBRARIES_LIST_ID = 101
    CONTENT_PANEL_ID = 201
    
    def __init__(self, *args, **kwargs):
        kodigui.BaseWindow.__init__(self, *args, **kwargs)
        self.libraries = []
        self.currentLibrary = None
        self.tasks = []
        
    def onFirstInit(self):
        """Called on first initialization"""
        xbmc.log('[PM4K Vertical] First init', xbmc.LOGINFO)
        self.loadLibraries()
        
    def loadLibraries(self):
        """Load Plex libraries from PM4K"""
        try:
            server = plexapp.SERVERMANAGER.selectedServer
            if not server:
                return
                
            sections = server.library.sections()
            self.libraries = []
            
            librariesControl = self.getControl(self.LIBRARIES_LIST_ID)
            librariesControl.reset()
            
            for section in sections:
                item = xbmcgui.ListItem(section.title)
                item.setArt({
                    'icon': section.composite or '',
                    'thumb': section.thumb or ''
                })
                item.setProperty('section_key', section.key)
                item.setProperty('section_type', section.type)
                librariesControl.addItem(item)
                self.libraries.append(section)
                
            xbmc.log('[PM4K Vertical] Loaded {} libraries'.format(len(self.libraries)), xbmc.LOGINFO)
            
        except Exception as e:
            xbmc.log('[PM4K Vertical] Error loading libraries: {}'.format(e), xbmc.LOGERROR)
            util.showNotification('Error', 'No se pudieron cargar las bibliotecas')
    
    def loadLibraryContent(self, section):
        """Load content for a library section"""
        try:
            contentControl = self.getControl(self.CONTENT_PANEL_ID)
            contentControl.reset()
            
            # Get first 50 items from library
            items = section.all(maxresults=50)
            
            for item in items:
                listItem = xbmcgui.ListItem(item.title)
                listItem.setArt({
                    'poster': item.thumb or '',
                    'fanart': item.art or ''
                })
                listItem.setProperty('rating_key', item.ratingKey)
                listItem.setProperty('type', item.type)
                contentControl.addItem(listItem)
                
            xbmc.log('[PM4K Vertical] Loaded {} items'.format(len(items)), xbmc.LOGINFO)
            
        except Exception as e:
            xbmc.log('[PM4K Vertical] Error loading content: {}'.format(e), xbmc.LOGERROR)
            util.showNotification('Error', 'No se pudo cargar el contenido')
    
    def onClick(self, controlID):
        """Handle click events"""
        if controlID == self.LIBRARIES_LIST_ID:
            # Library selected
            pos = self.getControl(self.LIBRARIES_LIST_ID).getSelectedPosition()
            if 0 <= pos < len(self.libraries):
                self.currentLibrary = self.libraries[pos]
                self.loadLibraryContent(self.currentLibrary)
                
        elif controlID == self.CONTENT_PANEL_ID:
            # Content item selected - open with PM4K
            listControl = self.getControl(self.CONTENT_PANEL_ID)
            item = listControl.getSelectedItem()
            if item:
                rating_key = item.getProperty('rating_key')
                # Let PM4K handle playback/info
                xbmc.executebuiltin('RunScript(script.plexmod,open,{})'.format(rating_key))
    
    def onAction(self, action):
        """Handle actions"""
        try:
            if action == xbmcgui.ACTION_NAV_BACK or action == xbmcgui.ACTION_PREVIOUS_MENU:
                self.doClose()
                return
        except:
            pass
            
        kodigui.BaseWindow.onAction(self, action)
