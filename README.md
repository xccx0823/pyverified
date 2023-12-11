# pyverify

基于Python实现的参数校验框架

## 安装

```shell
pip install pyverify
```

## 交易失败消息支持

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

## 框架支持

### Flask

1.获取form参数并解析

```python
from flask import Flask, jsonify

from pyverify import rule, message, ValidationError
from pyverify.frame.base import Params
from pyverify.frame.flask import assign

app = Flask(__name__)
message.english()

relus = dict(
    username=rule.str(required=True, isalnum=True, minLength=1, maxLength=20),
    password=rule.str(required=True, isalnum=True, minLength=1, maxLength=20)
)


# 拦截 pyverify 的 ValidationError 异常，定制返回消息格式。
@app.errorhandler(ValidationError)
def handler_exception(error):
    response = jsonify({'error': error.msg})
    response.status_code = 400
    return response


@app.route('/index', methods=['POST'])
@assign(form=relus)  # 必须在 app.route 装饰器下面
def index(params: Params):
    return params.form


if __name__ == '__main__':
    app.run()
```

2.获取json参数并解析，当设置`many=True`时，json参数应该为`[]`格式。

```python
...


@app.route('/index', methods=['POST'])
@assign(json=relus, many=True)
def index(params: Params):
    return params.json


...
```

3.获取query参数并解析。

```python
...


@app.route('/index', methods=['POST'])
@assign(query=relus)
def index(params: Params):
    return params.query


...
```

4.也支持多次解析不同的规则，但是解析相同类型的参数的化，后者会覆盖前者的解析结果

写法上可以这样写

```python
...


@app.route('/index', methods=['POST'])
@assign(query=query_rules, json=json_rules)
def index(params: Params):
    return {'query': params.query, 'json': params.json}


...
```

也可以这样写

```python
...


@app.route('/index', methods=['POST'])
@assign(query=query_rules)
@assign(json=json_rules)
def index(params: Params):
    return {'query': params.query, 'json': params.json}


...
```