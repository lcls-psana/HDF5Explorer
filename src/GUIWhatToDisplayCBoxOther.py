#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module GUIWhatToDisplayCBoxOther...
#
#------------------------------------------------------------------------

"""Generates GUI to select information for rendaring in the HDF5Explorer.

This software was developed for the SIT project.  If you use all or 
part of it, please give an appropriate acknowledgment.

@see RelatedModule

@version $Id: template!python!py 4 2008-10-08 19:27:36Z salnikov $

@author Mikhail S. Dubrovin
"""
from __future__ import absolute_import

#------------------------------
#  Module's version from CVS --
#------------------------------
__version__ = "$Revision: 4 $"
# $Source$

#--------------------------------
#  Imports of standard modules --
#--------------------------------
import sys
from PyQt5 import QtCore, QtGui, QtWidgets

#---------------------------------
#  Imports of base class module --
#---------------------------------

#-----------------------------
# Imports for other modules --
#-----------------------------
from . import ConfigParameters as cp

#---------------------
#  Class definition --
#---------------------
class GUIWhatToDisplayCBoxOther ( QtWidgets.QWidget ) :
    """Provides GUI to select information for rendering.

    Detailed description should be here...
    @see BaseClass
    @see OtherClass
    """

    #--------------------
    #  Class variables --
    #--------------------
    #publicStaticVariable = 0 
    #__privateStaticVariable = "A string"

    #----------------
    #  Constructor --
    #----------------

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.setGeometry(370, 350, 500, 30)
        self.setWindowTitle('What to display?')

        self.parent = parent

        self.frame = QtWidgets.QFrame(self)
        self.frame.setFrameStyle( QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken )
        self.frame.setLineWidth(0)
        self.frame.setMidLineWidth(1)
        self.frame.setGeometry(self.rect())
        
        titFont   = QtGui.QFont("Sans Serif", 12, QtGui.QFont.Bold)

        self.titWaveform = QtWidgets.QLabel('Other')
        self.titWaveform.setFont (titFont) 
        
        self.cboxWFWaveform    = QtWidgets.QCheckBox('Waveform',     self)
        self.cboxWFWaveVsEv    = QtWidgets.QCheckBox('WF vs Event',  self)
        self.cboxCO            = QtWidgets.QCheckBox('Correlations', self)
        self.cboxCC            = QtWidgets.QCheckBox('CalibCycles',  self)

        if cp.confpars.waveformWaveformIsOn : self.cboxWFWaveform.setCheckState(2)
        if cp.confpars.waveformWaveVsEvIsOn : self.cboxWFWaveVsEv.setCheckState(2)
        if cp.confpars.correlationsIsOn     : self.cboxCO        .setCheckState(2)
        if cp.confpars.calibcycleIsOn       : self.cboxCC        .setCheckState(2)

        self.showToolTips()

        gridWF = QtWidgets.QGridLayout()
        gridWF.addWidget(self.titWaveform,      0, 0)
        gridWF.addWidget(self.cboxWFWaveform,   1, 0)
        gridWF.addWidget(self.cboxWFWaveVsEv,   2, 0)
        gridWF.addWidget(self.cboxCO,           1, 1)
        gridWF.addWidget(self.cboxCC,           1, 2)
       #gridWF.addWidget(self.cboxED,           1, 3)


        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addLayout(gridWF)
        self.vbox.addStretch(1)     
        self.setLayout(self.vbox)
  
        self.cboxWFWaveform.stateChanged[int].connect(self.processCBoxWFWaveform)
        self.cboxWFWaveVsEv.stateChanged[int].connect(self.processCBoxWFWaveVsEv)
        self.cboxCO.stateChanged[int].connect(self.processCBoxCO)
        self.cboxCC.stateChanged[int].connect(self.processCBoxCC)

    def showToolTips(self):
        #self.butClose    .setToolTip('Close this window') 
        #self.butIMOptions.setToolTip('Adjust amplitude and other plot\nparameters for Image type plots.')
        #self.butCSOptions.setToolTip('Adjust amplitude and other plot\nparameters for CSpad type plots.')
        #self.butWFOptions.setToolTip('Adjust amplitude and other plot\nparameters for Waveform type plots.')
        pass


    def resizeEvent(self, e):
        #print 'resizeEvent' 
        self.frame.setGeometry(self.rect())


    def closeEvent(self, event):
        #print 'closeEvent'
        pass
        QtWidgets.QWidget.closeEvent(self, event)


    def processClose(self):
        #print 'Close button'
        self.close()


    def setActiveTabBarForIndex(self,ind):
        #print 'Here we have to set active tab bar for ind=', ind
        self.parent.tabBar.setCurrentIndex(ind) # 0,1,2,3 stands for CSpad, Image, Waveform, Proj., Corr. 


    def processCBoxCO(self, value):
        if self.cboxCO.isChecked():
            self.setActiveTabBarForIndex(self.parent.indTabCO)
            cp.confpars.correlationsIsOn = True
        else:
            cp.confpars.correlationsIsOn = False


    def processCBoxCC(self, value):
        if self.cboxCC.isChecked():
            self.setActiveTabBarForIndex(self.parent.indTabCC)
            cp.confpars.calibcycleIsOn = True
        else:
            cp.confpars.calibcycleIsOn = False


    def processCBoxWFWaveform(self, value):
        if self.cboxWFWaveform.isChecked():
            self.setActiveTabBarForIndex(self.parent.indTabWF)
            cp.confpars.waveformWaveformIsOn = True
        else:
            cp.confpars.waveformWaveformIsOn = False


    def processCBoxWFWaveVsEv(self, value):
        if self.cboxWFWaveVsEv.isChecked():
            self.setActiveTabBarForIndex(self.parent.indTabWF)
            cp.confpars.waveformWaveVsEvIsOn = True
        else:
            cp.confpars.waveformWaveVsEvIsOn = False


#-----------------------------
#  In case someone decides to run this module
#
if __name__ == "__main__" :
    app = QtWidgets.QApplication(sys.argv)
    ex  = GUIWhatToDisplayCBoxOther()
    ex.show()
    app.exec_()
#-----------------------------

