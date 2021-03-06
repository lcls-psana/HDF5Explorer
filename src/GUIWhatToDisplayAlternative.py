#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module GUIWhatToDisplayAlternative...
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
from . import ConfigParameters as cp
from . import GUISelectItems   as guiselitems

#---------------------
#  Class definition --
#---------------------
class GUIWhatToDisplayAlternative ( QtWidgets.QWidget ) :
    """Provides GUI to select information for rendering."""

    #--------------------
    #  Class variables --
    #--------------------
    #publicStaticVariable = 0 
    #__privateStaticVariable = "A string"

    #----------------
    #  Constructor --
    #----------------

    def __init__(self, parent=None, title=None):

        QtWidgets.QWidget.__init__(self, None) #parent=None

        self.parent = parent
        self.title  = title

        self.setGeometry(370, 350, 500, 30)
        self.setWindowTitle('What to display alternative GUI')

        self.frame = QtWidgets.QFrame(self)
        self.frame.setFrameStyle( QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken )
        self.frame.setLineWidth(0)
        self.frame.setMidLineWidth(1)
        self.frame.setGeometry(self.rect())
        
        titFont   = QtGui.QFont("Sans Serif", 12, QtGui.QFont.Bold)

        self.titFor    = QtWidgets.QLabel('For')
        self.titItem   = QtWidgets.QLabel(self.title)
        self.titItem   .setFont (titFont) 

        self.titH5Tree = QtWidgets.QLabel('check relevant dataset(s) from')
        self.butH5Tree = QtWidgets.QPushButton('HDF5 tree')
        self.butH5Tree.setStyleSheet("background-color: rgb(180, 255, 180); color: rgb(0, 0, 0)") # Yellowish
        
        self.hboxT = QtWidgets.QHBoxLayout()
        self.hboxT.addWidget(self.titFor)
        self.hboxT.addWidget(self.titItem)
        self.hboxT.addStretch(1)

        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.addWidget(self.titH5Tree)
        self.hbox.addWidget(self.butH5Tree)
        self.hbox.addStretch(1)

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.hboxT) 
        self.vbox.addLayout(self.hbox) 
        self.vbox.addStretch(1)

        self.setLayout(self.vbox)

        self.butH5Tree.clicked.connect(self.processDisplay)

        self.showToolTips()

    def showToolTips(self):
        self.butH5Tree.setToolTip('Open HDF5 tree GUI and select the items for plots.') 
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


    def processDisplay(self):
        if cp.confpars.treeWindowIsOpen :
            print('HDF5 tree GUI is already open, use it...')
            #self.butH5Tree.setText('Open HDF5 tree')
            #cp.confpars.guitree.close()
        else :
            print('Open HDF5 tree GUI')
            #self.butH5Tree.setText('Close HDF5 tree')
            cp.confpars.guitree = guiselitems.GUISelectItems(self)
            cp.confpars.guitree.move(self.pos().__add__(QtCore.QPoint(500,-300))) # (-50,-100)open window with offset w.r.t. parent
            cp.confpars.guitree.show()

#-----------------------------
#  In case someone decides to run this module
#
if __name__ == "__main__" :
    app = QtWidgets.QApplication(sys.argv)
    ex  = GUIWhatToDisplayAlternative()
    ex.show()
    app.exec_()
#-----------------------------

