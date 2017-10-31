#!_*_coding:utf-8_*_
#__author__:"Alex Li"

'''
handle all the logging works
'''

import logging
from conf import settings



def logger(log_type,*args):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    if log_type == 'bills' and args:
        logger = logging.getLogger(args[1])
        logger.setLevel(settings.LOG_LEVEL)
        log_file = "%s/log/bills/%s_bill.log" %(settings.BASE_DIR,args[0])
        bh = logging.FileHandler(log_file)
        bh.setLevel(settings.LOG_LEVEL)
        bh.setFormatter(formatter)
        logger.addHandler(bh)
        logger.info(args[2])
        logger.removeHandler(bh)
    elif log_type == 'login' and args:
        logger = logging.getLogger(args[1])
        logger.setLevel(settings.LOG_LEVEL)
        log_file = "%s/log/access.log" %settings.BASE_DIR
        loginh = logging.FileHandler(log_file)
        loginh.setLevel(settings.LOG_LEVEL)
        loginh.setFormatter(formatter)
        logger.addHandler(loginh)
        logger.info(args[2])
        logger.removeHandler(loginh)
    else:
        #create logger
        logger = logging.getLogger(log_type)
        logger.setLevel(settings.LOG_LEVEL)


        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(settings.LOG_LEVEL)

        # create file handler and set level to warning
        log_file = "%s/log/%s" %(settings.BASE_DIR, settings.LOG_TYPES[log_type])
        fh = logging.FileHandler(log_file)
        fh.setLevel(settings.LOG_LEVEL)


        # add formatter to ch and fh
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        # add ch and fh to logger
        # logger.addHandler(ch)
        logger.addHandler(fh)
        return logger
    # 'application' code
    '''logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')'''


