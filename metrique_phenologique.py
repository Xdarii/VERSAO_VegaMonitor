# -*- coding: utf-8 -*-
"""
/***************************************************************************
 metriquePhenologique
                                 A QGIS plugin
 calcul de metrique phenologique et pretraitement
                              -------------------
        begin                : 2016-04-29
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Dian
        email                : bah.mamadian@yahoo.fr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication,Qt
from PyQt4.QtGui import QAction, QIcon,QWidget, QPushButton, QApplication, QFileDialog, QMessageBox
from qgis.core import QgsMessageLog
from qgis.gui import QgsMessageBar
from PyQt4 import QtGui
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from metrique_phenologique_dialog import metriquePhenologiqueDialog
import os
import os.path
#from function_data_raster import open_data, write_data
#from clip import clipRaster

#from TVDI import TVDI_function
#from my_aggregate import block_reduce
from class_pretraitement import Pretraitement,detection_phenologique,CalculIndicateur

class metriquePhenologique:
    """QGIS Plugin Implementation."""
    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """

        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'metriquePhenologique_{}.qm'.format(locale))
        
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = metriquePhenologiqueDialog()
        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&pretraitement et pheno')
        QApplication.restoreOverrideCursor()
        self.on= 1
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'metriquePhenologique')
        self.toolbar.setObjectName(u'metriquePhenologique')
        
        
        
    
    def mes_action(self):
        
        """
        Gère les interactions entre utilisateur et l'interface.
        Manages interactions between user and interface.
        
        """
        self.dlg.pushButton_cheminNDVI.clicked.connect(self.acces_repertoire_ndvi)
        self.dlg.pushButton_cheminDOY.clicked.connect(self.acces_Repertoire_Doy)
        self.dlg.pushButton_cheminOut.clicked.connect(self.acces_repertoire_save)
        
        self.dlg.pushButton_cheminNDVI_metrique.clicked.connect(self.acces_repertoire_ndvi)
        self.dlg.pushButton_cheminOut_metrique.clicked.connect(self.acces_repertoire_save)
        self.dlg.pushButton_cheminZoneEtudes.clicked.connect(self.acces_Zone_Etudes)
        
        self.dlg.pushButton_cheminTemperature.clicked.connect(self.acces_repertoire_temperature)
        self.dlg.pushButton_cheminNDVI_temperature.clicked.connect(self.acces_repertoire_ndvi)
        
        self.dlg.pushButton_cheminSOS.clicked.connect(self.acces_fichier_sos)
        self.dlg.pushButton_cheminEOS.clicked.connect(self.acces_fichier_eos)
        self.dlg.pushButton_cheminTOS.clicked.connect(self.acces_fichier_tos)
        
        self.dlg.pushButton_cheminOut_temperature.clicked.connect(self.acces_repertoire_save)
        
        
        self.dlg.cancel.clicked.connect(self.stop)
        self.dlg.pushButton_execution.clicked.connect(self.validation)
        
        self.dlg.tci.clicked.connect(self.selection_tci)
        self.dlg.tvdi.clicked.connect(self.selection_tvdi)
        self.dlg.cwsi.clicked.connect(self.selection_cwsi)
        self.dlg.cumule.clicked.connect(self.selection_cumule)
        self.dlg.cumule_2.clicked.connect(self.selection_cumule)
        self.dlg.vhi.clicked.connect(self.selection_vhi)
        self.dlg.aggregate_Yes.clicked.connect(self.selection_aggregate_yes)
        self.dlg.aggregate_No.clicked.connect(self.selection_aggregate_no)
        
        self.dlg.radioButton_default.clicked.connect(self.selection_Default)
        self.dlg.radioButton_seuil.clicked.connect(self.selection_Seuil)
        
        self.dlg.decoupage.clicked.connect(self.selection_Decoupage)
        self.dlg.interpolation.clicked.connect(self.selection_Interpolation)
        self.dlg.lissage.clicked.connect(self.selection_Lissage)

        
        self.dlg.filtreInterpol.currentIndexChanged.connect(self.active_parametre)
        
        self.dlg.temperature_oui.clicked.connect(self.active_temperature)
        self.dlg.temperature_non.clicked.connect(self.active_temperature)
        
        self.dlg.radioButton_interpDefaut.clicked.connect(self.active_defaut_interpol)
        self.dlg.radioButton_autre_interpol.clicked.connect(self.active_defaut_interpol)
        self.dlg.cancel.clicked.connect(self.stop)
        
    def stop(self):
        
        QApplication.processEvents
        QApplication.restoreOverrideCursor()
        self.on=0

        
    def active_defaut_interpol(self):
        if self.dlg.radioButton_interpDefaut.isChecked():
            self.dlg.njours_interpolation.setEnabled(0)
        else:
            self.dlg.njours_interpolation.setEnabled(1)
            
    def active_temperature(self):
        """
        Manages parameters of temperature  
        """
        if self.dlg.temperature_oui.isChecked():
            self.dlg.frame_Tselect.setEnabled(1)
        else :
            self.dlg.frame_Tselect.setEnabled(0)
            
    def active_parametre(self,index):
        """
        Manages   filters  parameters
        """
        if self.dlg.filtreInterpol.currentIndex()==1:
            self.dlg.parametreSG.setEnabled(1)
            self.dlg.parametre_wh.setEnabled(0)
            
        if self.dlg.filtreInterpol.currentIndex()==2:
            self.dlg.parametreSG.setEnabled(0)
            self.dlg.parametre_wh.setEnabled(1)
            
        if self.dlg.filtreInterpol.currentIndex()==0:
            self.dlg.parametreSG.setEnabled(0)
            self.dlg.parametre_wh.setEnabled(0)
            
            
    def selection_Decoupage(self):
            """
            manages the cutting parameters
            """
            self.dlg.decoupage.setChecked(1)
            self.dlg.frame_decoupage.setEnabled(1)
            self.dlg.frame_interpolation.setEnabled(0)
            self.dlg.lissage.setChecked(0)
            self.dlg.frame_cheminDOY.setEnabled(0)
            
    def selection_Interpolation(self):
            """
            manages the interpolation parameters
            """
            self.dlg.interpolation.setChecked(1)
            self.dlg.frame_decoupage.setEnabled(0)
            self.dlg.frame_interpolation.setEnabled(1)
            self.dlg.frame_cheminDOY.setEnabled(1)
            self.dlg.cheminDOY.setEnabled(1)
            self.dlg.pushButton_cheminDOY.setEnabled(1)
            self.dlg.decoupage.setChecked(0)
            self.dlg.lissage.setChecked(0)
    def selection_Lissage(self):
            """
            manages the smoothing options
            """
            self.dlg.lissage.setChecked(1)
            self.dlg.frame_decoupage.setEnabled(0)
            self.dlg.frame_interpolation.setEnabled(0)
            self.dlg.decoupage.setChecked(0)
            self.dlg.frame_cheminDOY.setEnabled(0)
            #==================================
    def selection_cwsi(self):
        """
        manages the cwsi parameters
        """
        if self.dlg.cwsi.isChecked():
            self.dlg.frame_ndvi.setEnabled(0)
            if self.dlg.cumule.isChecked():
                self.dlg.frame_metrique.setEnabled(1)
                self.dlg.frame_aggregate.setEnabled(1)
            else:
                self.dlg.frame_metrique.setEnabled(0)
                self.dlg.frame_aggregate.setEnabled(0)
    def selection_tci(self):
            """
            manages the tci parameters
            """
            self.dlg.tci.setChecked(1)
            self.dlg.frame_ndvi.setEnabled(0)
            if self.dlg.cumule.isChecked():
                self.dlg.frame_metrique.setEnabled(1)
                self.dlg.frame_aggregate.setEnabled(1)
            else:
                self.dlg.frame_metrique.setEnabled(0)
                self.dlg.frame_aggregate.setEnabled(0)
    def selection_tvdi(self):
            """
            manages the tvdi parameters
            """
            self.dlg.tvdi.setChecked(1)
            self.dlg.frame_ndvi.setEnabled(1)
            if self.dlg.cumule.isChecked():
                self.dlg.frame_metrique.setEnabled(1)
            else:
                self.dlg.frame_metrique.setEnabled(0)
            self.dlg.frame_aggregate.setEnabled(1)
    def selection_cumule(self):
            """
            manages the cumul parameters
            """
            if  self.dlg.cumule.isChecked():
                self.dlg.cumule.setChecked(1)
                self.dlg.frame_metrique.setEnabled(1)
                self.dlg.frame_aggregate.setEnabled(1)
            else:
                
                self.dlg.cumule.setChecked(0)
                self.dlg.frame_metrique.setEnabled(0)
                if self.dlg.tvdi.isChecked() or self.dlg.vhi.isChecked():
                    self.dlg.frame_aggregate.setEnabled(1)
                else:
                    self.dlg.frame_aggregate.setEnabled(0)
                
    def selection_vhi(self):
            """
            manages the vhi parameters
            """
            self.dlg.vhi.setChecked(1)
            if self.dlg.cumule.isChecked():
                self.dlg.frame_metrique.setEnabled(1)
            else:
                self.dlg.frame_metrique.setEnabled(0)
            self.dlg.frame_aggregate.setEnabled(1)
            
    def selection_aggregate_yes(self):
            """
            manages the aggregation parameters if it is checks
            """
            self.dlg.frame_option_aggregate.setEnabled(1)
    def selection_aggregate_no(self):
            """
            manages the aggregation parameters if it is not checks
            """
            self.dlg.frame_option_aggregate.setEnabled(0)

    def acces_repertoire_temperature(self):

        """ allows to select the directory in where  the link of  TEMPERATURE data is located    
        
        """
        ndviPath = QFileDialog.getExistingDirectory(self.dlg,'Directory-Temperature','.')
        if ndviPath:
            
              self.dlg.cheminTemperature.setText(ndviPath)
              


