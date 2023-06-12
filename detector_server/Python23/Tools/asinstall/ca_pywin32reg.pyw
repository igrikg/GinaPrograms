"""
    Python Custom Action script for Windows installer to register the
    appropriate PyWin32 COM servers (as done by PyWin32's Wise-specific
    FinishInstall.py).

    Usage:
        pythonw -E -S ca_pywin32reg.pyw --register
                        OR
        pythonw -E -S ca_pywin32reg.pyw --unregister
    
    Notes:
        - Call with "pythonw.exe" to avoid a DOS box.
        - Call with "-E" to ignore environment variables like PYTHONHOME
          that could screw up the Python invocation.
        - Call with "-S" to NOT import site.py, which could be hosed on the
          target machine if sys.path is bogus.
"""


#---- internal logging facility

class Logger:
    """Internal logging for this module.

    By default the logging threshold is WARN and message are logged to
    /dev/null (unless a filename or stream is passed to the constructor).
    """
    DEBUG, INFO, WARN, ERROR, FATAL = range(5)
    def __init__(self, threshold=None, streamOrFileName=None):
        import types
        if threshold is None:
            self.threshold = self.WARN
        else:
            self.threshold = threshold
        if type(streamOrFileName) == types.StringType:
            self.stream = open(streamOrFileName, 'w')
            self._opennedStream = 1
        else:
            self.stream = streamOrFileName
            self._opennedStream = 0
    def close(self):
        if self._opennedStream:
            self.stream.close()
    def _getLevelName(self, level):
        levelNameMap = {
            self.DEBUG: "DEBUG",
            self.INFO: "INFO",
            self.WARN: "WARN",
            self.ERROR: "ERROR",
            self.FATAL: "FATAL",
        }
        return levelNameMap[level]
    def log(self, level, msg, *args):
        if level < self.threshold:
            return
        message = "%-5s - " % self._getLevelName(level)
        if len(args):
            message += msg % args
        else:
            message += msg
        message += "\n"
        self.stream.write(message)
        self.stream.flush()
    def debug(self, msg, *args):
        self.log(self.DEBUG, msg, *args)
    def info(self, msg, *args):
        self.log(self.INFO, msg, *args)
    def warn(self, msg, *args):
        self.log(self.WARN, msg, *args)
    def error(self, msg, *args):
        self.log(self.ERROR, msg, *args)
    def fatal(self, msg, *args):
        self.log(self.FATAL, msg, *args)
    def exception(self, msg=None, *args):
        import traceback, cStringIO
        s = cStringIO.StringIO()
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                  None, s)
        if msg:
            msg = msg + "\n" + s.getvalue()
        else:
            msg = s.getvalue()
        s.close()
        self.log(self.ERROR, msg, *args)
global log
log = None



#---- support stuff

class CustomActionError(Exception):
    pass


def _rebuildSysPath():
    """Safely rebuild sys.path presuming that the current sys.path is
    completely hosed. This can happen is, say, the environment in which this
    script is run has PYTHONHOME set to a bogus value.
    """
    import sys
    assert sys.platform.startswith("win"), "Can only do this on Windows."

    installDir = sys.executable
    while installDir[-1] != '\\':
        installDir = installDir[:-1]
    installDir = installDir[:-1]

    sys.path = ["",
                installDir + "\\Lib\\site-packages\\pythonwin",
                installDir + "\\Lib\\site-packages\\win32",
                installDir + "\\Lib\\site-packages\\win32\\Lib",
                installDir + "\\Lib\\site-packages",
                installDir + "\\DLLs",
                installDir + "\\Lib",
                installDir + "\\Lib\\plat-win",
                installDir]


def _registerCOMServer(desc, moduleName, functionName, cmdlineList):
    """Register a Python COM server.
    Gleaned from "src/PyWin32/Wise/Install Scripts/FinishInstall.py".
    """
    module = __import__(moduleName)
    for attr in moduleName.split('.')[1:]:
        module = getattr(module, attr)
    fn = getattr(module, functionName)
    sys.argv = ['ActivePython MSI Installer'] + cmdlineList
    fn()


def _unregisterCOMServer(desc, moduleName, functionName, cmdlineList):
    """Unregister a Python COM server.
    Gleaned from "src/PyWin32/Wise/Install Scripts/FinishInstall.py".
    """
    module = __import__(moduleName)
    for attr in moduleName.split('.')[1:]:
        module = getattr(module, attr)
    fn = getattr(module, functionName)
    sys.argv = ['ActivePython MSI Installer', '--unregister_info'] + cmdlineList
    fn()


#---- mainline

def main(argv):
    """(Un)Register all Python COM servers."""
    log.info("sys.path = %s", sys.path)
    log.info("argv = %s", argv)

    # Skip if cannot import win32com.
    # Given the MSI conditions for the custom action running the --unregister
    # part of this script that this action is run when win32com was never
    # installed.
    try:
        import win32com
    except ImportError:
        log.warn("Could not import win32com. My guess is this action "\
                 "was called when unintalling an ActivePython in which "\
                 "win32com had NOT been installed. Aborting.")
        return  
    
    # Process options.
    import getopt
    action = None
    optlist, dummys = getopt.getopt(argv[1:], '', ['register', 'unregister'])
    for opt, optarg in optlist:
        if opt == "--register":
            action = "register"
        elif opt == "--unregister":
            action = "unregister"
    if not action:
        raise CustomActionError("No action was specified: sys.argv=%s" % argv)

    comServers = [
        ("AXScript Engine", "win32com.axscript.client.pyscript", "Register",
         ["--debug"]),
        ("Python Interpreter", "win32com.servers.interp", "Register",
         ["--debug"]),
        ("Python Dictionary", "win32com.servers.dictionary", "Register",
         ["--debug"]),
    ]
    for args in comServers:
        if action == "register":
            log.info("Register: args=%s", args)
            _registerCOMServer(*args)
        elif action == "unregister":
            log.info("Unregister: args=%s", args)
            _unregisterCOMServer(*args)


if __name__ == '__main__':
    import sys
    _rebuildSysPath()

    # setup logging
    global log
    import tempfile, os
    scriptName = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    logFileName = os.path.join(tempfile.gettempdir(), scriptName + ".log")
    log = Logger(Logger.DEBUG, logFileName)
    
    try:
        retval = main(sys.argv)
    except:
        log.exception()
        log.info("sys.path = %s", sys.path)
        log.close()
        raise
    else:
        log.close()

    sys.exit(retval)


