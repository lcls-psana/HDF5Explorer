#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module GUIWhatToDisplayCBoxCSpad...
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
class GUIWhatToDisplayCBoxCSpad ( QtWidgets.QWidget ) :
    """Provides GUI to select information for rendering."""

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

        self.setGeometry(370, 350, 500, 150)
        self.setWindowTitle('What to display for CSpad?')

        self.parent = parent

        self.frame = QtWidgets.QFrame(self)
        self.frame.setFrameStyle( QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken )
        self.frame.setLineWidth(0)
        self.frame.setMidLineWidth(1)
        self.frame.setGeometry(self.rect())
        
        titFont   = QtGui.QFont("Sans Serif", 12, QtGui.QFont.Bold)

        self.titCSpad    = QtWidgets.QLabel('CSpad')
        self.titCSpad   .setFont (titFont) 

        self.titCSImage       = QtWidgets.QLabel('Images:')
        self.titCSSpectra     = QtWidgets.QLabel('Spectra:')
        self.titCSImageSpec   = QtWidgets.QLabel('Image & Spectrum:')
        self.titCSProjections = QtWidgets.QLabel('Projections:')

        self.cboxCSApplyTiltAngle = QtWidgets.QCheckBox('Apply tilt angle for Quad and Det.', self)
        self.cboxCSImageQuad      = QtWidgets.QCheckBox('Quad',               self)
        self.cboxCSImageDet       = QtWidgets.QCheckBox('Detector',           self)
        self.cboxCSImage          = QtWidgets.QCheckBox('8 of 2x1',           self)
        self.cboxCSImageOfPair    = QtWidgets.QCheckBox('1 of 2x1',           self)
        self.cboxCSSpectrum       = QtWidgets.QCheckBox('16 ASICs',           self)
        self.cboxCSSpectrumDet    = QtWidgets.QCheckBox('Detecror',           self)
        self.cboxCSSpectrum08     = QtWidgets.QCheckBox('8 of 2x1',           self)
        self.cboxCSProjX          = QtWidgets.QCheckBox('X',                  self)
        self.cboxCSProjY          = QtWidgets.QCheckBox('Y',                  self)
        self.cboxCSProjR          = QtWidgets.QCheckBox('R',                  self)
        self.cboxCSProjPhi        = QtWidgets.QCheckBox(u'\u03C6',            self) # Phi in Greek

        if cp.confpars.cspadImageOfPairIsOn : self.cboxCSImageOfPair   .setCheckState(2)
        if cp.confpars.cspadImageIsOn       : self.cboxCSImage         .setCheckState(2)
        if cp.confpars.cspadImageQuadIsOn   : self.cboxCSImageQuad     .setCheckState(2)
        if cp.confpars.cspadImageDetIsOn    : self.cboxCSImageDet      .setCheckState(2)
        if cp.confpars.cspadSpectrumIsOn    : self.cboxCSSpectrum      .setCheckState(2)
        if cp.confpars.cspadSpectrumDetIsOn : self.cboxCSSpectrumDet   .setCheckState(2)
        if cp.confpars.cspadSpectrum08IsOn  : self.cboxCSSpectrum08    .setCheckState(2)
        if cp.confpars.cspadProjXIsOn       : self.cboxCSProjX         .setCheckState(2)
        if cp.confpars.cspadProjYIsOn       : self.cboxCSProjY         .setCheckState(2)
        if cp.confpars.cspadProjRIsOn       : self.cboxCSProjR         .setCheckState(2)
        if cp.confpars.cspadProjPhiIsOn     : self.cboxCSProjPhi       .setCheckState(2)
        if cp.confpars.cspadApplyTiltAngle  : self.cboxCSApplyTiltAngle.setCheckState(2)

        self.showToolTips()

        gridCS = QtWidgets.QGridLayout()
        gridCS.addWidget(self. titCSpad,            0, 0)
        gridCS.addWidget(self.cboxCSApplyTiltAngle, 0, 2, 1, 3)

        gridCS.addWidget(self. titCSImage,          1, 0)
        gridCS.addWidget(self.cboxCSImage,          1, 1)
        gridCS.addWidget(self.cboxCSImageQuad,      1, 2)
        gridCS.addWidget(self.cboxCSImageDet,       1, 3)

        gridCS.addWidget(self. titCSSpectra,        2, 0)
        gridCS.addWidget(self.cboxCSSpectrum08,     2, 1)
        gridCS.addWidget(self.cboxCSSpectrum,       2, 2)
        gridCS.addWidget(self.cboxCSSpectrumDet,    2, 3)

        gridCS.addWidget(self. titCSImageSpec,      3, 0)
        gridCS.addWidget(self.cboxCSImageOfPair,    3, 1)

        gridCS.addWidget(self. titCSProjections,    4, 0)
        gridCS.addWidget(self.cboxCSProjX,          4, 1)
        gridCS.addWidget(self.cboxCSProjY,          4, 2)
        gridCS.addWidget(self.cboxCSProjR,          4, 3)
        gridCS.addWidget(self.cboxCSProjPhi,        4, 4)
        

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addLayout(gridCS) 
        self.setLayout(self.vbox)
  
        self.cboxCSImage.stateChanged[int].connect(self.processCBoxCSImage)
        self.cboxCSImageQuad.stateChanged[int].connect(self.processCBoxCSImageQuad)
        self.cboxCSImageDet.stateChanged[int].connect(self.processCBoxCSImageDet)
        self.cboxCSImageOfPair.stateChanged[int].connect(self.processCBoxCSImageOfPair)
        self.cboxCSSpectrum.stateChanged[int].connect(self.processCBoxCSSpectrum)
        self.cboxCSSpectrum08.stateChanged[int].connect(self.processCBoxCSSpectrum08)
        self.cboxCSSpectrumDet.stateChanged[int].connect(self.processCBoxCSSpectrumDet)
        self.cboxCSProjX.stateChanged[int].connect(self.processCBoxCSProjX)
        self.cboxCSProjY.stateChanged[int].connect(self.processCBoxCSProjY)
        self.cboxCSProjR.stateChanged[int].connect(self.processCBoxCSProjR)
        self.cboxCSProjPhi.stateChanged[int].connect(self.processCBoxCSProjPhi)
        self.cboxCSApplyTiltAngle.stateChanged[int].connect(self.processCBoxCSApplyTiltAngle)


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


    def setActiveTabBarForIndex(self,ind,subind=None):
        self.parent.tabBar.setCurrentIndex(ind)               # 0,1,2,3 stands for CSpad, Image, Waveform, Proj., Corr. 
        if subind != None :
            self.parent.guiTab.tabBar.setCurrentIndex(subind) # 0,1,2,3 stands for X,Y,R,Phi


    def processCBoxCSProjX(self, value):
        if self.cboxCSProjX.isChecked():
            self.setActiveTabBarForIndex(self.parent.indTabPR,0) # 0 stands for X
            cp.confpars.cspadProjXIsOn = True
        else:
            cp.confpars.cspadProjXIsOn = False


    def processCBoxCSProjY(self, value):
        if self.cboxCSProjY.isChecked():
            self.setActiveTabBarForIndex(self.parent.indTabPR,1) # 1 stands for Y
            cp.confpars.cspadProjYIsOn = True
        else:
            cp.confpars.cspadProjYIsOn = False


    def processCBoxCSProjR(self, value):
        if self.cboxCSProjR.isChecked():
            self.setActiveTabBarForIndex(self.parent.indTabPR,2) # 2 stands for R
            cp.confpars.cspadProjRIsOn = True
        else:
            cp.confpars.cspadProjRIsOn = False


    def processCBoxCSProjPhi(self, value):
        if self.cboxCSProjPhi.isChecked():
            self.setActiveTabBarForIndex(self.parent.indTabPR,3) # 3 stands for Phi
            cp.confpars.cspadProjPhiIsOn = True
        else:
            cp.confpars.cspadProjPhiIsOn = False


    def processCBoxCSImage(self, value):
        if self.cboxCSImage.isChecked():
            self.setActiveTabBarForIndex(self.parent.indTabCS)
            cp.confpars.cspadImageIsOn = True
        else:
            cp.confpars.cspadImageIsOn = False


    def processCBoxCSImageOfPair(self, value):
        if self.cboxCSImageOfPair.isChecked():
            self.setActiveTabBarForIndex(self.parent.indTabCS)
            cp.confpars.cspadImageOfPairIsOn = True
        else:
            cp.confpars.cspadImageOfPairIsOn = False


    def processCBoxCSApplyTiltAngle(self, value):
        if self.cboxCSApplyTiltAngle.isChecked():
            self.setActiveTabBarForIndex(self.parent.indTabCS)
            cp.confpars.cspadApplyTiltAngle = True
        else:
            cp.confpars.cspadApplyTiltAngle = False


    def processCBoxCSImageQuad(self, value):
        if self.cboxCSImageQuad.isChecked():
            self.setActiveTabBarForIndex(self.parent.indTabCS)
            cp.confpars.cspadImageQuadIsOn = True
        else:
            cp.confpars.cspadImageQuadIsOn = False


    def processCBoxCSImageDet(self, value):
        if self.cboxCSImageDet.isChecked():
            self.setActiveTabBarForIndex(self.parent.indTabCS)
            cp.confpars.cspadImageDetIsOn = True
        else:
            cp.confpars.cspadImageDetIsOn = False


    def processCBoxCSSpectrum(self, value):
        if self.cboxCSSpectrum.isChecked():
            self.setActiveTabBarForIndex(self.parent.indTabCS)
            cp.confpars.cspadSpectrumIsOn = True
        else:
            cp.confpars.cspadSpectrumIsOn = False


    def processCBoxCSSpectrum08(self, value):
        if self.cboxCSSpectrum08.isChecked():
            self.setActiveTabBarForIndex(self.parent.indTabCS)
            cp.confpars.cspadSpectrum08IsOn = True
        else:
            cp.confpars.cspadSpectrum08IsOn = False


    def processCBoxCSSpectrumDet(self, value):
        if self.cboxCSSpectrumDet.isChecked():
            self.setActiveTabBarForIndex(self.parent.indTabCS)
            cp.confpars.cspadSpectrumDetIsOn = True
        else:
            cp.confpars.cspadSpectrumDetIsOn = False


#-----------------------------
#  In case someone decides to run this module
#
if __name__ == "__main__" :
    app = QtWidgets.QApplication(sys.argv)
    ex  = GUIWhatToDisplayCBoxCSpad()
    ex.show()
    app.exec_()
#-----------------------------

