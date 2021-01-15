from functools import singledispatch

print(list(map(lambda x: x * 2, [1, 2, 3, 4, 5])))


@singledispatch
def age(obj):
    print("请传入合法类型的参数")


@age.register(int)
def _(age):
    print("我已经{}岁了".format(age))


@age.register(str)
def _(age):
    print("I am {} years old".format(age))


age(23)
age('twenty three')
age(['23'])

# 普通装饰器


def logger(func):
    def wrapper(* args, **kw):
        print("我开始准备执行：{}函数了".format(func.__name__))

        func(*args, **kw)

        print("我执行完了")
    return wrapper


@logger
def add(x, y):
    print(f"{x} + {y} = {x+y}")


add(200, 40)

# 带参装饰器


def say_hello(contry):
    def wrapper(func):
        def deco(*args, **kw):
            if contry == "china":
                print("你好")
            elif contry == "america":
                print("hello")
            else:
                return
        return deco
    return wrapper


@say_hello("china")
def xiaoming():
    pass


@say_hello("america")
def jack():
    pass


xiaoming()
jack()


# 类装饰器
class c_logger(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, * args, **kw):
        print("[INFO]: the function {func}() is running..."
              .format(func=self.func.__name__))
        return self.func(*args, **kw)


@c_logger
def say(something):
    print(f"say {something} !")


say("hello")


#带参类装饰器

class cp_looger(object):
    def __init__(self, level="INFO"):
        self.level = level
    
    def __call__(self, func):
        def wrapper(* args, **kw):
            print("[{level}]: the function {func}() is running..." \
                  .format(level=self.level, func=func.__name__))
            func(* args, **kw)
        return wrapper

@cp_looger(level="WARNING")
def say_cp(something):
    print(f"say {something} !")

say_cp("hello")