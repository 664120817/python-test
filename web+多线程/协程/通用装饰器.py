
def function_out(func):
    def function_in(*args,**kwargs):
        print("装饰器1")
        return func(*args,**kwargs)
    return function_in

def function_out2(func):
    def function_in2(*args,**kwargs):
        print("装饰器2")
        return func(*args,**kwargs)
    return function_in2


@function_out2
@function_out
def login(*args,**kwargs):
    return (args,kwargs)



result = login((1,2),{'a':'b'})
# result = login(5,a = 10)
print(result)