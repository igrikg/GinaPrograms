#!/usr/bin/env python

import sys, os, string, array
import getpass, os.path, shutil
import gc
import socket
import time
import select
from qt import *
import Command
import copy
import Numeric 

#from RunGlobals import RunGlobals

from dasyclientGui import DasyClientMainWindow
import PyDVT
#PyDVT.SetBinding("QwtBinding")
PyDVT.SetBinding("QtBinding")
import PyDVT.View as View
import PyDVT.GraphView as GraphView
import PyDVT.Data as Data
import PyDVT.DataSelection as DataSelection
import PyDVT.Filter as Filter
from PyDVT.ImageView import *

import PyDVT.EdfFileData as EdfFileData
import EdfFile
from C111ExtendedImageView import C111ExtendedImageView
from PyDVT.Binding import Dialog,Container,Pen
from PyDVT.MeshView import MeshView,MeshFilter
from PyDVT.DataSelection import RectSelection
from Command import Command


NONE = "None" 
DEF_PORT = 12111  ;
EMPTY_IP = "xxx.xxx.xxx.xxx" 
serverIP = EMPTY_IP
serverPort = DEF_PORT
OP_MODE = "UNKNOWN" ;
VIEW = "" ;
GRAPH = "" ;

##############################################################################

class StorageParameters(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("StorageParameters")

        StorageParametersLayout = QVBoxLayout(self,11,6,"StorageParametersLayout")
        spacer = QSpacerItem(307,16,QSizePolicy.Expanding,QSizePolicy.Minimum)
        StorageParametersLayout.addItem(spacer)

        self.groupBox1 = QGroupBox(self,"groupBox1")
        groupBox1_font = QFont(self.groupBox1.font())
        groupBox1_font.setBold(1)
        groupBox1_font.setUnderline(1)
        self.groupBox1.setFont(groupBox1_font)
        self.groupBox1.setFrameShape(QGroupBox.Box)
        self.groupBox1.setFrameShadow(QGroupBox.Raised)
        self.groupBox1.setAlignment(QGroupBox.AlignAuto)
        self.groupBox1.setFlat(0)

        self.storeOnDasyServerCheckBox = QCheckBox(self.groupBox1,"storeOnDasyServerCheckBox")
        self.storeOnDasyServerCheckBox.setGeometry(QRect(20,20,280,20))
        storeOnDasyServerCheckBox_font = QFont(self.storeOnDasyServerCheckBox.font())
        storeOnDasyServerCheckBox_font.setBold(0)
        storeOnDasyServerCheckBox_font.setUnderline(0)
        self.storeOnDasyServerCheckBox.setFont(storeOnDasyServerCheckBox_font)
        self.storeOnDasyServerCheckBox.setChecked(1)

        self.filesHeaderLineEdit = QLineEdit(self.groupBox1,"filesHeaderLineEdit")
        self.filesHeaderLineEdit.setGeometry(QRect(190,110,110,20))
        filesHeaderLineEdit_font = QFont(self.filesHeaderLineEdit.font())
        filesHeaderLineEdit_font.setUnderline(0)
        self.filesHeaderLineEdit.setFont(filesHeaderLineEdit_font)
        self.filesHeaderLineEdit.setFrameShape(QLineEdit.LineEditPanel)
        self.filesHeaderLineEdit.setFrameShadow(QLineEdit.Sunken)

        self.localDirLineEdit = QLineEdit(self.groupBox1,"localDirLineEdit")
        self.localDirLineEdit.setGeometry(QRect(180,80,120,20))
        localDirLineEdit_font = QFont(self.localDirLineEdit.font())
        localDirLineEdit_font.setUnderline(0)
        self.localDirLineEdit.setFont(localDirLineEdit_font)
        self.localDirLineEdit.setFrameShape(QLineEdit.LineEditPanel)
        self.localDirLineEdit.setFrameShadow(QLineEdit.Sunken)

        self.textLabel3 = QLabel(self.groupBox1,"textLabel3")
        self.textLabel3.setGeometry(QRect(10,80,160,20))
        textLabel3_font = QFont(self.textLabel3.font())
        textLabel3_font.setBold(0)
        textLabel3_font.setUnderline(0)
        self.textLabel3.setFont(textLabel3_font)
        self.textLabel3.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        self.textLabel4 = QLabel(self.groupBox1,"textLabel4")
        self.textLabel4.setGeometry(QRect(20,110,170,21))
        textLabel4_font = QFont(self.textLabel4.font())
        textLabel4_font.setBold(0)
        textLabel4_font.setUnderline(0)
        self.textLabel4.setFont(textLabel4_font)

        self.blockSizeSpinBox = QSpinBox(self.groupBox1,"blockSizeSpinBox")
        self.blockSizeSpinBox.setGeometry(QRect(20,50,32,21))
        self.blockSizeSpinBox.setMaxValue(8)
        self.blockSizeSpinBox.setMinValue(1)

        self.textLabel2 = QLabel(self.groupBox1,"textLabel2")
        self.textLabel2.setGeometry(QRect(60,50,210,21))
        textLabel2_font = QFont(self.textLabel2.font())
        textLabel2_font.setBold(0)
        textLabel2_font.setUnderline(0)
        self.textLabel2.setFont(textLabel2_font)

        self.uniqFileIdCheckBox = QCheckBox(self.groupBox1,"uniqFileIdCheckBox")
        self.uniqFileIdCheckBox.setGeometry(QRect(20,140,270,20))
        uniqFileIdCheckBox_font = QFont(self.uniqFileIdCheckBox.font())
        uniqFileIdCheckBox_font.setBold(0)
        uniqFileIdCheckBox_font.setUnderline(0)
        self.uniqFileIdCheckBox.setFont(uniqFileIdCheckBox_font)
        StorageParametersLayout.addWidget(self.groupBox1)
        spacer_2 = QSpacerItem(307,16,QSizePolicy.Expanding,QSizePolicy.Minimum)
        StorageParametersLayout.addItem(spacer_2)

        self.groupBox2 = QGroupBox(self,"groupBox2")
        groupBox2_font = QFont(self.groupBox2.font())
        groupBox2_font.setBold(1)
        groupBox2_font.setUnderline(1)
        self.groupBox2.setFont(groupBox2_font)
        self.groupBox2.setFrameShape(QGroupBox.Box)
        self.groupBox2.setFrameShadow(QGroupBox.Raised)

        self.textLabel5 = QLabel(self.groupBox2,"textLabel5")
        self.textLabel5.setGeometry(QRect(20,30,110,20))
        textLabel5_font = QFont(self.textLabel5.font())
        textLabel5_font.setBold(0)
        textLabel5_font.setUnderline(0)
        self.textLabel5.setFont(textLabel5_font)

        self.textLabel5_3 = QLabel(self.groupBox2,"textLabel5_3")
        self.textLabel5_3.setGeometry(QRect(20,90,110,20))
        textLabel5_3_font = QFont(self.textLabel5_3.font())
        textLabel5_3_font.setBold(0)
        textLabel5_3_font.setUnderline(0)
        self.textLabel5_3.setFont(textLabel5_3_font)

        self.textLabel5_2 = QLabel(self.groupBox2,"textLabel5_2")
        self.textLabel5_2.setGeometry(QRect(20,60,120,20))
        textLabel5_2_font = QFont(self.textLabel5_2.font())
        textLabel5_2_font.setBold(0)
        textLabel5_2_font.setUnderline(0)
        self.textLabel5_2.setFont(textLabel5_2_font)

        self.textLabel5_3_2 = QLabel(self.groupBox2,"textLabel5_3_2")
        self.textLabel5_3_2.setGeometry(QRect(20,120,110,20))
        textLabel5_3_2_font = QFont(self.textLabel5_3_2.font())
        textLabel5_3_2_font.setBold(0)
        textLabel5_3_2_font.setUnderline(0)
        self.textLabel5_3_2.setFont(textLabel5_3_2_font)

        self.ftpHostLineEdit = QLineEdit(self.groupBox2,"ftpHostLineEdit")
        self.ftpHostLineEdit.setGeometry(QRect(141,31,160,20))
        ftpHostLineEdit_font = QFont(self.ftpHostLineEdit.font())
        ftpHostLineEdit_font.setUnderline(0)
        self.ftpHostLineEdit.setFont(ftpHostLineEdit_font)
        self.ftpHostLineEdit.setAlignment(QLineEdit.AlignHCenter)

        self.ftpUserLineEdit = QLineEdit(self.groupBox2,"ftpUserLineEdit")
        self.ftpUserLineEdit.setGeometry(QRect(140,60,160,20))
        ftpUserLineEdit_font = QFont(self.ftpUserLineEdit.font())
        ftpUserLineEdit_font.setUnderline(0)
        self.ftpUserLineEdit.setFont(ftpUserLineEdit_font)
        self.ftpUserLineEdit.setAlignment(QLineEdit.AlignHCenter)

        self.ftpPassLineEdit = QLineEdit(self.groupBox2,"ftpPassLineEdit")
        self.ftpPassLineEdit.setGeometry(QRect(140,90,160,20))
        ftpPassLineEdit_font = QFont(self.ftpPassLineEdit.font())
        ftpPassLineEdit_font.setUnderline(0)
        self.ftpPassLineEdit.setFont(ftpPassLineEdit_font)
        self.ftpPassLineEdit.setEchoMode(QLineEdit.Password)
        self.ftpPassLineEdit.setAlignment(QLineEdit.AlignHCenter)

        self.ftpDirLineEdit = QLineEdit(self.groupBox2,"ftpDirLineEdit")
        self.ftpDirLineEdit.setGeometry(QRect(140,120,160,20))
        ftpDirLineEdit_font = QFont(self.ftpDirLineEdit.font())
        ftpDirLineEdit_font.setUnderline(0)
        self.ftpDirLineEdit.setFont(ftpDirLineEdit_font)
        self.ftpDirLineEdit.setAlignment(QLineEdit.AlignHCenter)
        StorageParametersLayout.addWidget(self.groupBox2)

        self.buttonGroup1 = QButtonGroup(self,"buttonGroup1")
        self.buttonGroup1.setFrameShadow(QButtonGroup.Raised)

        self.okPushButton = QPushButton(self.buttonGroup1,"okPushButton")
        self.okPushButton.setGeometry(QRect(10,10,60,26))

        self.closePushButton = QPushButton(self.buttonGroup1,"closePushButton")
        self.closePushButton.setGeometry(QRect(130,10,82,26))

        self.cancelPushButton = QPushButton(self.buttonGroup1,"cancelPushButton")
        self.cancelPushButton.setGeometry(QRect(220,10,80,26))
        StorageParametersLayout.addWidget(self.buttonGroup1)

        self.languageChange()

        self.resize(QSize(333,482).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.cancelPushButton,SIGNAL("clicked()"),self,SLOT("reject()"))
        self.connect(self.closePushButton,SIGNAL("clicked()"),self,SLOT("close()"))
        self.connect(self.okPushButton,SIGNAL("clicked()"),self.okPushed)
        #self.connect(self.localDirLineEdit,SIGNAL("lostFocus()"),self.validateLocalDir)
        self.connect(self.localDirLineEdit,SIGNAL("returnPressed()"),self.validateLocalDir)
        self.params = { } ;
        self.params["ok"]  = False ;
        self.params["dasy_store"] = 1 ;
        self.params["block_size"] = 4 ;
        self.params["local_dir"] = "C:\\TEMP" ;
        self.params["header"] = "DASY" ;
        self.params["uniq_id"] = 1 ;
         
        self.params["ftp_host"]  = "www.esrf.fr" ;
        self.params["ftp_login"] = "guest"  ;
        self.params["ftp_pass"] = "anonymous" ;
        self.params["ftp_dir"] = "/tmp" ;


    def languageChange(self):
        self.setCaption(self.__tr("Data transfer/storage parameters"))
        self.groupBox1.setTitle(self.__tr("Data transfer parameters "))
        self.storeOnDasyServerCheckBox.setText(self.__tr(" Store data files on DasyServer computer ( C:\\TEMP )"))
        QToolTip.add(self.storeOnDasyServerCheckBox,self.__tr("If not checked data files are distroyed on DasyServer computer "))
        self.filesHeaderLineEdit.setText(self.__tr(" DASY"))
        QToolTip.add(self.filesHeaderLineEdit,self.__tr("A string used as header for data files names on lacal computer "))
        self.localDirLineEdit.setText(self.__tr(" C:\\TEMP"))
        QToolTip.add(self.localDirLineEdit,self.__tr("The directory where data files are stored on the local computer "))
        self.textLabel3.setText(self.__tr("  Local DIR for data files storage :"))
        QToolTip.add(self.textLabel3,self.__tr("The directory where data files are stored on the local computer"))
        self.textLabel4.setText(self.__tr("Header for local data files names :"))
        QToolTip.add(self.textLabel4,self.__tr("A string used as header for data files names on lacal computer "))
        QToolTip.add(self.blockSizeSpinBox,self.__tr("The block size used for data transfers between DasyServer and the client "))
        self.textLabel2.setText(self.__tr(" Block size for data transfers ( in Kbytes )"))
        QToolTip.add(self.textLabel2,self.__tr("The block size used for data transfers between DasyServer and the client "))
        self.uniqFileIdCheckBox.setText(self.__tr(" Give each local data file a uniq identifier"))
        QToolTip.add(self.uniqFileIdCheckBox,self.__tr("If not checked the same file will be overwritten "))
        self.groupBox2.setTitle(self.__tr(" FTP transfer parameters "))
        self.textLabel5.setText(self.__tr("FTP host for tansfers :"))
        QToolTip.add(self.textLabel5,self.__tr("A host name or a complete valid IP address "))
        self.textLabel5_3.setText(self.__tr("FTP password of login :"))
        QToolTip.add(self.textLabel5_3,self.__tr("A valid password for the above user on the yet above computer "))
        self.textLabel5_2.setText(self.__tr("FTP login for transfers :"))
        QToolTip.add(self.textLabel5_2,self.__tr("A valid user name to connect to above computer "))
        self.textLabel5_3_2.setText(self.__tr("FTP dir on FTP host:"))
        QToolTip.add(self.textLabel5_3_2,self.__tr("A valid and FTP writable directory for data files "))
        self.ftpHostLineEdit.setText(self.__tr("www.esrf.fr"))
        QToolTip.add(self.ftpHostLineEdit,self.__tr("The host where DasyServer stores data files "))
        self.ftpUserLineEdit.setText(self.__tr("guest "))
        QToolTip.add(self.ftpUserLineEdit,self.__tr("The user name DasyServer uses to open FTP transfer "))
        self.ftpPassLineEdit.setText(self.__tr("anonymous"))
        QToolTip.add(self.ftpPassLineEdit,self.__tr("The password DasyServer uses for FTP connection "))
        self.ftpDirLineEdit.setText(self.__tr("\\tmp"))
        QToolTip.add(self.ftpDirLineEdit,self.__tr("The directory DasyServer uses for data files  "))
        self.buttonGroup1.setTitle(QString.null)
        self.okPushButton.setText(self.__tr("OK"))
        self.closePushButton.setText(self.__tr("CLOSE"))
        self.cancelPushButton.setText(self.__tr("CANCEL"))
        
    def setStorParams(self, dictp):
        
        if( dictp["dasy_store"] == 1 ):
            self.storeOnDasyServerCheckBox.setChecked(True)
        else:
            self.storeOnDasyServerCheckBox.setChecked(False)
        
        self.blockSizeSpinBox.setValue( int( dictp["block_size"]) ) ;
        self.localDirLineEdit.setText( str(dictp["local_dir"] ) ) ;
        self.filesHeaderLineEdit.setText( str(dictp["header"] ) ) ;
        
        if( dictp["uniq_id"] == 1 ):
            self.uniqFileIdCheckBox.setChecked(True);
        else:
            self.uniqFileIdCheckBox.setChecked(False);
         
        self.ftpHostLineEdit.setText ( str( dictp["ftp_host"] ) ) ;
        self.ftpUserLineEdit.setText ( str( dictp["ftp_login"] ) ) ;
        self.ftpPassLineEdit.setText ( str( dictp["ftp_pass"] ) ) ;
        self.ftpDirLineEdit.setText ( str( dictp["ftp_dir"] ) ) ;
        self.params["ok"] = False ;
        
    def getStorParams(self):
        return( self.params ) ;


    def validateLocalDir(self):
        #print "StorageParameters.validateLocalDir(): Not implemented yet"
        if( os.path.exists( str(self.localDirLineEdit.text()) ) == False ):
            QMessageBox.warning(self,"Warning",self.trUtf8("This directory does not exist ! Please change!"))
            return self


    def okPushed(self):
        #print "StorageParameters.okPushed(): Not implemented yet"
        if( os.path.exists( str( self.localDirLineEdit.text() ) ) == False ):
            QMessageBox.warning(self,"Warning",self.trUtf8("This directory does not exist ! Please change!"))
            return self
            
        self.params["ok"] = True ;
        if( self.storeOnDasyServerCheckBox.isChecked() ):
            self.params["dasy_store"] = 1 ;
        else:
            self.params["dasy_store"] = 0 ;
            
        self.params["block_size"] = self.blockSizeSpinBox.value( ) ;
        self.params["local_dir"] = str( self.localDirLineEdit.text() ) ;
        self.params["header"] = str( self.filesHeaderLineEdit.text() ) ;
        
        if( self.uniqFileIdCheckBox.isChecked()  ):
            self.params["uniq_id"] = 1 ;
        else:
            QMessageBox.information(self,"Information",
                self.trUtf8("The local file will be overwritten for each DATA transfer.\n"))
            self.params["uniq_id"] = 0 ;
        
        self.params["ftp_host"]  = str( self.ftpHostLineEdit.text() ) ;
        self.params["ftp_login"] = str( self.ftpUserLineEdit.text() ) ;
        self.params["ftp_pass"] = str( self.ftpPassLineEdit.text() ) ;
        self.params["ftp_dir"] = str( self.ftpDirLineEdit.text() ) ;
        #print self.params ;
        self.close() ;

    def __tr(self,s,c = None):
        return qApp.translate("StorageParameters",s,c)
        
#######################################################################################################

class RemoteParams(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)
        
        if not name:
            self.setName("RemoteParams")

        self.line1 = QFrame(self,"line1")
        self.line1.setGeometry(QRect(10,70,271,20))
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)

        self.PortLabel = QLabel(self,"PortLabel")
        self.PortLabel.setGeometry(QRect(50,50,121,21))
        PortLabel_font = QFont(self.PortLabel.font())
        PortLabel_font.setBold(1)
        self.PortLabel.setFont(PortLabel_font)
        self.PortLabel.setFrameShape(QLabel.Box)
        self.PortLabel.setFrameShadow(QLabel.Plain)
        self.PortLabel.setLineWidth(1)
        self.PortLabel.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        self.CANCELButton = QPushButton(self,"CANCELButton")
        self.CANCELButton.setGeometry(QRect(210,90,60,21))

        self.OKButton = QPushButton(self,"OKButton")
        self.OKButton.setGeometry(QRect(20,90,50,21))

        self.CLOSEButton = QPushButton(self,"CLOSEButton")
        self.CLOSEButton.setGeometry(QRect(80,90,60,21))

        self.IPaddrLabel = QLabel(self,"IPaddrLabel")
        self.IPaddrLabel.setGeometry(QRect(10,20,161,21))
        IPaddrLabel_font = QFont(self.IPaddrLabel.font())
        IPaddrLabel_font.setBold(1)
        self.IPaddrLabel.setFont(IPaddrLabel_font)
        self.IPaddrLabel.setFrameShape(QLabel.Box)
        self.IPaddrLabel.setFrameShadow(QLabel.Plain)
        self.IPaddrLabel.setLineWidth(1)
        self.IPaddrLabel.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        self.PortSpinBox = QSpinBox(self,"PortSpinBox")
        self.PortSpinBox.setGeometry(QRect(170,50,80,21))
        self.PortSpinBox.setMaxValue(100000)
        self.PortSpinBox.setMinValue(1)
        self.PortSpinBox.setValue(7)

        self.lineEdit1 = QLineEdit(self,"lineEdit1")
        self.lineEdit1.setGeometry(QRect(170,20,100,21))
        self.lineEdit1.setAlignment(QLineEdit.AlignHCenter)

        self.languageChange()

        self.resize(QSize(291,126).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.OKButton,SIGNAL("clicked()"), self.okParams )
        self.connect(self.CLOSEButton,SIGNAL("clicked()"),self,SLOT("close()"))
        self.connect(self.CANCELButton,SIGNAL("clicked()"),self,SLOT("reject()"))
        self.connect(self.lineEdit1,SIGNAL("returnPressed()"), self.okParams)

    def languageChange(self):
        global serverPort
        global serverIP
        
        self.setCaption(self.__tr("Remote Server Parameters Configuration"))
        self.PortLabel.setText(self.__tr("  DASY Server port :"))
        self.CANCELButton.setText(self.__tr("Cancel"))
        self.OKButton.setText(self.__tr("OK"))
        self.CLOSEButton.setText(self.__tr("Close"))
        self.IPaddrLabel.setText(self.__tr("  DASY Server  IP address :"))
        self.lineEdit1.setText(self.__tr(str(serverIP)) )
        self.PortSpinBox.setValue(serverPort)

    def __tr(self,s,c = None):
        return qApp.translate("RemoteParams",s,c)
        
    def okParams(self):
        global serverPort
        global serverIP
        
        #print "OK PARAMS"
        serverPort = self.PortSpinBox.value()
        ipaddr = self.lineEdit1.text()
        if( len(ipaddr) > 0 ):
            serverIP = ipaddr
        self.close() ;
        return;
        
