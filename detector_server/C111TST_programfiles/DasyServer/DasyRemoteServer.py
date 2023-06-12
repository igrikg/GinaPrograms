########################################################
#                           #
# Definition of the function which one execute the code #
#                           #
#########################################################

import sys, os, string, array
import getpass, os.path, shutil
import gc, time
import threading
import unicodedata
import socket
import select
import ftplib
import c111
import ConfigParser
from c111cfg1D import C111Cfg1D
from c111cfg2D import C111Cfg2D
from c111globals1D import C111Globals1D
from c111globals2D import C111Globals2D
from C111GUI_HeaderFile import *
from RunGlobals import RunGlobals
    
class DasyRemoteServer:
    def __init__(self,*args):

        #DASY_NETWORK_PORT = 12111 ;
        self.constg = C111Globals2D() ;
        self.constg1D = C111Globals1D() ;
        self.constg2D = C111Globals2D() ;
        self.varg = RunGlobals();
        
        self.DBG = False ;
        self.conn = "" ;
        self.sock = "" ;

    def req_exit(self,msg):
        print msg
        req = "" ;
        req = raw_input( "Strike a key to exit: " );
        exit(1)
    
    def get_cfg(self):
        
        self.varg.c111 = c111.c111()
        self.varg.list_devices = self.varg.c111.searchDev()
        exception_dev = 'Device search error'
        if (self.varg.list_devices[0] == -1):
            self.req_exit("Cannot find C/P111 device(s)  !!" ) ;
            
        bc = -1
        self.varg.FD = self.varg.c111.open(self.varg.list_devices[1])
        if( self.DBG == True):
            self.varg.c111.setLibDebug(1)
            self.varg.c111.setDriverDebug(self.varg.FD,4)
        else:
            self.varg.c111.setLibDebug(0)
            self.varg.c111.setDriverDebug(self.varg.FD,0)
        try:
            bc = self.varg.c111.getBootConfig(self.varg.FD)
        except:
            self.req_exit("Cannot access device !!" ) ;
        
        self.varg.cfg_path =  self.constg.CFG_PATH_MAIN  +  self.constg.CFG_PATH_SERVER  ;
        f2d = self.varg.cfg_path + self.constg.CFG_SERVER_FILE2D ;
        f1d = self.varg.cfg_path + self.constg.CFG_SERVER_FILE1D ;
        
        if( os.path.exists( f2d ) == True ):
            self.varg.CFG_TYPE = 2 ;
            self.varg.CurrentCfg = C111Cfg2D("Default settings" )
            self.varg.CurrentCfg.SetTdcHandle( self.varg.FD )
            self.varg.CurrentCfg.FromFile( f2d ) ;
            self.constg = self.constg2D ;
        elif( os.path.exists( f1d ) == True ):
            self.varg.CFG_TYPE = 1 ;
            self.varg.CurrentCfg = C111Cfg1D("Default settings" )
            self.varg.CurrentCfg.SetTdcHandle( self.varg.FD )
            self.varg.CurrentCfg.FromFile( f1d ) 
            self.constg = self.constg1D ;
        else:
            self.req_exit("No config file for Dasy server !!" ) ;
            
        if( self.DBG == True): 
            self.varg.CurrentCfg.PrintCfg()  
        real_opmode = self.varg.CurrentCfg.GetRealOperationMode() ;
        
        TDC_getstatus = self.varg.c111.getTdcStatus(self.varg.FD)
        if (TDC_getstatus['AcqState'] == 1):
            self.varg.START_TDC = 1 ;
            
        runset = self.varg.CurrentCfg.ToRunSettings()
        tdcset = self.varg.CurrentCfg.ToTdcSettings()
        if( self.varg.CurrentCfg.GetFiniteTimeLength() != 0 ):
                self.varg.finiteAcqTimeOn = 1
    
        if( self.varg.CFG_TYPE == 2):     
            rdh_1 = [   0, runset[ self.constg.IDX_START_COL] , runset[ self.constg.IDX_END_COL] ,
                                runset[ self.constg.IDX_START_ROW], runset[ self.constg.IDX_END_ROW] ,
                                runset[ self.constg.IDX_BINNING]      ]
                                        
            rdh_2 = [   1, runset[ self.constg.IDX_START_COL] , runset[ self.constg.IDX_END_COL] ,
                            runset[ self.constg.IDX_START_ROW], runset[ self.constg.IDX_END_ROW],
                            runset[ self.constg.IDX_BINNING]        ]
                            
            rdh_3 = [   2, runset[ self.constg.IDX_START_COL] , runset[ self.constg.IDX_END_COL] ,
                            runset[ self.constg.IDX_START_ROW], runset[ self.constg.IDX_END_ROW] ,
                            runset[ self.constg.IDX_BINNING]       ]
                                            
            rdh_4 = [   3, runset[ self.constg.IDX_START_COL] , runset[ self.constg.IDX_END_COL] ,
                            runset[ self.constg.IDX_START_ROW], runset[ self.constg.IDX_END_ROW] ,
                            runset[ self.constg.IDX_BINNING]       ]
        elif( self.varg.CFG_TYPE == 1):
            rdh_1 = [   ( runset[self.constg.IDX_FIRST_CHAN ]  ),
                            runset[ self.constg.IDX_START_COL] , runset[ self.constg.IDX_END_COL] ,
                            runset[ self.constg.IDX_START_ROW], runset[ self.constg.IDX_END_ROW] ,
                            runset[ self.constg.IDX_BINNING]      ]
                                    
            rdh_2 = [   runset[self.constg.IDX_SECOND_CHAN ]  ,
                            runset[ self.constg.IDX_START_COL] , runset[ self.constg.IDX_END_COL] ,
                            runset[ self.constg.IDX_START_ROW], runset[ self.constg.IDX_END_ROW],
                            runset[ self.constg.IDX_BINNING]        ]
                    
            rdh_3 = [   runset[self.constg.IDX_THIRD_CHAN ]  ,
                            runset[ self.constg.IDX_START_COL] , runset[ self.constg.IDX_END_COL] ,
                            runset[ self.constg.IDX_START_ROW], runset[ self.constg.IDX_END_ROW] ,
                            runset[ self.constg.IDX_BINNING]       ]
                                    
            rdh_4 = [   runset[self.constg.IDX_FOURTH_CHAN ]  ,
                            runset[ self.constg.IDX_START_COL] , runset[ self.constg.IDX_END_COL] ,
                            runset[ self.constg.IDX_START_ROW], runset[ self.constg.IDX_END_ROW] ,
                            runset[ self.constg.IDX_BINNING]       ]
        else:
            self.req_exit("BAD config file for Dasy server !!" ) ;
                
        self.varg.rdh = [ rdh_1, rdh_2, rdh_3, rdh_4 ]
        if( self.DBG == True):
                print "RD: " , self.varg.rdh ;
        try:
            self.varg.c111.stopTdc(self.varg.FD);
            self.varg.CurrentCfg.DownloadToTdc();
        except:
            self.req_exit("Cannot stop and/or configure TDC !") ;
        
            
    def get_port(self):
        
        dport = self.constg.DASY_NETWORK_PORT
        f = self.constg.CFG_PATH_MAIN  +  self.constg.CFG_PATH_SERVER + "DasyServerParams.cfg" ;
        if( os.path.exists( f ) == True ):
            fp = open( f , 'r' )
            strr = fp.read()
            portd = strr.split(":") ;
            dport = int(portd[1]) ;
            fp.close();
        return(dport);
    
    def read_histo_2D(self):
        
        self.varg.array_buf_1 = ""
        self.varg.array_buf_1_Bank0 = ""
        self.varg.array_buf_1_Bank1 = ""
        self.varg.data_2D = ""
        gc.collect()
        config = self.varg.CurrentCfg.ToTdcSettings()
        nb_BankAcq = config[ self.constg.IDX_ACQU_BANK ]
        GFD_mode = config[ self.constg.IDX_PILEUPY ]
        runset = self.varg.CurrentCfg.ToRunSettings()
        if (self.DBG == True):
            print "GFD_MODE: 2D "
            print "CFG: ", config
            print " RDH: ", self.varg.rdh[0]
                    
        if  (nb_BankAcq == 0):
            self.varg.c111.setAcqBank(self.varg.FD,0)
            config[ self.constg.IDX_ACQU_BANK ] = 0
            self.varg.array_buf_1_Bank0 = self.varg.c111.readHistogram_gfd2D(self.varg.FD, config,self.varg.rdh[0])
            self.varg.c111.setAcqBank(self.varg.FD,1)
            config[ self.constg.IDX_ACQU_BANK ] = 1
            self.varg.array_buf_1_Bank1 = self.varg.c111.readHistogram_gfd2D(self.varg.FD, config,self.varg.rdh[0])
        elif(nb_BankAcq == 1):
            self.varg.c111.setAcqBank(self.varg.FD,1)
            config[ self.constg.IDX_ACQU_BANK ] = 1
            self.varg.array_buf_1_Bank1 = self.varg.c111.readHistogram_gfd2D(self.varg.FD, config,self.varg.rdh[0])
            self.varg.c111.setAcqBank(self.varg.FD,0)
            config[ self.constg.IDX_ACQU_BANK ] = 0
            self.varg.array_buf_1_Bank0 = self.varg.c111.readHistogram_gfd2D(self.varg.FD, config,self.varg.rdh[0])
    
        self.varg.array_buf_1 = self.varg.array_buf_1_Bank0 + self.varg.array_buf_1_Bank1
        return(0) ;
        
    def save_2D(self):
        
        tag = int(time.time())
        htag = "GFD2D_" + str(tag) ;
        filename = str("C:\\TEMP\\" ) + htag  + ".edf" ;
        if (self.DBG == True):
            print "SAVE 2D : ", filename ;
        fp = open( filename , 'w' ) ;
        fp.close();
        #header = {'Title'    : "C111_GFD2D_data"}
        header = {'Title'    :  htag }
        file_edf = EdfFile.EdfFile( filename )
        #  file_edf = EdfFile.EdfFile(str(new_DataFilename) + ".edf")
        file_edf.WriteImage(header,self.varg.array_buf_1,1,'UnsignedLong',0,'HighByteFirst')
        file_edf.File.close()
        self.varg.last_saved_file = filename ;
        if (self.DBG == True):
            print "SAVED 2D in: ", self.varg.last_saved_file ;
        self.varg.array_buf_1 = ""
        self.varg.array_buf_1_Bank0 = ""
        self.varg.array_buf_1_Bank1 = ""
        self.varg.data_2D = ""
        gc.collect() ;
        
        return(0);
    
    def read_histo_1D(self):
        
        config = self.varg.CurrentCfg.ToTdcSettings()
        
        BankAcq = config[ self.constg.IDX_ACQU_BANK ]
        if( BankAcq == 0 ):
            self.varg.c111.setAcqBank(self.varg.FD, 0)
            config[ self.constg.IDX_ACQU_BANK ] = 0;
            self.varg.array_buf_1_Bank1 = self.varg.c111.readHistogram_1D(self.varg.FD, config,self.varg.rdh[0])
            if ( config[ self.constg.IDX_OPERATION_MODE] == self.constg.MHIT or
                 config[ self.constg.IDX_OPERATION_MODE] == self.constg.MHIP   ):
                if (self.DBG == True):
                    print "MHIT/MHIP mode"
                self.varg.array_buf_2_Bank1 = self.varg.c111.readHistogram_1D(self.varg.FD,config,self.varg.rdh[1])
                self.varg.array_buf_3_Bank1 = self.varg.c111.readHistogram_1D(self.varg.FD,config,self.varg.rdh[2])
                self.varg.array_buf_4_Bank1 = self.varg.c111.readHistogram_1D(self.varg.FD,config,self.varg.rdh[3])
                
            self.varg.c111.setAcqBank(self.varg.FD, 1)
            config[ self.constg.IDX_ACQU_BANK ] = 1
                
            self.varg.array_buf_1_Bank0 = self.varg.c111.readHistogram_1D(self.varg.FD,config,self.varg.rdh[0])
            if ( config[ self.constg.IDX_OPERATION_MODE] == self.constg.MHIT or
                 config[ self.constg.IDX_OPERATION_MODE] == self.constg.MHIP   ):
                if (self.DBG == True):
                    print "MHIT/MHIP mode"
                self.varg.array_buf_2_Bank0 = self.varg.c111.readHistogram_1D(self.varg.FD,config,self.varg.rdh[1])
                self.varg.array_buf_3_Bank0 = self.varg.c111.readHistogram_1D(self.varg.FD,config,self.varg.rdh[2])
                self.varg.array_buf_4_Bank0 = self.varg.c111.readHistogram_1D(self.varg.FD, config,self.varg.rdh[3])
    
        if( BankAcq == 1 ):
            self.varg.c111.setAcqBank(self.varg.FD, 1)
            config[ self.constg.IDX_ACQU_BANK ] = 1
            self.varg.array_buf_1_Bank0 = self.varg.c111.readHistogram_1D(self.varg.FD, config,self.varg.rdh[0])
            if ( config[ self.constg.IDX_OPERATION_MODE] == self.constg.MHIT or
                 config[ self.constg.IDX_OPERATION_MODE] == self.constg.MHIP   ):
                if (self.DBG == True):
                    print "MHIT/MHIP mode"
                self.varg.array_buf_2_Bank0 = self.varg.c111.readHistogram_1D(self.varg.FD,config,self.varg.rdh[1])
                self.varg.array_buf_3_Bank0 = self.varg.c111.readHistogram_1D(self.varg.FD,config,self.varg.rdh[2])
                self.varg.array_buf_4_Bank0 = self.varg.c111.readHistogram_1D(self.varg.FD,config,self.varg.rdh[3])
                
            self.varg.c111.setAcqBank(self.varg.FD,  0)
            config[ self.constg.IDX_ACQU_BANK ] = 0
                
            self.varg.array_buf_1_Bank1 = self.varg.c111.readHistogram_1D(self.varg.FD,config,self.varg.rdh[0])
            if ( config[ self.constg.IDX_OPERATION_MODE] == self.constg.MHIT or
                 config[ self.constg.IDX_OPERATION_MODE] == self.constg.MHIP   ):
                if (self.DBG == True):
                    print "MHIT/MHIP mode"
                self.varg.array_buf_2_Bank1 = self.varg.c111.readHistogram_1D(self.varg.FD,config,self.varg.rdh[1])
                self.varg.array_buf_3_Bank1 = self.varg.c111.readHistogram_1D(self.varg.FD,config,self.varg.rdh[2])
                self.varg.array_buf_4_Bank1 = self.varg.c111.readHistogram_1D(self.varg.FD, config,self.varg.rdh[3])
            
        self.varg.array_buf_1 = (self.varg.array_buf_1_Bank0 + self.varg.array_buf_1_Bank1)
            
        if ( config[ self.constg.IDX_OPERATION_MODE] == self.constg.MHIT or
                 config[ self.constg.IDX_OPERATION_MODE] == self.constg.MHIP   ):
            if (self.DBG == True): print "MHIT mode"
            self.varg.array_buf_2 = (self.varg.array_buf_2_Bank0 + self.varg.array_buf_2_Bank1)
            self.varg.array_buf_3 = (self.varg.array_buf_3_Bank0 + self.varg.array_buf_3_Bank1)
            self.varg.array_buf_4 = (self.varg.array_buf_4_Bank0 + self.varg.array_buf_4_Bank1)  
            
        return(0);
        
    def save_1D(self):
        
        config = self.varg.CurrentCfg.ToTdcSettings()
        
        tag = int(time.time())
        if ( config[ self.constg.IDX_OPERATION_MODE] == self.constg.MHIT):
            h = "MHIT_";
        elif(  config[ self.constg.IDX_OPERATION_MODE] == self.constg.MHIP ):
            h = "MHIP_";
        else: ### GFD1D
            h = "GFD1D_";
        htag = h  + str(tag) ;
        filename = str("C:\\TEMP\\" ) + htag  + ".dat" ;
        if (self.DBG == True):
            print "SAVE 1D : ", filename ;
        
        tdcset = self.varg.CurrentCfg.ToTdcSettings()
        runset = self.varg.CurrentCfg.ToRunSettings()
        startCol = runset[ self.constg.IDX_START_COL ]
        endCol = runset[ self.constg.IDX_END_COL ]
        r = ( endCol - startCol ) 
        if( (r %2) != 0 ): r = r - 1 ;
        if( runset[ self.constg.IDX_BINNING ] == 1 ): r = r/2 ;
        
        fp = open( filename , 'w' ) ;
        
        if( self.varg.CurrentCfg.GetRealOperationMode() == self.constg.GFD ):     
            for i in range( r ):
                fp.write(str(self.varg.array_buf_1[i]) + " \n")
        elif (self.varg.CurrentCfg.GetRealOperationMode() != self.constg.GFD and runset[ self.constg.IDX_CHANNELS_NUMBER ] == 1):
            for i in range( r ):
                fp.write(str(self.varg.array_buf_1[i]) + " \n")
                #print " idx: ", i , " data: ", self.varg.array_buf_1[i]         
        elif (runset[ self.constg.IDX_CHANNELS_NUMBER ] == 2):
            for i in range( r ):
                fp.write(str(self.varg.array_buf_1[i])+ "\t" +  str(self.varg.array_buf_2[i]) + " \n")
        elif (runset[ self.constg.IDX_CHANNELS_NUMBER ] == 3):
            for i in range( r ):
                fp.write(str(self.varg.array_buf_1[i])+ "\t" + str(self.varg.array_buf_2[i]) + "\t" + str(self.varg.array_buf_3[i]) + " \n")
        elif (runset[ self.constg.IDX_CHANNELS_NUMBER ] == 4):
            for i in range( r ):
                file_data.write(str(self.varg.array_buf_1[i])+ "\t" + str(self.varg.array_buf_2[i]) + "\t" + 
                                        str(self.varg.array_buf_3[i]) + "\t" + str(self.varg.array_buf_4[i]) + " \n")
        fp.close();
        self.varg.last_saved_file = filename ;
        if (self.DBG == True):
            print "SAVED 1D in: ", self.varg.last_saved_file ;
            
        return(0);
        
    def get_hw_data(self):
        
        ret = -1;
        
        if( self.varg.CFG_TYPE == 2):     
            ret = self.read_histo_2D() ;
            if( ret != 0):
                self.sock.send("DATA;NOTOK; Read data from hardware failed !");
                return(ret);
            ret = self.save_2D();
            if( ret != 0):
                self.sock.send("DATA;NOTOK; Save of acquisition failed !");
                return(ret);
        elif( self.varg.CFG_TYPE == 1):
            ret = self.read_histo_1D() ;
            if( ret != 0):
                self.sock.send("DATA;NOTOK; Read data from hardware failed !");
                return(ret);
            ret = self.save_1D();
            if( ret != 0):
                self.sock.send("DATA;NOTOK; Save of acquisition failed !");
                return(ret);
        else:        
            return -1 ;
        ### data acq + data save OK
        return 0 ;
        
    def snd_data(self):
        
        block_size = ( 1024 * self.varg.bsize )  ;
        ret = -1;  msg = "" ;
         
        if( self.varg.FD == -1):
                #msg = " No device attached !!\n Need to attach one first !!! \n"
                #print msg
                self.sock.send("DATA;NOTOK; No P/C111 device attached to DasyServer !");
                return
        
        TDC_getstatus = self.varg.c111.getTdcStatus(self.varg.FD)
        if (TDC_getstatus['AcqState'] == 1):
            #msg = " TDC running !!! \n"
            #print msg
            self.sock.send("DATA;NOTOK; TDC is running. Stop it first !");
            return ;
        
        self.varg.last_saved_file = "None" ;
        ret = self.get_hw_data() ;   
        if( ret != 0): 
            self.sock.send("DATA;NOTOK;Failed reading data on TDC  !!");
            return ;
        barr = "" ;
        gc.collect()
        f = self.varg.last_saved_file ;
        #f = "C:\TEMP\GFD2D_1195115502.edf" ;
        if( os.path.exists( f ) == True ):
            fp = open( f , 'rb' )
            barr = fp.read()
            fp.close();
            size = len(barr) ; 
            msg = "DATA;SIZE;" + str(size) ;
            try:
                self.sock.send(msg);
            except socket.error,msgerr:
                print msgerr ;
                return ;
            #print msg ;
            try:
                answer = "" ;
                answer = self.sock.recv(1024) ;
            except socket.error,msgerr:
                print msgerr ;
                return;
                
            if( answer[:7] != "DATA;OK"):
                if( self.varg.store == 0 ):
                    os.remove(f);
                return ;
                    
            totalsent = 0
            fp = open( f , 'rb' )
            barr = "" ;
            gc.collect() ;
            while (totalsent < size):
                barr = fp.read(block_size);
                try:
                    sent = self.sock.send(barr);
                except socket.error,msgerr:
                    print msgerr ;
                    return
                
                if sent == 0:
                    raise RuntimeError,  "socket connection broken"
                totalsent = totalsent + sent
                try:
                    answer = "" ;
                    answer = self.sock.recv(1024) ;
                except socket.error,msgerr:
                    print msgerr ;
                    return
                
                #print "ANSWER: " , answer ;
                if( answer[:7] != "DATA;OK"):
                    #print "BAD ANSWER: ", answer ;
                    fp.close();   
                    return ;
                #print "SENT: ", totalsent ,  "LEN TO TRANSFER: ", size ;
                barr = "" ;
                #gc.collect() ;
    
            fp.close();           
            msg = "DATA;END" ;  #print "SENT: " , msg ;
            
            if( self.varg.store == 0 ):
                os.remove(f);
            try:
                self.sock.send(msg);
            except socket.error,msgerr:
                print msgerr ;
                return ;
        else:
            try:
                self.sock.send("DATA;NOTOK; No acquisition was saved. Nothing to send !");
            except socket.error,msgerr:
                print msgerr ;
                return ;
        return
        
    def clear_mem(self):
        
        if( self.varg.FD == -1):
                #msg = " No device attached !!\n Need to attach one first !!! \n"
                #print msg
                self.sock.send("CLEAR;NOTOK; No P/C111 device attached to DasyServer !");
                return
                
        TDC_getstatus = self.varg.c111.getTdcStatus(self.varg.FD)
        if (TDC_getstatus['AcqState'] == 1):
            #msg = " TDC  running !!! \n"
            #print msg
            self.sock.send("CLEAR;NOTOK; TDC is running. Stop it first !");
            return ;
            
        try:     
            self.varg.c111.stopTdc(self.varg.FD)
            self.varg.c111.setAcqBank(self.varg.FD,0)
            self.varg.c111.initBank(self.varg.FD,0,0)
            self.varg.c111.setAcqBank(self.varg.FD,1)
            self.varg.c111.initBank(self.varg.FD,0,0)
        except:
            self.sock.send("CLEAR;NOTOK");
            return ;
            
        self.varg.START_TDC = 0   
        self.sock.send("CLEAR;OK");
        return
        
    def start_tdc(self):
        
        if( self.varg.FD == -1):
                #msg = " No device attached !!\n Need to attach one first !!! \n"
                #print msg
                self.sock.send("START;NOTOK; No P/C111 device attached to DasyServer !");
                return
            
        TDC_getstatus = self.varg.c111.getTdcStatus(self.varg.FD)
        if (TDC_getstatus['AcqState'] == 1):
            #msg = " TDC already running !!! \n"
            #print msg
            self.sock.send("START;NOTOK; TDC is running. Stop it first !");
            return ;
        
        try:  
            self.varg.c111.startTdc(self.varg.FD , self.varg.CurrentCfg.GetFiniteTimeLength() * 1000000 )
        except:
            self.sock.send("START;NOTOK; Start TDC failed !");
            return ;
                
        self.varg.START_TDC = 1 ;
        self.sock.send("START;OK");
        return
        
    def stop_tdc(self):
        
        if( self.varg.FD == -1):
                #msg = " No device attached !!\n Need to attach one first !!! \n"
                #print msg
                self.sock.send("STOP;NOTOK; No P/C111 device attached to DasyServer !");
                return
        
        try:
            self.varg.c111.stopTdc(self.varg.FD)
        except:
            self.sock.send("STOP;NOTOK; Stop TDC failed !");
            return ;
            
        self.varg.START_TDC = 0
        self.sock.send("STOP;OK");
        return
        
    def snd_stats(self):
        
        if( self.varg.FD == -1):
                #msg = " No device attached !!\n Need to attach one first !!! \n"
                #print msg
                self.sock.send("STATS;NOTOK; No P/C111 device attached to DasyServer !");
                return
                
        gettdcconfig = self.varg.c111.getTdcConfig(self.varg.FD)
        TDC_getstatus = self.varg.c111.getTdcStatus(self.varg.FD)
        
        if (int(gettdcconfig[ self.constg.IDX_INTERRUPT_TIMER]) != 1) :
            #print "STATS: Timer interruption hasn't been set on TDC configuration "
            self.sock.send("STATS;NOTOK; Timer interruption hasn't been set on TDC configuration ");
            return;
            
        gettdcstatistic = self.varg.c111.getTdcStatistics(self.varg.FD)
        starts = gettdcstatistic['ComStarts']
        rej = gettdcstatistic['RejEvents']
        qp = 0
        if( starts > 0 ):
            qp = (100 * rej) / starts
        
        stats_val =   "Nb of hits on Channel 3 :  " + str(gettdcstatistic['HitsCh3'] ) + "\n" + \
                                "Nb of hits on Channel 2 :  " + str(gettdcstatistic['HitsCh2'] ) + "\n" + \
                                "Nb of hits on Channel 1 :  " + str(gettdcstatistic['HitsCh1'] ) + "\n" + \
                                "Nb of hits on Channel 0 :  " + str(gettdcstatistic['HitsCh0'] ) + "\n" + \
                                "Elapsed Time (s) :  " + str(gettdcstatistic['ElapsedTime'])  + "\n" + \
                                "Nb common Starts :  " + str(gettdcstatistic['ComStarts'] ) + "\n" + \
                                "Nb of rejected Events :  " + str(gettdcstatistic['RejEvents'] ) + "\n" + \
                                "Starts / Rejected ( % )  :  " + str(qp) + "\n" + \
                                "Nb of ALU overflow events  :  " + str(gettdcstatistic['ALUOvfs']) + "\n" ;
        
        self.sock.send(stats_val);
        return  
        
    def snd_cfg(self):
        
        barr = "" ;
            
        if( self.varg.CFG_TYPE == 2 ):    
            f = self.varg.cfg_path + self.constg.CFG_SERVER_FILE2D ;
        elif( self.varg.CFG_TYPE == 1 ):    
            f = self.varg.cfg_path + self.constg.CFG_SERVER_FILE1D ;
        else:
            self.sock.send("CFG;NOTOK; Bad configuration type !");
            return ;
            
        #print "CONF: " , f ;
        if( os.path.exists( f ) == True ):
            fp = open( f , 'rb' )
            barr = fp.read()
            fp.close();
            self.sock.send(barr);
        else:
            self.sock.send("CFG;NOTOK; Could not find configuration file");
        return
    
    def new_bsiz( self,buff ):
        try:
            cmd , size = buff.split(";") ;
        except:
            msg = "BSIZE;NOTOK; Bad command format !!"
            self.varg.bsize = 1 ;
            self.sock.send(msg);
            return ;
            
        #print "CMD: " , cmd , " SIZE: ", size 
        self.varg.bsize =  int(size) ;
        if( self.varg.bsize < 1 or self.varg.bsize > 8):
            msg = "BSIZE;NOTOK; Must be in [1..8] !!"
            self.varg.bsize = 1 ;
        else:
            msg = "BSIZE;OK" ;
        self.sock.send(msg);
        return ;

    
    def new_stor( self,buff ):
        try:
            cmd , flag = buff.split(";") ;
        except:
            msg = "STOR;NOTOK; Bad command format !!"
            self.varg.store = 1 ;
            self.sock.send(msg);
            return ;
            
        #print "CMD: " , cmd , " FLAG: ", flag 
        
        if( flag == "YES" ):
            self.varg.store = 1 ;
            msg = "STOR;OK" ;
        elif( flag == "NO" ):
            self.varg.store = 0 ;
            msg = "STOR;OK" ;
        else:
            msg = "STOR;NOTOK; Must YES or NO !!"
            
        self.sock.send(msg);
        return ;


    def new_pftp(self, buff):
        try:
            cmd , host , login , passwd , directory = buff.split(";") ;
        except:
            msg = "PFTP;NOTOK; Bad command format !!"
            self.sock.send(msg);
            return ;
        
        if( self.DBG == True):
            print "CMD: " , cmd , " HOST: ", host 
            print "LOGIN: ", login , "PASS: ", passwd 
            print "DIR: ", directory ;
        
        self.ftp_serv = host ;
        self.ftp_login = login ;
        self.ftp_pass = passwd ;
        self.ftp_dir = directory ;
        
        msg = "PFTP;OK" ;
        self.sock.send(msg);
        return ;
        
    def snd_ftp(self):
        if( self.DBG == True):
            print self.ftp_serv
            print self.ftp_login
            print self.ftp_pass 
            print self.ftp_dir 
            
        if( ( self.ftp_serv == "None" ) or ( self.ftp_login == "None") or ( self.ftp_pass == "None" )) :
            self.sock.send("FTP;NOTOK; FTP parameters not given !");
            return
                      
        if( self.varg.FD == -1):
            #msg = " No device attached !!\n Need to attach one first !!! \n"
            #print msg
            self.sock.send("FTP;NOTOK; No P/C111 device attached to DasyServer !");
            return
        
        TDC_getstatus = self.varg.c111.getTdcStatus(self.varg.FD)
        if (TDC_getstatus['AcqState'] == 1):
            #msg = " TDC running !!! \n"
            #print msg
            self.sock.send("FTP;NOTOK; TDC is running. Stop it first !");
            return ;
        
        self.varg.last_saved_file = "None" ;
        ret = self.get_hw_data() ;   
        if( ret != 0): 
            self.sock.send("FTP;NOTOK;Failed reading data on TDC  !!");
            return ;
        f = self.varg.last_saved_file ;
        #f = "C:\TEMP\GFD2D_1195115502.edf" ;
        
        if( os.path.exists( f ) == True ):
            fp = open( f , 'rb' )
            barr = fp.read()
            fp.close();
            size = len(barr) ; 
            msg = "FTP;SIZE;" + str(size) ; 
            self.sock.send(msg);
        else:
            try:
                self.sock.send("FTP;NOTOK; No acquisition was saved. Nothing to send !");
            except socket.error,msgerr:
                print msgerr ;
                return ;
                
        try:
            answer = "" ;
            answer = self.sock.recv(1024) ;
        except socket.error,msgerr:
            print msgerr ;
            return;
                
        if( answer[:6] != "FTP;OK"):
            if( self.varg.store == 0 ):
                os.remove(f);
            return ;
            
