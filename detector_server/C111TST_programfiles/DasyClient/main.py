########################################################
#							#
# Definition of the function which one execute the code #
#							#
#########################################################
import sys, os, string, array
import gc
from qt import *
from DasyClientGuiimpl import DasyClientMainWindowImpl

#############################################################
#
#############################################################

def main(args): 

    a = QApplication( sys.argv )      
    y = DasyClientMainWindowImpl()
    a.setMainWidget( y )
    y.show()
    a.exec_loop()

if __name__=="__main__":
    main(sys.argv)