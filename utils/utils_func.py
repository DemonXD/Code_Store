import time
import hashlib
import pickle
import functools

def CMlist(list1, list2):
    l = len(list1)  + len(list2)
    target_list = []
    for i in range(0, l-1):
        if len(list1) != 0:
            target_list.append(list1.pop(0))
        if len(list2) != 0:
            target_list.append(list2.pop(0))
    return target_list

# test func
# print(CMlist([1,3,5,7,9], [2,4,6,8,10,11,'a','b']))
# the result should be: 1,2,3,4,5,6,7,8,9,10,11,a,b


def separated_list_with_n(list, width):
    '''
        separated list with the width you want
    '''
    return [list[x:x+width] for x in range(0, len(list), width)]


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