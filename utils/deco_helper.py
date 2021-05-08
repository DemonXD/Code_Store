import time
import hashlib
import pickle
import functools
import logging
from __future__ import annotations
import functools
import datetime
import traceback


def asyncDecorator():
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args):
             # Some fancy foo stuff
            return await func(*args)
        return wrapped
    return wrapper

def dictcache(duration = -1):
    _cache = {}
    def _memoize(function):
        def _is_obsolete(entry, duration):
            if duration == -1: #永不过期
                return False
            return time.time() - entry['time'] > duration

        def _compute_key(function, args, kw):
            '''序列化并求其哈希值'''
            key = pickle.dumps((function.__name__, args, kw))
            return hashlib.sha1(key).hexdigest()

        @functools.wraps(function)
        def __memoize(*args, **kw):
            key = _compute_key(function, args, kw)
            if key in _cache:
                if _is_obsolete(_cache[key], duration) is False:
                    return _cache[key]['value']
            result = function(*args, **kw)
            _cache[key] = {
                'value' : result,
                'time'  : time.time()
            }
            return _cache[key]['value']
        return __memoize
    return _memoize

def timecost(func):
    @functools.wraps(func)
    def timer(*args):
        start = time.time()
        value = func(*args)
        end = time.time()
        print(f"{func.__name__} cost: {round((end-start), 3)}")
        return value
    return timer


############log
def create_logger():
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger("example_logger")
    logger.setLevel(logging.INFO)
 
    # create the logging file handler
    fh = logging.FileHandler(r"/path/to/test.log")
 
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
 
    # add handler to logger object
    logger.addHandler(fh)
    return logger
 
logger = create_logger()

def CusExceptionDecorator(logger):
    """
    A decorator that wraps the passed in function and logs 
    exceptions should one occur
 
    @param logger: The logging object
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                # log the exception
                err = "There was an exception in  "
                err += func.__name__
                logger.exception(err)
 
                # re-raise the exception
                raise
        return wrapper
    return decorator


#############log_2
# 异常输出
def except_output(msg='异常'):
    # msg用于自定义函数的提示信息
    def except_execute(func):
        @functools.wraps(func)
        def execept_print(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                sign = '=' * 60 + '\n'
                print(f'{sign}>>>异常时间：\t{datetime.datetime.now()}\n>>>异常函数：\t{func.__name__}\n>>>{msg}：\t{e}')
                print(f'{sign}{traceback.format_exc()}{sign}')
        return execept_print
    return except_execute