import time


def timer_decorator(func):
    def wrapper(*args, **kwargs):
        tstart = time.time()
        res = func(*args, **kwargs)
        tfinish = time.time()
        return tfinish - tstart, res
    return wrapper


def timer(func):
    '''
    returns (time, func_result)
    '''
    tstart = time.time()
    res = func()
    tfinish = time.time()
    return tfinish - tstart, res
