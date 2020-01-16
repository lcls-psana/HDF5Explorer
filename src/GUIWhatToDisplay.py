#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module GUIWhatToDisplay...
#
#------------------------------------------------------------------------

"""Generates GUI to select information for rendaring in the HDF5Explorer.

This software was developed for the SIT project.  If you use all or 
part of it, please give an appropriate acknowledgment.

@see RelatedModule

@version $Id: template!python!py 4 2008-10-08 19:27:36Z salnikov $

@author Mikhail S. Dubrovin
"""
from __future__ import print_function
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
from . import ConfigParameters                as cp
from . import GlobalMethods                   as gm
from . import GUIWhatToDisplayCBoxCSpad       as cboxCS
from . import GUIWhatToDisplayCBoxImage       as cboxIM
from . import GUIWhatToDisplayCBoxOther       as cboxOT
from . import GUIWhatToDisplayAlternative     as wtdAL
from . import GUIWhatToDisplayForImage        as wtdIM
from . import GUIWhatToDisplayForCSpad        as wtdCS
from . import GUIWhatToDisplayForWaveform     as wtdWF
from . import GUIWhatToDisplayForProjections  as wtdPR
from . import GUICorrelation                  as wtdCO
from . import GUICalibCycle                   as wtdCC
from . import GUIConfiguration                as guiconfig
from . import GUISelection                    as guisel
from . import GUIBackground                   as guiBG
from . import GUIGainCorrection               as guiGC

