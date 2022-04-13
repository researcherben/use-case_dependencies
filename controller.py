#!/usr/bin/env python3

# Ben Payne, 2021
# https://creativecommons.org/licenses/by/4.0/
# Attribution 4.0 International (CC BY 4.0)

"""
"""

import os
import json

# https://docs.python.org/3/howto/logging.html
import logging

# https://gist.github.com/ibeex/3257877
from logging.handlers import RotatingFileHandler

if __name__ == "__main__":

    # maxBytes=10000 = 10kB
    # maxBytes=100000 = 100kB
    # maxBytes=1000000 = 1MB
    # maxBytes=10000000 = 10MB
    log_size = 10000000
    # maxBytes=100000000 = 100MB
    # https://gist.github.com/ibeex/3257877
    handler_debug = RotatingFileHandler(
        "critical_and_error_and_warning_and_info_and_debug.log",
        maxBytes=log_size,
        backupCount=2,
    )
    handler_debug.setLevel(logging.DEBUG)
    handler_info = RotatingFileHandler(
        "critical_and_error_and_warning_and_info.log",
        maxBytes=log_size,
        backupCount=2,
    )
    handler_info.setLevel(logging.INFO)
    handler_warning = RotatingFileHandler(
        "critical_and_error_and_warning.log",
        maxBytes=log_size,
        backupCount=2,
    )
    handler_warning.setLevel(logging.WARNING)

    # https://docs.python.org/3/howto/logging.html
    logging.basicConfig(
        # either (filename + filemode) XOR handlers
        # filename="test.log", # to save entries to file instead of displaying to stderr
        # filemode="w", # https://docs.python.org/dev/library/functions.html#filemodes
        handlers=[handler_debug, handler_info, handler_warning],
        # if the severity level is INFO,
        # the logger will handle only INFO, WARNING, ERROR, and CRITICAL messages
        # and will ignore DEBUG messages
        level=logging.DEBUG,
        format="%(asctime)s|%(filename)-13s|%(levelname)-5s|%(lineno)-4d|%(funcName)-20s|%(message)s"  # ,
        # https://stackoverflow.com/questions/6290739/python-logging-use-milliseconds-in-time-format/7517430#7517430
        # datefmt="%m/%d/%Y %I:%M:%S %f %p", # https://strftime.org/
    )

    #    logger = logging.getLogger(__name__)

    # https://docs.python.org/3/howto/logging.html
    # if the severity level is INFO, the logger will handle only INFO, WARNING, ERROR, and CRITICAL messages and will ignore DEBUG messages
    # handler.setLevel(logging.INFO)
    # handler.setLevel(logging.DEBUG)

    logger = logging.getLogger(__name__)

    # http://matplotlib.1069221.n5.nabble.com/How-to-turn-off-matplotlib-DEBUG-msgs-td48822.html
    # https://github.com/matplotlib/matplotlib/issues/14523
    logging.getLogger("matplotlib").setLevel(logging.WARNING)


#    logger.addHandler(handler)




# EOF
