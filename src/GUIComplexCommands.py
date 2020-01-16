
#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module GUIComplexCommands...
#
#------------------------------------------------------------------------

"""GUI which handles the Average, Correlations, and CalibCycles buttons in the HDF5Explorer package.

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
import os

from PyQt5 import QtCore, QtGui, QtWidgets
import time   # for sleep(sec)

#-----------------------------
# Imports for other modules --
#-----------------------------
from . import ConfigParameters as cp
from . import DrawEvent        as drev

#---------------------
#  Class definition --
#---------------------
class GUIComplexCommands ( QtWidgets.QWidget ) :
    """GUI which handles the Average, Correlations, and CalibCycles buttons

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
    def __init__ (self, parent=None, wplayer=None) :
        """Constructor"""

        self.wplayer = wplayer

        QtWidgets.QWidget.__init__(self, parent)

        self.setGeometry(370, 10, 500, 30)
        self.setWindowTitle('Average and Correlation')
        self.palette = QtGui.QPalette()
        self.resetColorIsSet = False

        self.frame = QtWidgets.QFrame(self)
        self.frame.setFrameStyle( QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken ) #Box, Panel | Sunken, Raised 
        self.frame.setLineWidth(0)
        self.frame.setMidLineWidth(1)
        self.frame.setGeometry(self.rect())
        #self.frame.setVisible(True)

        self.drawev   = drev.DrawEvent(self)

        #self.titComplex = QtGui.QLabel('Multi-events:')
        self.titOver    = QtWidgets.QLabel('over')
        self.titEvents  = QtWidgets.QLabel('ev.')

        self.avevEdit = QtWidgets.QLineEdit(str(cp.confpars.numEventsAverage))
        self.avevEdit.setMaximumWidth(45)
        self.avevEdit.setValidator(QtGui.QIntValidator(1,1000000,self))

        self.butAverage       = QtWidgets.QPushButton("Average")
        self.butCorr          = QtWidgets.QPushButton("Correlations")
        self.butCalibC        = QtWidgets.QPushButton("CalibCycles")
        self.butWaveVsEv      = QtWidgets.QPushButton("WF vs Ev")
        self.butWaveVsEvIncCC = QtWidgets.QPushButton("+1 CC")
        self.butWaveVsEvDecCC = QtWidgets.QPushButton("-1 CC")

        self.butWaveVsEvIncCC.setMaximumWidth(45)
        self.butWaveVsEvDecCC.setMaximumWidth(45)

        #self.butAverage      .setStyleSheet("background-color: rgb(0, 255, 0); color: rgb(0, 0, 0)")
        #self.butCorr         .setStyleSheet("background-color: magenta; color: rgb(0, 0, 0)")
        self.butAverage      .setStyleSheet("background-color: rgb(230, 255, 230); color: rgb(0, 0, 0)")
        self.butCorr         .setStyleSheet("background-color: rgb(255, 230, 255); color: rgb(0, 0, 0)")
        self.butCalibC       .setStyleSheet("background-color: rgb(255, 255, 220); color: rgb(0, 0, 0)")
        self.butWaveVsEv     .setStyleSheet("background-color: rgb(220, 255, 255); color: rgb(0, 0, 0)")
        self.butWaveVsEvIncCC.setStyleSheet("background-color: rgb(220, 255, 255); color: rgb(0, 0, 0)")
        self.butWaveVsEvDecCC.setStyleSheet("background-color: rgb(220, 255, 255); color: rgb(0, 0, 0)")
        
        #self.closeplts= QtGui.QPushButton("Close plots")
        #self.exit     = QtGui.QPushButton("Exit")
        
        hboxA = QtWidgets.QHBoxLayout()
        #hboxA.addWidget(self.titComplex)
        hboxA.addWidget(self.butAverage)
        hboxA.addWidget(self.titOver)
        hboxA.addWidget(self.avevEdit)
        hboxA.addWidget(self.titEvents)
        hboxA.addStretch(2)
        hboxA.addWidget(self.butCorr)
        hboxA.addWidget(self.butCalibC)

        hboxB = QtWidgets.QHBoxLayout()
        hboxB.addWidget(self.butWaveVsEvDecCC)
        hboxB.addWidget(self.butWaveVsEv)
        hboxB.addWidget(self.butWaveVsEvIncCC)
        hboxB.addStretch()

        vbox  = QtWidgets.QVBoxLayout()
        vbox.addLayout(hboxA)
        vbox.addLayout(hboxB)

        self.setLayout(vbox)

        self.butAverage.clicked.connect(self.processAverage)
        self.butCorr.clicked.connect(self.processCorrelations)
        self.butCalibC.clicked.connect(self.processCalibCycles)
        self.butWaveVsEv.clicked.connect(self.processWaveVsEv)
        self.butWaveVsEvIncCC.clicked.connect(self.processWaveVsEvIncCC)
        self.butWaveVsEvDecCC.clicked.connect(self.processWaveVsEvDecCC)
        self.avevEdit.editingFinished .connect(self.processAverageEventsEdit)

        #self.setFocus()
        #self.resize(500, 300)
        #print 'End of init'

    #-------------------
    # Private methods --
    #-------------------

    def resizeEvent(self, e):
        #print 'resizeEvent' 
        self.frame.setGeometry(self.rect())


    def closeEvent(self, event):
        #print 'closeEvent'
        self.drawev.quitDrawEvent()
        self.SHowIsOn = False
        QtWidgets.QWidget.closeEvent(self, event)


    def processQuit(self):
        #print 'Quit button is clicked'
        self.close() # this call closeEvent()


    def processCorrelations(self):
        print('Correlations')
        self.drawev.drawCorrelationPlots()


    def processCalibCycles(self):
        print('CalibCycles')
        self.drawev.drawCalibCyclePlots()


    def processWaveVsEv(self):
        print('WaveVsEv')
        self.drawev.drawWaveVsEventPlots()


    def processWaveVsEvIncCC(self):
        print('WaveVsEvIncCC')
        self.drawev.drawWaveVsEventPlots(1)


    def processWaveVsEvDecCC(self):
        print('WaveVsEvDecCC')
        self.drawev.drawWaveVsEventPlots(-1)


    def processAverage(self):
        print('Start Average')
        cp.confpars.eventCurrent     = int(self.wplayer.numbEdit.displayText())
        cp.confpars.numEventsAverage = int(self.avevEdit.displayText())
        self.drawev.averageOverEvents()        
        self.wplayer.numbEdit.setText(str(cp.confpars.eventCurrent))


    def processAverageEventsEdit(self):    
        print('AverageEventsEdit', end=' ')
        cp.confpars.numEventsAverage = int(self.avevEdit.displayText())
        print('Set numEventsAverage : ', cp.confpars.numEventsAverage)        


    def processClosePlots(self):
        #print 'Close plots',
        self.drawev.quitDrawEvent()

#-----------------------------
#  In case someone decides to run this module
#
if __name__ == "__main__" :
    app = QtWidgets.QApplication(sys.argv)
    ex  = GUIComplexCommands()
    ex.show()
    app.exec_()
#-----------------------------
