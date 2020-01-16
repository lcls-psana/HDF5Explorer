#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module GUISelectionWindow...
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
from . import GlobalMethods    as gm

#---------------------
#  Class definition --
#---------------------
class GUISelectionWindow ( QtWidgets.QWidget ) :
    """GUI manipulates with parameters for event selection in particular window of the image."""

    #----------------
    #  Constructor --
    #----------------

    def __init__(self, parent=None, window=0):
        QtWidgets.QWidget.__init__(self, parent)

        print('GUISelectionWindow for region', window)

        self.window = window

        self.setGeometry(370, 350, 500, 150)
        self.setWindowTitle('Adjust selection parameters')

        self.palette = QtGui.QPalette()

        self.frame = QtWidgets.QFrame(self)
        self.frame.setFrameStyle( QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken ) #Box, Panel | Sunken, Raised 
        self.frame.setLineWidth(0)
        self.frame.setMidLineWidth(1)
        self.frame.setGeometry(self.rect())
        self.frame.setVisible(False)

        titFont12 = QtGui.QFont("Sans Serif", 12, QtGui.QFont.Bold)
        titFont10 = QtGui.QFont("Sans Serif", 10, QtGui.QFont.Bold)

        self.titXminmax= QtWidgets.QLabel('Xmin, Xmax:')
        self.titYminmax= QtWidgets.QLabel('Ymin, Ymax:')

        self.char_expand = u'\u25BE' # down-head triangle
        height = 20
        width  = 50

        self.editSelectionThr   = QtWidgets.QLineEdit(str(cp.confpars.selectionWindowParameters[self.window][0]))
        self.editSelectionXmin  = QtWidgets.QLineEdit(str(cp.confpars.selectionWindowParameters[self.window][2]))
        self.editSelectionXmax  = QtWidgets.QLineEdit(str(cp.confpars.selectionWindowParameters[self.window][3]))
        self.editSelectionYmin  = QtWidgets.QLineEdit(str(cp.confpars.selectionWindowParameters[self.window][4]))
        self.editSelectionYmax  = QtWidgets.QLineEdit(str(cp.confpars.selectionWindowParameters[self.window][5]))

        self.editSelectionThr   .setMaximumWidth(width)
        self.editSelectionXmin  .setMaximumWidth(width)
        self.editSelectionXmax  .setMaximumWidth(width)
        self.editSelectionYmin  .setMaximumWidth(width)
        self.editSelectionYmax  .setMaximumWidth(width)

        self.editSelectionThr   .setMaximumHeight(40)
        self.editSelectionXmin  .setMaximumHeight(height)
        self.editSelectionXmax  .setMaximumHeight(height)
        self.editSelectionYmin  .setMaximumHeight(height)
        self.editSelectionYmax  .setMaximumHeight(height)

        self.editSelectionThr   .setValidator(QtGui.QIntValidator(0,30000,self))
        self.editSelectionXmin  .setValidator(QtGui.QIntValidator(0, 2000,self))
        self.editSelectionXmax  .setValidator(QtGui.QIntValidator(0, 2000,self))
        self.editSelectionYmin  .setValidator(QtGui.QIntValidator(0, 2000,self))
        self.editSelectionYmax  .setValidator(QtGui.QIntValidator(0, 2000,self))

        self.titThreshold  = QtWidgets.QLabel('Threshold on intensity')
        self.radioInWin    = QtWidgets.QRadioButton("integral")
        self.radioInBin    = QtWidgets.QRadioButton("maximal")
        self.radioGroup    = QtWidgets.QButtonGroup()
        self.radioGroup.addButton(self.radioInWin)
        self.radioGroup.addButton(self.radioInBin)

        if cp.confpars.selectionWindowParameters[self.window][1] : self.radioInBin.setChecked(True)
        else :                                                     self.radioInWin.setChecked(True)

        self.titSelDataSet        = QtWidgets.QLabel('Dataset:')
        self.butSelDataSet = QtWidgets.QPushButton(cp.confpars.selectionWindowParameters[self.window][6])
        self.butSelDataSet.setMaximumWidth(350)
        self.setButSelDataSetTextAlignment()

        self.popupMenuForDataSet = QtWidgets.QMenu()
        self.fillPopupMenuForDataSet()


        grid = QtWidgets.QGridLayout()

        grid.addWidget(self.titSelDataSet,       0, 0)
        grid.addWidget(self.butSelDataSet,       0, 1, 1, 4)

        grid.addWidget(self.titThreshold,        1, 0, 2, 2)
        grid.addWidget(self.editSelectionThr,    1, 2, 2, 1)
        grid.addWidget(self.radioInBin,          1, 3)
        grid.addWidget(self.radioInWin,          2, 3)

        grid.addWidget(self.titXminmax,          4, 0)
        grid.addWidget(self.editSelectionXmin,   4, 1)
        grid.addWidget(self.editSelectionXmax,   4, 2)

        grid.addWidget(self.titYminmax,          5, 0)
        grid.addWidget(self.editSelectionYmin,   5, 1)
        grid.addWidget(self.editSelectionYmax,   5, 2)


        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addLayout(grid) 
        self.vbox.addStretch(1)     

        if parent == None :
            self.setLayout(self.vbox)
            self.show()

        self.radioInBin.clicked.connect(self.processRadioInBin)
        self.radioInWin.clicked.connect(self.processRadioInWin)
        self.editSelectionThr.editingFinished .connect(self.processEditSelectionThr)
        self.editSelectionXmin.editingFinished .connect(self.processEditSelectionXmin)
        self.editSelectionXmax.editingFinished .connect(self.processEditSelectionXmax)
        self.editSelectionYmin.editingFinished .connect(self.processEditSelectionYmin)
        self.editSelectionYmax.editingFinished .connect(self.processEditSelectionYmax)
        self.butSelDataSet.clicked.connect(self.processMenuForDataSet)
  
        cp.confpars.selectionWindowIsOpen = True

        self.showToolTips()

    #-------------------
    # Private methods --
    #-------------------

    def showToolTips(self):
        # Tips for buttons and fields:
        #self           .setToolTip('This GUI deals with the configuration parameters for waveforms.')
        self.radioInBin       .setToolTip('Select between threshold in bin or in entire window.')
        self.radioInWin       .setToolTip('Select between threshold in bin or in entire window.')
        #self.editSelectionXmin.setToolTip('This field can be edited for Manual control only.')
        #self.editSelectionXmax.setToolTip('This field can be edited for Manual control only.')
        #self.editSelectionYmin.setToolTip('This field can be edited for Manual control only.')
        #self.editSelectionYmax.setToolTip('This field can be edited for Manual control only.')


    def setEditFieldsReadOnly(self, isReadOnly=False):

        if isReadOnly == True : self.palette.setColor(QtGui.QPalette.Base,QtGui.QColor('grey'))
        else :                  self.palette.setColor(QtGui.QPalette.Base,QtGui.QColor('white'))

        self.editSelectionXmin.setPalette(self.palette)
        self.editSelectionXmax.setPalette(self.palette)
        self.editSelectionYmin.setPalette(self.palette)
        self.editSelectionYmax.setPalette(self.palette)

        self.editSelectionXmin.setReadOnly(isReadOnly)
        self.editSelectionXmax.setReadOnly(isReadOnly)
        self.editSelectionYmin.setReadOnly(isReadOnly)
        self.editSelectionYmax.setReadOnly(isReadOnly)


    def resizeEvent(self, e):
        self.frame.setGeometry(self.rect())


    def getVBoxForLayout(self):
        return self.vbox


    def setParentWidget(self,parent):
        self.parentWidget = parent


    def closeEvent(self, event):
        cp.confpars.selectionWindowIsOpen = False
        QtWidgets.QWidget.closeEvent(self, event)


    def processClose(self):
        self.close()


    def processRadioInBin(self):
        cp.confpars.selectionWindowParameters[self.window][1] = True


    def processRadioInWin(self):
        cp.confpars.selectionWindowParameters[self.window][1] = False


    def processEditSelectionThr(self):
        cp.confpars.selectionWindowParameters[self.window][0] = int(self.editSelectionThr.displayText())        


    def processEditSelectionXmin(self):
        cp.confpars.selectionWindowParameters[self.window][2] = int(self.editSelectionXmin.displayText())        


    def processEditSelectionXmax(self):
        cp.confpars.selectionWindowParameters[self.window][3] = int(self.editSelectionXmax.displayText())        


    def processEditSelectionYmin(self):
        cp.confpars.selectionWindowParameters[self.window][4] = int(self.editSelectionYmin.displayText())        


    def processEditSelectionYmax(self):
        cp.confpars.selectionWindowParameters[self.window][5] = int(self.editSelectionYmax.displayText())        


    def setButSelDataSetTextAlignment(self):
        if self.butSelDataSet.text() == 'None' :
            self.butSelDataSet.setStyleSheet('Text-align:center')
        else :
            self.butSelDataSet.setStyleSheet('Text-align:right')


    def fillPopupMenuForDataSet(self):
        #print 'fillPopupMenuForDataSet'
        self.popupMenuForDataSet.addAction('None')
        for dsname in cp.confpars.list_of_checked_item_names :
            imageIsInTheName = gm.ImageIsInTheName(dsname)
            cspadIsInTheName = gm.CSpadIsInTheName(dsname)
            if imageIsInTheName or cspadIsInTheName:

                self.popupMenuForDataSet.addAction(dsname)


    def processMenuForDataSet(self):
        #print 'MenuForDataSet'
        actionSelected = self.popupMenuForDataSet.exec_(QtGui.QCursor.pos())
        if actionSelected==None : return
        selected_ds = actionSelected.text()
        self.butSelDataSet.setText( selected_ds )
        self.setButSelDataSetTextAlignment()
        cp.confpars.selectionWindowParameters[self.window][6] = str(selected_ds)


#-----------------------------
#  In case someone decides to run this module
#
if __name__ == "__main__" :
    app = QtWidgets.QApplication(sys.argv)
    ex  = GUISelectionWindow()
    ex.show()
    app.exec_()
#-----------------------------

