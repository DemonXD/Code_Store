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

- marshmallow/Pydantic(序列化，反序列化对象库)  
    - 可以用于固定参数的校验
    - 数据库存储中间对象
    ```Python
    ########### marshmallow
    from pprint import pprint
    from marshmallow import Schema, fields, ValidationError

    class UserSchema(Schema):
        name = fields.String(required=True)
        age = fields.Integer(required=True, error_messages={'required': 'Age is required.'})
        city = fields.String(
            required=True,
            error_messages={'required': {'message': 'City required', 'code': 400}},
        )
        email = fields.Email()

    try:
        result = UserSchema().load({'email': 'foo@bar.com'})
    except ValidationError as err:
        pprint(err.messages)

    ############ Pydantic
    from pydantic import BaseModel, ValidationError, validator


    class UserModel(BaseModel):
        name: str
        username: str
        password1: str
        password2: str

        @validator('name')
        def name_must_contain_space(cls, v):
            if ' ' not in v:
                raise ValueError('must contain a space')
            return v.title()

        @validator('password2')
        def passwords_match(cls, v, values, **kwargs):
            if 'password1' in values and v != values['password1']:
                raise ValueError('passwords do not match')
            return v

        @validator('username')
        def username_alphanumeric(cls, v):
            assert v.isalnum(), 'must be alphanumeric'
            return v
    ```

- glob(遍历文件夹的库)
    ```Python
    import glob
    path = /target/path
    # recursive 逐级遍历
    # 第一个** 表示该目录下所有的目录
    # 第二个* 表示所有xlsx类型的文件
    for file in glob(f"{path}/**/*.xlsx", recursive=True):
        pass
    ```

- librose(音频处理)
    ```Python
    import librosa
    audio_path = '../T08-violin.wav'
    x , sr = librosa.load(audio_path)

    print(type(x), type(sr))
    # <class 'numpy.ndarray'> <class 'int'>

    print(x.shape, sr)
    # (396688,) 22050

    # 以44.1KHz重新采样
    librosa.load(audio_path, sr=44100)
    ```