#---------------------
#  Class definition --
#---------------------
class GUIWhatToDisplay ( QtWidgets.QWidget ) :
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

        self.setGeometry(370, 350, 500, 600)
        self.setWindowTitle('What and how to display')

        self.parent = parent

        self.frame = QtWidgets.QFrame(self)
        self.frame.setFrameStyle( QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken )
        self.frame.setLineWidth(0)
        self.frame.setMidLineWidth(1)
        self.frame.setGeometry(self.rect())
        
        self.butClose         = QtWidgets.QPushButton('Quit')
        self.butSave          = QtWidgets.QPushButton('Save')

        self.indTabOpen  = 0
        self.tabBar      = QtWidgets.QTabBar()
        self.tabBar.setShape(QtWidgets.QTabBar.RoundedNorth)
       #self.tabBar.setShape(QtGui.QTabBar.TriangularNorth)
        self.indTabCS    = self.tabBar.addTab('CSpad')
        self.indTabIM    = self.tabBar.addTab('Image')
        self.indTabWF    = self.tabBar.addTab('Waveform')
        self.indTabPR    = self.tabBar.addTab('Proj.')
        self.indTabCO    = self.tabBar.addTab('Corr.')
        self.indTabCC    = self.tabBar.addTab('CalibC.')
        self.indTabEmpty = self.tabBar.addTab(12*' ')
        self.tabBar.setTabEnabled(self.indTabEmpty,False)
        self.isFirstEntry = True

        self.tabBar.setTabTextColor(self.indTabCS,QtGui.QColor('red'))
        self.tabBar.setTabTextColor(self.indTabIM,QtGui.QColor('blue'))
        self.tabBar.setTabTextColor(self.indTabWF,QtGui.QColor('green'))
        self.tabBar.setTabTextColor(self.indTabPR,QtGui.QColor('magenta'))
        self.tabBar.setTabTextColor(self.indTabCO,QtGui.QColor('black'))
        self.tabBar.setTabTextColor(self.indTabCC,QtGui.QColor('red'))

        self.tabBarBot           = QtWidgets.QTabBar()
        self.tabBarBot.setShape(QtWidgets.QTabBar.RoundedSouth)
        #self.tabBarBot.setShape(QtGui.QTabBar.TriangularSouth)
        self.indTabBotConfig     = self.tabBarBot.addTab('Configuration')
        self.indTabBotSelect     = self.tabBarBot.addTab('Selection')
        self.indTabBotBackground = self.tabBarBot.addTab('Bkgd Subtr.')
        self.indTabBotGainCorr   = self.tabBarBot.addTab('Gain Corr.')
        self.indTabBotEmpty      = self.tabBarBot.addTab(18*' ')
        self.tabBarBot.setTabEnabled(self.indTabBotEmpty,False)
        
        self.hboxT = QtWidgets.QHBoxLayout()
        self.hboxT.addWidget(self.tabBar) 

        self.guiTab = wtdCS.GUIWhatToDisplayForCSpad()          
        self.guiTab.setMinimumHeight(240)

        self.hboxD = QtWidgets.QHBoxLayout()
        self.hboxD.addWidget(self.guiTab)
        self.guiTab.close()

        self.hboxC = QtWidgets.QHBoxLayout()
        #self.hboxC.addWidget(self.butRefresh)
        self.hboxC.addWidget(self.butSave)
        self.hboxC.addStretch(2)
        self.hboxC.addWidget(self.butClose)

        self.hboxTB = QtWidgets.QHBoxLayout()
        self.hboxTB.addWidget(self.tabBarBot) 

        self.vboxB = QtWidgets.QVBoxLayout()
        self.isOpenCS = False
        self.isOpenIM = False
        self.isOpenOT = False
        
        self.makeVBoxB()

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addLayout(self.vboxB)
        self.vbox.addStretch(1)     
        self.vbox.addLayout(self.hboxT)
        self.vbox.addLayout(self.hboxD) 
        self.vbox.addLayout(self.hboxTB)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.hboxC)

        self.setLayout(self.vbox)
  
        #self.connect(self.butRefresh,       QtCore.SIGNAL('clicked()'),           self.processRefresh   )
        self.butSave.clicked.connect(self.processSave)
        self.butClose.clicked.connect(self.processClose)
        self.tabBar.currentChanged[int].connect(self.processTabBar)
        self.tabBarBot.currentChanged[int].connect(self.processTabBarBot)

        self.showToolTips()

        cp.confpars.wtdWindowIsOpen = True




    def makeVBoxB(self):

        cspadDatasetIsChecked = gm.CSpadDatasetIsChecked()
        imageDatasetIsChecked = gm.ImageDatasetIsChecked()
        wavefDatasetIsChecked = gm.WaveformDatasetIsChecked()
        correDatasetIsChecked = gm.CorrelationDatasetIsChecked()
        calibDatasetIsChecked = gm.CalibCycleDatasetIsChecked()

        self.vertSize = 365 # accounts for the tab bars and buttons vertical size

        if self.isOpenCS: self.cboxguiCS.close()
        if self.isOpenIM: self.cboxguiIM.close()
        if self.isOpenOT: self.cboxguiOT.close()

        if cspadDatasetIsChecked :
            self.cboxguiCS = cboxCS.GUIWhatToDisplayCBoxCSpad(self)
            self.cboxguiCS.setFixedHeight(150)
            self.vertSize += 150
            self.vboxB.addWidget(self.cboxguiCS) 
            self.indTabOpen = self.indTabCS 
            self.isOpenCS = True

        if imageDatasetIsChecked :
            self.cboxguiIM = cboxIM.GUIWhatToDisplayCBoxImage(self)
            self.cboxguiIM.setFixedHeight(80)
            self.vertSize += 80
            self.vboxB.addWidget(self.cboxguiIM) 
            self.indTabOpen = self.indTabIM 
            self.isOpenIM = True

        if wavefDatasetIsChecked or correDatasetIsChecked :
            self.cboxguiOT = cboxOT.GUIWhatToDisplayCBoxOther(self)
            self.cboxguiOT.setFixedHeight(70)
            self.vertSize += 70
            self.vboxB.addWidget(self.cboxguiOT)
            if wavefDatasetIsChecked : self.indTabOpen = self.indTabWF 
            if correDatasetIsChecked : self.indTabOpen = self.indTabCO 
            self.isOpenOT = True

        #self.cboxguiAlternative = wtdAL.GUIWhatToDisplayAlternative(self, self.title)
        #self.vbox.addWidget(self.cboxguiAlternative)

        if  self.isFirstEntry:
            self.isFirstEntry = False
            #self.tabBar.setCurrentIndex(0)
            self.tabBar.setCurrentIndex(self.indTabOpen)

        self.processTabBar()

        self.setFixedSize(500, self.vertSize)


    def showToolTips(self):
        self.butClose    .setToolTip('Close this window') 


    def resizeEvent(self, e):
        #print 'resizeEvent' 
        self.frame.setGeometry(self.rect())


    def closeEvent(self, event):
        print('closeEvent for WTD GUI')
        if self.isOpenCS: self.cboxguiCS.close()
        if self.isOpenIM: self.cboxguiIM.close()
        if self.isOpenOT: self.cboxguiOT.close()
        self.guiTab.close()
        self.tabBar.close()
        self.tabBarBot.close()
        cp.confpars.wtdWindowIsOpen = False
        QtWidgets.QWidget.closeEvent(self, event)


    def processClose(self):
        print('Close button is clicked for WTD GUI')
        self.close()


    def processSelection(self):
        #print 'Selection'
        self.hboxD.removeWidget(self.guiTab)
        self.guiTab.close()
        self.guiTab = cp.confpars.guiselection = guisel.GUISelection() 
        self.guiTab.setMinimumHeight(240)
        self.hboxD.addWidget(self.guiTab)


    def processConfiguration(self):
        #print 'Configuration'
        self.hboxD.removeWidget(self.guiTab)
        self.guiTab.close()
        self.guiTab = cp.confpars.guiconfig = guiconfig.GUIConfiguration() 
        self.guiTab.setMinimumHeight(240)
        self.hboxD.addWidget(self.guiTab)

    def processBackground(self):
        #print 'Background'
        self.hboxD.removeWidget(self.guiTab)
        self.guiTab.close()
        self.guiTab = cp.confpars.guiBG = guiBG.GUIBackground() 
        self.guiTab.setMinimumHeight(240)
        self.hboxD.addWidget(self.guiTab)


    def processGainCorrection(self):
        #print 'GainCorrection'
        self.hboxD.removeWidget(self.guiTab)
        self.guiTab.close()
        self.guiTab = cp.confpars.guiGC = guiGC.GUIGainCorrection() 
        self.guiTab.setMinimumHeight(240)
        self.hboxD.addWidget(self.guiTab)

    def processSave(self):
        print('Save')
        cp.confpars.writeParameters()


    def processRefresh(self):
        print('Refresh WTD GUI')
        self.makeVBoxB()
    

    def processTabBarBot(self):
        indTab = self.tabBarBot.currentIndex()
        #print 'TabBarBot index=',indTab
        if indTab == self.indTabBotEmpty      : return
        if indTab == self.indTabBotSelect     : self.processSelection()
        if indTab == self.indTabBotConfig     : self.processConfiguration()
        if indTab == self.indTabBotBackground : self.processBackground()
        if indTab == self.indTabBotGainCorr   : self.processGainCorrection()

        self.tabBar.setCurrentIndex(self.indTabEmpty)


    def processTabBar(self):
        indTab = self.tabBar.currentIndex()
        self.indTabOpen = indTab
        #print 'TabBar index=',indTab

        if indTab == self.indTabEmpty: return

        cspadDatasetIsChecked = gm.CSpadDatasetIsChecked()
        imageDatasetIsChecked = gm.ImageDatasetIsChecked()
        wavefDatasetIsChecked = gm.WaveformDatasetIsChecked()
        correDatasetIsChecked = gm.CorrelationDatasetIsChecked()
        calibDatasetIsChecked = gm.CalibCycleDatasetIsChecked()

        self.hboxD.removeWidget(self.guiTab)
        self.guiTab.close()

        if indTab == self.indTabCS:
            if cspadDatasetIsChecked: self.guiTab = wtdCS.GUIWhatToDisplayForCSpad()
            else :                    self.guiTab = wtdAL.GUIWhatToDisplayAlternative(None, 'CSpad')

        if indTab == self.indTabIM:
            if imageDatasetIsChecked: self.guiTab = wtdIM.GUIWhatToDisplayForImage()
            else :                    self.guiTab = wtdAL.GUIWhatToDisplayAlternative(None, 'Image')

        if indTab == self.indTabWF:
            if wavefDatasetIsChecked: self.guiTab = wtdWF.GUIWhatToDisplayForWaveform()
            else :                    self.guiTab = wtdAL.GUIWhatToDisplayAlternative(None, 'Waveforms')

        if indTab == self.indTabPR:
            if cspadDatasetIsChecked or imageDatasetIsChecked:
                                      self.guiTab = wtdPR.GUIWhatToDisplayForProjections()
            else :                    self.guiTab = wtdAL.GUIWhatToDisplayAlternative(None, 'CSpad or Image projections')

        if indTab == self.indTabCO:
            if correDatasetIsChecked: self.guiTab = wtdCO.GUICorrelation()
            else :                    self.guiTab = wtdAL.GUIWhatToDisplayAlternative(None, 'Correlations')

        if indTab == self.indTabCC:
            if calibDatasetIsChecked: self.guiTab = wtdCC.GUICalibCycle()
            else :                    self.guiTab = wtdAL.GUIWhatToDisplayAlternative(None, 'CalibCycle')

        #if indTab == self.indTabED:
        #    self.guiTab = QtGui.QLabel('Sorry, this GUI is not implemented yet.\n' + 
        #                               'Will select 1-D parameters for plot vs event number.')

        self.guiTab.setMinimumHeight(240)
        self.hboxD.addWidget(self.guiTab)
        
        self.tabBarBot.setCurrentIndex(self.indTabBotEmpty)


#-----------------------------
#  In case someone decides to run this module
#
if __name__ == "__main__" :
    app = QtWidgets.QApplication(sys.argv)
    ex  = GUIWhatToDisplay()
    ex.show()
    app.exec_()
#-----------------------------

