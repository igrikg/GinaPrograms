"""
    Python Custom Action script for Windows installer to remove generated
    files on uninstall.

    Usage:
        pythonw -E -S ca_rmgen.pyw <installdir>
    
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


def _rmCompiledPythonFiles(coreSitePackages, dirName, files):
    import glob, os
    for pattern in ["*.pyc", "*.pyo"]:
        for file in glob.glob(os.path.join(dirName, pattern)):
            try:
                log.info("Removing '%s'", file)
                os.remove(file)
            except OSError:
                pass
    # Trim non-core site packages from files to prevent descending into them.
    if os.path.basename(dirName) == "site-packages":
        toRemove = []
        for file in files:
            if file not in coreSitePackages:
                toRemove.append(file)
        for file in toRemove:
            files.remove(file)


def _rmtreeOnError(rmFunction, filePath, excInfo):
    if excInfo[0] == OSError:
        # presuming because file is read-only
        os.chmod(filePath, 0777)
        rmFunction(filePath)

def _rmtree(dirname):
    import shutil
    shutil.rmtree(dirname, 0, _rmtreeOnError)



#---- mainline

def main(argv):
    """Do custom action work here."""
    log.info("sys.path = %s", sys.path)
    log.info("argv = %s", argv)

    import os, glob
    if len(argv) != 2:
        raise CustomActionError("Incorrect number of args: sys.argv=%s" % argv)
    installDir = argv[1]
    if not os.path.isdir(installDir):
        raise CustomActionError("Given install dir does not exist: '%s'"\
                                % installDir)

    # HACK: This script is trying to delete all ActivePython byte-code files.
    # The problem is that is *generates* Python byte-code files when it
    # imports modules. The only way to turn that off is to make the directory
    # read-only. Testing shows that 'shutil.pyc' is the only turd that gets
    # left, so make its dir read-only. XXX I am concerned that when uninstall
    # leaves the "Lib" dir on disk (if, for example, Lib\site-packages is
    # being used) that have "Lib" read-only might cause other problems.
    import shutil
    shutilDir = os.path.dirname(shutil.__file__)
    os.chmod(shutilDir, 0555)

    # Remove *.pyc, *.pyo for installed .py files.
    # (Be sure to NOT descend into site-packages/... dirs not installed by
    # the ActivePython core.)
    coreSitePackages = ["Pythonwin", "win32", "win32com", "win32comext",
                        "PPM"]
    log.info("Removing compiled python files.")
    os.path.walk(installDir, _rmCompiledPythonFiles, coreSitePackages)

    # Remove .chw files in the Doc dir
    for file in glob.glob(os.path.join(installDir, "Doc", "*.chw")):
        try:
            log.info("Removing '%s'", file)
            os.remove(file)
        except OSError:
            pass

    # Remove the win32com/gen_py directory.
    genPyDir = os.path.join(installDir, "Lib", "site-packages", "win32com",
                            "gen_py")
    if os.path.exists(genPyDir):
        log.info("Removing '%s'", genPyDir)
        _rmtree(genPyDir)

    # Remove the Pythonwin/pywin/default.cfc
    defaultCfc = os.path.join(installDir, "Lib", "site-packages", "Pythonwin",
                              "pywin", "default.cfc")
    try:
        if os.path.exists(defaultCfc):
            log.info("Removing '%s'", defaultCfc)
            os.remove(defaultCfc)
    except OSError:
        pass


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


