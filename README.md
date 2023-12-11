# pyverify

基于Python实现的优秀的参数校验框架

## 安装

```shell
pip install pyverify
```

## 使用

### 如何改变报错返回的信息

1.默认为中文报错信息，如果想使用英文，则使用`message.english()`方法设置。

```python
from pyverify import rule
from pyverify.msg import message

message.english()

rule.phone().parse('tel', '123456')
```

2.自定义报错信息

```python
from pyverify import rule
from pyverify.msg import message


class NewMsg:
    phone = '{key}的值{value}并不是电话号码'


message.reload(NewMsg)

rule.phone().parse('tel', '123456')
```

### Flask框架支持

```python
from flask import Flask, jsonify

from pyverify import rule, message, ValidationError
from pyverify.frame.flask import assign

app = Flask(__name__)
message.english()

relus = dict(
    username=rule.str(required=True, isalnum=True, minLength=1, maxLength=20),
    password=rule.str(required=True, isalnum=True, minLength=1, maxLength=20)
)


# 拦截 pyverify 的 ValidationError 异常，定制返回消息格式
@app.errorhandler(ValidationError)
def handler_exception(error):
    response = jsonify({'error': error.msg})
    response.status_code = 400
    return response


@app.route('/login', methods=['POST'])
@assign(relus)  # 必须在 app.route 装饰器下面
def login(params):
    print(params)
    return "success"


if __name__ == '__main__':
    app.run()
```