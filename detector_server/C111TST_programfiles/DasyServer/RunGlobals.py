

class RunGlobals:
    def __init__(self,*args):
        self.user = "" 
        self.CurrentCfg = 0 ; 
        self.list_devices = [ ]
        self.data_2D = "" 
        self.FD = -1
        self.START_TDC = -1
        self.mode_GFD1D = -1
        self.mode_GFD2D = -1
        self.START_TDC_parameters = 0 
        self.rdh = [ ]
        self.AcquisitionDATA  = -1 
        self.new_DeviceFilename = "" 
        self.new_ImageFilename = "" 
        self.array_buf_1_Bank0 = ""
        self.array_buf_1_Bank1 = "" 
        self.array_buf_1 = ""
        self.array_buf_2_Bank0 = ""
        self.array_buf_2_Bank1 = ""
        self.array_buf_2 = ""
        self.array_buf_3_Bank0 = ""
        self.array_buf_3_Bank1 = ""
        self.array_buf_3 = ""
        self.array_buf_4_Bank0 = ""
        self.array_buf_4_Bank1 = ""
        self.array_buf_4 = ""
        self.c111 = ""
        self.cfg_path = ""
        self.statsActive = 0
        self.finiteAcqTimeOn = 0
        self.CFG_TYPE = 0 ;
        self.last_saved_file = "C:\\TEMP\\none.edf" 
        self.bsize = 1 ; # data blocks sent to client are 1024 * bsize , so min is 1024 ;
        self.ftp_serv = "None" ;
        self.ftp_login = "None";
        self.ftp_pass = "None";
        self.ftp_dir = "None" ;
        self.store = 1 ; # store or not data in local files ? default is yes
    