###########################################################################

class MyView(C111ExtendedImageView):
#class MyView(PyDVT.ExtendedImageView):
#class MyView(QSplitter):
# Constructor
# ~~~~~~~~~~~
    def __init__(self, *args):
        apply(C111ExtendedImageView.__init__,(self,) + args)
    #apply(ExtendedImageView.__init__,(self,) , { "SelectionCallback":1, })
        
# Destructor
# ~~~~~~~~~~
    def __del__(self, *args):
        pass
    
    def EventSelection(self,source):    
        global VIEW
        global GRAPH
        
        sel=source.GetDataSelection()
        if sel==None:
            return
        
        et = source.GetType( )
        if (et=="Rect"):
                if (hasattr(self,"Dialog3d")==0) or self.Dialog3d.IsVisible()==0:
                        self.Dialog3d=MeshView(None)
                        self.Dialog3d.SetSize(600,400)
                        self.Dialog3d.Show()
                        self.Dialog3d.setFocus()
                self.Dialog3d.SetSource(MeshFilter(None,sel)) 
                self.Dialog3d.Show()
        else:
            GRAPH.Show()
            GRAPH.SetSource(GraphView.GraphFilter("",sel,pen=Pen((255,0,0),0,"solid")))
            
            VIEW.Update()
            return

    def focusInEvent (self,e):
        self.GetDrawable().setFocus()
        VIEW.Update()
    
    
