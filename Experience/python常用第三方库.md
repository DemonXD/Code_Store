### 列举一些好用的第三方库

- easydict[简化字典的使用]
    ```Python
    from easydict import EasyDict as edict
    d = edict({"a":1, "b":2, "c":3})
    print(d.a) # => 1
    ```

- fire (自动将函数和类命令行化)
    ```Python
    import fire

    def hello(name="World"):
    return "Hello %s!" % name

    if __name__ == '__main__':
    fire.Fire(hello)
    ```
    Then, from the command line, you can run:
    ```Shell
    python hello.py  # Hello World!
    python hello.py --name=David  # Hello David!
    python hello.py --help  # Shows usage information.
    ```
    Here's an example of calling Fire on a class.
    ```Python
    import fire

    class Calculator(object):
    """A simple calculator class."""

    def double(self, number):
        return 2 * number

    if __name__ == '__main__':
    fire.Fire(Calculator)
    ```
    Then, from the command line, you can run:
    ```Shell
    python calculator.py double 10  # 20
    python calculator.py double --number=15  # 30
    ```
- Arrow(聪明操作时间的库)
```Python
import arrow
arrow.get('2013-05-11T21:23:58.970460+07:00')
# <Arrow [2013-05-11T21:23:58.970460+07:00]>

utc = arrow.utcnow()
utc
# <Arrow [2013-05-11T21:23:58.970460+00:00]>

utc = utc.shift(hours=-1)
utc
# <Arrow [2013-05-11T20:23:58.970460+00:00]>

local = utc.to('US/Pacific')
local
# <Arrow [2013-05-11T13:23:58.970460-07:00]>

local.timestamp()
# 1368303838.970460

local.format()
# '2013-05-11 13:23:58 -07:00'

local.format('YYYY-MM-DD HH:mm:ss ZZ')
# '2013-05-11 13:23:58 -07:00'

local.humanize()
# 'an hour ago'

# local.humanize(locale='ko-kr')
# '한시간 전'
```