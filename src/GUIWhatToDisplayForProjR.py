#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module GUIWhatToDisplayForProjR...
#
#------------------------------------------------------------------------

"""GUI manipulates with parameters for event selection in particular window of the image.

This software was developed for the SIT project.  If you use all or 
part of it, please give an appropriate acknowledgment.

@see RelatedModule

@version $Id: template!python!py 4 2008-10-08 19:27:36Z salnikov $

@author Mikhail S. Dubrovin
"""
from __future__ import print_function
from __future__ import division
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

#-----------------------------
# Imports for other modules --
#-----------------------------
from . import ConfigParameters as cp

#---------------------
#  Class definition --
#---------------------
class GUIWhatToDisplayForProjR ( QtWidgets.QWidget ) :
    """GUI manipulates with parameters for event selection in particular window of the image."""

    #----------------
    #  Constructor --
    #----------------

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        print('GUIWhatToDisplayForProjR')

        self.setGeometry(370, 350, 500, 150)
        self.setWindowTitle('Adjust selection parameters')

        self.palette_grey  = QtGui.QPalette()
        self.palette_white = QtGui.QPalette()
        self.palette_grey  .setColor(QtGui.QPalette.Base,QtGui.QColor('grey'))
        self.palette_white .setColor(QtGui.QPalette.Base,QtGui.QColor('white'))

        self.frame = QtWidgets.QFrame(self)
        self.frame.setFrameStyle( QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken ) #Box, Panel | Sunken, Raised 
        self.frame.setLineWidth(0)
        self.frame.setMidLineWidth(1)
        self.frame.setGeometry(self.rect())
        self.frame.setVisible(False)

        titFont12 = QtGui.QFont("Sans Serif", 12, QtGui.QFont.Bold)
        titFont10 = QtGui.QFont("Sans Serif", 10, QtGui.QFont.Bold)

        #self.char_expand = u'\u25BE' # down-head triangle
        height = 22
        width  = 50

        self.titRminmax      = QtWidgets.QLabel('R   min, max:')
        self.titPhiminmax    = QtWidgets.QLabel('Phi min, max:')

        self.editProjNSlices = QtWidgets.QLineEdit(str(cp.confpars.projR_NSlices ))
        self.editProjSliWidth= QtWidgets.QLineEdit(str(cp.confpars.projR_SliWidth))
        self.editProjNBins   = QtWidgets.QLineEdit(str(cp.confpars.projR_NBins   ))
        self.editProjBinWidth= QtWidgets.QLineEdit(str(cp.confpars.projR_BinWidth))        
        self.editProjRmin    = QtWidgets.QLineEdit(str(cp.confpars.projR_Rmin    ))
        self.editProjRmax    = QtWidgets.QLineEdit(str(cp.confpars.projR_Rmax    ))
        self.editProjPhimin  = QtWidgets.QLineEdit(str(cp.confpars.projR_Phimin  ))
        self.editProjPhimax  = QtWidgets.QLineEdit(str(cp.confpars.projR_Phimax  ))

        #self.editProjRmin    .setMaximumWidth(width)
        #self.editProjRmax    .setMaximumWidth(width)
        #self.editProjPhimin  .setMaximumWidth(width)
        #self.editProjPhimax  .setMaximumWidth(width)

        #self.editProjRmin    .setMaximumHeight(height)
        #self.editProjRmax    .setMaximumHeight(height)
        #self.editProjPhimin  .setMaximumHeight(height)
        #self.editProjPhimax  .setMaximumHeight(height)

        self.editProjNSlices .setValidator(QtGui.QIntValidator(1,   50,self))
        self.editProjSliWidth.setValidator(QtGui.QIntValidator(1,  360,self))
        self.editProjNBins   .setValidator(QtGui.QIntValidator(1, 1000,self))
        self.editProjBinWidth.setValidator(QtGui.QIntValidator(1, 1000,self))

        self.editProjRmin    .setValidator(QtGui.QIntValidator(   0, 1000,self))
        self.editProjRmax    .setValidator(QtGui.QIntValidator(   0, 1000,self))
        self.editProjPhimin  .setValidator(QtGui.QIntValidator(-180,  180,self))
        self.editProjPhimax  .setValidator(QtGui.QIntValidator(-180,  180,self))

        self.radioBinWidth = QtWidgets.QRadioButton("Bin width:")
        self.radioNBins    = QtWidgets.QRadioButton("N bins:")
        self.radioGroupBin = QtWidgets.QButtonGroup()
        self.radioGroupBin.addButton(self.radioBinWidth)
        self.radioGroupBin.addButton(self.radioNBins)

        self.radioSliWidth = QtWidgets.QRadioButton("Sector width:")
        self.radioNSlices  = QtWidgets.QRadioButton("N sectors:")
        self.radioGroupSli = QtWidgets.QButtonGroup()
        self.radioGroupSli.addButton(self.radioSliWidth)
        self.radioGroupSli.addButton(self.radioNSlices)

        if cp.confpars.projR_BinWidthIsOn : self.radioBinWidth.setChecked(True)
        else :                              self.radioNBins.   setChecked(True)

        if cp.confpars.projR_SliWidthIsOn : self.radioSliWidth.setChecked(True)
        else :                              self.radioNSlices. setChecked(True)

        self.setBinWidthReadOnly(not cp.confpars.projR_BinWidthIsOn)
        self.setSliWidthReadOnly(not cp.confpars.projR_SliWidthIsOn)


        grid = QtWidgets.QGridLayout()

        grid.addWidget(self.titRminmax,          0, 0, 2, 1)
        grid.addWidget(self.editProjRmin    ,    0, 1, 2, 1)
        grid.addWidget(self.editProjRmax    ,    0, 2, 2, 1)
        grid.addWidget(self.radioNBins      ,    0, 3)
        grid.addWidget(self.radioBinWidth   ,    1, 3)
        grid.addWidget(self.editProjNBins   ,    0, 4)
        grid.addWidget(self.editProjBinWidth,    1, 4)

        
        grid.addWidget(self.titPhiminmax,        2, 0, 2, 1)
        grid.addWidget(self.editProjPhimin  ,    2, 1, 2, 1)
        grid.addWidget(self.editProjPhimax  ,    2, 2, 2, 1)
        grid.addWidget(self.radioNSlices    ,    2, 3)
        grid.addWidget(self.radioSliWidth   ,    3, 3)
        grid.addWidget(self.editProjNSlices ,    2, 4)
        grid.addWidget(self.editProjSliWidth,    3, 4)

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addLayout(grid) 
        self.vbox.addStretch(1)     

        if parent == None :
            self.setLayout(self.vbox)
            self.show()

        self.radioBinWidth.clicked.connect(self.processRadioBinWidth)
        self.radioNBins.clicked.connect(self.processRadioNBins)
        self.radioSliWidth.clicked.connect(self.processRadioSliWidth)
        self.radioNSlices.clicked.connect(self.processRadioNSlices)

        self.editProjNSlices.editingFinished .connect(self.processEditProjNSlices)
        self.editProjSliWidth.editingFinished .connect(self.processEditProjSliWidth)
        self.editProjNBins.editingFinished .connect(self.processEditProjNBins)
        self.editProjBinWidth.editingFinished .connect(self.processEditProjBinWidth)
        self.editProjRmin.editingFinished .connect(self.processEditProjRmin)
        self.editProjRmax.editingFinished .connect(self.processEditProjRmax)
        self.editProjPhimin.editingFinished .connect(self.processEditProjPhimin)
        self.editProjPhimax.editingFinished .connect(self.processEditProjPhimax)
 
