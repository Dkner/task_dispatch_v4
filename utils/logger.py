import logging

# create logger
log_path = "../log/runtime.log"
fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
datefmt = "%a %d %b %Y %H:%M:%S"
logging.basicConfig(filename=log_path, level=logging.NOTSET, format=fmt, datefmt=datefmt)
Logger = logging.getLogger("Logger")