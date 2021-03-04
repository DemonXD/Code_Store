##############################################
#   Author :        Miles Xu
#   Email  :        kanonxmm@163.com
#   Date   :        2021/03/03 20:45
#   License:        MIT
#   Desc.  :        ...
##############################################
import os
import logging
import logging.config

# 日志放在用户根目录下
logdir = os.path.join(os.path.expanduser('~'), 'Tmplogs\\')

config = {
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
        # 其他的 formatter
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': f'{logdir}logging_debug.log',
            'level': 'DEBUG',
            'formatter': 'simple'
        },
        # 其他的 handler
        'infofile':{
            'class': 'logging.FileHandler',
            'filename': f'{logdir}logging_info.log',
            'level': 'INFO',
            'formatter': 'simple'
        },
        'errorfile':{
            'class': 'logging.FileHandler',
            'filename': f'{logdir}logging_error.log',
            'level': 'ERROR',
            'formatter': 'simple'
        }
    },
    'loggers':{
        'StreamLogger': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'FileLogger': {
            # 既有 console Handler，还有 file Handler
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
        # 其他的 Logger
        "FileInfoLogger":{
            'handlers': ['console', 'file'],
            'level': 'INFO',
        },
        "FileErrorLogger":{
            'handlers': ['console', 'file'],
            'level': 'ERROR'
        }
    }
}

logging.config.dictConfig(config)
StreamLogger = logging.getLogger("StreamLogger")
FileLogger = logging.getLogger("FileLogger")
FileInfoLogger = logging.getLogger("FileInfoLogger")
FileErrorLogger = logging.getLogger("FileErrorLogger")