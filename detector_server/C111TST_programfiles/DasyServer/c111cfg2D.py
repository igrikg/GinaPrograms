from qt import *
import sys, os, string
import ConfigParser
import c111
from c111globals2D import C111Globals2D
#from ConfigC111 import ConfigC111Dialog

TRUE = 1
YES = 1
NO = 0
FALSE = 0
DBG = 0
#DBG = 1

class C111Cfg2D:
    def __init__(self,name=None , fl=0):
        self.globs = C111Globals2D()
        self.file_header = """
########################################################
# Example of config file for C111Gui application
########################################################
#
#      [RunSettings]
#      Device: string with os path to device
#      Roi: string, YES always
#      StartColumn: int from 0 to 1000/4095 (GFD/MHIT)
#      EndColumn: int as previous
#      StartRow: int from 0 to 1000/4095 (GFD/MHIT)
#      EndRow: int as previous
#      EnableFiniteTime: string, YES/NO
#      FiniteTimeLength: int (sec)
#      DisplayUpdateInterval: int (sec)
#      Binning: string: YES/NO
#
########################################################
#
#      [TdcSettings]
#      Timeout: int, nanosec from 0 to ....
#      OperationMode: string, GFD always
#      OperationType: string, NORMAL/TEST
#      SkipBit: string, NO always
#      ExternalInhibit: string, YES/NO
#      PileUpX: string, YES always
#      PileUpY: string, YES always
#      OffsetX: int, nanosec from 0 to ...
#      OffsetY: int, nanosec from 0 to ...
#      Resolution: string, QUART/HALF/FULL
#      PanelMonitor: string, GATE always
#      MuxSelection: string, NONE/MASK4/COUNTERS
#      InterruptTimer: string, YES/NO
#      StatsTimerLength: int, sec from 0 to ....
#      AcquisitionBank: int, 0
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
                self.cfg.set("TdcSettings", "SkipBit","NO" )
            if( not self.cfg.has_option('TdcSettings','ExternalInhibit') ):
                self.cfg.set("TdcSettings", "ExternalInhibit", "NO" )   
            if( not self.cfg.has_option('TdcSettings','PileUpX')):
                self.cfg.set("TdcSettings", "PileUpX", "YES" )
            if( not self.cfg.has_option('TdcSettings','PileUpY')):
                self.cfg.set("TdcSettings", "PileUpY", "YES" )
            if( not self.cfg.has_option('TdcSettings','OffsetX')):
                self.cfg.set("TdcSettings", "OffsetX", 0 )
            if( not self.cfg.has_option('TdcSettings','OffsetY')):
                self.cfg.set("TdcSettings", "OffsetY", 0 )
            if( not self.cfg.has_option('TdcSettings','Resolution')):
                self.cfg.set("TdcSettings", "Resolution", "QUART" )
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
            print "Filename: " , filename
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
        if( not self.cfg.has_option("RunSettings","EnableFiniteTime") ):
            self.cfg.set("RunSettings","EnableFiniteTime", "NO" )
        if( not self.cfg.has_option("RunSettings","FiniteTimeLength") ):
            self.cfg.set("RunSettings","FiniteTimeLength", 0 )
        if( not self.cfg.has_option("RunSettings","DisplayUpdateInterval") ):
            self.cfg.set("RunSettings","DisplayUpdateInterval", 0 )
        if( not self.cfg.has_option("RunSettings","Binning") ):
            self.cfg.set("RunSettings","Binning", "NO" )
                
        self.cfg.set("TdcSettings", "Timeout", config[self.globs.IDX_TIMEOUT] )
        self.cfg.set("TdcSettings", "OperationMode", "GFD" ) 
        
        if( config[self.globs.IDX_OPERATION_TYPE] == 1):
            self.cfg.set("TdcSettings", "OperationType", "TEST" )
        else:
            self.cfg.set("TdcSettings", "OperationType", "NORMAL" ) 
        self.cfg.set("TdcSettings", "SkipBit", "NO" )    
        if( config[self.globs.IDX_EXT_INHIBIT] == 1):
            self.cfg.set("TdcSettings", "ExternalInhibit", "YES" )
        else:
            self.cfg.set("TdcSettings", "ExternalInhibit", "NO" )   
            
        self.cfg.set("TdcSettings", "PileUpX", "YES" )
        self.cfg.set("TdcSettings", "PileUpY", "YES" )
        
        self.cfg.set("TdcSettings", "OffsetX", config[self.globs.IDX_OFFSETX] )
        self.cfg.set("TdcSettings", "OffsetY", config[self.globs.IDX_OFFSETY] )
        
        if( config[self.globs.IDX_RESOLUTION] == 0):
            self.cfg.set("TdcSettings", "Resolution", "FULL" )
        elif( config[self.globs.IDX_RESOLUTION] == 1):
            self.cfg.set("TdcSettings", "Resolution", "HALF" )
        elif( config[self.globs.IDX_RESOLUTION] == 4):
            self.cfg.set("TdcSettings", "Resolution", "QUART" )

        self.cfg.set("TdcSettings", "PannelMonitor", "GATE" )
        self.cfg.set("TdcSettings", "MuxSelection", "NONE")
            
        if( config[self.globs.IDX_INTERRUPT_TIMER] == 1):
            self.cfg.set("TdcSettings", "InterruptTimer", "YES" )
            self.cfg.set("TdcSettings", "StatsTimerLength", config[self.globs.IDX_STATS_TIMER_LENGTH] )
        else:
            self.cfg.set("TdcSettings", "InterruptTimer", "NO" )
            self.cfg.set("TdcSettings", "StatsTimerLength", 0 )
            
        self.cfg.set("TdcSettings", "AcquisitionBank", 0 )
        #self.state = self.globs.CFG_MODIFIED
        
    def FromRunSettings(self, runset):
        self.cfg_from = self.globs.FROMINTERNAL
        if( not self.cfg.has_section("RunSettings") ):
            self.cfg.add_section("RunSettings")
        self.cfg.set( "RunSettings","Device", runset[self.globs.IDX_DEVICE] )
        self.cfg.set("RunSettings","Roi", "YES" )
        self.cfg.set("RunSettings","StartColumn", runset[self.globs.IDX_START_COL] )
        self.cfg.set("RunSettings","EndColumn", runset[self.globs.IDX_END_COL] )
        self.cfg.set("RunSettings","StartRow", runset[self.globs.IDX_START_ROW] )
        self.cfg.set("RunSettings","EndRow", runset[self.globs.IDX_END_ROW] )
        if( runset[self.globs.IDX_ENABLE_FINITE_TIME] == 0 ):
            self.cfg.set("RunSettings","EnableFiniteTime", "NO" )
            self.cfg.set("RunSettings","FiniteTimeLength", 0  )
        else:
            self.cfg.set("RunSettings","EnableFiniteTime", "YES" )
            self.cfg.set("RunSettings","FiniteTimeLength", runset[self.globs.IDX_FINITE_TIME_LENGTH]  )
            
        self.cfg.set("RunSettings","DisplayUpdateInterval", 
                        runset[self.globs.IDX_DISPLAY_UPDATE_INTERVAL] )
        if( runset[self.globs.IDX_BINNING] == 1):
            self.cfg.set("RunSettings","Binning", "YES" )
        else:
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
                self.cfg.set("TdcSettings", "SkipBit","NO" )
        if( not self.cfg.has_option('TdcSettings','ExternalInhibit') ):
            self.cfg.set("TdcSettings", "ExternalInhibit", "NO" )   
        if( not self.cfg.has_option('TdcSettings','PileUpX')):
            self.cfg.set("TdcSettings", "PileUpX", "YES" )
        if( not self.cfg.has_option('TdcSettings','PileUpY')):
            self.cfg.set("TdcSettings", "PileUpY", "YES" )
        if( not self.cfg.has_option('TdcSettings','OffsetX')):
            self.cfg.set("TdcSettings", "OffsetX", 0 )
        if( not self.cfg.has_option('TdcSettings','OffsetY')):
            self.cfg.set("TdcSettings", "OffsetY", 0 )
        if( not self.cfg.has_option('TdcSettings','Resolution')):
            self.cfg.set("TdcSettings", "Resolution", "QUART" )
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
        print "c111Cfg.PrintCfg: Path: ", self.GetCfgDirPath() , "\n"
        for section in self.cfg.sections():
            print "Section: ", section
            for opt in self.cfg.items( section ):
                print "Option: ", opt       
        
    def SaveToFile(self, filename=None):
        if( filename == None or filename == "" ):
            filename = self.filename
        if( filename == None or filename == "" ):
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
        if( om == "GFD" ):
            return(0)
        else:
            return(1)
        
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
        config[self.globs.IDX_OPERATION_MODE] = self.globs.GFD ;
        ot = self.cfg.get("TdcSettings", "OperationType")
        if( ot == "TEST" ): config[self.globs.IDX_OPERATION_TYPE] = 1 ;
        else: config[self.globs.IDX_OPERATION_TYPE] = 0 ;
        config[self.globs.IDX_SKIP] = 0 ;
        ei = self.cfg.get("TdcSettings", "ExternalInhibit")
        if( ei == "YES" ): config[self.globs.IDX_EXT_INHIBIT] = 1 ;
        else: config[self.globs.IDX_EXT_INHIBIT] = 0 ;
        config[self.globs.IDX_PILEUPX] = 1 ;
        config[self.globs.IDX_PILEUPY] = 1 ;
        config[self.globs.IDX_OFFSETX] = self.cfg.getint("TdcSettings", "OffsetX") ;
        config[self.globs.IDX_OFFSETY] = self.cfg.getint("TdcSettings", "OffsetY") ;
        fr = self.cfg.get("TdcSettings", "Resolution")
        if( fr == "FULL" ): config[self.globs.IDX_RESOLUTION] = 0 ;
        elif( fr == "HALF" ): config[self.globs.IDX_RESOLUTION] = 1 ;
        else: config[self.globs.IDX_RESOLUTION] = 4 ;
        pm = self.cfg.get("TdcSettings", "PannelMonitor")
        config[self.globs.IDX_MONITOR] = 0 ;
        it = self.cfg.get("TdcSettings", "InterruptTimer")
        if( it == "YES" ): 
            config[self.globs.IDX_INTERRUPT_TIMER] = 1 ;
            config[self.globs.IDX_STATS_TIMER_LENGTH] = self.cfg.getint("TdcSettings", "StatsTimerLength")
        else: 
            config[self.globs.IDX_INTERRUPT_TIMER] = 0 ;
            config[self.globs.IDX_STATS_TIMER_LENGTH] = 0
        config[self.globs.IDX_ACQU_BANK] = 0
        return config
        
    def ToRunSettings(self):
        runset = ["DEVICE", 0 , 0 , 0 , 0 , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        runset[self.globs.IDX_DEVICE] = self.cfg.get( "RunSettings","Device" )
        runset[self.globs.IDX_ROI] = 1
        runset[self.globs.IDX_START_COL] = self.cfg.getint("RunSettings","StartColumn" )
        runset[self.globs.IDX_END_COL] = self.cfg.getint("RunSettings","EndColumn" )
        runset[self.globs.IDX_START_ROW] = self.cfg.getint("RunSettings","StartRow" )
        runset[self.globs.IDX_END_ROW] = self.cfg.getint("RunSettings","EndRow" )
        
        ft = self.cfg.get("RunSettings","EnableFiniteTime" )
        if( ft == "YES" ):
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
        return p
            
    def GetStatTimerLength( self ):
        l = self.cfg.getint("TdcSettings", "StatsTimerLength")
        return( l )

            
        
        

        
        