#    def acces_repertoire_temperature_ndvi(self):
#
#        """ allows to select the directory in where  the link of  NDVI  data is located for the
#        
#        """
#        ndviPath = QFileDialog.getExistingDirectory(self.dlg,'Directory-NDVI','.')
#        if ndviPath:
#            
#              self.dlg.cheminNDVI_temperature.setText(ndviPath)

    def acces_repertoire_temperature_sos(self):

        """ allows to select the directory in where  the link of  SOS data is located    
        
        """
        ndviPath = QFileDialog.getExistingDirectory(self.dlg,'Directory-SOS','.')
        if ndviPath:
            
              self.dlg.cheminSOS_temperature.setText(ndviPath)

    def acces_repertoire_temperature_eos(self):

        """ allows to select the directory in where  the link of  EOS data is located    
        
        """
        ndviPath = QFileDialog.getExistingDirectory(self.dlg,'Directory-EOS','.')
        if ndviPath:
            
              self.dlg.cheminEOS_temperature.setText(ndviPath)

    def acces_repertoire_temperature_tos(self):
        """ allows to select the directory in where  the link of  TOS data is located    
        
        """
        ndviPath = QFileDialog.getExistingDirectory(self.dlg,'Directory-TOS','.')
        if ndviPath:
            
              self.dlg.cheminTOS_temperature.setText(ndviPath)

    def acces_repertoire_ndvi(self):
        """ allows to select the directory in where  the link of  NDVI data is located    
        
        """
        ndviPath = QFileDialog.getExistingDirectory(self.dlg,u'Directory-NDVI','.')
        if ndviPath:
            if self.dlg.MOD13Q1.currentIndex()==0:    
              self.dlg.cheminNDVI.setText(ndviPath)
            if self.dlg.MOD13Q1.currentIndex()==1: 
              self.dlg.cheminNDVI_metrique.setText(ndviPath)
            if self.dlg.MOD13Q1.currentIndex()==2: 
              self.dlg.cheminNDVI_temperature.setText(ndviPath)
