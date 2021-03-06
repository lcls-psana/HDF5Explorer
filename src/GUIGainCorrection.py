#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module GUIGainCorrection...
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
from shutil import copy

from PyQt5 import QtCore, QtGui, QtWidgets
#import time   # for sleep(sec)

#-----------------------------
# Imports for other modules --
#-----------------------------

from . import ConfigParameters        as cp
from . import GlobalMethods           as gm
import numpy                   as np
from . import FastArrayTransformation as fat

#---------------------
#  Class definition --
#---------------------
class GUIGainCorrection ( QtWidgets.QWidget ) :
    """GUI works with gain correction parameters management"""

    #----------------
    #  Constructor --
    #----------------
    def __init__ ( self, parent=None ) :
        """Constructor"""

        QtWidgets.QWidget.__init__(self, parent)

        #self.parent = cp.confpars.guimain

        self.setGeometry(370, 350, 500, 150)
        self.setWindowTitle('Gain correction')

        self.frame = QtWidgets.QFrame(self)
        self.frame.setFrameStyle( QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken )
        self.frame.setLineWidth(0)
        self.frame.setMidLineWidth(1)
        self.frame.setGeometry(self.rect())

        aveFileName = cp.confpars. aveDirName + '/' + cp.confpars. aveFileName        

        self.titFile     = QtWidgets.QLabel('Gain correction file:')
        self.titMake     = QtWidgets.QLabel('the gain correction file from' + aveFileName)

        self.butBrowse   = QtWidgets.QPushButton("Browse")
        self.butMake     = QtWidgets.QPushButton("Make")

        self.cboxApply   = QtWidgets.QCheckBox('Apply gain correction',self)

        self.setCBState()

        #cp.confpars.confParsDirName  = os.getenv('HOME')
        path          = cp.confpars.gainDirName + '/' + cp.confpars.gainFileName
        self.fileEdit = QtWidgets.QLineEdit(path)
        
        self.showToolTips()

        grid = QtWidgets.QGridLayout()
        grid.addWidget(self.cboxApply,     0, 0, 1, 5)    
        grid.addWidget(self.titFile,       2, 0)    
        grid.addWidget(self.fileEdit,      3, 0, 1, 5)    
        grid.addWidget(self.butBrowse,     3, 5)    
        grid.addWidget(self.butMake,       4, 0)
        grid.addWidget(self.titMake,       4, 1, 1, 5)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(grid)
        vbox.addStretch(1)
        self.setLayout(vbox)

        self.butBrowse.clicked.connect(self.processBrowse)
        self.butMake.clicked.connect(self.processMake)
        self.fileEdit.editingFinished .connect(self.processFileEdit)
        self.cboxApply.stateChanged[int].connect(self.processCBoxApply)

        cp.confpars.gainGUIIsOpen = True


    #-------------------
    #  Public methods --
    #-------------------

    def showToolTips(self):
        # Tips for buttons and fields:
        #self           .setToolTip('This GUI deals with the configuration parameters.')
        self.fileEdit  .setToolTip('Type the file path name here,\nor better use "Browse" button.')
        self.butBrowse .setToolTip('Select the file path name\n for gain correction.')
        self.butMake   .setToolTip('Make the gain correction file from the latest averaged image.')

    def setParent(self,parent) :
        self.parent = parent

    def closeEvent(self, event):
        #print 'closeEvent'
        cp.confpars.gainGUIIsOpen = False
        QtWidgets.QWidget.closeEvent(self, event)

            
    def processExit(self):
        #print 'Exit button'
        self.close()

    def resizeEvent(self, e):
        #print 'resizeEvent' 
        self.frame.setGeometry(self.rect())

    def refreshGUIWhatToDisplay(self):
        cp.confpars.guiwhat.processRefresh()

    def processCBoxApply(self, value):
        print('CBoxApply')
        if self.cboxApply.isChecked():
            cp.confpars.gainCorrectionIsOn = self.loadGainCorrectionArrayFromFile()
        else:
            cp.confpars.gainCorrectionIsOn = False
        self.setCBState()

    def setCBState(self):
        if cp.confpars.gainCorrectionIsOn : self.cboxApply.setCheckState(2)
        else :                              self.cboxApply.setCheckState(0)

    def processMake(self):
        src = cp.confpars. aveDirName + '/' + cp.confpars. aveFileName
        dst = cp.confpars.gainDirName + '/' + cp.confpars.gainFileName
        print('Make the file', dst, 'from', src)       
        self.makeGainCorrectionFile(src,dst);

    def processBrowse(self):
        print('Browse')
        self.path = str(self.fileEdit.displayText())
        self.dirName,self.fileName = os.path.split(self.path)
        print('dirName  : %s' % (self.dirName))
        print('fileName : %s' % (self.fileName))
        self.path = QtWidgets.QFileDialog.getOpenFileName(self,'Open file',self.dirName)[0]
        self.dirName,self.fileName = os.path.split(str(self.path))
        if self.dirName == '' or self.fileName == '' :
            print('Input dirName or fileName is empty... use default values')  
        else :
            self.fileEdit.setText(self.path)
            cp.confpars.gainDirName  = self.dirName
            cp.confpars.gainFileName = self.fileName

    def processFileEdit(self):
        print('FileEdit')
        self.path = str(self.fileEdit.displayText())
        cp.confpars.gainDirName,cp.confpars.gainFileName = os.path.split(self.path)
        print('Set dirName  : %s' % (cp.confpars.gainDirName))
        print('Set fileName : %s' % (cp.confpars.gainFileName))


    def makeGainCorrectionFile(self, src, dst):
        try:
            arr_ave       = gm.getNumpyArrayFromFile(fname=src, datatype=np.float32)
        except IOError :
            print('\n',60*'=',\
                  '\nERROR: Failed to load the file', cp.confpars.aveFileName,\
                  '\nCheck if the file',cp.confpars.aveFileName,'exists.',\
                  '\nIf it does not exist, it needs to be created.',\
                  '\nUse procedure "Average" for the dataset representing',\
                  '\nthe flat field illumination to create the file', cp.confpars.aveFileName,\
                  '\nThen, click on "Make" button again.',\
                  '\n',60*'=')
            return False

        arr_gain_corr = fat.getGainCorrectionArrayFromAverage(arr_ave)
        gm.saveNumpyArrayInFile(arr_gain_corr,  fname=dst , format='%f') # , format='%i')
        return True


    def loadGainCorrectionArrayFromFile(self):
        gcfname = cp.confpars.gainDirName + '/' + cp.confpars.gainFileName
        try :
            cp.confpars.arr_gain = gm.getNumpyArrayFromFile(fname=gcfname, datatype=np.float32)
            return True
        except IOError :
            print('\n',60*'=',\
                  '\nERROR: Failed to load the gain correction array...',\
                  '\nCheck if the file',gcfname,'exists.',\
                  '\nIf it does not exist, it needs to be created.',\
                  '\nUse procedure "Average" for the dataset representing',\
                  '\nthe flat field illumination to create the file', cp.confpars.aveFileName,\
                  '\nThen, click on "Make" button to create the file for gain correction.',\
                  '\n',60*'=')
            return False
 
#-----------------------------
#  In case someone decides to run this module
#
if __name__ == "__main__" :

    app = QtWidgets.QApplication(sys.argv)
    widget = GUIGainCorrection ()
    widget.show()
    app.exec_()

#-----------------------------
