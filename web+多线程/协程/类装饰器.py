class Test():
    def __init__(self,func):
        print("这是一个初始化方法")
        self.func=func
    def run(self):
        print("正在奔跑")

    def __call__(self, *args, **kwargs):
        print("这是一个实例方法")
        self.func(*args, **kwargs)


# t=Test()
# t() #__call__方法在实例中可直接调用


@Test
def login(*args, **kwargs):
    print("login方法",*args, **kwargs)

login(88)