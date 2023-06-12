# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\WinDriver\wizard\my_projects\DasyClient\DasyClientGui.ui'
#
# Created: mar. 30. oct. 09:19:06 2007
#      by: The PyQt User Interface Compiler (pyuic) 3.8
#
# WARNING! All changes made in this file will be lost!


from qt import *


class DasyClientMainWindow(QMainWindow):
    def __init__(self,parent = None,name = None,fl = 0):
        QMainWindow.__init__(self,parent,name,fl)
        self.statusBar()

        if not name:
            self.setName("DasyClientMainWindow")

        self.setCentralWidget(QWidget(self,"qt_central_widget"))
        DasyClientMainWindowLayout = QGridLayout(self.centralWidget(),1,1,11,6,"DasyClientMainWindowLayout")

        self.line1_2 = QFrame(self.centralWidget(),"line1_2")
        self.line1_2.setGeometry(QRect(20,0,321,20))
        self.line1_2.setFrameShape(QFrame.HLine)
        self.line1_2.setFrameShadow(QFrame.Sunken)
        self.line1_2.setFrameShape(QFrame.HLine)
        
        DasyClientMainWindowLayout.addMultiCellWidget(self.line1_2,0,0,0,4)

        self.statusTextLabel = QLabel(self.centralWidget(),"statusTextLabel")
        self.statusTextLabel.setGeometry(QRect(110,60,150,30))
        statusTextLabel_font = QFont(self.statusTextLabel.font())
        statusTextLabel_font.setBold(1)
        self.statusTextLabel.setFont(statusTextLabel_font)
        self.statusTextLabel.setFrameShape(QLabel.Panel)
        self.statusTextLabel.setTextFormat(QLabel.AutoText)
        self.statusTextLabel.setAlignment(QLabel.AlignCenter)
        
        DasyClientMainWindowLayout.addMultiCellWidget(self.statusTextLabel,2,2,1,3)
        

        self.startButton = QPushButton(self.centralWidget(),"startButton")
        self.startButton.setGeometry(QRect(270,60,71,30))
        self.startButton.setPaletteBackgroundColor(QColor(88,236,125))
        startButton_font = QFont(self.startButton.font())
        startButton_font.setBold(1)
        self.startButton.setFont(startButton_font)
        
        DasyClientMainWindowLayout.addWidget(self.startButton,2,4)

        self.stopButton = QPushButton(self.centralWidget(),"stopButton")
        self.stopButton.setGeometry(QRect(20,60,81,30))
        self.stopButton.setPaletteForegroundColor(QColor(255,255,255))
        self.stopButton.setPaletteBackgroundColor(QColor(255,35,35))
        
        
        pal = QPalette()
        cg = QColorGroup()
        cg.setColor(QColorGroup.Foreground,Qt.black)
        cg.setColor(QColorGroup.Button,QColor(255,35,35))
        cg.setColor(QColorGroup.Light,QColor(255,129,129))
        cg.setColor(QColorGroup.Midlight,QColor(255,65,65))
        cg.setColor(QColorGroup.Dark,QColor(127,1,1))
        cg.setColor(QColorGroup.Mid,QColor(170,1,1))
        cg.setColor(QColorGroup.Text,Qt.black)
        cg.setColor(QColorGroup.BrightText,Qt.white)
        cg.setColor(QColorGroup.ButtonText,Qt.white)
        cg.setColor(QColorGroup.Base,Qt.white)
        cg.setColor(QColorGroup.Background,QColor(212,208,200))
        cg.setColor(QColorGroup.Shadow,Qt.black)
        cg.setColor(QColorGroup.Highlight,QColor(0,0,128))
        cg.setColor(QColorGroup.HighlightedText,Qt.white)
        cg.setColor(QColorGroup.Link,Qt.black)
        cg.setColor(QColorGroup.LinkVisited,Qt.black)
        pal.setActive(cg)
        cg.setColor(QColorGroup.Foreground,Qt.black)
        cg.setColor(QColorGroup.Button,QColor(255,35,35))
        cg.setColor(QColorGroup.Light,QColor(255,129,129))
        cg.setColor(QColorGroup.Midlight,QColor(255,40,40))
        cg.setColor(QColorGroup.Dark,QColor(127,1,1))
        cg.setColor(QColorGroup.Mid,QColor(170,1,1))
        cg.setColor(QColorGroup.Text,Qt.black)
        cg.setColor(QColorGroup.BrightText,Qt.white)
        cg.setColor(QColorGroup.ButtonText,Qt.white)
        cg.setColor(QColorGroup.Base,Qt.white)
        cg.setColor(QColorGroup.Background,QColor(212,208,200))
        cg.setColor(QColorGroup.Shadow,Qt.black)
        cg.setColor(QColorGroup.Highlight,QColor(0,0,128))
        cg.setColor(QColorGroup.HighlightedText,Qt.white)
        cg.setColor(QColorGroup.Link,QColor(0,0,255))
        cg.setColor(QColorGroup.LinkVisited,QColor(255,0,255))
        pal.setInactive(cg)
        cg.setColor(QColorGroup.Foreground,QColor(128,128,128))
        cg.setColor(QColorGroup.Button,QColor(255,35,35))
        cg.setColor(QColorGroup.Light,QColor(255,129,129))
        cg.setColor(QColorGroup.Midlight,QColor(255,40,40))
        cg.setColor(QColorGroup.Dark,QColor(127,1,1))
        cg.setColor(QColorGroup.Mid,QColor(170,1,1))
        cg.setColor(QColorGroup.Text,QColor(128,128,128))
        cg.setColor(QColorGroup.BrightText,Qt.white)
        cg.setColor(QColorGroup.ButtonText,Qt.white)
        cg.setColor(QColorGroup.Base,Qt.white)
        cg.setColor(QColorGroup.Background,QColor(212,208,200))
        cg.setColor(QColorGroup.Shadow,Qt.black)
        cg.setColor(QColorGroup.Highlight,QColor(0,0,128))
        cg.setColor(QColorGroup.HighlightedText,Qt.white)
        cg.setColor(QColorGroup.Link,QColor(0,0,255))
        cg.setColor(QColorGroup.LinkVisited,QColor(255,0,255))
        pal.setDisabled(cg)
        self.stopButton.setPalette(pal)
        stopButton_font = QFont(self.stopButton.font())
        stopButton_font.setBold(1)
        self.stopButton.setFont(stopButton_font)
        
        DasyClientMainWindowLayout.addWidget(self.stopButton,2,0)

        self.line1 = QFrame(self.centralWidget(),"line1")
        self.line1.setGeometry(QRect(20,130,321,20))
        self.line1.setFrameShape(QFrame.HLine)
        self.line1.setFrameShadow(QFrame.Sunken)
        self.line1.setFrameShape(QFrame.HLine)
        
        DasyClientMainWindowLayout.addMultiCellWidget(self.line1,4,4,0,4)

        self.clearButton = QPushButton(self.centralWidget(),"clearButton")
        self.clearButton.setGeometry(QRect(140,100,91,31))
        self.clearButton.setPaletteBackgroundColor(QColor(252,168,0))
        
        DasyClientMainWindowLayout.addWidget(self.clearButton,3,2)

        self.line1_4 = QFrame(self.centralWidget(),"line1_4")
        self.line1_4.setGeometry(QRect(20,180,321,20))
        self.line1_4.setFrameShape(QFrame.HLine)
        self.line1_4.setFrameShadow(QFrame.Sunken)
        self.line1_4.setFrameShape(QFrame.HLine)
        
        DasyClientMainWindowLayout.addMultiCellWidget(self.line1_4,6,6,0,4)

        self.getFtpButton = QPushButton(self.centralWidget(),"getFtpButton")
        getFtpButton_font = QFont(self.getFtpButton.font())
        getFtpButton_font.setBold(1)
        self.getFtpButton.setFont(getFtpButton_font)

        DasyClientMainWindowLayout.addWidget(self.getFtpButton,5,2)

        self.showStatsButton = QPushButton(self.centralWidget(),"showStatsButton")
        showStatsButton_font = QFont(self.showStatsButton.font())
        showStatsButton_font.setBold(1)
        self.showStatsButton.setFont(showStatsButton_font)

        DasyClientMainWindowLayout.addMultiCellWidget(self.showStatsButton,5,5,3,4)

        self.getDataButton = QPushButton(self.centralWidget(),"getDataButton")
        getDataButton_font = QFont(self.getDataButton.font())
        getDataButton_font.setBold(1)
        self.getDataButton.setFont(getDataButton_font)

        DasyClientMainWindowLayout.addMultiCellWidget(self.getDataButton,5,5,0,1)

        self.line1_3 = QFrame(self.centralWidget(),"line1_3")
        self.line1_3.setGeometry(QRect(20,230,321,20))
        self.line1_3.setFrameShape(QFrame.HLine)
        self.line1_3.setFrameShadow(QFrame.Sunken)
        self.line1_3.setFrameShape(QFrame.HLine)
        
        DasyClientMainWindowLayout.addMultiCellWidget(self.line1_3,8,8,0,4)

        self.logTextEdit = QTextEdit(self.centralWidget(),"logTextEdit")
        self.logTextEdit.setGeometry(QRect(20,250,321,160))
        self.logTextEdit.setVScrollBarMode(QTextEdit.AlwaysOn)
        self.logTextEdit.setHScrollBarMode(QTextEdit.AlwaysOn)
        
        DasyClientMainWindowLayout.addMultiCellWidget(self.logTextEdit,9,9,0,4)

        self.closeConnButton = QPushButton(self.centralWidget(),"closeConnButton")
        self.closeConnButton.setGeometry(QRect(110,200,150,31))
        closeConnButton_font = QFont(self.closeConnButton.font())
        closeConnButton_font.setBold(1)
        self.closeConnButton.setFont(closeConnButton_font)
        
        DasyClientMainWindowLayout.addMultiCellWidget(self.closeConnButton,7,7,1,3)

        self.connectButton = QPushButton(self.centralWidget(),"connectButton")
        self.connectButton.setGeometry(QRect(140,20,90,31))
        self.connectButton.setPaletteBackgroundColor(QColor(170,255,255))
        
        DasyClientMainWindowLayout.addWidget(self.connectButton,1,2)

        #self.fileNewAction = QAction(self,"fileNewAction")
        #self.fileOpenAction = QAction(self,"fileOpenAction")
        #self.fileSaveAction = QAction(self,"fileSaveAction")
        #self.fileSaveAsAction = QAction(self,"fileSaveAsAction")
        #self.filePrintAction = QAction(self,"filePrintAction")
        self.fileExitAction = QAction(self,"fileExitAction")
        self.fileKillAction = QAction(self,"fileKillAction")
        self.fileCfgAction = QAction(self,"fileCfgAction")
        self.fileViewAction = QAction(self,"fileViewAction")
        
        #self.editUndoAction = QAction(self,"editUndoAction")
        #self.editRedoAction = QAction(self,"editRedoAction")
        self.editConnAction = QAction(self,"editConnAction")
        self.editStoreAction = QAction(self,"editStoreAction")
        #self.editPasteAction = QAction(self,"editPasteAction")
        #self.editFindAction = QAction(self,"editFindAction")
        
        #self.helpContentsAction = QAction(self,"helpContentsAction")
        #self.helpIndexAction = QAction(self,"helpIndexAction")
        self.helpAboutAction = QAction(self,"helpAboutAction")

        self.MenuBar = QMenuBar(self,"MenuBar")

        self.MenuBar.setGeometry(QRect(0,0,363,29))

        self.fileMenu = QPopupMenu(self)
        #self.fileNewAction.addTo(self.fileMenu)
        #self.fileOpenAction.addTo(self.fileMenu)
        #self.fileSaveAction.addTo(self.fileMenu)
        #self.fileSaveAsAction.addTo(self.fileMenu)
        #self.fileMenu.insertSeparator()
        #self.filePrintAction.addTo(self.fileMenu)
        
        self.fileCfgAction.addTo(self.fileMenu)
        self.fileViewAction.addTo(self.fileMenu)
        self.fileKillAction.addTo(self.fileMenu)
        self.fileMenu.insertSeparator()
        self.fileExitAction.addTo(self.fileMenu)
        
        self.MenuBar.insertItem(QString(""),self.fileMenu,2)

        self.EditMenu = QPopupMenu(self)
        #self.editUndoAction.addTo(self.EditMenu)
        #self.editRedoAction.addTo(self.EditMenu)
        #self.EditMenu.insertSeparator()
        self.editConnAction.addTo(self.EditMenu)
        self.editStoreAction.addTo(self.EditMenu)
        #self.editPasteAction.addTo(self.EditMenu)
        #self.EditMenu.insertSeparator()
        #self.editFindAction.addTo(self.EditMenu)
        self.MenuBar.insertItem(QString(""),self.EditMenu,3)

        self.helpMenu = QPopupMenu(self)
        #self.helpContentsAction.addTo(self.helpMenu)
        #self.helpIndexAction.addTo(self.helpMenu)
        #self.helpMenu.insertSeparator()
        self.helpAboutAction.addTo(self.helpMenu)
        self.helpMenu.insertItem( "DasyServer Help", self.serverHelp)
        self.MenuBar.insertItem(QString(""),self.helpMenu,4)
        

        self.languageChange()

        self.resize(QSize(363,483).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        #self.connect(self.fileNewAction,SIGNAL("activated()"),self.fileNew)
        #self.connect(self.fileOpenAction,SIGNAL("activated()"),self.fileOpen)
        #self.connect(self.fileSaveAction,SIGNAL("activated()"),self.fileSave)
        #self.connect(self.fileSaveAsAction,SIGNAL("activated()"),self.fileSaveAs)
        #self.connect(self.filePrintAction,SIGNAL("activated()"),self.filePrint)
        self.connect(self.fileExitAction,SIGNAL("activated()"),self.fileExit)
        self.connect(self.fileKillAction,SIGNAL("activated()"),self.fileKill)
        self.connect(self.fileCfgAction,SIGNAL("activated()"),self.getCfg)
        self.connect(self.fileViewAction,SIGNAL("activated()"),self.viewImage)
        
        #self.connect(self.editUndoAction,SIGNAL("activated()"),self.editUndo)
        #self.connect(self.editRedoAction,SIGNAL("activated()"),self.editRedo)
        self.connect(self.editConnAction,SIGNAL("activated()"),self.editConn)
        self.connect(self.editStoreAction,SIGNAL("activated()"),self.editStore)
        #self.connect(self.editPasteAction,SIGNAL("activated()"),self.editPaste)
        #self.connect(self.editFindAction,SIGNAL("activated()"),self.editFind)
        
        #self.connect(self.helpIndexAction,SIGNAL("activated()"),self.helpIndex)
        #self.connect(self.helpContentsAction,SIGNAL("activated()"),self.helpContents)
        self.connect(self.helpAboutAction,SIGNAL("activated()"),self.helpAbout)
        
        self.connect(self.connectButton,SIGNAL("clicked()"),self.connectServer)
        self.connect(self.stopButton,SIGNAL("clicked()"),self.sendStop)
        self.connect(self.startButton,SIGNAL("clicked()"),self.sendStart)
        self.connect(self.clearButton,SIGNAL("clicked()"),self.sendClear)
        self.connect(self.getDataButton,SIGNAL("clicked()"),self.getData)
        self.connect(self.showStatsButton,SIGNAL("clicked()"),self.showStats)
        self.connect(self.getFtpButton,SIGNAL("clicked()"),self.getFtp)

        self.connect(self.closeConnButton,SIGNAL("clicked()"),self.leaveServer)
        

    def languageChange(self):
        self.setCaption(self.__tr("Dasy Client GUI"))
        self.statusTextLabel.setText(self.__tr(" CONNECTION STATUS"))
        self.startButton.setText(self.__tr("START"))
        self.stopButton.setText(self.__tr("STOP"))
        self.clearButton.setText(self.__tr("CLEAR"))
        self.getDataButton.setText(self.__tr("DATA GET"))
        self.getFtpButton.setText(self.__tr("FTP GET"))
        self.showStatsButton.setText(self.__tr("SHOW STATS"))
        self.closeConnButton.setText(self.__tr("CLOSE CONNECTION"))
        self.connectButton.setText(self.__tr("CONNECT"))
        #self.fileNewAction.setText(self.__tr("New"))
        #self.fileNewAction.setMenuText(self.__tr("&New"))
        #self.fileNewAction.setAccel(self.__tr("Ctrl+N"))
        #self.fileOpenAction.setText(self.__tr("Open"))
        #self.fileOpenAction.setMenuText(self.__tr("&Open..."))
        #self.fileOpenAction.setAccel(self.__tr("Ctrl+O"))
        #self.fileSaveAction.setText(self.__tr("Save"))
        #self.fileSaveAction.setMenuText(self.__tr("&Save"))
        #self.fileSaveAction.setAccel(self.__tr("Ctrl+S"))
        #self.fileSaveAsAction.setText(self.__tr("Save As"))
        #self.fileSaveAsAction.setMenuText(self.__tr("Save &As..."))
        #self.fileSaveAsAction.setAccel(QString.null)
        #self.filePrintAction.setText(self.__tr("Print"))
        #self.filePrintAction.setMenuText(self.__tr("&Print..."))
        #self.filePrintAction.setAccel(self.__tr("Ctrl+P"))
        self.fileExitAction.setText(self.__tr("Exit"))
        self.fileExitAction.setMenuText(self.__tr("E&xit"))
        self.fileExitAction.setAccel(QString.null)
        
        self.fileKillAction.setText(self.__tr("Kill DASY Server"))
        self.fileKillAction.setMenuText(self.__tr("&Kill server"))
        self.fileKillAction.setAccel(QString.null)
        
        self.fileCfgAction.setText(self.__tr("Get server config"))
        self.fileCfgAction.setMenuText(self.__tr("&Get DASY currently used config for P/C111"))
        self.fileCfgAction.setAccel(QString.null)
        
        self.fileViewAction.setText(self.__tr("View a 2D image ( .edf file format )"))
        self.fileViewAction.setMenuText(self.__tr("&View 2D image"))
        self.fileViewAction.setAccel(QString.null)
        
        #self.editUndoAction.setText(self.__tr("Undo"))
        #self.editUndoAction.setMenuText(self.__tr("&Undo"))
        #self.editUndoAction.setAccel(self.__tr("Ctrl+Z"))
        #self.editRedoAction.setText(self.__tr("Redo"))
        #self.editRedoAction.setMenuText(self.__tr("&Redo"))
        #self.editRedoAction.setAccel(self.__tr("Ctrl+Y"))
        
        self.editConnAction.setText(self.__tr("Server IP address and port number to use "))
        self.editConnAction.setMenuText(self.__tr("&Connection parameters"))
        self.editConnAction.setAccel(self.__tr("Ctrl+P"))
        
        self.editStoreAction.setText(self.__tr("Directory for data and/or stats files storage"))
        self.editStoreAction.setMenuText(self.__tr("&Storage parameters"))
        self.editStoreAction.setAccel(self.__tr("Ctrl+S"))
        
        #self.editPasteAction.setText(self.__tr("Paste"))
        #self.editPasteAction.setMenuText(self.__tr("&Paste"))
        #self.editPasteAction.setAccel(self.__tr("Ctrl+V"))
        #self.editFindAction.setText(self.__tr("Find"))
        #self.editFindAction.setMenuText(self.__tr("&Find..."))
        #self.editFindAction.setAccel(self.__tr("Ctrl+F"))
        
        #self.helpContentsAction.setText(self.__tr("Contents"))
        #self.helpContentsAction.setMenuText(self.__tr("&Contents..."))
        #self.helpContentsAction.setAccel(QString.null)
        #self.helpIndexAction.setText(self.__tr("Index"))
        #self.helpIndexAction.setMenuText(self.__tr("&Index..."))
        #self.helpIndexAction.setAccel(QString.null)
        
        self.helpAboutAction.setText(self.__tr("About"))
        self.helpAboutAction.setMenuText(self.__tr("&About"))
        self.helpAboutAction.setAccel(QString.null)
        
        self.MenuBar.findItem(2).setText(self.__tr("&File"))
        self.MenuBar.findItem(3).setText(self.__tr("&Edit"))
        self.MenuBar.findItem(4).setText(self.__tr("&Help"))

    def fileNew(self):
        print "DasyClientMainWindow.fileNew(): Not implemented yet"

    def fileOpen(self):
        print "DasyClientMainWindow.fileOpen(): Not implemented yet"

    def fileSave(self):
        print "DasyClientMainWindow.fileSave(): Not implemented yet"

    def fileSaveAs(self):
        print "DasyClientMainWindow.fileSaveAs(): Not implemented yet"

    def fileKill(self):
        print "DasyClientMainWindow.fileKill(): Not implemented yet"

    def fileExit(self):
        print "DasyClientMainWindow.fileExit(): Not implemented yet"

    def editUndo(self):
        print "DasyClientMainWindow.editUndo(): Not implemented yet"

    def editRedo(self):
        print "DasyClientMainWindow.editRedo(): Not implemented yet"

    def editConn(self):
        print "DasyClientMainWindow.editConn(): Not implemented yet"

    def editStore(self):
        print "DasyClientMainWindow.editStore(): Not implemented yet"

    def editPaste(self):
        print "DasyClientMainWindow.editPaste(): Not implemented yet"

    def editFind(self):
        print "DasyClientMainWindow.editFind(): Not implemented yet"

    def helpIndex(self):
        print "DasyClientMainWindow.helpIndex(): Not implemented yet"

    def helpContents(self):
        print "DasyClientMainWindow.helpContents(): Not implemented yet"
        
    def serverHelp(self):
        print "DasyClientMainWindow.serverHelp(): Not implemented yet"

    def helpAbout(self):
        print "DasyClientMainWindow.helpAbout(): Not implemented yet"

    def connectServer(self):
        print "DasyClientMainWindow.connectServer(): Not implemented yet"

    def sendStop(self):
        print "DasyClientMainWindow.sendStop(): Not implemented yet"

    def sendStart(self):
        print "DasyClientMainWindow.sendStart(): Not implemented yet"

    def sendClear(self):
        print "DasyClientMainWindow.sendClear(): Not implemented yet"

    def getData(self):
        print "DasyClientMainWindow.getData(): Not implemented yet"
        
    def getCfg(self):
        print "DasyClientMainWindow.getCfg(): Not implemented yet"

    def showStats(self):
        print "DasyClientMainWindow.showStats(): Not implemented yet"

    def leaveServer(self):
        print "DasyClientMainWindow.leaveServer(): Not implemented yet"
        
    def getFtp(self):
        print "DasyClientMainWindow.getFtp(): Not implemented yet"
        
    def viewImage(self):
        print "DasyClientMainWindow.viewImage(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("DasyClientMainWindow",s,c)