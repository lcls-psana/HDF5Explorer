#--------------------------------------------------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#  Module ImageWithGUI...
#
#------------------------------------------------------------------------

"""Plots for any 'image' record in the EventeDisplay project.

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
import os
import random

import numpy as np

import matplotlib
#matplotlib.use('GTKAgg') # forse Agg rendering to a GTK canvas (backend)
#matplotlib.use('Qt4Agg') # forse Agg rendering to a Qt4 canvas (backend)
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

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

class MyNavigationToolbar ( NavigationToolbar ) :
    """ Need to re-emplement a few methods in order to get control on toolbar button click"""

    #def __init__(self, canvas):
        #print 'MyNavigationToolbar.__init__'
        #self.canvas = canvas
        #self.coordinates = True
        ##QtGui.QToolBar.__init__( self, parent )
        #NavigationToolbar2.__init__( self, canvas, None )
        #self = canvas.toolbar


    def home(self, *args) :
        print('Home is clicked')
        fig = self.canvas.figure
        fig.myXmin = None
        fig.myXmax = None
        fig.myYmin = None
        fig.myYmax = None
        NavigationToolbar.home(self)

    def zoom(self, *args) :
        print('Zoom is clicked')
        NavigationToolbar.zoom(self)
        #self.canvas.draw()
        #fig  = self.canvas.figure
        #axes = fig.gca() 
        #bounds = axes.viewLim.bounds
        #fig.myXmin = bounds[0]
        #fig.myXmax = bounds[0] + bounds[2] 
        #fig.myYmin = bounds[1] + bounds[3]
        #fig.myYmax = bounds[1]
        #fig.myZoomIsOn = True
        #print 'zoom: Xmin, Xmax, Ymin, Ymax =', fig.myXmin, fig.myXmax, fig.myYmin, fig.myYmax




    #def back(self, *args) :
    #    print 'Back is clicked'
    #    NavigationToolbar.back(self)

    #def forward(self, *args):
    #    print 'Forward is clicked'
    #    NavigationToolbar.forward(self)

    #def pan(self,*args):
    #    print 'Pan is clicked'
    #    NavigationToolbar.pan(self)

    #def save_figure(self, *args):
    #    print 'Save is clicked'
    #    NavigationToolbar.save_figure(self)

#---------------------


class ImageWithGUI (QtWidgets.QMainWindow) :
#class ImageWithGUI (QtGui.QWidget) :
    """Plots for any 'image' record in the EventeDisplay project."""

    #----------------
    #  Constructor --
    #----------------

    def __init__(self, parent=None, fig=None, arr=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setWindowTitle('PyQt GUI with matplotlib')

        self.styleSheetGrey  = "background-color: rgb(100, 100, 100); color: rgb(0, 0, 0)"
        self.styleSheetWhite = "background-color: rgb(230, 230, 230); color: rgb(0, 0, 0)"

        self.arr = arr        
        self.fig = fig

        self.fig.myXmin = None
        self.fig.myXmax = None
        self.fig.myYmin = None
        self.fig.myYmax = None
        self.fig.myZmin = None
        self.fig.myZmax = None
        self.fig.myNBins = 100

        self.create_main_frame()
        self.create_status_bar()

        #self.on_draw()

    #-------------------
    #  Public methods --
    #-------------------

    def set_image_array(self,arr):

        self.arr = arr
        self.on_draw(self.fig.myXmin, self.fig.myXmax, self.fig.myYmin, self.fig.myYmax, self.fig.myZmin, self.fig.myZmax)



    def on_draw(self, xmin=None, xmax=None, ymin=None, ymax=None, zmin=None, zmax=None):
        """Redraws the figure"""

        if xmin == None or xmax == None or ymin == None or ymax == None :
            self.arrwin  = self.arr
            self.range   = None # original image range in pixels
        else :
            xmin = int(xmin)
            xmax = int(xmax)
            ymin = int(ymin)
            ymax = int(ymax)

            print('xmin, xmax, ymin, ymax =', xmin, xmax, ymin, ymax)
            self.arrwin =  self.arr[ymin:ymax,xmin:xmax]
            self.range  = [xmin, xmax, ymax, ymin]


        if self.cbox_log.isChecked() : self.arr2d = np.log(self.arrwin)
        else :                         self.arr2d =        self.arrwin

        self.fig.clear()        

        #self.axes1 = self.fig.add_subplot(211)
        gs = gridspec.GridSpec(4, 4)
        zmin = self.intOrNone(zmin)
        zmax = self.intOrNone(zmax)

        h1Range = (zmin,zmax)
        if zmin==None and zmax==None : h1Range = None

        print('h1Range = ', h1Range)

        #self.fig.myaxesH = self.fig.add_subplot(212)
        self.fig.myaxesH = self.fig.add_subplot(gs[3,:])
        self.fig.myaxesH.hist(self.arr.flatten(), bins=self.fig.myNBins, range=h1Range)#, range=(Amin, Amax)) 
        Nmin, Nmax = self.fig.myaxesH.get_ylim() 
        yticks = np.arange(Nmin, Nmax, int((Nmax-Nmin)/4))
        if len(yticks)<2 : yticks = [Nmin,Nmax]
        self.fig.myaxesH.set_yticks( yticks )

        zmin,zmax      = self.fig.myaxesH.get_xlim() 
        coltickslocs   = self.fig.myaxesH.get_xticks()
        #coltickslabels = self.fig.myaxesH.get_xticklabels()
        print('colticks =', coltickslocs)#, coltickslabels
 
        self.fig.myZmin, self.fig.myZmax = zmin, zmax
        self.setEditFieldValues()

        self.fig.myaxesI = self.fig.add_subplot(gs[0:3,:])
        self.fig.myaxesI.grid(self.cbox_grid.isChecked())
        self.fig.myaxesImage = self.fig.myaxesI.imshow(self.arr2d, origin='upper', interpolation='nearest', extent=self.range, aspect='auto')
        self.fig.myaxesImage.set_clim(zmin,zmax)
        self.fig.mycolbar = self.fig.colorbar(self.fig.myaxesImage, pad=0.1, fraction=0.15, shrink=1.0, aspect=15, orientation=1, ticks=coltickslocs) #orientation=1,
        #self.fig.mycolbar.set_clim(zmin,zmax)

        self.fig.canvas.mpl_connect('button_press_event',   self.processMouseButtonPress) 
        self.fig.canvas.mpl_connect('button_release_event', self.processMouseButtonRelease) 
        self.canvas.draw()


    def setEditFieldValues(self) :
        self.editXmin.setText( str(self.intOrNone(self.fig.myXmin)) )
        self.editXmax.setText( str(self.intOrNone(self.fig.myXmax)) )

        self.editYmin.setText( str(self.intOrNone(self.fig.myYmin)) )
        self.editYmax.setText( str(self.intOrNone(self.fig.myYmax)) ) 

        self.editZmin.setText( str(self.intOrNone(self.fig.myZmin)) )
        self.editZmax.setText( str(self.intOrNone(self.fig.myZmax)) )

        self.setEditFieldColors()


       
    def setEditFieldColors(self) :
        
        if self.cboxXIsOn.isChecked(): self.styleSheet = self.styleSheetWhite
        else                         : self.styleSheet = self.styleSheetGrey
        self.editXmin.setStyleSheet('Text-align:left;' + self.styleSheet)
        self.editXmax.setStyleSheet('Text-align:left;' + self.styleSheet)

        if self.cboxYIsOn.isChecked(): self.styleSheet = self.styleSheetWhite
        else                         : self.styleSheet = self.styleSheetGrey
        self.editYmin.setStyleSheet('Text-align:left;' + self.styleSheet)
        self.editYmax.setStyleSheet('Text-align:left;' + self.styleSheet)

        if self.cboxZIsOn.isChecked(): self.styleSheet = self.styleSheetWhite
        else                         : self.styleSheet = self.styleSheetGrey
        self.editZmin.setStyleSheet('Text-align:left;' + self.styleSheet)
        self.editZmax.setStyleSheet('Text-align:left;' + self.styleSheet)

        self.editXmin.setReadOnly( not self.cboxXIsOn.isChecked() )
        self.editXmax.setReadOnly( not self.cboxXIsOn.isChecked() )

        self.editYmin.setReadOnly( not self.cboxYIsOn.isChecked() )
        self.editYmax.setReadOnly( not self.cboxYIsOn.isChecked() )

        self.editZmin.setReadOnly( not self.cboxZIsOn.isChecked() )
        self.editZmax.setReadOnly( not self.cboxZIsOn.isChecked() )


    def processDraw(self) :
        #fig = event.canvas.figure
        fig = self.fig
        self.on_draw(fig.myXmin, fig.myXmax, fig.myYmin, fig.myYmax, fig.myZmin, fig.myZmax)



    def processMouseButtonPress(self, event) :
        print('MouseButtonPress')
        self.fig = event.canvas.figure

        if event.inaxes == self.fig.mycolbar.ax : self.mousePressOnColorBar (event)
        if event.inaxes == self.fig.myaxesI     : self.mousePressOnImage    (event)
        if event.inaxes == self.fig.myaxesH     : self.mousePressOnHistogram(event)


    def mousePressOnImage(self, event) :
        print('Image')


    def mousePressOnHistogram(self, event) :
        print('Histogram')
        lims = self.fig.myaxesH.get_xlim()
        self.setColorLimits(event, lims[0], lims[1], event.xdata)


    def mousePressOnColorBar(self, event) :
        print('Color bar')
        lims = self.fig.myaxesImage.get_clim()
        colmin = lims[0]
        colmax = lims[1]
        range = colmax - colmin
        value = colmin + event.xdata * range
        self.setColorLimits(event, colmin, colmax, value)



    def setColorLimits(self, event, colmin, colmax, value) :

        print(colmin, colmax, value)

        # left button
        if event.button is 1 :
            if value > colmin and value < colmax :
                colmin = value
                print("New mininum: ", colmin)

        # middle button
        elif event.button is 2 :
            #colmin, colmax = self.getImageAmpLimitsFromWindowParameters()
            print('Reset fig') # ,fig.number #, fig.nwin 
            colmin = None
            colmax = None

        # right button
        elif event.button is 3 :
            if value > colmin and value < colmax :
                colmax = value
                print("New maximum: ", colmax)

        self.fig.myZmin = colmin
        self.fig.myZmax = colmax

        self.processDraw()


    def processMouseButtonRelease(self, event) :

        fig         = event.canvas.figure # or plt.gcf()
        #figNum      = fig.number 
        self.fig    = fig
        axes        = event.inaxes # fig.gca() 
                
        if event.inaxes == fig.myaxesI and event.button == 1 : # Left button
            bounds = axes.viewLim.bounds
            fig.myXmin = bounds[0] 
            fig.myXmax = bounds[0] + bounds[2]  
            fig.myYmin = bounds[1] + bounds[3] 
            fig.myYmax = bounds[1] 
            fig.myZoomIsOn = True
            print(' Xmin, Xmax, Ymin, Ymax =', fig.myXmin, fig.myXmax, fig.myYmin, fig.myYmax)

            xlims = self.fig.myaxesI.get_xlim()
            print(' xlims=', xlims)


        if event.button == 2 : #or event.button == 3 : # middle or right button
            fig.myXmin = None
            fig.myXmax = None
            fig.myYmin = None
            fig.myYmax = None
            fig.myZmin = None
            fig.myZmax = None
            self.on_draw()

            #plt.draw() # redraw the current figure
            fig.myZoomIsOn = False

        self.setEditFieldValues()


    def processCBoxes(self):
        self.setEditFieldColors()


    def stringOrNone(self,value):
        if value == None : return 'None'
        else             : return str(value)


    def intOrNone(self,value):
        if value == None : return None
        else             : return int(value)


    def processEditXmin(self):
        self.fig.myXmin = self.editXmin.displayText()


    def processEditXmax(self):
        self.fig.myXmax = self.editXmax.displayText()


    def processEditYmin(self):
        self.fig.myYmin = self.editYmin.displayText()


    def processEditYmax(self):
        self.fig.myYmax = self.editYmax.displayText()


    def processEditZmin(self):
        self.fig.myZmin = self.editZmin.displayText()


    def processEditZmax(self):
        self.fig.myZmax = self.editZmax.displayText()




 
    def create_main_frame(self):
        self.main_frame = QtWidgets.QWidget()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
                
        # Other GUI controls
        #
        self.but_draw  = QtWidgets.QPushButton("&Draw")
        self.but_quit  = QtWidgets.QPushButton("&Quit")
        self.cbox_grid = QtWidgets.QCheckBox("Show &Grid")
        self.cbox_grid.setChecked(False)
        self.cbox_log  = QtWidgets.QCheckBox("&Log")
        self.cbox_log.setChecked(False)

        self.cboxXIsOn = QtWidgets.QCheckBox("X min, max:")
        self.cboxYIsOn = QtWidgets.QCheckBox("Y min, max:")
        self.cboxZIsOn = QtWidgets.QCheckBox("Z min, max:")

        self.editXmin  = QtWidgets.QLineEdit(self.stringOrNone(self.fig.myXmin))
        self.editXmax  = QtWidgets.QLineEdit(self.stringOrNone(self.fig.myXmax))
        self.editYmin  = QtWidgets.QLineEdit(self.stringOrNone(self.fig.myYmin))
        self.editYmax  = QtWidgets.QLineEdit(self.stringOrNone(self.fig.myYmax))
        self.editZmin  = QtWidgets.QLineEdit(self.stringOrNone(self.fig.myZmin))
        self.editZmax  = QtWidgets.QLineEdit(self.stringOrNone(self.fig.myZmax))

        width = 60
        self.editXmin.setMaximumWidth(width)
        self.editXmax.setMaximumWidth(width)
        self.editYmin.setMaximumWidth(width)
        self.editYmax.setMaximumWidth(width)
        self.editZmin.setMaximumWidth(width)
        self.editZmax.setMaximumWidth(width)

        self.editXmin.setValidator(QtGui.QIntValidator(0,100000,self))
        self.editXmax.setValidator(QtGui.QIntValidator(0,100000,self)) 
        self.editYmin.setValidator(QtGui.QIntValidator(0,100000,self))
        self.editYmax.setValidator(QtGui.QIntValidator(0,100000,self)) 
        self.editZmin.setValidator(QtGui.QIntValidator(-100000,100000,self))
        self.editZmax.setValidator(QtGui.QIntValidator(-100000,100000,self))
 
        self.but_draw.clicked.connect(self.processDraw)
        self.but_quit.clicked.connect(self.on_quit)
        self.cbox_grid.stateChanged[int].connect(self.processDraw)
        self.cbox_log.stateChanged[int].connect(self.processDraw)

        self.cboxXIsOn.stateChanged[int].connect(self.processCBoxes)
        self.cboxYIsOn.stateChanged[int].connect(self.processCBoxes)
        self.cboxZIsOn.stateChanged[int].connect(self.processCBoxes)

        self.editXmin.editingFinished .connect(self.processEditXmin)
        self.editXmax.editingFinished .connect(self.processEditXmax)
        self.editYmin.editingFinished .connect(self.processEditYmin)
        self.editYmax.editingFinished .connect(self.processEditYmax)
        self.editZmin.editingFinished .connect(self.processEditZmin)
        self.editZmax.editingFinished .connect(self.processEditZmax)

        # Create the navigation toolbar, tied to the canvas
        #
        #self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)
        self.mpl_toolbar = MyNavigationToolbar(self.canvas, self.main_frame)
        
        # Layout with box sizers
        # 
        hbox = QtWidgets.QHBoxLayout()
        hbox.addWidget(self.but_draw)
        hbox.addWidget(self.cbox_grid)
        hbox.addStretch(1)
        hbox.addWidget(self.but_quit)
        #hbox.setAlignment(w, QtCore.Qt.AlignVCenter)

        hboxX = QtWidgets.QHBoxLayout()
        hboxX.addWidget(self.cboxXIsOn)
        hboxX.addWidget(self.editXmin)
        hboxX.addWidget(self.editXmax)
        hboxX.addStretch(1)

        hboxY = QtWidgets.QHBoxLayout()
        hboxY.addWidget(self.cboxYIsOn)
        hboxY.addWidget(self.editYmin)
        hboxY.addWidget(self.editYmax)
        hboxY.addStretch(1)

        hboxZ = QtWidgets.QHBoxLayout()
        hboxZ.addWidget(self.cboxZIsOn)
        hboxZ.addWidget(self.editZmin)
        hboxZ.addWidget(self.editZmax)
        hboxZ.addWidget(self.cbox_log)
        hboxZ.addStretch(1)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addWidget(self.mpl_toolbar)
        
        vbox.addLayout(hboxX)
        vbox.addLayout(hboxY)
        vbox.addLayout(hboxZ)
        vbox.addLayout(hbox)

        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)

        self.setEditFieldColors()    
        self.setEditFieldValues()

    
    def create_status_bar(self):
        self.status_text = QtWidgets.QLabel("Status bar info is here")
        self.statusBar().addWidget(self.status_text, 1)



    def on_quit(self):
        print('Quit')
        self.close()
          
#-----------------------------

def main():

    app = QtWidgets.QApplication(sys.argv)

    fig = Figure((5.0, 10.0), dpi=100, facecolor='w',edgecolor='w',frameon=True)

    mu, sigma = 200, 25
    arr = mu + sigma*np.random.standard_normal(size=2400)
    #arr = np.arange(2400)
    arr.shape = (40,60)

    #ex  = ImageWithGUI(None, fig, arr)
    ex  = ImageWithGUI(None, fig)
    ex.set_image_array(arr)

    ex.show()
    app.exec_()
        
#-----------------------------
#  In case someone decides to run this module
#
if __name__ == "__main__" :
    main()

#-----------------------------