############################################################################

def Hostname():
  return socket.gethostname()

class SocketError(Exception):
  pass

class Socket:
  def __init__(self,host=Hostname(),port=10000,verbose=1):
    self.host=host
    self.port=port
    self.SocketError=SocketError()
    self.verbose=verbose
    try:
      if self.verbose:print 'SocketUtils:Creating Socket()'
      self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error,msg:
      raise SocketError,'Error in Socket Object Creation!!'
    
  def Close(self):
    if self.verbose:print 'SocketUtils:Closing socket!!'
    self.sock.close()
    if self.verbose:print 'SocketUtils:Socket Closed!!'
    
  def __str__(self):
    return 'SocketUtils.Socket\nSocket created on Host='+str(self.host)+',Port='+str(self.port)

class SocketClient(Socket):
  def Connect(self,rhost=Hostname(),rport=10000):
    self.rhost,self.rport=rhost,rport
    try:
      if self.verbose:print 'Connecting to '+str(self.rhost)+' on port '+str(self.rport)
      self.sock.connect((self.rhost,self.rport))
      if self.verbose: print 'Connected !!!'
      socket.setdefaulttimeout(300) ;   
    except socket.error,msg:
      raise SocketError,'Connection refused to '+str(self.rhost)+' on port '+str(self.rport)

  def Send(self,data):
        try:
            #if self.verbose:print 'Sending data of size ',len(data)
            self.sock.send(data)
            #if self.verbose: print 'Data sent:' + data
        except socket.error,msg:
            raise SocketError,msg

  def Receive(self,size=1024):
    #if self.verbose: print 'Receiving data...'
    try:
        return self.sock.recv(size)
    except socket.error,msg:
        raise SocketError,msg

  def __str__(self):
    return 'SocketUtils.SocketClient\nClient connected to Host='+str(self.rhost)+',Port='+str(self.rport)

