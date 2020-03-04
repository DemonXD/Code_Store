---
title: Python Official Lib
created: '2020-03-04T00:46:36.614Z'
modified: '2020-03-04T06:44:33.209Z'
---

# Python Official Lib

[python3 基础库传送门](https://docs.python.org/zh-cn/3/library/)

## functools
- **@cached_property**
  - 加了缓存功能的property 使用情况，高计算资源消耗
- **cmp_to_key**
  - 对于类似sorted(key=) 中的key使用，使用较少
- **@lru_cache**
  - 适用于重用上次的计算结果时使用，对于每次调用都变化，且函数的参数及关键词不可哈希的，不推荐也不能使用
- **@total_ordering**
  - 帮助生成全比较排序方法，此类必须包含以下方法之一：__lt__() 、__le__()、__gt__() 或 __ge__()。另外，此类必须支持 __eq__() 方法。
```Python
@total_ordering
class Student:
    def _is_valid_operand(self, other):
        return (hasattr(other, "lastname") and
                hasattr(other, "firstname"))
    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return ((self.lastname.lower(), self.firstname.lower()) ==
                (other.lastname.lower(), other.firstname.lower()))
    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return ((self.lastname.lower(), self.firstname.lower()) <
                (other.lastname.lower(), other.firstname.lower()))
```
- **partial**
  - 返回一个固定某一参数的方法
```Python
def add(a: int, b: int) -> int:
    return a + b
add2 = partial(add, a=1, b=1)
addbase1 = partial(add, a=1)
print(add2()) # return 2
print(addbase1(b=2)) # return 3
```
- **partialmethod**
  - 一般用在描述器类中，返回一个新的描述器，即用在类中，返回一个类似partial的方法，当直接作用在一个函数上时，则会创建一个func的绑定方法
```Python
# 官网示例
class Cell(object):
     def __init__(self):
         self._alive = False
     @property
     def alive(self):
         return self._alive
     def set_state(self, state):
         self._alive = bool(state)
     set_alive = partialmethod(set_state, True)
     set_dead = partialmethod(set_state, False)

c = Cell()
c.alive # False
c.set_alive() # self._alive = True
c.alive # True

def add(a: int = 1, b: int = 2):
    return a + b
addclass = partialmethod(add)
addclass() # 报错，不可直接调用
addclass.__dict__ # {
                  #    'func': <function __main__.add(a: int = 1, b: int = 2)>,
                  #    'args': (),
                  #    'keywords': {}
                  # }
addclass.func() # return 3
```
- **reduce**
  - 累加计算，将func的两个参数从左致右累积的应用到iterable条目
```Python
a = reduce(lambda x, y: x+y, [1, 2, 3, 4, 5])
a # 15
a = reduce(lambda x, y: x+y, ['1', '2', '3', '4', '5'])
a # '12345'
```
- **@singledispatch**
  - 单分派类型函数，一般用在同一个函数不同类型参数有不通的表现上使用
```Python
@singledispatch
def schar(a, verbose=False):
    if verbose:
        print("verbose pattern, ", a)
    else:
        print(a)

# 等价与 schar.register(str, _)
@schar.register(str)
def _(a, verbose=False):
    if verbose:
        print("verbose pattern, ", a)
    else:
        print(a + " char")

schar(1) # 1
schar('a') # a char
```
- **@singledispatchmethod**
  - 在类中使用，无需导入，实现和singledispatch一样

- **update_wrapper**
  - 为partial对象添加原函数的__name__和__doc__ 属性
```Python
def power(base, exponent):
    """Docstring"""
    return base ** exponent

square = functools.partial(power)
functools.update_wrapper(square, power)

print square.__name__ # power
print square.__doc__  # Docstring
```
- **@wraps**
  - 定义一个装饰器
```Python
def my_decorator(f):
    @functools.wraps(f)
    def wrapper(*args, **kwds):
        print("i am a decorator")
        return f(*args, **kwds)
    return wrapper

@my_decorator
def a():
    print("exec a func")

a() # return:
    # i am a decorator
    # exec a func
```

## collections
替换 python内建容器`dict, list, set, tuple`

- **ChainMap**
  - 快速的合并多个字典，有顺序关系, 从后向前
```Python
cm = ChainMap({"a": "a", "b": "b"}, {"c": "c", "d": "d"})
list(cm) # "c", "d", "a", "b"
```

- **Counter**
  - 提供快速且方便的计数器工具, 参数可hash, 本质是字典的子类，拓展的方法有most_common()：表示出现频次最多的项目，elements() 返回正整数技术的元素， update区别于dict的替换，而是加上，subtract却别与dict的替换，而是减去; Counter 之间还可以有4中运算法则，+：合并，-：减去，&：取双方最小值，|：取双方最大值
```Python
sample1 = Counter(a=2, b=1, c=0, d=-1)
sorted(sample1.elements()) # ['a', 'a', 'b']
sample2 = Counter('abracadabra')
sample2.most_common(3) # [('a', 5), ('b', 2), ('r', 2)]
sample3 = Counter(a=4, b=2, c=0, d=-2)
sample4 = Counter(a=1, b=1, c=3, d=4)
sample3.subtract(sample4)
sample3 # Counter({'a': 3, 'b': 1, 'c': -3, 'd': -6})
```

- **deque**
  - 返回一个新的双向队列对象，从左到右初始化
```Python
>>> from collections import deque
>>> d = deque('ghi')                 # make a new deque with three items
>>> for elem in d:                   # iterate over the deque's elements
...     print(elem.upper())
G
H
I

>>> d.append('j')                    # add a new entry to the right side
>>> d.appendleft('f')                # add a new entry to the left side
>>> d                                # show the representation of the deque
deque(['f', 'g', 'h', 'i', 'j'])

>>> d.pop()                          # return and remove the rightmost item
'j'
>>> d.popleft()                      # return and remove the leftmost item
'f'
>>> list(d)                          # list the contents of the deque
['g', 'h', 'i']
>>> d[0]                             # peek at leftmost item
'g'
>>> d[-1]                            # peek at rightmost item
'i'

>>> list(reversed(d))                # list the contents of a deque in reverse
['i', 'h', 'g']
>>> 'h' in d                         # search the deque
True
>>> d.extend('jkl')                  # add multiple elements at once
>>> d
deque(['g', 'h', 'i', 'j', 'k', 'l'])
>>> d.rotate(1)                      # right rotation
>>> d
deque(['l', 'g', 'h', 'i', 'j', 'k'])
>>> d.rotate(-1)                     # left rotation
>>> d
deque(['g', 'h', 'i', 'j', 'k', 'l'])

>>> deque(reversed(d))               # make a new deque in reverse order
deque(['l', 'k', 'j', 'i', 'h', 'g'])
>>> d.clear()                        # empty the deque
>>> d.pop()                          # cannot pop from an empty deque
Traceback (most recent call last):
    File "<pyshell#6>", line 1, in -toplevel-
        d.pop()
IndexError: pop from an empty deque

>>> d.extendleft('abc')              # extendleft() reverses the input order
>>> d
deque(['c', 'b', 'a'])
```

- **defaultdict**
  - 返回类似dict的对象，是dict的子类，并实现了default_factory方法
```Python
s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)]
d = defaultdict(list)
for k, v in s:
    d[k].append(v)

sorted(d.items()) # [('blue', [2, 4]), ('red', [1]), ('yellow', [1, 3])]
```

- **namedtuple**
  - 可以理解为简化版的，创建类
```Python
>>> # Basic example
>>> Point = namedtuple('Point', ['x', 'y'])
>>> p = Point(11, y=22)     # instantiate with positional or keyword arguments
>>> p[0] + p[1]             # indexable like the plain tuple (11, 22)
33
>>> x, y = p                # unpack like a regular tuple
>>> x, y
(11, 22)
>>> p.x + p.y               # fields also accessible by name
33
>>> p                       # readable __repr__ with a name=value style
Point(x=11, y=22)

>>> class Point(namedtuple('Point', ['x', 'y'])):
...     __slots__ = ()
...     @property
...     def hypot(self):
...         return (self.x ** 2 + self.y ** 2) ** 0.5
...     def __str__(self):
...         return 'Point: x=%6.3f  y=%6.3f  hypot=%6.3f' % (self.x, self.y, self.hypot)

>>> for p in Point(3, 4), Point(14, 5/7):
...     print(p)
Point: x= 3.000  y= 4.000  hypot= 5.000
Point: x=14.000  y= 0.714  hypot=14.018
```

- **OrderedDict**
  - dict 子类实例，具有专门用于重新排列字典顺序的方法
```Python
class LastUpdatedOrderedDict(OrderedDict):
    'Store items in the order the keys were last added'

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)
```

- **UserDict**、**UserList**、**UserString**
  - 模拟类，值通过data属性获取
## itertools(可以使用封装程度更好的more-itertools)
### 无穷迭代器
- **count()**
  - count(start, [step]), 从start开始步进为1的无穷迭代器
- **cycle()**
  - cycle(plist), 无限循环plist
- **repeat()**
  - repeat(elem[, n]) 重复n次元素elem，默认重复无限次
### 根据最短输入序列长度停止的迭代器
- **accumulate()**
  - accumulate(plist) 返回每次叠加值
```Python
accumulate([1, 2, 3, 4, 5]) -> 1, 3, 6, 10, 15
```
- **chain()**
  - chain(plist, llist) -> 返回合并后的所有元素
  - chain('ABC', 'DEF') --> A B C D E F
- **chain.from_iterable()**
  - 从已知可迭代器返回所有元素
  - chain.from_iterable(['ABC', 'DEF']) --> A B C D E F
- **compress()**
  - 根据条件返回当前位置的元素
  - compress('ABCDEF', [1,0,1,0,1,1]) --> A C E F
- **dropwhile()**
  - 首次真值测试失败开始返回元素
  - dropwhile(lambda x: x<5, [1,4,6,4,1]) --> 6 4 1
- **filterfalse()**
  - 筛选器，筛选条件为假的值
  - filterfalse(lambda x: x%2, range(10)) --> 0 2 4 6 8
- **groupby()**
  - 更具key(v)值分组的迭代器, 注意，对相邻的分组，如果中间隔着别的组数据，则会分开
```Python
import itertools
l = [("a", 1), ("a", 2), ("b", 3), ("b", 4), ("a", 6)]
key_f = lambda x: x[0]

for key, group in itertools.groupby(l, key_f):
    print key + ": " + str(list(group))
OUTPUT
a: [('a', 1), ('a', 2)]
b: [('b', 3), ('b', 4)]
a: [('a', 6)]
```

- **islice(seq, [start,] stop [,step])**
  - seq[start:stop:step]中的元素
  - islice('ABCDEFG', 2, None) --> C D E F G
- **starmap(func, seq)**
  - 对序列中每个元素执行指定的方法，元素的结构要和方法的参数一样
  - starmap(pow, [(2,5), (3,2), (10,3)]) --> 32 9 1000
- **takewhile(pred, seq)**
  - 返回序列中的值，除非该元素的真值测试为假，则中断
  - takewhile(lambda x: x<5, [1,4,6,4,1]) --> 1 4
- **tee(iter, n)**
  - 将一个迭代器，拆分为n个迭代器
  - ltee = tee([1, 2, 3, 4, 5], 5) --> 五个只有一个元素的迭代器
- **zip_longest(p, q, ...)**
  - 返回两个迭代器各个对应元素组成的set，无元素的补充空值
  - zip_longest('ABCD', 'xy', fillvalue='-') --> Ax By C- D-
### 排列组合迭代器
- **product(p,q,...[repeat=1])**
  - 计算元素的笛卡尔积
- **permutations(p[, r])**
  - 对长度为r的元祖（列表），所有可能的排列
- **combinations(p, r)**
  - 长度r元祖，有序，无重复元素
  - combinations([1, 2, 3], 2) --> (1, 2), (1, 3), (2, 3)
- **combinations_with_replacement(p, r)**
  - 长度r的元祖，有序，无重复元素
  - combinations([1, 2, 3], 2) --> (1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)
