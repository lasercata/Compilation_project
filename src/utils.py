#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''File defining useful functions for the whole project'''

##-Imports
import logging

##-Functions
def get_logger(prog_name: str, debug_lvl: int = 0) -> logging.Logger:
    '''
    Makes and return a new logger

    Args:
        prog_name (str): the program name to print
        debug_lvl (int, optionnal): the debuging level
    '''

    if debug_lvl > 0:
        logger_lvl = logging.DEBUG
    else:
        logger_lvl = logging.INFO

    logger = logging.getLogger(prog_name)
    logger.setLevel(logger_lvl)
    ch = logging.StreamHandler()
    ch.setLevel(logger_lvl)

    if debug_lvl <= 1:
        formatter = logging.Formatter('[%(name)s] %(message)s')
    else:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger
