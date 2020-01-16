#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module GUIConfiguration...
#
#------------------------------------------------------------------------

"""GUI works with configuration parameters management"""
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
import os

from PyQt5 import QtCore, QtGui, QtWidgets
#import time   # for sleep(sec)

#-----------------------------
# Imports for other modules --
#-----------------------------

from . import ConfigParameters as cp

#---------------------
#  Class definition --
#---------------------
class GUIConfiguration ( QtWidgets.QWidget ) :
    """GUI works with configuration parameters management"""

    #----------------
    #  Constructor --
    #----------------
    def __init__ ( self, parent=None ) :
        """Constructor"""

        QtWidgets.QWidget.__init__(self, parent)

        self.parent = cp.confpars.guimain

        self.setGeometry(370, 350, 500, 150)
        self.setWindowTitle('Configuration')

        self.frame = QtWidgets.QFrame(self)
        self.frame.setFrameStyle( QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken )
        self.frame.setLineWidth(0)
        self.frame.setMidLineWidth(1)
        self.frame.setGeometry(self.rect())
        
        self.titFile     = QtWidgets.QLabel('File with configuration parameters:')
        self.titPars     = QtWidgets.QLabel('Operations on configuration parameters:')
        self.titRadio    = QtWidgets.QLabel('At program start:')

        self.butBrowse   = QtWidgets.QPushButton("Browse")
        self.butRead     = QtWidgets.QPushButton("Read")
        self.butWrite    = QtWidgets.QPushButton("Save")
        self.butDefault  = QtWidgets.QPushButton("Reset default")
        self.butPrint    = QtWidgets.QPushButton("Print current")
        #self.butExit     = QtGui.QPushButton("Quit")

        self.radioRead   = QtWidgets.QRadioButton("Read parameters from file")
        self.radioDefault= QtWidgets.QRadioButton("Set default")
        self.radioGroup  = QtWidgets.QButtonGroup()
        self.radioGroup.addButton(self.radioRead)
        self.radioGroup.addButton(self.radioDefault)
        if cp.confpars.readParsFromFileAtStart : self.radioRead.setChecked(True)
        else :                                   self.radioDefault.setChecked(True)

        #cp.confpars.confParsDirName  = os.getenv('HOME')
        path          = cp.confpars.confParsDirName + '/' + cp.confpars.confParsFileName
        self.fileEdit = QtWidgets.QLineEdit(path)
        
        self.showToolTips()

        hboxT1 = QtWidgets.QHBoxLayout()
        hboxT1.addWidget(self.titFile)

        hboxF = QtWidgets.QHBoxLayout()
        hboxF.addWidget(self.fileEdit)
        hboxF.addWidget(self.butBrowse)

        grid = QtWidgets.QGridLayout()
        grid.addWidget(self.titPars,       0, 0, 1, 3)
        grid.addWidget(self.butRead,       1, 0)
        grid.addWidget(self.butWrite,      1, 1)
        grid.addWidget(self.butDefault,    1, 2)
        grid.addWidget(self.butPrint,      1, 3)
        #grid.addWidget(self.titRadio,      2, 0)
        #grid.addWidget(self.radioRead,     2, 1, 1, 2)
        #grid.addWidget(self.radioDefault,  3, 1, 1, 2)
        #grid.addWidget(self.butExit,       4, 3)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addStretch(2)
        vbox.addLayout(hboxT1)
        vbox.addLayout(hboxF)
        vbox.addStretch(1)     
        vbox.addLayout(grid)

        self.setLayout(vbox)

        #self.connect(self.butExit,      QtCore.SIGNAL('clicked()'),          self.processExit         )
        self.butRead.clicked.connect(self.processRead)
        self.butWrite.clicked.connect(self.processWrite)
        self.butPrint.clicked.connect(self.processPrint)
        self.butDefault.clicked.connect(self.processDefault)
        self.butBrowse.clicked.connect(self.processBrowse)
        self.radioRead.clicked.connect(self.processRadioRead)
        self.radioDefault.clicked.connect(self.processRadioDefault)
        self.fileEdit.editingFinished .connect(self.processFileEdit)

        cp.confpars.configGUIIsOpen = True


    #-------------------
    #  Public methods --
    #-------------------

    def showToolTips(self):
        # Tips for buttons and fields:
        #self           .setToolTip('This GUI deals with the configuration parameters.')
        #self.butExit   .setToolTip('Quit this GUI and close the window.')
        self.fileEdit  .setToolTip('Type the file path name here,\nor better use "Browse" button.')
        self.butBrowse .setToolTip('Select the file path name\nto read/write the configuration parameters.')
        self.butRead   .setToolTip('Read the configuration parameters from file.')
        self.butWrite  .setToolTip('Save (write) the configuration parameters in file.')
        self.butDefault.setToolTip('Reset the configuration parameters\nto their default values.')
        self.butPrint  .setToolTip('Print current values of the configuration parameters.')
        self.radioRead .setToolTip('If this button is ON and configuration parameters are saved,\n' +
                                   'then they will be read from file at the next start of this program.')
        self.radioDefault.setToolTip('If this button is ON and configuration parameters are saved,\n' +
                                     'then they will be reset to the default values at the next start of this program.')

    def setParent(self,parent) :
        self.parent = parent

    def closeEvent(self, event):
        #print 'closeEvent'
        cp.confpars.configGUIIsOpen = False
        QtWidgets.QWidget.closeEvent(self, event)


    def processExit(self):
        #print 'Exit button'
        self.close()

    def resizeEvent(self, e):
        #print 'resizeEvent' 
        self.frame.setGeometry(self.rect())

    def refreshGUIWhatToDisplay(self):
        cp.confpars.guiwhat.processRefresh()
        
    def processRead(self):
        print('Read')
        cp.confpars.readParameters(self.confParsFileName())
        self.parent.fileEdit.setText(cp.confpars.dirName + '/' + cp.confpars.fileName)
        self.refreshGUIWhatToDisplay()

    def processWrite(self):
        print('Write')
        cp.confpars.writeParameters(self.confParsFileName())

    def processDefault(self):
        print('Set default values of configuration parameters')
        cp.confpars.setDefaultParameters()
        self.parent.fileEdit.setText(cp.confpars.dirName + '/' + cp.confpars.fileName)
        self.refreshGUIWhatToDisplay()

    def processPrint(self):
        print('Print')
        cp.confpars.Print()

    def processRadioRead(self):
        print('RadioRead')
        cp.confpars.readParsFromFileAtStart = True

    def processRadioDefault(self):
        print('RadioDefault')
        cp.confpars.readParsFromFileAtStart = False

    def processBrowse(self):
        print('Browse')
        self.path = str(self.fileEdit.displayText())
        self.dirName,self.fileName = os.path.split(self.path)
        print('dirName  : %s' % (self.dirName))
        print('fileName : %s' % (self.fileName))
        self.path = QtWidgets.QFileDialog.getOpenFileName(self,'Open file',self.dirName)[0]
        self.dirName,self.fileName = os.path.split(str(self.path))
        #self.path = cp.confpars.confParsDirName + '/' + cp.confpars.confParsFileName
        #self.path = self.dirName+'/'+self.fileName
        if self.dirName == '' or self.fileName == '' :
            print('Input dirName or fileName is empty... use default values')  
        else :
            self.fileEdit.setText(self.path)
            cp.confpars.confParsDirName  = self.dirName
            cp.confpars.confParsFileName = self.fileName

    def processFileEdit(self):
        print('FileEdit')
        self.path = str(self.fileEdit.displayText())
        cp.confpars.confParsDirName,cp.confpars.confParsFileName = os.path.split(self.path)
        print('Set dirName  : %s' % (cp.confpars.confParsDirName))
        print('Set fileName : %s' % (cp.confpars.confParsFileName))
 
    def confParsFileName(self):
        #One have to check that file exists...
        fname = str(self.fileEdit.displayText())
        return fname

#-----------------------------
#  In case someone decides to run this module
#
if __name__ == "__main__" :

    app = QtWidgets.QApplication(sys.argv)
    widget = GUIConfiguration ()
    widget.show()
    app.exec_()

#-----------------------------