###################################################################################

class DasyClientMainWindowImpl(DasyClientMainWindow):
    def __init__(self, *args):
        global VIEW
        global GRAPH
        
        apply(DasyClientMainWindow.__init__,(self,) + args)
        self.sc = "None"
        
        self.CMD_CLEAR = "CLEAR" ;
        self.CMD_START = "START" ;
        self.CMD_STOP = "STOP" ;
        self.CMD_STATS = "STATS" ;
        self.CMD_DATA = "DATA" ;
        self.CMD_CFG = "CFG";
        self.CMD_EXIT = "EXIT" ;
        self.CMD_BSIZE = "BSIZE" ;
        self.CMD_PFTP = "PFTP";
        self.CMD_FTP = "FTP";
        self.CMD_STORE = "STOR" ;
        
        self.stor_params = { } ;
        self.stor_params["dasy_store"] = 1 ;
        self.stor_params["block_size"] = 4 ;
        self.stor_params["local_dir"] = "C:\\TEMP" ;self.stor_params["local_dir"]
        self.stor_params["header"] = "DASY" ;
        self.stor_params["uniq_id"] = 1 ;
         
        self.stor_params["ftp_host"]  = "www.esrf.fr" ;
        self.stor_params["ftp_login"] = "guest"  ;
        self.stor_params["ftp_pass"] = "anonymous" ;
        self.stor_params["ftp_dir"] = "/tmp" ;
        
        self.img_dir = self.stor_params["local_dir"] ;
        
        self.statusTextLabel.setText("NOT CONNECTED") ;
        VIEW = MyView( )
        GRAPH = GraphView.GraphView(None,
        {"AddStyleSelect":1,"AddStatus":1,"AutoHideStatus":1,"AddCursorSelect":1,"AddLog":0})
        GRAPH.AddMenuPopupItem("Toggle Log X",self.Log_X)
        GRAPH.AddMenuPopupItem("Toggle Log Y",self.Log_Y)
        GRAPH.SetSize(300 , 200)
        #self.stor_dialg = StorageParameters(self,  "STORPARS", 0 , Qt.WType_Dialog) ;
        
        
    # For the graph display option:
