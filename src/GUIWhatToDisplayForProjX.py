#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module GUIWhatToDisplayForProjX...
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
class GUIWhatToDisplayForProjX ( QtWidgets.QWidget ) :
    """GUI manipulates with parameters for event selection in particular window of the image."""

    #----------------
    #  Constructor --
    #----------------

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        print('GUIWhatToDisplayForProjX')

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

        self.titXminmax      = QtWidgets.QLabel('X min, max:')
        self.titYminmax      = QtWidgets.QLabel('Y min, max:')

        self.editProjNSlices = QtWidgets.QLineEdit(str(cp.confpars.projX_NSlices ))
        self.editProjSliWidth= QtWidgets.QLineEdit(str(cp.confpars.projX_SliWidth))
        self.editProjNBins   = QtWidgets.QLineEdit(str(cp.confpars.projX_NBins   ))
        self.editProjBinWidth= QtWidgets.QLineEdit(str(cp.confpars.projX_BinWidth))        
        self.editProjXmin    = QtWidgets.QLineEdit(str(cp.confpars.projX_Xmin    ))
        self.editProjXmax    = QtWidgets.QLineEdit(str(cp.confpars.projX_Xmax    ))
        self.editProjYmin    = QtWidgets.QLineEdit(str(cp.confpars.projX_Ymin  ))
        self.editProjYmax    = QtWidgets.QLineEdit(str(cp.confpars.projX_Ymax  ))


        self.editProjNSlices .setValidator(QtGui.QIntValidator(1, 1000,self))
        self.editProjSliWidth.setValidator(QtGui.QIntValidator(1, 2000,self))
        self.editProjNBins   .setValidator(QtGui.QIntValidator(1, 1000,self))
        self.editProjBinWidth.setValidator(QtGui.QIntValidator(1, 2000,self))

        self.editProjXmin    .setValidator(QtGui.QIntValidator(0, 2000,self))
        self.editProjXmax    .setValidator(QtGui.QIntValidator(0, 2000,self))
        self.editProjYmin    .setValidator(QtGui.QIntValidator(0, 2000,self))
        self.editProjYmax    .setValidator(QtGui.QIntValidator(0, 2000,self))

        self.radioBinWidth = QtWidgets.QRadioButton("Bin width:")
        self.radioNBins    = QtWidgets.QRadioButton("N bins:")
        self.radioGroupBin = QtWidgets.QButtonGroup()
        self.radioGroupBin.addButton(self.radioBinWidth)
        self.radioGroupBin.addButton(self.radioNBins)

        self.radioSliWidth = QtWidgets.QRadioButton("Slice width:")
        self.radioNSlices  = QtWidgets.QRadioButton("N slices:")
        self.radioGroupSli = QtWidgets.QButtonGroup()
        self.radioGroupSli.addButton(self.radioSliWidth)
        self.radioGroupSli.addButton(self.radioNSlices)

        if cp.confpars.projX_BinWidthIsOn : self.radioBinWidth.setChecked(True)
        else :                              self.radioNBins.   setChecked(True)

        if cp.confpars.projX_SliWidthIsOn : self.radioSliWidth.setChecked(True)
        else :                              self.radioNSlices. setChecked(True)

        self.setBinWidthReadOnly(not cp.confpars.projX_BinWidthIsOn)
        self.setSliWidthReadOnly(not cp.confpars.projX_SliWidthIsOn)


        grid = QtWidgets.QGridLayout()

        grid.addWidget(self.titXminmax,          0, 0, 2, 1)
        grid.addWidget(self.editProjXmin    ,    0, 1, 2, 1)
        grid.addWidget(self.editProjXmax    ,    0, 2, 2, 1)
        grid.addWidget(self.radioNBins      ,    0, 3)
        grid.addWidget(self.radioBinWidth   ,    1, 3)
        grid.addWidget(self.editProjNBins   ,    0, 4)
        grid.addWidget(self.editProjBinWidth,    1, 4)

        
        grid.addWidget(self.titYminmax,          2, 0, 2, 1)
        grid.addWidget(self.editProjYmin    ,    2, 1, 2, 1)
        grid.addWidget(self.editProjYmax    ,    2, 2, 2, 1)
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
        self.editProjXmin.editingFinished .connect(self.processEditProjXmin)
        self.editProjXmax.editingFinished .connect(self.processEditProjXmax)
        self.editProjYmin.editingFinished .connect(self.processEditProjYmin)
        self.editProjYmax.editingFinished .connect(self.processEditProjYmax)
 
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
        cp.confpars.projX_NSlices  = int(self.editProjNSlices .displayText())
        self.setSlicing()

    def processEditProjSliWidth(self):
        cp.confpars.projX_SliWidth = int(self.editProjSliWidth.displayText())        
        self.setSlicing()

    def processEditProjNBins   (self):
        cp.confpars.projX_NBins    = int(self.editProjNBins   .displayText())        
        self.setBinning()

    def processEditProjBinWidth(self):
        cp.confpars.projX_BinWidth = int(self.editProjBinWidth.displayText())        
        self.setBinning()

    def processEditProjXmin    (self):
        cp.confpars.projX_Xmin     = int(self.editProjXmin    .displayText())        
        self.setBinning()

    def processEditProjXmax    (self):
        cp.confpars.projX_Xmax     = int(self.editProjXmax    .displayText())        
        self.setBinning()

    def processEditProjYmin  (self):
        cp.confpars.projX_Ymin   = int(self.editProjYmin  .displayText())        
        self.setSlicing()

    def processEditProjYmax  (self):
        cp.confpars.projX_Ymax   = int(self.editProjYmax  .displayText())        
        self.setSlicing()


    def setBinning(self) :
        if cp.confpars.projX_BinWidthIsOn :
            cp.confpars.projX_NBins    = (cp.confpars.projX_Xmax - cp.confpars.projX_Xmin) // cp.confpars.projX_BinWidth
            self.editProjNBins.setText( str(cp.confpars.projX_NBins) )            
        else :
            cp.confpars.projX_BinWidth = (cp.confpars.projX_Xmax - cp.confpars.projX_Xmin) // cp.confpars.projX_NBins
            self.editProjBinWidth.setText( str(cp.confpars.projX_BinWidth) )  


    def setSlicing(self) :
        if cp.confpars.projX_SliWidthIsOn :
            cp.confpars.projX_NSlices  = (cp.confpars.projX_Ymax - cp.confpars.projX_Ymin) // cp.confpars.projX_SliWidth
            self.editProjNSlices.setText( str(cp.confpars.projX_NSlices) )            
        else :
            cp.confpars.projX_SliWidth = (cp.confpars.projX_Ymax - cp.confpars.projX_Ymin) // cp.confpars.projX_NSlices
            self.editProjSliWidth.setText( str(cp.confpars.projX_SliWidth) )  


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
        cp.confpars.projX_BinWidthIsOn = True
        self.setBinWidthReadOnly(False)


    def processRadioNBins(self):
        cp.confpars.projX_BinWidthIsOn = False
        self.setBinWidthReadOnly(True)


    def processRadioSliWidth(self):
        cp.confpars.projX_SliWidthIsOn = True
        self.setSliWidthReadOnly(False)


    def processRadioNSlices(self):
        cp.confpars.projX_SliWidthIsOn = False
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
    ex  = GUIWhatToDisplayForProjX()
    ex.show()
    app.exec_()
#-----------------------------

