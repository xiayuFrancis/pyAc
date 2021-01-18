astr = 'ABC'
alist = [1, 2, 3]
adict = {"name":"xy", "age":18}

agen = (i for i in range(4, 8))

def gen(*args, **kw):
    for item in args:
        for i in item:
            yield i
            
new_list = gen(astr, alist, adict, agen)
print(list(new_list))

def gen2(*args, **kw):
    for item in args:
        yield from item

agen2 = (i for i in range(4, 8))
new_list2 = gen(astr, alist, adict, agen2)
print(list(new_list2))