########################################################
#							#
# Definition of the function which one execute the code #
#							#
#########################################################

import sys, os, string, array
import getpass, os.path, shutil
import gc, time
from DasyRemoteServer import DasyRemoteServer
    
if( sys.platform == "win32"):
    from win32event import CreateMutex
    from win32api import GetLastError
    from winerror import ERROR_ALREADY_EXISTS

def req_exit(msg):
    print msg
    req = "" ;
    req = raw_input( "Strike a key to exit: " );
    exit(1)

    
#############################################################
#
#############################################################
def main(args): 
    dbg = False ;
    #dbg = True ;
    print  "################################################"
    print  "#     DASY REMOTE SERVER (V 1.0) STARTED !!!   #" ;
    print  "#         Ctrl+Break to close   #"
    print  "############################################"
    if( sys.platform == "win32"):
        handle = CreateMutex(None, 1, 'A unique mutex name')
        if GetLastError( ) == ERROR_ALREADY_EXISTS:
    # Take appropriate action, as this is the second
    # instance of this script; for example:
            req_exit("DasyServer Already running !!! Exiting !!!" ) ;
    
    ds = DasyRemoteServer() ;
    ds.run( dbg ) ;
    

if __name__=="__main__":
	main(sys.argv)