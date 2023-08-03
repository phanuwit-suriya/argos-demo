import logging
import uuid


class ErrorFormatter(logging.Formatter):
    """
    LogRecord attributes
    asctiem       %(asctime)s     Human-readable time when the LogRecord was created.
    created       %(created)f     Time when the LogRecord was created (as returned by time.time())
    filename      %(filename)s    Filename portion of pathname
    funcName      %(funcName)s    Name of function containing the logging call
    levelname     %(levelname)s   Text logging level for message ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
    levelno       %(levelno)s     Numeric logging level for the message (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    lineno        %(lineno)d      Source line number where the logging callwas issued (if avaialble)
    message       %(message)s     The logged message, computed as msg % args
    module        %(module)s      Module (name portion of filename)
    msecs         %(msecs)d       Millisecond portion of the time when the LogRecord was created
    name          %(name)s        Name of the logger used to log the call
    pathname      %(pathname)s    Full pathname of the source file where the logging call was issued (if available)
    process       %(process)d     Process ID (if available)
    processname       %(processName)s     Porcess name (if available)
    relativeCreated   %(relativeCreated)d Time in milliseconds when the LogRecord was created, relative to the time the logging module was loaded
    thread        %(thread)d      Thread ID (if available)
    threadName    %(threadName)s  Thread name (if available)
    """

    def format(self, record):
        _format = '{"timestamp": "%(asctime)s", "levelname": "%(levelname)s", "message": "%(message)s", "traceback": "%(traceback)s"},'

        if record.exc_info:
            exc_info = repr(super().formatException(record.exc_info))
            exc_info = exc_info.strip("'") \
                .replace("\\\\", "/") \
                .replace("\\'", "'") \
                .replace('"', "'")

            record.traceback = exc_info
            record.exc_info = None

        return logging.Formatter(_format).format(record)


class LogFormatter(logging.Formatter):

    def format(self, record):
        _format = '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"},'

        return logging.Formatter(_format).format(record)
