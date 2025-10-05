import time
def now_ts():
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