#ftp = ftplib.FTP('')
#ftp.connect(monadresse, monport)
#ftp.login(monlogin, monpassword)

        try:
            #session = ftplib.FTP(  self.ftp_serv , self.ftp_login , self.ftp_pass  )
            session = ftplib.FTP('') ;
            #print "Session ok ..."
            if self.DBG == True:
                session.set_debuglevel( 2 )
            session.connect( self.ftp_serv )
            #print "Connect ok ...."
            session.login( self.ftp_login , self.ftp_pass  ) ;
            #print "Login ok ...."
            monfichier = open( f ,'rb')
        # On ouvre le fichier à envoyer
            if( self.ftp_dir[0] == "/" ): # Unix path
                if( self.ftp_dir[:-1] != "/" ):
                    self.ftp_dir += "/" ;
            else: # windows path
                if( self.ftp_dir[:-1] != "\\" ):
                    self.ftp_dir += "\\" ;
            cmd = "STOR " + self.ftp_dir + os.path.basename(f) ;
            if( self.DBG == True):
                print cmd ;
            session.storbinary( cmd , monfichier)
            #print "STOR  ok ...."
            monfichier.close()
            session.quit()
            #print "Session quit  ok ...."
        except Exception, emsg:
            #print "FTP: ERR-MSG: " , emsg
            msg = "FTP;NOTOK; " + str(emsg ) ;
            self.sock.send( msg );
            return ;
            
        msg = "FTP;END" ;  #print "SENT: " , msg ;
        try:
            self.sock.send(msg);
        except socket.error,msgerr:
            print msgerr ;
            return ;
        if( self.varg.store == 0 ):
                os.remove(f);  
        return ;

        
    def run(self,dbg = False): 
    
        self.DBG = dbg ;
        
        self.get_cfg();
        dport = self.get_port() ;
        print "DasyServer: opening port: " , dport  
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.bind(('', dport))
        self.conn.listen(1)
        
        # loop waiting for connections 
        # terminate with Ctrl-Break on Win32, Ctrl-C on Unix
        try:
            while True:
                gc.collect() ;
                try:
                    self.sock, address = self.conn.accept(  )
                except socket.error,msg:
                    print msg ;
                print "Connected from", address
                while True:
                    try:
                        receivedData = self.sock.recv(8192)
                    except socket.error,msg:
                        print msg ;
                        break ;
                      
                    if not receivedData: break
                    #print "RCV: " , receivedData
                    sav = receivedData ;
                    receivedData = string.upper(receivedData) ;
                    if( receivedData[0] == 'E'):
                        self.conn.close()
                        exit(1);
                    elif( ( receivedData[0] == 'D') and (len(receivedData) < 5)  ): # cmd DATA
                        self.snd_data();
                    elif( receivedData[0] == 'B'): # cmd BSIZE
                        self.new_bsiz(receivedData );
                    elif( receivedData[:5] == 'CLEAR'):
                        self.clear_mem();
                    elif( receivedData[:3] == 'CFG') : # cmd CFG
                        self.snd_cfg();
                    elif( receivedData[:5] == 'START'):
                        self.start_tdc();
                    elif( receivedData[:4] == 'STOP'):
                        self.stop_tdc();
                    elif( receivedData[:4] == 'STOR'):
                        self.new_stor(receivedData);
                    elif( receivedData[:5] == 'STATS'):
                        self.snd_stats();
                    elif( receivedData[:4] == 'PFTP' ):
                        self.new_pftp(sav);
                    elif( receivedData[:3] == 'FTP'): 
                        self.snd_ftp();
                    else:
                        #print "WHAT TO DO ?"
                        try:
                            self.sock.sendall(receivedData)
                        except socket.error,msg:
                            print msg ;
                            break ;
                try:
                    self.sock.close(  )
                except socket.error,msg:
                    print msg ;
                print "Disconnected from", address
        finally:
            self.conn.close(  )