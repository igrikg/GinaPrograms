from qt import *
import sys, os, string
import ConfigParser
import c111
from c111globals1D import C111Globals1D
#from ConfigC111 import ConfigC111Dialog

TRUE = 1
YES = 1
NO = 0
FALSE = 0
DBG = 0
#DBG = 1

class C111Cfg1D:
    def __init__(self,name=None , fl=0):
        self.globs = C111Globals1D()
        self.file_header = """
########################################################
# Example of config file for C111Gui application
########################################################
#
#      [RunSettings]
#      Device: string with os path to device
#      Roi: string, YES always ?
#      StartColumn: int from 0 to 1000/4095 (GFD/MHIT)
#      EndColumn: int as previous
#      StartRow: int --- UNUSED for 1D case
#      EndRow: int --- UNUSED for 1D case
#      ChannelsNumber: int from 1 to 4
#      FirstChannel: int , always 0
#      SecondChannel: int , always 1
#      ThirdChannel: int , always 2
#      FourthChannel: int , always 3
#      EnableFiniteTime: string, YES/NO
#      FiniteTimeLength: int (sec)
#      DisplayUpdateInterval: int (sec)
#      Binning: string: YES/NO
#
########################################################
#
#      [TdcSettings]
#      Timeout: int, nanosec from 0 to ....
#      OperationMode: string, GFD1D/MHIT/MHIP
#      OperationType: string, NORMAL/TEST
#      Skip bit: string YES/NO
#      ExternalInhibit: string, YES/NO
#      PileUpX: string, YES always
#      PileUpY: string, ALWAYS NO in 1D case
#      OffsetX: int, nanosec from 0 to ...
#      OffsetY: int, ALWAYS 0 in 1D case
#      Resolution: string, QUART/HALF/FULL
#      PanelMonitor: string, GATE always
#      MuxSelection: string, NONE always
#      InterruptTimer: string, YES/NO
#      StatsTimerLength: int, sec from 0 to ....
#      AcquisitionBank: int, 0/1
#
########################################################
"""

        self.name = name
        self.dir_path = ""
        self.cfg = ConfigParser.RawConfigParser() ;
        self.filename = ""
        self.c111 = c111.c111()
        self.c111Handle = None
        self.checkSections()
        self.state = self.globs.CFG_CREATED 
        
    def checkSections(self):
        if( not self.cfg.has_section("RunSettings") ):
            self.cfg.add_section("RunSettings")
            if( not self.cfg.has_option('RunSettings','Device') ):
                self.cfg.set( "RunSettings","Device", "PXI2::9::0")
            if( not self.cfg.has_option("RunSettings","Roi") ):
                self.cfg.set("RunSettings","Roi", "YES")
            if( not self.cfg.has_option("RunSettings","StartColumn") ):
                self.cfg.set("RunSettings","StartColumn", 0 )
            if( not self.cfg.has_option("RunSettings","EndColumn") ):
                self.cfg.set("RunSettings","EndColumn", 0 )
            if( not self.cfg.has_option("RunSettings","StartRow") ):
                self.cfg.set("RunSettings","StartRow", 0 )
            if( not self.cfg.has_option("RunSettings","EndRow") ):
                self.cfg.set("RunSettings","EndRow", 0 )
            if( not self.cfg.has_option("RunSettings","ChannelsNumber") ):
                self.cfg.set("RunSettings","ChannelsNumber", 1 )
            if( not self.cfg.has_option("RunSettings","FirstChannel") ):
                self.cfg.set("RunSettings","FirstChannel", 0 )
            if( not self.cfg.has_option("RunSettings","SecondChannel") ):
                self.cfg.set("RunSettings","SecondChannel", 0 )
            if( not self.cfg.has_option("RunSettings","ThirdChannel") ):
                self.cfg.set("RunSettings","ThirdChannel", 0 )
            if( not self.cfg.has_option("RunSettings","FourthChannel") ):
                self.cfg.set("RunSettings","FourthChannel", 0 )
            if( not self.cfg.has_option("RunSettings","EnableFiniteTime") ):
                self.cfg.set("RunSettings","EnableFiniteTime", "NO" )
            if( not self.cfg.has_option("RunSettings","FiniteTimeLength") ):
                self.cfg.set("RunSettings","FiniteTimeLength", 0 )
            if( not self.cfg.has_option("RunSettings","DisplayUpdateInterval") ):
                self.cfg.set("RunSettings","DisplayUpdateInterval", 0 )
            if( not self.cfg.has_option("RunSettings","Binning") ):
                self.cfg.set("RunSettings","Binning", "NO" )


        if( not self.cfg.has_section("TdcSettings")):
            self.cfg.add_section("TdcSettings")    
            if( not self.cfg.has_option('TdcSettings','Timeout') ):    
                self.cfg.set("TdcSettings", "Timeout", 0 )
            if( not self.cfg.has_option('TdcSettings','OperationMode') ):
                self.cfg.set("TdcSettings", "OperationMode", "GFD" )
            if( not self.cfg.has_option('TdcSettings','OperationType') ):
                self.cfg.set("TdcSettings", "OperationType", "NORMAL" )
            if( not self.cfg.has_option('TdcSettings','SkipBit') ):
                self.cfg.set("TdcSettings", "SkipBit", "NO" )    
            if( not self.cfg.has_option('TdcSettings','ExternalInhibit') ):
                self.cfg.set("TdcSettings", "ExternalInhibit", "NO" )   
            if( not self.cfg.has_option('TdcSettings','PileUpX')):
                self.cfg.set("TdcSettings", "PileUpX", "YES" )
            if( not self.cfg.has_option('TdcSettings','OffsetX')):
                self.cfg.set("TdcSettings", "OffsetX", 0 )
            if( not self.cfg.has_option('TdcSettings','PileUpY')):
                self.cfg.set("TdcSettings", "PileUpY", "NO" )
            if( not self.cfg.has_option('TdcSettings','OffsetY')):
                self.cfg.set("TdcSettings", "OffsetY", 0 )
            if( not self.cfg.has_option('TdcSettings','Resolution')):
                self.cfg.set("TdcSettings", "Resolution", "HALF" )
            if( not self.cfg.has_option('TdcSettings','PannelMonitor')):
                self.cfg.set("TdcSettings", "PannelMonitor", "GATE" )
            if( not self.cfg.has_option('TdcSettings','MuxSelection')):
                self.cfg.set("TdcSettings", "MuxSelection", "NONE")
            if( not self.cfg.has_option('TdcSettings','InterruptTimer')):
                self.cfg.set("TdcSettings", "InterruptTimer", "NO" )
            if( not self.cfg.has_option('TdcSettings','StatsTimerLength')):
                self.cfg.set("TdcSettings", "StatsTimerLength", 0 )
            if( not self.cfg.has_option('TdcSettings','AcquisitionBank')):   
                self.cfg.set("TdcSettings", "AcquisitionBank", 0 )
        
    def FromFile(self, filename):
        #print "FromFile: ", filename
        self.filename = filename
        d = string.split( str(self.filename), "/" )
        if( DBG == 1 ):
            print "c111Cfg.FromFile: pathList: ", d
        f = d[ len(d) -1 ]
            
        if( self.name == None ):
            self.name = f
        else:
            self.name = self.name + ": " + f
        self.cfg_from = self.globs.FROMFILE
        try:
            fp = open(filename)
        except:
            self.filename = ""
            if( DBG == 1 ):
                print "c111Cfg.FromFile: Bad fileName: ", filename
            return
        self.cfg.readfp( fp )
        fp.close()
        #print "Sections", self.cfg.has_section("RunSettings")
        if( not self.cfg.has_section('RunSettings') ):
            exc = "MissingSectionRunSettings"
            raise exc, "RunSettings section is missing !!!"
            return
        if( not self.cfg.has_section("TdcSettings") ):
            exc = "MissingSectionTdcSettings"
            raise exc, "TdcSettings section is missing !!!"
            return
        self.state = self.globs.CFG_MODIFIED
    
    def GetName(self):
        if( self.name ):
            return( self.name )
        else:
            return( "None")        

    def SetName(self, name):
        self.name = name
        return
        
    def FromTdcSettings(self, config):
        self.cfg_from = self.globs.FROMINTERNAL
        if( not self.cfg.has_section("RunSettings") ):
            self.cfg.add_section("RunSettings")
        if( not self.cfg.has_option('RunSettings','Device') ):
            self.cfg.set( "RunSettings","Device", "PXI2::9::0")
        if( not self.cfg.has_option("RunSettings","Roi") ):
            self.cfg.set("RunSettings","Roi", "YES")
        if( not self.cfg.has_option("RunSettings","StartColumn") ):
            self.cfg.set("RunSettings","StartColumn", 0 )
        if( not self.cfg.has_option("RunSettings","EndColumn") ):
            self.cfg.set("RunSettings","EndColumn", 0 )
        if( not self.cfg.has_option("RunSettings","StartRow") ):
            self.cfg.set("RunSettings","StartRow", 0 )
        if( not self.cfg.has_option("RunSettings","EndRow") ):
            self.cfg.set("RunSettings","EndRow", 0 )
        if( not self.cfg.has_option("RunSettings","ChannelsNumber") ):
            self.cfg.set("RunSettings","ChannelsNumber", 1 )
        if( not self.cfg.has_option("RunSettings","FirstChannel") ):
            self.cfg.set("RunSettings","FirstChannel", 0 )
        if( not self.cfg.has_option("RunSettings","SecondChannel") ):
            self.cfg.set("RunSettings","SecondChannel", 1 )
        if( not self.cfg.has_option("RunSettings","ThirdChannel") ):
            self.cfg.set("RunSettings","ThirdChannel", 2 )
        if( not self.cfg.has_option("RunSettings","FourthChannel") ):
            self.cfg.set("RunSettings","FourthChannel", 3 )
        if( not self.cfg.has_option("RunSettings","EnableFiniteTime") ):
            self.cfg.set("RunSettings","EnableFiniteTime", "NO" )
        if( not self.cfg.has_option("RunSettings","FiniteTimeLength") ):
            self.cfg.set("RunSettings","FiniteTimeLength", 0 )
        if( not self.cfg.has_option("RunSettings","DisplayUpdateInterval") ):
            self.cfg.set("RunSettings","DisplayUpdateInterval", 0 )
        if( not self.cfg.has_option("RunSettings","Binning") ):
            self.cfg.set("RunSettings","Binning", "NO" )
                
        self.cfg.set("TdcSettings", "Timeout", config[self.globs.IDX_TIMEOUT] )
        if( config[self.globs.IDX_OPERATION_MODE] == 1):
            self.cfg.set("TdcSettings", "OperationMode", "MHIT" )
            self.cfg.set("TdcSettings", "OffsetX", 0 )
            self.cfg.set("TdcSettings", "OffsetY", 0 ) # ALWAYS for 1D case
        elif( config[self.globs.IDX_OPERATION_MODE] == 2):
            self.cfg.set("TdcSettings", "OperationMode", "MHIP" )
            self.cfg.set("TdcSettings", "OffsetX", 0 )
            self.cfg.set("TdcSettings", "OffsetY", 0 ) # ALWAYS for 1D case
        else:
            self.cfg.set("TdcSettings", "OperationMode", "GFD1D" ) 
            self.cfg.set("TdcSettings", "OffsetX", config[self.globs.IDX_OFFSETX] )
            self.cfg.set("TdcSettings", "OffsetY", 0 ) # ALWAYS for 1D case
        
        if( config[self.globs.IDX_OPERATION_TYPE] == 1):
            self.cfg.set("TdcSettings", "OperationType", "TEST" )
        else:
            self.cfg.set("TdcSettings", "OperationType", "NORMAL" ) 
        
        if( config[self.globs.IDX_SKIP] == 1):
            self.cfg.set("TdcSettings", "SkipBit", "YES" )
        else:
            self.cfg.set("TdcSettings", "SkipBit", "NO" ) 
                
        if( config[self.globs.IDX_EXT_INHIBIT] == 1):
            self.cfg.set("TdcSettings", "ExternalInhibit", "YES" )
        else:
            self.cfg.set("TdcSettings", "ExternalInhibit", "NO" )   
            
        self.cfg.set("TdcSettings", "PileUpX", "YES" )
        self.cfg.set("TdcSettings", "PileUpY", "NO" )  # ALWAYS for 1D case
        
        if( config[self.globs.IDX_RESOLUTION] == 0):
            self.cfg.set("TdcSettings", "Resolution", "FULL" )
        elif( config[self.globs.IDX_RESOLUTION] == 1):
            self.cfg.set("TdcSettings", "Resolution", "HALF" )
        elif( config[self.globs.IDX_RESOLUTION] == 4):
            self.cfg.set("TdcSettings", "Resolution", "QUART" )
            
        if( config[self.globs.IDX_INTERRUPT_TIMER] == 1):
            self.cfg.set("TdcSettings", "InterruptTimer", "YES" )
            self.cfg.set("TdcSettings", "StatsTimerLength", config[self.globs.IDX_STATS_TIMER_LENGTH] )
        else:
            self.cfg.set("TdcSettings", "InterruptTimer", "NO" )
            self.cfg.set("TdcSettings", "StatsTimerLength", 0 )
            
        self.cfg.set("TdcSettings", "AcquisitionBank", config[self.globs.IDX_ACQU_BANK] )
        #self.state = self.globs.CFG_MODIFIED
        
    def FromRunSettings(self, runset):
        self.cfg_from = self.globs.FROMINTERNAL
        if( not self.cfg.has_section("RunSettings") ):
            self.cfg.add_section("RunSettings")
        self.cfg.set( "RunSettings","Device", runset[self.globs.IDX_DEVICE] )
        self.cfg.set("RunSettings","Roi", "YES" )
        self.cfg.set("RunSettings","StartColumn", runset[self.globs.IDX_START_COL] )
        self.cfg.set("RunSettings","EndColumn", runset[self.globs.IDX_END_COL] )
        self.cfg.set("RunSettings","StartRow", 0 )  # ALWAYS FOR 1D case
        self.cfg.set("RunSettings","EndRow", 0 )  # ALWAYS For 1D case
        self.cfg.set("RunSettings","ChannelsNumber", runset[self.globs.IDX_CHANNELS_NUMBER] )
        self.cfg.set("RunSettings","FirstChannel", 0 )
        self.cfg.set("RunSettings","SecondChannel", 1 )
        self.cfg.set("RunSettings","ThirdChannel", 2 )
        self.cfg.set("RunSettings","FourthChannel", 3 )
        if( runset[self.globs.IDX_ENABLE_FINITE_TIME] == 0 ):
            self.cfg.set("RunSettings","EnableFiniteTime", "NO" )
            self.cfg.set("RunSettings","FiniteTimeLength", 0  )
        else:
            self.cfg.set("RunSettings","EnableFiniteTime", "YES" )
            self.cfg.set("RunSettings","FiniteTimeLength", runset[self.globs.IDX_FINITE_TIME_LENGTH]  )
            
        self.cfg.set("RunSettings","DisplayUpdateInterval", runset[self.globs.IDX_DISPLAY_UPDATE_INTERVAL] )
        if( runset[self.globs.IDX_BINNING] == 1):
            self.cfg.set("RunSettings","Binning", "YES" )
        else:
            self.cfg.set("RunSettings","Binning", "NO" )
        
        if( not self.cfg.has_section("TdcSettings")):
            self.cfg.add_section("TdcSettings")    
        if( not self.cfg.has_option('TdcSettings','Timeout') ):    
            self.cfg.set("TdcSettings", "Timeout", 0 )
        if( not self.cfg.has_option('TdcSettings','OperationMode') ):
            self.cfg.set("TdcSettings", "OperationMode", "GFD1D" )
        if( not self.cfg.has_option('TdcSettings','OperationType') ):
            self.cfg.set("TdcSettings", "OperationType", "NORMAL" )
        if( not self.cfg.has_option('TdcSettings','SkipBit') ):
                self.cfg.set("TdcSettings", "SkipBit", "NO" )    
        if( not self.cfg.has_option('TdcSettings','ExternalInhibit') ):
            self.cfg.set("TdcSettings", "ExternalInhibit", "NO" )   
        if( not self.cfg.has_option('TdcSettings','PileUpX')):
            self.cfg.set("TdcSettings", "PileUpX", "YES" )
        if( not self.cfg.has_option('TdcSettings','PileUpY')):
            self.cfg.set("TdcSettings", "PileUpY", "NO" )  # ALWAYS FOR 1D case
        if( not self.cfg.has_option('TdcSettings','OffsetX')):
            self.cfg.set("TdcSettings", "OffsetX", 0 )
        if( not self.cfg.has_option('TdcSettings','OffsetY')):
            self.cfg.set("TdcSettings", "OffsetY", 0 )
        if( not self.cfg.has_option('TdcSettings','Resolution')):
            self.cfg.set("TdcSettings", "Resolution", "HALF" )
        if( not self.cfg.has_option('TdcSettings','PannelMonitor')):
            self.cfg.set("TdcSettings", "PannelMonitor", "GATE" )
        if( not self.cfg.has_option('TdcSettings','MuxSelection')):
            self.cfg.set("TdcSettings", "MuxSelection", "NONE")
        if( not self.cfg.has_option('TdcSettings','InterruptTimer')):
            self.cfg.set("TdcSettings", "InterruptTimer", "NO" )
        if( not self.cfg.has_option('TdcSettings','StatsTimerLength')):
            self.cfg.set("TdcSettings", "StatsTimerLength", 0 )
        if( not self.cfg.has_option('TdcSettings','AcquisitionBank')):   
            self.cfg.set("TdcSettings", "AcquisitionBank", 0 )
        #self.state = self.globs.CFG_MODIFIED
            
    def FromSettings( self , sett ):
        self.FromTdcSettings( sett['TdcSettings'] )
        self.FromRunSettings( sett['RunSettings'] )
        
    def PrintCfg(self):
        print "c111Cfg.PrintCfg: Configuration: ", self.GetName() , "\n"
        for section in self.cfg.sections():
            print "Section: ", section
            for opt in self.cfg.items( section ):
                print "Option: ", opt       
        
    def SaveToFile(self, filename=None):
        if( filename == None or filename ==  "" ):
            filename = self.filename
        if( filename == None or filename ==  "" ):
            filename = "DefaultFile_Windows.cfg"
        fp = open( filename , 'w' )
        fp.write( self.file_header )
        fp.write( "\n")
        self.cfg.write( fp )
        fp.close()
        if( self.state == self.globs.CFG_DOWNLOADED):
            self.state = self.globs.CFG_DOWNLOADED_SAVED
        elif( self.state == self.globs.CFG_SAVED_DOWNLOADED or
                self.state == self.globs.CFG_DOWNLOADED_SAVED):
            pass
        else:
            self.state = self.globs.CFG_SAVED
        
    def GetOperationMode(self):
        if( self.c111Handle is None ):
            return -1
        om = self.cfg.get("TdcSettings", "OperationMode")
        if( om == "GFD1D" ):
            return(0)
        elif( om == "MHIP"):
            return(2)
        elif( om == "MHIT"):
            return(1)
        else:
            return(-1)
        
    def GetRealOperationMode( self ):
        if( self.c111Handle is None ):
            return -1
        try:
            tdc = self.c111.getTdcConfig( self.c111Handle )
        except:
            pass
        om = tdc[self.globs.IDX_OPERATION_MODE] 
        return( om )

    def ToTdcSettings(self):
        config = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        config[self.globs.IDX_TIMEOUT] = self.cfg.getint("TdcSettings", "Timeout")
        om = self.cfg.get("TdcSettings", "OperationMode")
        if( om == "MHIT"): 
            config[self.globs.IDX_OPERATION_MODE] = 1 ;
        elif( om == "MHIP"):
            config[self.globs.IDX_OPERATION_MODE] = 2;
        else: 
            config[self.globs.IDX_OPERATION_MODE] = 0 ;
        ot = self.cfg.get("TdcSettings", "OperationType")
        if( ot == "TEST" ): config[self.globs.IDX_OPERATION_TYPE] = 1 ;
        else: config[self.globs.IDX_OPERATION_TYPE] = 0 ;
        sk = self.cfg.get("TdcSettings", "SkipBit")
        if( sk == "YES"): config[self.globs.IDX_SKIP] = 1 ;
        else: config[self.globs.IDX_SKIP] = 0 ;
        ei = self.cfg.get("TdcSettings", "ExternalInhibit")
        if( ei == "YES" ): config[self.globs.IDX_EXT_INHIBIT] = 1 ;
        else: config[self.globs.IDX_EXT_INHIBIT] = 0 ;
        config[self.globs.IDX_PILEUPX] = 1 ;
        config[self.globs.IDX_PILEUPY] = 0 ;
        config[self.globs.IDX_OFFSETX] = self.cfg.getint("TdcSettings", "OffsetX") ;
        if( om == "MHIT" or om == "MHIP" ):
            config[self.globs.IDX_OFFSETX] = 0
        config[self.globs.IDX_OFFSETY] = 0
        fr = self.cfg.get("TdcSettings", "Resolution")
        if( fr == "FULL" ): config[self.globs.IDX_RESOLUTION] = 0 ;
        elif( fr == "HALF" ): config[self.globs.IDX_RESOLUTION] = 1 ;
        else: config[self.globs.IDX_RESOLUTION] = 4 ;
        config[self.globs.IDX_MONITOR] = 0 ;
        it = self.cfg.get("TdcSettings", "InterruptTimer")
        if( it == "YES" ): 
            config[self.globs.IDX_INTERRUPT_TIMER] = 1 ;
            config[self.globs.IDX_STATS_TIMER_LENGTH] = self.cfg.getint("TdcSettings", "StatsTimerLength")
        else: 
            config[self.globs.IDX_INTERRUPT_TIMER] = 0 ;
            config[self.globs.IDX_STATS_TIMER_LENGTH] = 0
        config[self.globs.IDX_ACQU_BANK] = self.cfg.getint("TdcSettings", "AcquisitionBank")
        return config
        
    def ToRunSettings(self):
        runset = ["DEVICE", 0 , 0 , 0 , 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        runset[self.globs.IDX_DEVICE] = self.cfg.get( "RunSettings","Device" )
        runset[self.globs.IDX_ROI] = 1
        runset[self.globs.IDX_START_COL] = self.cfg.getint("RunSettings","StartColumn" )
        runset[self.globs.IDX_END_COL] = self.cfg.getint("RunSettings","EndColumn" )
        runset[self.globs.IDX_START_ROW] = 0
        runset[self.globs.IDX_END_ROW] = 0
        runset[self.globs.IDX_CHANNELS_NUMBER] = self.cfg.getint("RunSettings","ChannelsNumber" )
        runset[self.globs.IDX_FIRST_CHAN] = self.cfg.getint("RunSettings","FirstChannel" ) 
        runset[self.globs.IDX_SECOND_CHAN] = self.cfg.getint("RunSettings","SecondChannel" )
        runset[self.globs.IDX_THIRD_CHAN] = self.cfg.getint("RunSettings","ThirdChannel" )
        runset[self.globs.IDX_FOURTH_CHAN] = self.cfg.getint("RunSettings","FourthChannel" )
        
        f = self.cfg.get("RunSettings","EnableFiniteTime" )
        if( f == "YES" ):
            runset[self.globs.IDX_ENABLE_FINITE_TIME] = 1
            runset[self.globs.IDX_FINITE_TIME_LENGTH] = self.cfg.getint("RunSettings","FiniteTimeLength" )
        else:
            runset[self.globs.IDX_ENABLE_FINITE_TIME] = 0
            runset[self.globs.IDX_FINITE_TIME_LENGTH] = 0
            
        runset[self.globs.IDX_DISPLAY_UPDATE_INTERVAL] = self.cfg.getint("RunSettings",
                                                                                                    "DisplayUpdateInterval" )
        b = self.cfg.get("RunSettings","Binning" )
        if( b == "YES"):
            runset[self.globs.IDX_BINNING] = 1
        else:
            runset[self.globs.IDX_BINNING] = 0
        if( DBG == 1):
            print "c111Cfg.ToRunSettings: ", runset
            
        return runset
        
    def ToSettings( self ):
        sett = { 'TdcSettings':0 , 'RunSettings':0 }
        tdc = self.ToTdcSettings()
        run = self.ToRunSettings()
        sett['TdcSettings'] = tdc
        sett['RunSettings'] = run
        return sett
        
    def SetTdcHandle( self, tdc_handle ):
        self.c111Handle = tdc_handle
               
    def DownloadToTdc( self ):
        if( self.c111Handle is None ):
            return -1
        tdc = self.ToTdcSettings( )
        self.c111.setTdcConfig( self.c111Handle, tdc )
        if( self.state == self.globs.CFG_SAVED):
            self.state = self.globs.CFG_SAVED_DOWNLOADED
        elif( self.state == self.globs.CFG_SAVED_DOWNLOADED or
                self.state == self.globs.CFG_DOWNLOADED_SAVED):
            pass
        else:
            self.state = self.globs.CFG_DOWNLOADED

    def GetState(self):
        return( self.state );
        
    def GetFiniteTimeLength(self):
        tl = self.cfg.getint("RunSettings","FiniteTimeLength" )
        return(tl)
        
    def GetUpdateInterval( self ):
        ti = self.cfg.getint("RunSettings", "DisplayUpdateInterval" )
        return(ti)
        
    def SetCfgDirPath( self, dir_path ):
        self.dir_path = dir_path 
           
    def GetCfgDirPath( self ):
        if( self.c111Handle is None ):
            p = -1
        else:
            p = self.dir_path
        #print "CFG: ", str( self.dir_path) , "  :  " , str(p)
        return p
 
    def GetStatTimerLength( self ):
        l = self.cfg.getint("TdcSettings", "StatsTimerLength")
        return( l )
 
"""         
    def GetCfgDirPath( self ):
        if( self.c111Handle is None ):
            return -1
        tdc = self.ToTdcSettings( )
        print "GET PATH: OM : ", tdc[self.globs.IDX_OPERATION_MODE]
        if( tdc[self.globs.IDX_OPERATION_MODE] == self.globs.GFD):
            f = self.globs.CFG_PATH_GFD1D
        elif( tdc[self.globs.IDX_OPERATION_MODE] == self.globs.MHIT):
            f = self.globs.CFG_PATH_MHIT
        elif( tdc[self.globs.IDX_OPERATION_MODE] == self.globs.MHIP):
            f = self.globs.CFG_PATH_MHIP
        else:
            f = self.globs.CFG_PATH_MAIN
        return(f)
"""
            

            
        
        

        
        