# -----------------------------
    def Log_X(self):
        global GRAPH

        self.graph.LogX = not self.graph.LogX
        if self.graph.LogX:
            self.graph.SetXScaleLog()
        else:
            self.graph.SetXScaleLinear()
        self.graph.Update()
    
    def Log_Y(self):
        global GRAPH
        
        self.graph.LogY = not self.graph.LogY
        if self.graph.LogY:
            self.graph.SetYScaleLog(1.0)
        else:
            self.graph.SetYScaleLinear()
        self.graph.Update()

        
    def connectServer(self, *args):
        global constg ;
        global serverPort;
        global serverIP;
        
        if( serverIP ==  EMPTY_IP  ):
            #print "Enter connection params first"
            #return
            self.statusTextLabel.setText("NOT CONNECTED") ;
            rempars_dialg = RemoteParams(self,  "REMPARS", 0 , Qt.WType_Dialog) 
            rempars_dialg.show()
            rempars_dialg.exec_loop
            return
        
        if( self.sc == NONE ):
            print "Connection to: " , serverIP , " on port: " ,  serverPort , "\n" 
            strlog = "Connecting ...."
            strlog = "Connection to: " + str(serverIP) +  " on port: " +  str(serverPort) + "\n"  ;
            self.logTextEdit.append(strlog)
            try:
                self.sc = SocketClient()
                self.sc.Connect(str(serverIP), serverPort )
                self.statusTextLabel.setText("CONNECTED") ;
            except SocketError,msg:
                #print "Socket Error: ", msg
                self.logTextEdit.append("SOCKET ERROR: " + str(msg) + "\n")
                self.statusTextLabel.setText("SOCKET ERROR") ;
                return
         
        strlog = "Hello Dasy Server !!!"
        try:
            self.sc.Send(strlog)
            self.logTextEdit.append("SENT: "+ strlog + "\n")
        except SocketError,msg:
                #print "Socket Error: ", msg
                self.logTextEdit.append("SOCKET ERROR: " + str(msg) + "\n")
                self.statusTextLabel.setText("SOCKET ERROR") ;
                return;
         
        try:   
            strlog = self.sc.Receive()
            self.logTextEdit.append( "RECIEVED: "  + strlog + "\n")
            self.statusTextLabel.setText("READY") ;
        except SocketError,msg:
            #print "Socket Error: ", msg
            self.logTextEdit.append("SOCKET ERROR: " + str(msg) + "\n")
            self.statusTextLabel.setText("SOCKET ERROR") ;
            return ;
        self.getCfg() ;
        self.sendBsize();
        self.sendPftp() ;
        self.sendStore() ;
    
    def editStore(self, *args):
        #print "DasyClientMainWindowImpl.editStore(): Not implemented yet"
        stor_dialg = StorageParameters(self,  "STORPARS", 1 , Qt.WType_Dialog) ;
        stor_dialg.setStorParams( self.stor_params );
        stor_dialg.show()
        stor_dialg.exec_loop()
        params = stor_dialg.getStorParams()
        #print "EditStore\n" , params 
        if( params["ok"]  == True ):
            for k in self.stor_params.keys():
                self.stor_params[k] = params[k]
            
            #self.stor_params["dasy_store"] =  params["dasy_store"] ;
            #self.stor_params["block_size"] = params["block_size"] ;
            #self.stor_params["local_dir"] =  params["local_dir"] ;
            #self.stor_params["header"] =  params["header"] ;
            #self.stor_params["uniq_id"] = params["uniq_id"] ;
             
            #self.stor_params["ftp_host"]  = params["ftp_host"] ;
            #self.stor_params["ftp_login"] =  params["ftp_login"] ;
            #self.stor_params["ftp_pass"] = params["ftp_pass"] ;
            #self.stor_params["ftp_dir"] = params["ftp_dir"] ;
            #print self.stor_params ;
            
            if( self.sc != NONE ):
                self.sendBsize();
                self.sendPftp() ;
                self.sendStore() ;
        
   
    def serverHelp(self, *args):
                pid = os.spawnl( os.P_NOWAIT, "C:\Program Files\Internet Explorer\IEXPLORE.EXE"  ,  
                                                       " C:\Python23\Lib\site-packages\C111GUI-2D\DasyServerHelp.mht")
                                                            
    def viewImage(self):
        global VIEW
        global GRAPH
        
        VIEW = "" ;
        GRAPH = "" ;
        gc.collect() ;
        
        VIEW = MyView( )
        GRAPH = GraphView.GraphView(None,
        {"AddStyleSelect":1,"AddStatus":1,"AutoHideStatus":1,"AddCursorSelect":1,"AddLog":0})
        GRAPH.AddMenuPopupItem("Toggle Log X",self.Log_X)
        GRAPH.AddMenuPopupItem("Toggle Log Y",self.Log_Y)
        GRAPH.SetSize(300 , 200)
            
        fname = QFileDialog.getOpenFileName( str( self.img_dir )  , "Image files (*.edf)", 
                    self, "View Image file dialog"
                    "Choose a filename to View" )
        if fname.isEmpty():
            return
            
        d = string.split( str(fname), "/" )
        #print "D: ", d
        filename = "" 
        for i in range(len(d) -1):
            filename = filename + d[i] + "\\"
        filename = filename + d[len(d)-1]
        self.img_dir = os.path.dirname( str(filename ))
        data_2D = ""
        gc.collect()
        data_2D= EdfFileData.EdfFileData()
        data_2D.SetSource(filename)
        VIEW.SetSource(ColormapFilter(None,RectSelection(data_2D)))
        data_2D.LoadSource()
        #container.Show()
        VIEW.SetSize(800,800)
        VIEW.Show()
        VIEW.Update( )
        return
    
    def editConn(self, *args):
        rempars_dialg = RemoteParams(self,  "REMPARS", 0 , Qt.WType_Dialog) 
        rempars_dialg.show()
        rempars_dialg.exec_loop

    
    def fileExit(self, *args):
        if( self.sc != NONE ):
            self.sc.Close()
            self.statusTextLabel.setText("CONNECTION CLOSED") ;
            self.sc = "None" ;
            self.logTextEdit.append( "Connection to Dasy Server closed. \n"  )
            print ""
        else:
            self.logTextEdit.append( "No Dasy Server server connection to close ! \n"  )
        qApp.closeAllWindows()
        qApp.quit()            
    
    def getFtp(self,*args):
        size = 1024 ;
        
        if( self.sc == NONE ):
            self.logTextEdit.append( "No Dasy Server server connection opened ! \n"  )
            return ;
            
        try:
            self.sc.Send( self.CMD_FTP)
        except SocketError,msg:
            self.logTextEdit.append("SOCKET ERROR: " + str(msg) + "\n")
            return ;
         
        self.logTextEdit.append( "SENT:"  +  self.CMD_FTP  +  " \n"  )
        size_msg = self.sc.Receive(1024) ;
        if( size_msg[:10] == "FTP;NOTOK" ):
            self.logTextEdit.append( size_msg + "\n")
            return ;   

        #print "RCV FRAME: " , size_msg ;
        s1, s2  , img_size = size_msg.split(";") ;
        s1 = s1 + s2 ; 
        #print "RECV: " , s1 , " IMG_SIZE: ", img_size 
        self.sc.Send( "FTP;OK" )
        self.logTextEdit.append( "RECEIVING: " + size_msg + "\n")
        self.logTextEdit.append( "Server is transfering data file to  ... \n")  
        self.logTextEdit.append(self.stor_params["ftp_host"] +  "\n")  
        self.logTextEdit.append("In directory: "+ self.stor_params["ftp_dir"] +  "\n")  
        rcv_msg = self.sc.Receive(size) ;
        if( rcv_msg[:7] != "FTP;END" ):
            self.logTextEdit.append("Transfer failed !!!  " + rcv_msg +  "\n")  
        else:
            self.logTextEdit.append( rcv_msg +  "\n")  
            
        return ;
        
    def getData(self, *args):
        global OP_MODE ;
        
        size = 1024 * int( self.stor_params["block_size"] ) ; 
        barr = "" ; rcv_msg = "" ;   cpt = 1 ; 
        gc.collect() ;
        
        if( self.sc != NONE ):
            try:
                self.sc.Send( self.CMD_DATA )
            except SocketError,msg:
                self.logTextEdit.append("SOCKET ERROR: " + str(msg) + "\n")
                return ;
            self.logTextEdit.append( "SENT:" + self.CMD_DATA + " \n"  )
            
            self.logTextEdit.append( "DasyServer is busy reading TDC memory ....." + " \n"  )
            self.logTextEdit.append( "Please be patient  ....."  + " \n"  )
            
            pd = QProgressDialog( "DasyServer is busy reading TDC memory ....", "WAITING ....  ", 100 , self , "progr" , True )
            pd.setProgress(99);
            pd.show()
            
            size_msg = self.sc.Receive(1024) ;
            if( size_msg[:10] == "DATA;NOTOK" ):
                pd.close()
                self.logTextEdit.append( size_msg + "\n")
                return ;
        
            print "RCV FRAME: " , size_msg ;
            s1, s2  , img_size = size_msg.split(";") ;
            s1 = s1 + s2 ; 
            print "RECV: " , s1 , " IMG_SIZE: ", img_size 
            pd.close()
            self.sc.Send( "DATA;OK" )
            self.logTextEdit.append( size_msg + "\n")
            
            #self.stor_params["local_dir"] = "C:\\TEMP" ;
            #self.stor_params["header"] = "DASY" ;
            #self.stor_params["uniq_id"] = 1 ;
        
            f =  self.stor_params["local_dir"] ;
            if( f[:-1] != "\\" ): f += "\\" ;
            f += self.stor_params["header"] ;
            if ( self.stor_params["uniq_id"] == 1 ):
                tag = int(time.time())
                f = f + str( tag ) ;
            
            if( ( OP_MODE == "GFD-1D" ) or ( OP_MODE == "MHIT" ) or ( OP_MODE == "MHIP" ) ) :
                f = f + ".data" ;
            else:
                f = f +  ".edf" ;
            len_rcv = 0 ;
            fp = open( f , 'wb' ) ;
            fp.close();
            self.logTextEdit.append( "RECIEVING DATA BLOCKS ... \n")  
            fp = open( f , 'wb' ) ; 
            nb_blocks = int(int(img_size) / size)
            
            while( 1 ):
                rcv_msg = "" ; 
                rcv_msg = self.sc.Receive(size) ;
                if( rcv_msg[:8] != "DATA;END" ):
                    len_rcv += len(rcv_msg);
                    if( len_rcv > int(img_size) ):
                        msg = "data size received: " + str(len_rcv) + " Too big !!! Close connection !!!"  ;
                        self.logTextEdit.append( msg )
                        self.sc.Close() ;
                        break ;
                    if ( (cpt % 100) == 0 ):
                        msg = "rcv block: " + str(cpt) + " "  + "data size received: " + str(len_rcv)  ;
                        self.logTextEdit.append( msg )
                    cpt += 1 ;
                    fp.write(rcv_msg) ;
                    self.sc.Send("DATA;OK");
                else: ## END DATA !!
                    break ;
                        
            fp.close();
            self.logTextEdit.append( "\n" + rcv_msg + "\n")
            self.logTextEdit.append( "STORED: "  + f + "\n")
            barr = "" ; rcv_msg = "" ;
            gc.collect() ;
        else:
            self.logTextEdit.append( "No Dasy Server server connection opened ! \n"  )
            
    def getCfg(self, *args):
        global OP_MODE
        
        if( self.sc != NONE ):
            f = "C:\\TEMP\\DasyServer.cfg" ;
            fp = open( f , 'wb' )
            try:
                self.sc.Send( self.CMD_CFG )
            except SocketError,msg:
                self.logTextEdit.append("SOCKET ERROR: " + str(msg) + "\n")
                return ;
                
            self.logTextEdit.append( "SENT:" + self.CMD_CFG + " \n"  )
            barr = self.sc.Receive(256*1024) ;
            self.logTextEdit.append( "GET CONFIG: \n"  )
            self.logTextEdit.append( barr  )
            self.logTextEdit.append( "\nEND CONFIG: \n"  )
            fp.write(barr) ;
            fp.close();
            self.logTextEdit.append( "STORED: "  + f + "\n")
            file = open( f ,'r')
            for line in file:
                #print line
                #print line[:13] ;
                if( (line[:13] == "operationmode") or (line[:13] == "OPERATIONMODE") ) :
                    line = string.rstrip( line , "\n" ) ;
                    #print line[-5:] ;
                    if( line[-4:] == "MHIT" or line[-4:] == "mhit" ) :
                        #print "GET OPERATIONMODE AS MHIT"  ;
                        OP_MODE = "MHIT" ;
                    if( line[-4:] == "MHIP" or line[-4:] == "mhip" ) :
                        #print "GET OPERATIONMODE AS MHIP"  ;
                        OP_MODE = "MHIP" ;
                    if( line[-3:] == "GFD" or line[-3:] == "gfd" ) :
                        #print "GET OPERATIONMODE AS GFD-2D"  ;
                        OP_MODE = "GFD-2D" ;
                    if( line[-5:] == "GFD1D" or line[-5:] == "gfd1d" ) :
                        #print "GET OPERATIONMODE AS GFD-1D"  ;
                        OP_MODE = "GFD-1D" ;
            file.close()
            status = "READY: "+ OP_MODE ;
            
            self.statusTextLabel.setText(status) ;
        else:
            self.logTextEdit.append( "No Dasy Server server connection opened ! \n"  )
    
    def helpAbout(self, *args):
        print "DasyClientMainWindowImpl.helpAbout(): Not implemented yet"
    
    def fileKill(self, *args):
        if( self.sc != NONE ):
            try:
                self.sc.Send( self.CMD_EXIT )
                self.logTextEdit.append( "SENT:" + self.CMD_EXIT + " \n"  )
            except SocketError,msg:
            #print "Socket Error: ", msg
                self.logTextEdit.append("SOCKET ERROR: " + str(msg) + "\n")
            
            try:
                strlog = self.sc.Receive()
                self.logTextEdit.append( "RECIEVED: "  + strlog + "\n")
            except SocketError,msg:
            #print "Socket Error: ", msg
                self.logTextEdit.append("SOCKET ERROR: " + str(msg) + "\n")
                
            self.sc.Close()
            self.statusTextLabel.setText("CONNECTION CLOSED") ;
            self.sc = "None" ;
            self.logTextEdit.append( "Connection to Dasy Server closed. \n"  )
            print ""
        else:
            self.logTextEdit.append( "No Dasy Server server connection to close ! \n"  )
            
    def leaveServer(self, *args):
        if( self.sc != NONE ):  
            self.sc.Close()
            self.statusTextLabel.setText("CONNECTION CLOSED") ;
            self.sc = NONE ;
            self.logTextEdit.append( "Connection to Dasy Server closed. \n"  )
            print ""
        else:
            self.logTextEdit.append( "No Dasy Server server connection to close ! \n"  )
            
    def sendClear(self, *args):
        if( self.sc != NONE ):
            try:
                self.sc.Send( self.CMD_CLEAR )
                self.logTextEdit.append( "SENT:" + self.CMD_CLEAR + " \n"  )
            except SocketError,msg:
            #print "Socket Error: ", msg
                self.logTextEdit.append("SOCKET ERROR: " + str(msg) + "\n")
            
            try:
                strlog = self.sc.Receive()
                self.logTextEdit.append( "RECIEVED: "  + strlog + "\n")
            except SocketError,msg:
            #print "Socket Error: ", msg
                self.logTextEdit.append("SOCKET ERROR: " + str(msg) + "\n")
                
        else:
            self.logTextEdit.append( "No Dasy Server server connection opened ! \n"  )
    
    def sendStart(self, *args):
        if( self.sc != NONE ):
            try:
                self.sc.Send( self.CMD_START )
                self.logTextEdit.append( "SENT:" + self.CMD_START + " \n"  )
            except SocketError,msg:
            #print "Socket Error: ", msg
                self.logTextEdit.append("SOCKET ERROR: " + str(msg) + "\n")
            
            try:
                strlog = self.sc.Receive()
                self.logTextEdit.append( "RECIEVED: "  + strlog + "\n")
            except SocketError,msg:
            #print "Socket Error: ", msg
                self.logTextEdit.append("SOCKET ERROR: " + str(msg) + "\n")
                
        else:
            self.logTextEdit.append( "No Dasy Server server connection opened ! \n"  )

    
    def sendPftp(self, *args):
        
        if( self.sc != NONE ):
            try:
                msg = self.CMD_PFTP + ";" + self.stor_params["ftp_host"] + ";" + self.stor_params["ftp_login"] ;
                msg = msg +  ";" + self.stor_params["ftp_pass"] + ";" + self.stor_params["ftp_dir"] ; 
                self.sc.Send( msg )
                self.logTextEdit.append( "SENT:" + msg + " \n"  )
            except SocketError,emsg:
            #print "Socket Error: ", msg
                self.logTextEdit.append("SOCKET ERROR: " + str(emsg) + "\n")
            
            try:
                strlog = self.sc.Receive()
                self.logTextEdit.append( "RECIEVED: "  + strlog + "\n")
            except SocketError,emsg:
            #print "Socket Error: ", msg
                self.logTextEdit.append("SOCKET ERROR: " + str(emsg) + "\n")
                
        else:
            self.logTextEdit.append( "No Dasy Server server connection opened ! \n"  )
                
    
    def sendBsize(self, *args):
        if( self.sc != NONE ):
            try:
                msg = self.CMD_BSIZE + ";" + str( self.stor_params["block_size"] ) ;
                self.sc.Send( msg )
                self.logTextEdit.append( "SENT:" + msg + " \n"  )
            except SocketError,emsg:
            #print "Socket Error: ", msg
                self.logTextEdit.append("SOCKET ERROR: " + str(emsg) + "\n")
            
            try:
                strlog = self.sc.Receive()
                self.logTextEdit.append( "RECIEVED: "  + strlog + "\n")
            except SocketError,emsg:
            #print "Socket Error: ", msg
                self.logTextEdit.append("SOCKET ERROR: " + str(emsg) + "\n")
                
        else:
            self.logTextEdit.append( "No Dasy Server server connection opened ! \n"  )
    
        
    def sendStore(self, *args):
        if( self.sc == NONE ):
            self.logTextEdit.append( "No Dasy Server server connection opened ! \n"  )
            return ;
            
        if( self.stor_params["dasy_store"]  == 1 ):
            #print "sendStore: self.store == " , self.store ;
            msg = self.CMD_STORE + ";" + str("YES") ;
        else:
            #print "senStore: self.store == " , self.store ;
            msg = self.CMD_STORE + ";" + str("NO") ;
            
        try:
            self.sc.Send( msg )
            self.logTextEdit.append( "SENT:" + msg + " \n"  )
        except SocketError,emsg:
        #print "Socket Error: ", msg
            self.logTextEdit.append("SOCKET ERROR: " + str(emsg) + "\n")
        try:
            strlog = self.sc.Receive()
            self.logTextEdit.append( "RECIEVED: "  + strlog + "\n")
        except SocketError,emsg:
        #print "Socket Error: ", msg
            self.logTextEdit.append("SOCKET ERROR: " + str(emsg) + "\n")
    
    def sendStop(self, *args):
        if( self.sc != NONE ):
            try:
                self.sc.Send( self.CMD_STOP )
                self.logTextEdit.append( "SENT:" + self.CMD_STOP + " \n"  )
            except SocketError,msg:
            #print "Socket Error: ", msg
                self.logTextEdit.append("SOCKET ERROR: " + str(msg) + "\n")
            
            try:
                strlog = self.sc.Receive()
                self.logTextEdit.append( "RECIEVED: "  + strlog + "\n")
            except SocketError,msg:
            #print "Socket Error: ", msg
                self.logTextEdit.append("SOCKET ERROR: " + str(msg) + "\n")
                
        else:
            self.logTextEdit.append( "No Dasy Server server connection opened ! \n"  )
    
    def showStats(self, *args):
        if( self.sc != NONE ):
            try:
                self.sc.Send( self.CMD_STATS )
                self.logTextEdit.append( "SENT:" + self.CMD_STATS + " \n"  )
            except SocketError,msg:
            #print "Socket Error: ", msg
                self.logTextEdit.append("SOCKET ERROR: " + str(msg) + "\n")
            
            try:
                strlog = self.sc.Receive()
                self.logTextEdit.append( "RECIEVED: \n"  + strlog + "\n")
            except SocketError,msg:
            #print "Socket Error: ", msg
                self.logTextEdit.append("SOCKET ERROR: " + str(msg) + "\n")
                
        else:
            self.logTextEdit.append( "No Dasy Server server connection opened ! \n"  )
            
    def helpAbout(self):
        QMessageBox.information(self,"Dasy Server test client",
        " Version 1.0. Author: B. Scaringella (23-12) \n Copyright (c)  2007 by  ESRF Grenoble, France")
        
        