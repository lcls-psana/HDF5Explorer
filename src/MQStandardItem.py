#------------------------------
# File and Version Information:
#  $Id$
#
# Description:
#------------------------------
"""Module MQStandardItem reimplement QtGui.QStandardItem for sort()

This software was developed for the SIT project.
If you use all or part of it, please give an appropriate acknowledgment.

@see project modules
    * :py:class:`HDF5Explorer.HDF5TreeViewModel`
    * :py:class:`HDF5Explorer.GUISelectItems`

@version $Id$
@author Mikhail S. Dubrovin
"""
#------------------------------
__version__ = "$Revision$"

from PyQt4.QtGui import QStandardItem

#------------------------------

class MQStandardItem(QStandardItem) :

    def __init__(self, grpname) : # QStandardItem or QString text
        print 'XXX MQStandardItem'
        QStandardItem.__init__(self, grpname)


    def __lt__(self, other) : # QStandardItem other
        sd = self .accessibleDescription()
        od = other.accessibleDescription()
        #print 'XXX __lt__: self, other:', sd, od, sd[0]=='G', od[0]=='D'
        if sd[0]=='G' and od[0]=='D' : return False
        else : return True
        #return QStandardItem.__lt__(self, other)


#    def __ge__(self, other) : # QStandardItem other
#        sd = self .accessibleDescription()
#        od = other.accessibleDescription()
#        print 'XXX __ge__: self, other:', sd, od
#        if sd[0]=='G' and od[0]=='D' : return True
#        return QStandardItem.__ge__(self, other)


#    def __cmp__(self, other) : # QStandardItem other
#        sd = self .accessibleDescription()
#        od = other.accessibleDescription()
#        print 'XXX __cmp__: self, other:', sd, od
#        return QStandardItem.__cmp__(other)

#        if   isinstance(self, h5py.Group) and isinstance(other, h5py.Dataset) : return  1
#        elif isinstance(self, h5py.Dataset) and isinstance(other, h5py.Group) : return -1
#        else : return QStandardItem.__cmp__(other)

#------------------------------