#    def acces_Repertoire_NdviMetrique(self):
#        
#        ndviPath = QFileDialog.getExistingDirectory(self.dlg,u'Directory-NDVI','.')
#          
#        if ndviPath:
#          
#          self.dlg.cheminNDVI_metrique.setText(ndviPath)

    def acces_fichier_sos(self):
        """ allows to select the file of SOS data    
        
        """
        ndviPath = QFileDialog.getOpenFileName(self.dlg, 
                                            u"Directory-SOS", 
                                            u"/home/puiseux/images", 
                                            u"Images (*.tif )")
          
        if ndviPath:
          
          self.dlg.cheminSOS_temperature.setText(ndviPath)
          
    def acces_fichier_eos(self):
        """ allows to select the file of EOS data    
        
        """
        ndviPath = QFileDialog.getOpenFileName(self.dlg, 
                                            u"Directory-EOS", 
                                            u"/home/puiseux/images", 
                                            u"Images (*.tif )")
          
        if ndviPath:
          
          self.dlg.cheminEOS_temperature.setText(ndviPath)

    def acces_fichier_tos(self):
        """ allows to select the file of TOS data    
        
        """
        ndviPath = QFileDialog.getOpenFileName(self.dlg, 
                                            u"Directory-TOS", 
                                            u"/home/puiseux/images", 
                                            u"Images (*.tif )")
          
        if ndviPath:
          
          self.dlg.cheminTOS_temperature.setText(ndviPath)

              
    def acces_Repertoire_Doy(self):
        
        """ allows to select the directory  of  DOY data   
        
        """
        
        
        doyPath = QFileDialog.getExistingDirectory(self.dlg,u'Directory-DOY','.')
          
        if doyPath:
          
          self.dlg.cheminDOY.setText(doyPath)
          