#        cp.confpars.selectionWindowIsOpen = True

        self.setSlicing()
        self.setBinning()
        self.showToolTips()

    #-------------------
    # Private methods --
    #-------------------

    def showToolTips(self):
        pass
        # Tips for buttons and fields:
        #self           .setToolTip('This GUI deals with the configuration parameters for waveforms.')
        #self.radioInBin       .setToolTip('Select between threshold in bin or in entire window.')
        #self.radioInWin       .setToolTip('Select between threshold in bin or in entire window.')
        #self.editSelectionXmin.setToolTip('This field can be edited for Manual control only.')

    def processEditProjNSlices (self):
        cp.confpars.projR_NSlices  = int(self.editProjNSlices .displayText())
        self.setSlicing()

    def processEditProjSliWidth(self):
        cp.confpars.projR_SliWidth = int(self.editProjSliWidth.displayText())        
        self.setSlicing()

    def processEditProjNBins   (self):
        cp.confpars.projR_NBins    = int(self.editProjNBins   .displayText())        
        self.setBinning()

    def processEditProjBinWidth(self):
        cp.confpars.projR_BinWidth = int(self.editProjBinWidth.displayText())        
        self.setBinning()

    def processEditProjRmin    (self):
        cp.confpars.projR_Rmin     = int(self.editProjRmin    .displayText())        
        self.setBinning()

    def processEditProjRmax    (self):
        cp.confpars.projR_Rmax     = int(self.editProjRmax    .displayText())        
        self.setBinning()

    def processEditProjPhimin  (self):
        cp.confpars.projR_Phimin   = int(self.editProjPhimin  .displayText())        
        self.setSlicing()

    def processEditProjPhimax  (self):
        cp.confpars.projR_Phimax   = int(self.editProjPhimax  .displayText())        
        self.setSlicing()


    def setBinning(self) :
        if cp.confpars.projR_BinWidthIsOn :
            cp.confpars.projR_NBins    = (cp.confpars.projR_Rmax - cp.confpars.projR_Rmin) // cp.confpars.projR_BinWidth
            self.editProjNBins.setText( str(cp.confpars.projR_NBins) )            
        else :
            cp.confpars.projR_BinWidth = (cp.confpars.projR_Rmax - cp.confpars.projR_Rmin) // cp.confpars.projR_NBins
            self.editProjBinWidth.setText( str(cp.confpars.projR_BinWidth) )  


    def setSlicing(self) :
        if cp.confpars.projR_SliWidthIsOn :
            cp.confpars.projR_NSlices  = (cp.confpars.projR_Phimax - cp.confpars.projR_Phimin) // cp.confpars.projR_SliWidth
            self.editProjNSlices.setText( str(cp.confpars.projR_NSlices) )            
        else :
            cp.confpars.projR_SliWidth = (cp.confpars.projR_Phimax - cp.confpars.projR_Phimin) // cp.confpars.projR_NSlices
            self.editProjSliWidth.setText( str(cp.confpars.projR_SliWidth) )  


    def setBinWidthReadOnly(self, isReadOnly=False):
        if isReadOnly == True :
            self.editProjNBins    .setPalette(self.palette_white)
            self.editProjBinWidth .setPalette(self.palette_grey )
        else :
            self.editProjNBins    .setPalette(self.palette_grey )
            self.editProjBinWidth .setPalette(self.palette_white)

        self.editProjNBins    .setReadOnly(not isReadOnly)
        self.editProjBinWidth .setReadOnly(isReadOnly)


    def setSliWidthReadOnly(self, isReadOnly=False):
        if isReadOnly == True :
           self.editProjNSlices  .setPalette(self.palette_white)
           self.editProjSliWidth .setPalette(self.palette_grey )
        else :
           self.editProjNSlices  .setPalette(self.palette_grey )
           self.editProjSliWidth .setPalette(self.palette_white)

        self.editProjNSlices  .setReadOnly(not isReadOnly)
        self.editProjSliWidth .setReadOnly(isReadOnly)


    def processRadioBinWidth(self):
        cp.confpars.projR_BinWidthIsOn = True
        self.setBinWidthReadOnly(False)


    def processRadioNBins(self):
        cp.confpars.projR_BinWidthIsOn = False
        self.setBinWidthReadOnly(True)


    def processRadioSliWidth(self):
        cp.confpars.projR_SliWidthIsOn = True
        self.setSliWidthReadOnly(False)


    def processRadioNSlices(self):
        cp.confpars.projR_SliWidthIsOn = False
        self.setSliWidthReadOnly(True)


    def getVBoxForLayout(self):
        return self.vbox


    def setParentWidget(self,parent):
        self.parentWidget = parent


    def resizeEvent(self, e):
        self.frame.setGeometry(self.rect())


    def closeEvent(self, event):
        #cp.confpars.....WindowIsOpen = False
        pass
        QtWidgets.QWidget.closeEvent(self, event)
    

    def processClose(self):
        self.close()

#-----------------------------
#  In case someone decides to run this module
#
if __name__ == "__main__" :
    app = QtWidgets.QApplication(sys.argv)
    ex  = GUIWhatToDisplayForProjR()
    ex.show()
    app.exec_()
#-----------------------------

