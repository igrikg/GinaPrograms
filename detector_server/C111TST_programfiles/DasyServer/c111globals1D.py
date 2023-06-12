 
import sys,os
 
class C111Globals1D:
    def __init__(self):       
        
        self.GFD = 0 ;  self.MHIT = 1 ;
        self.GFD1D = 0 ; self.MHIP = 2 ;
        self.TEST = 1 ; self.NORMAL = 0 ;
        self.GATE = 0 ; self.CLEARERR = 1 ; self.ALUOVF = 2 ; self.ASIC = 3 ;
        self.COUNTERS = 0 ; self.MASK4 = 1 ;
        self.BANK_ZERO = 0 ; self.BANK_ONE = 1 ;
        self.GFD_MAX_TIMEOUT = 307 ;
        self.MHIT_MAX_TIMEOUT = 2450 ;
        self.GFD_FULL_MAX_VALUE = 16383 ;
        self.GFD_HALF_MAX_VALUE = 4095 ;
        self.GFD_QUART_MAX_VALUE = 2047 ;
        self.MHIT_FULL_MAX_VALUE = 16383 ;
        self.MHIT_HALF_MAX_VALUE = 4095 ;
        #self.MHIT_FULL_MAX_VALUE = 4095 ;
        self.FROMINTERNAL = 1 ; self.FROMFILE = 2; self.FROMNONE = 0 ;
        
        self.IDX_TIMEOUT = 0 ; self.IDX_OPERATION_MODE = 1;
        self.IDX_OPERATION_TYPE = 2 ; self.IDX_SKIP = 3 ;
        self.IDX_EXT_INHIBIT = 4 ;
        self.IDX_PILEUPX = 5 ; self.IDX_PILEUPY = 6 ; 
        self.IDX_OFFSETX = 7 ; self.IDX_OFFSETY = 8 ;
        self.IDX_RESOLUTION = 9 ; self.IDX_MONITOR = 10 ;
        self.IDX_MUX_SELECTION = 11 ; self.IDX_INTERRUPT_TIMER = 12 ;
        self.IDX_STATS_TIMER_LENGTH = 13 ; self.IDX_ACQU_BANK =14 ;
        
        self.IDX_DEVICE = 0 ; self.IDX_ROI = 1 ; self.IDX_START_COL = 2;
        self.IDX_END_COL = 3 ; self.IDX_START_ROW = 4 ; self.IDX_END_ROW = 5 ;
        self.IDX_CHANNELS_NUMBER = 6 ; self.IDX_FIRST_CHAN = 7 ;
        self.IDX_SECOND_CHAN = 8 ; self.IDX_THIRD_CHAN = 9 ; self.IDX_FOURTH_CHAN = 10 ;
        self.IDX_ENABLE_FINITE_TIME = 11 ; self.IDX_FINITE_TIME_LENGTH = 12 ;
        self.IDX_DISPLAY_UPDATE_INTERVAL = 13 ;
        self.IDX_BINNING = 14 ;
    
        self.BAD_CONFIG_CHOICE = -1 ; self.CONFIG_CHECK_OK = 0 ;
        self.CFG_CREATED = 1 ; self.CFG_MODIFIED = 2 ;
        self.CFG_SAVED = 3 ; self.CFG_DOWNLOADED = 4 ;
        self.CFG_SAVED_DOWNLOADED = 5 ;
        self.CFG_DOWNLOADED_SAVED = 6 ;
        
        self.DASY_NETWORK_PORT = 12111 ;
        self.CFG_SERVER_FILE1D = "DasyServer1D.cfg"
        self.CFG_SERVER_FILE2D = "DasyServer2D.cfg"
        
        if( sys.platform == "win32"):
            self.CFG_PATH_MAIN = "C:\Program Files\C111TST\C111GUI\\"
            self.CFG_PATH_USER = "C:\\Documents and Settings\\All Users\\C111GUI\\"
            self.CFG_DIR_GFD1D = "GFD1D\\"
            self.CFG_DIR_GFD2D = "GFD2D\\"
            self.CFG_DIR_MHIT = "MHIT\\"
            self.CFG_DIR_MHIP = "MHIP\\"
            self.CFG_PATH_SERVER = "SERVER\\"
            self.CFG_PATH_PROG = "C:\\Program Files\\C111TST\\"
            self.CFG_PATH_PROG_SERVER = "DasyServer\\"
        else:
            self.CFG_PATH_MAIN = "/usr/local/ESRF/C111GUI/"
            self.CFG_PATH_USER = "$HOME/"
            self.CFG_DIR_GFD1D = "GFD1D/"
            self.CFG_DIR_GFD2D = "GFD2D/"
            self.CFG_DIR_MHIT = "MHIT/"
            self.CFG_DIR_MHIP = "MHIP/"
            self.CFG_PATH_SERVER = "SERVER/"
            self.CFG_PATH_PROG = "/usr/local/ESRF/"
            self.CFG_PATH_PROG_SERVER = "DasyServer/"
            
        
"""
        if( sys.platform == "win32"):
            self.CFG_PATH_MAIN = "C:\Program Files\C111TST\C111GUI\\"
            self.CFG_PATH_GFD1D = self.CFG_PATH_MAIN + "GFD1D\\"
            self.CFG_PATH_GFD2D = self.CFG_PATH_MAIN + "GFD2D\\"
            self.CFG_PATH_MHIT = self.CFG_PATH_MAIN + "MHIT\\"
            self.CFG_PATH_MHIP = self.CFG_PATH_MAIN + "MHIP\\"
        else:
            self.CFG_PATH_MAIN = "/usr/local/ESRF/C111GUI/"
            self.CFG_PATH_GFD1D = self.CFG_PATH_MAIN + "GFD1D/"
            self.CFG_PATH_GFD2D = self.CFG_PATH_MAIN + "GFD2D/"
            self.CFG_PATH_MHIT = self.CFG_PATH_MAIN + "MHIT/"
            self.CFG_PATH_MHIP = self.CFG_PATH_MAIN + "MHIP/"
            
"""
        