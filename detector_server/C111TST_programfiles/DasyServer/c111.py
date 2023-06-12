#/*+*****************************************************************************
#
# File       : C111.PY (Python module of the c111 CUB card,
#	       Class function of the C111PY.C python extension)
# Project    : Solaris Device Driver for CUB+C111 Compact-PCI board
# Description: Python module which import c111py.c to define the different function
#	       declared on the python C extension (c111py.c)
#              It adds help for users to know the different command.
#               
# 
# Author(s)  : B. Scaringella
# Original   : Feb 2004
#
# $Revision: May 2004, JUNE 2005
# $Log: $
#
# Copyright (c) 2003 by European Synchrotron Radiation Facility,
#                       Grenoble, France
#
#*****************************************************************************-*/



#---------------------------------------------------------------------------
#			Python header file
#---------------------------------------------------------------------------

import string
import sys


#---------------------------------------------------------------------------
#			Private header file
#---------------------------------------------------------------------------

import c111py

#---------------------------------------------------------------------------
#TODO: why not in the class??
tab='c111:'

#---------------------------------------------------------------------------
# No traceback on exception, we don't want the user to debug our code
sys.tracebacklimit=0


#---------------------------------------------------------------------------
class c111:
   def __init__(self):
      self.data = []

   def help(self,cmd=''):
      """

      get the list of commands available or a command detail

      help()
         return the list of commands available.
      help('cmd')
         extract info from the class method 'cmd' comments. These ones
         must have as first line a short description and then
         after a blank line the detailed syntax of the command.
      """

      mdoc=''
      m=dir(c111)
      m.sort()
      if(cmd):
        if(not (cmd in m)):
          longdoc=cmd+' - '+'unknown command'
        else:
          mydoc=eval('self.'+cmd+'.__doc__')
          if(mydoc):
            mylines=string.split(mydoc,'\n')
            longdoc=''
            for j in mylines[2:]:
              longdoc=longdoc+"%s\n"%(j)
          else:
            longdoc=cmd+' - '+'not documented'
        mdoc=longdoc
      else:
        mdocs={}
        idx=0
        mlen=0
        for i in m:
          if(i[0] != '_'):
            mydoc=eval('self.'+i+'.__doc__')
            if(mydoc):
              mylines=string.split(mydoc,'\n')
              shortdoc=string.lstrip(mylines[1])
            else:
              shortdoc='not documented'
            mdocs[i]=shortdoc
            idx=idx+1
            tmp=len(i)
            if(tmp>mlen): mlen=tmp
        keys=mdocs.keys()
        keys.sort()
        for j in keys:
          mdoc=mdoc+"%*s - %s\n"%(mlen+2,j,mdocs[j])
      print mdoc
      return mdoc

   def setLibDebug(self,dbg_flag):
      """

      set/unset debug on c111lib.c (C library of function)
      setLibDebug(),
      input argument:  dbg_flag (debug flag) = 0, off
     			                       1, on
      output argument: PyNone object if OK / error object if NOTOK
      """
      return c111py.c111py_setLibDebug(dbg_flag)

   def searchDev(self):
      """

      function to search for c111 devices

      searchDev(),
      input argument:  None 
      output argument: PyList object,
      		       first field is error flag: 0 = OK
		       				  1 = Error
		       if OK next list items are device names
		       if error next list item is error string
      """
      return c111py.c111py_searchDev()

   def open(self,device_name):
      """

      function to make open on a c111my device

      open(),
      input argument:  a string with device(descriptor) name
      output argument: PyNone object if OK / error object if NOTOK
      """
      return c111py.c111py_open(device_name)
      
   def reopen(self,device_name):
      """

      function to make open on a c111my device

      open(),
      input argument:  a string with device(descriptor) name
      output argument: PyNone object if OK / error object if NOTOK
      """
      return c111py.c111py_reopen(device_name)
   
   def close(self,FD):
      """

      function to close opened c111 device

      close(),
      input argument:  file descriptor returned by open()
      output argument: PyNone object if OK / error object if NOTOK
      """
      c111py.c111py_close(FD)

   def setDriverDebug(self,FD,level):
      """

      set the debug level of the C111 driver

      setDriverDebug(),
      input argument:  file descriptor returned by open, 
                       level: 0, no verbose at all
                              1, to 4: print out debug messages on /var/log/messages
      output argument: PyNone object if OK / error object if NOTOK
      """
      c111py.c111py_setDbgLevel(FD,level)

   def getDriverDebug(self,FD):
      """

      get the debug level of the C111 driver
      
      getDriverDebug(),
      input argument:  file descriptor returned by open
      output argument: tuple object (driver debug level as integer and string) if OK / error object if NOTOK
                       level: 0, no verbose at all
                              1 to 4, print out debug messages on /var/log/messages
      """
      return c111py.c111py_getDbgLevel(FD)

   def getLastHistSum(self,FD):
      """

      get the sum of hits for last accquisition
      
      getLastHistSum(),
      input argument:  file descriptor returned by open
      output argument: tuple object ( hist sum as integer and string) if OK / error object if NOTOK
                       
      """
      return c111py.c111py_getLastHistSum(FD)
      

   def loadVirtex(self,FD,bootconfig, bitfilepath):
      """

      load Virtex in order that card can be used 
	
      loadVirtex(),
      input argument:  file descriptor returned by open,
                       bootconfig: 0 = GFD, 1 = MHIT, 2 = MHIP
                       bitfilepath: full path for the bit files
      output argument: PyNone object if OK / error object if NOTOK
      """
      c111py.c111py_loadVirtex(FD,bootconfig,bitfilepath)

   def getBootConfig(self,FD):
      """

      get the boot configuration from the C111 driver

      getBootConfig(),
      input argument:  file descriptor returned by open,
      output argument: integer object if OK / error object if NOTOK
                       boot config: 0 == GFD,   1 == MHIT,   2 == MHIP
      """
      return c111py.c111py_getBootConfig(FD)

   def getCubStatus(self,FD):
      """

      get CUB status structure from C111 driver

      getCubStatus(),
      input argument  : file descriptor returned by open 
      output argument : Dictionary object with key,value pair for each field in the
                        c111_cubstatus structure if OK / error object if NOTOK
      
      This function gets CUB status from (CUB_STATUS) register:
 *      - status for each of 6 low voltages (1 means LV = OK):
 *                  index LV value 
 *                  0     1.8V
 *                  1     2.5V
 *                  2     3.3V
 *                  3     5V
 *                  4     +12V
 *                  5     -12V
 *              - overall status for LV (1 = OK, 0 = at least 1 LV is not OK)
 *      - 33MHz PhaseLockLoop status  (1 = OK, 0 = not OK)
 *      - CUB serial number
 *
      """
      return c111py.c111py_getCubStatus(FD)

   def getNbCards(self,FD):
      """      

      get nb of C111 cards
      getNbCards(),
      input argument  : file descriptor returned by open 
      output argument : Integer object(nb of C111 cards) if OK / error object if NOTOK
      """
      return c111py.c111py_getNbCards(FD)

   def clearItCnts(self,FD):
      """

      Clear interrupt counts which serve only for debugging.

      clearItCnts()
      input argument  : file descriptor returned by open 
      output argument : PyNone object if OK / error object if NOTOK
      """
      c111py.c111py_clearItCnts(FD)

   def getItCnts(self,FD):
      """

      Get the interrupt counts structure
       
      getItCnts(),
      input argument:  file descriptor returned by open
      output argument: Dictionary object with key,value pair for each field in the
                       c111_itcnts structure / error object if NOTOK
      """
      return c111py.c111py_getItCnts(FD)

   def setTdcConfig(self,FD,c111_listtdcconfig):
      """

      set the TDC configuration in the C111 driver
      
      setTdcConfig(),
      input argument:  file descriptor returned by open,
                       c111_tdcconfig TDC configuration structure
                       
    config->timeout           = (u16)0; /* will be filled on return */
    config->mode.mode_select  = (u8)0; /* will be filled on return */
    config->mode.mode_type    = (u8)0; /* will be filled on return */
    config->skip              = (u8)0; /* will be filled on return */
    config->extinhfc          = (u8)0; /* will be filled on return */
    config->pileup.pileup_x   = (u8)0; /* will be filled on return */
    config->pileup.pileup_y   = (u8)0; /* will be filled on return */
    config->offset.offset_x   = (u16)0; /* will be filled on return */
    config->offset.offset_y   = (u16)0; /* will be filled on return */
    config->halfres           = (u8)0; /* will be filled on return */
    config->fpmonitor.monitor = (u8)0; /* will be filled on return */
    config->fpmonitor.muxsel  = (u8)0; /* will be filled on return */
    config->timer.it_enable   = (u8)0; /* will be filled on return */
    config->timer.duration    = (u16)0; /* will be filled on return */
    config->acq_bank          = 0; /* will be filled on return */

      output argument: PyNone object if OK / error object if NOTOK
      """
      c111py.c111py_setTdcConfig(FD,c111_listtdcconfig)

   def getTdcConfig(self,FD):
      """

      get the TDC config from the shadow copy in dev private structure 
      
      getTdcConfig(),
      input argument:  file descriptor returned by open
      output argument: c111_tdcconfig structure as a list object if OK / error object if NOTOK
      
    config->timeout           = (u16)0; /* will be filled on return */
    config->mode.mode_select  = (u8)0; /* will be filled on return */
    config->mode.mode_type    = (u8)0; /* will be filled on return */
    config->skip              = (u8)0; /* will be filled on return */
    config->extinhfc          = (u8)0; /* will be filled on return */
    config->pileup.pileup_x   = (u8)0; /* will be filled on return */
    config->pileup.pileup_y   = (u8)0; /* will be filled on return */
    config->offset.offset_x   = (u16)0; /* will be filled on return */
    config->offset.offset_y   = (u16)0; /* will be filled on return */
    config->halfres           = (u8)0; /* will be filled on return */
    config->fpmonitor.monitor = (u8)0; /* will be filled on return */
    config->fpmonitor.muxsel  = (u8)0; /* will be filled on return */
    config->timer.it_enable   = (u8)0; /* will be filled on return */
    config->timer.duration    = (u16)0; /* will be filled on return */
    config->acq_bank          = 0; /* will be filled on return */

      """
      return c111py.c111py_getTdcConfig(FD)

   def getTdcConfigHw(self,FD):
      """

      get the TDC config from the hardware = device registers
      
      getTdcConfigHw(),
      input argument:  file descriptor returned by open
      output argument: c111_tdcconfig structure as a list object if OK / error object if NOTOK
      """
      return c111py.c111py_getTdcConfigHw(FD)

   def setPowerUpDn(self,FD,pupdn):
      """

      set the ASIC power up or down
      
      setPowerUpDn(),
      input argument:  file descriptor returned by open,
                       pupdn: 0, down
	 	              1, up
      output argument: PyNone object if OK / error object if NOTOK
      """
      c111py.c111py_setPowerUpDn(FD,pupdn)

   def getPowerUpDn(self,FD):
      """

      Give the status of ASIC power (up or down)
      
      getPowerUpDn(),
      input argument:  file descriptor returned by open
      output argument: integer object (ASIC power state up(1)/down(0)) if OK / error object if NOTOK
      """
      return c111py.c111py_getPowerUpDn(FD)

   def setAcqBank(self,FD,bank_id):
      """
 
      select a bank for data acquisition
      
      setAcqBank(),
      input argument:  file descriptor returned by open,
                       bank index: 0 or 1
      output argument: PyNone object if OK / error object if NOTOK
      """
      c111py.c111py_setAcqBank(FD,bank_id)

   def initBank(self,FD,init_value,incr_flag):
      """

      Initialisation of the memory bank selected.
      
      initBank(),
      input argument:  file descriptor returned by open,
                       c111_initbank structure : init value
		                                 increment flag
      output argument: PyNone object if OK / error object if NOTOK
      """
      c111py.c111py_initBank(FD,init_value,incr_flag)

   def startTdc(self,FD,time_sft):
      """

      function which one start the TDC to perform a data acquisition
      
      startTdc(),
      input argument:  file descriptor returned by open
                       software timer duration(microsecond)
      output argument: PyNone object if OK / error object if NOTOK
      """
      #print "Before c111py.c111py_startTdc()"
      c111py.c111py_startTdc(FD,time_sft)
      #print "After c111py.c111py_startTdc()"
        
   def stopTdc(self,FD):
      """

      function which one stop the TDC
      
      stopTdc(),
      input argument:  file descriptor returned by open
      output argument: PyNone object if OK / error object if NOTOK     
      """
      c111py.c111py_stopTdc(FD)

   def getTdcStatus(self,FD):
      """

      function which one give the TDC status from the driver
      
      getTdcStatus(),
      input argument:  file descriptor returned by open
      output argument: Dictionary object with key,value pair for each field in the
                       c111_tdcstatus structure if OK / error object if NOTOK
      """
      return c111py.c111py_getTdcStatus(FD)

   def getTdcStatistics(self,FD):
      """

      function which one give the TDC statistic from the driver
      
      getTdcStatistics(),
      input argument:  file descriptor returned by open
      output argument: Dictionary object with key,value pair for each field in the
      c111_statistics * = structure with 8 fields:
 *                  - elapsed time (in seconds <= from statist.
 *                                    timer register)
 *                                  - nb of hits on channels 0->3
 *                                  - MHIT only: nb of lost hits
 *                                  - GFD/MHIP only: nb of common starts
 *                                  - GFD only: nb of rejected events
 *                                  - GFD only: nb of ALU overflow events 
                       c111_statistics structure if OK / error object if NOTOK
      """
      return c111py.c111py_getTdcStatistics(FD)

   def readHistogram_1D(self,FD,c111_listtdcconfig,c111_listreadhist):
      """

      Read selected histogram from a memory bank 
      This function is implemented only in "fast" form = using 
      rdmem_arg and RdMem command since data size in this case is
      always 32 bits.
      
      readHistogram(),
      input argument:  file descriptor returned by open,
                       TDC configuration structure,
                       read histogram structure
      output argument: 1 dimensional array of data acquisition buffer, mode MHIT/GFD 1D
      """
      return c111py.c111py_readHistogram_1D(FD, c111_listtdcconfig, c111_listreadhist)

   def readHistogram_gfd2D(self,FD,c111_listtdcconfig,c111_listreadhist):
      """

      Read selected histogram from a memory bank 
      This function is implemented only in "fast" form = using 
      rdmem_arg and RdMem command since data size in this case is
      always 32 bits.
      
      readHistogram(),
      input argument:  file descriptor returned by open,
                       TDC configuration structure,
                       read histogram structure
      output argument: 2 dimensional array of data acquisition buffer, mode GFD 2D 
      """
      if( sys.platform == "win32"):
        return c111py.c111py_readHistogram_2D(FD, c111_listtdcconfig, c111_listreadhist)
      else:
        return c111py.c111py_readHistogram_gfd2D(FD, c111_listtdcconfig, c111_listreadhist)

# CONTINUE HERE
# 

#c111 = c111()
#devs = c111.searchDev()
#print devs[1]
#fd = c111.open(devs[1])