#    def acces_Chemin_save_temperature(self):
#        """
#        permet de selectionner le repertoire d'enregistrement des fichiers
#        """
#        savePath = QFileDialog.getExistingDirectory(self.dlg,u"Directory-save",'.')
#              
#        if savePath:
#        
#                self.dlg.cheminOut_temperature.setText(savePath)
      
    def acces_repertoire_save(self):
        
        """ allows to select the directory in where  the data will be save   
        
        """
        savePath = QFileDialog.getExistingDirectory(self.dlg,u'Directory-save','.')
              
        if savePath:
            if self.dlg.MOD13Q1.currentIndex()==0:        
                self.dlg.cheminOut.setText(savePath)
            if self.dlg.MOD13Q1.currentIndex()==1:        
                self.dlg.cheminOut_metrique.setText(savePath)
            if self.dlg.MOD13Q1.currentIndex()==2:        
                self.dlg.cheminOut_temperature.setText(savePath)
                
                      
#    def acces_Chemin_SaveMetrique(self,var):
#        """
#        permet de selectionner le repertoire d'enregistrement des fichiers
#        """
#        savePath = QFileDialog.getExistingDirectory(self.dlg,u'Directory-save','.')
#                  
#        if savePath:
#                      
#                      self.dlg.cheminOut_metrique.setText(savePath)



    def acces_Zone_Etudes(self):
        
        """ 
        allows to select the directory  of  ROI data   
        
        """
        
        
        zonePath = QFileDialog.getOpenFileName(self.dlg, u"Directory-ROI", 
                                               u"/home/puiseux/", 
                                               u"Images (*.shp )")
          
        if zonePath:
          
          self.dlg.zoneEmprise.setText(zonePath)
          
          
    def selection_Default(self):
        """
        avoids the user to change the threshold by locking        
        """
        self.dlg.frame_seuil.setEnabled(0)
        
    def selection_Seuil(self):
        """
        alloiws the user to change the threshold        
        """
        
        self.dlg.frame_seuil.setEnabled(1)
        self.dlg.seuilEOS.setEnabled(1)
        self.dlg.seuilSOS.setEnabled(1)
        
    def selection_NDVI(self):
        """
        locks the DOY       
        """
        self.dlg.cheminDOY.setEnabled(0)
        self.dlg.cheminNDVI.setEnabled(1)

        
    def selection_DOY(self):
        """
        unlocks the DOY       
        """
        self.dlg.cheminNDVI.setEnabled(0)
        self.dlg.cheminDOY.setEnabled(1)

    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('metriquePhenologique', message)


        

#%%
    def validation(self):
        
        """
        cette fonction permet de determiner l'action à réaliser quand on clique sur 
        Valider
        
        """
        if self.dlg.MOD13Q1.currentIndex()==0:        
            pretraitement=Pretraitement(self.dlg,self.iface)
    
            if pretraitement.on:
                if self.dlg.decoupage.isChecked():
                    pretraitement.decoupage()
                if self.dlg.interpolation.isChecked():
                    pretraitement.interpolation()
                if self.dlg.lissage.isChecked():
                    pretraitement.lisser()
        if self.dlg.MOD13Q1.currentIndex()==1:    
            
            pheno=detection_phenologique(self.dlg,self.iface)
            if pheno.on:
                pheno.estimation()
            
        if self.dlg.MOD13Q1.currentIndex()==2:        
            indicateur=CalculIndicateur(self.dlg,self.iface)
            
            if indicateur.on:
                
                if self.dlg.cwsi.isChecked():
                    indicateur.cwsi()
                if self.dlg.tci.isChecked():
                    indicateur.tci()
                    QApplication.restoreOverrideCursor()
                if self.dlg.vhi.isChecked():
                    indicateur.vhi()
                    QApplication.restoreOverrideCursor()
                if self.dlg.tvdi.isChecked():
                    indicateur.tvdi()
        self.showDlg       
        QApplication.restoreOverrideCursor()                
#%%
    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def showDlg(self):
        
        
        self.dlg=metriquePhenologiqueDialog()
        self.mes_action()
        self.stop() 
        QApplication.restoreOverrideCursor()
        self.dlg.show()

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/metriquePhenologique/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'pretraite et métrique pheno'),
            callback=self.showDlg,
            parent=self.iface.mainWindow())

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&pretraitement et pheno'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


