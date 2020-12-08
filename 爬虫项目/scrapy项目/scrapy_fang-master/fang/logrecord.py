from functools import wraps
# import inspect
import logging

# 创建logger
logger = logging.getLogger('func_log')
logger.setLevel(logging.DEBUG)

# 写入日志
fh = logging.FileHandler('error.log')
fh.setLevel(logging.DEBUG)

# 输出控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# handler输出格式
formatter = logging.Formatter('[%(asctime)s][%(thread)d][%(filename)s][line: %(lineno)d][%(levelname)s] ## %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 绑定handler
logger.addHandler(fh)
logger.addHandler(ch)


# 装饰器:打印函数名并写入日志
def decorator(function):
    @wraps(function)
    def inner(*args, **kwargs):
        result = function()
        logger.debug('%s' %result)


    return inner



@decorator
def func():
    pass

if __name__ == '__main__':

    func()