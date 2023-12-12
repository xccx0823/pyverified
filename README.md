# pyverify

基于Python实现的参数校验框架

* [1 安装](#1-安装)
* [2 使用](#2-使用)
* [3 校验失败消息支持](#3-校验失败消息支持)
    * [3\.1 如何改变报错返回的信息](#31-如何改变报错返回的信息)
* [4 框架支持](#4-框架支持)
    * [4\.1 Flask](#41-flask)
* [5 类型以及校验规则](#5-类型以及校验规则)
    * [5\.1 基本数据类型规则](#51-基本数据类型规则)
        * [5\.1\.1 str类型](#511-str类型)
        * [5\.1\.2 int类型](#512-int类型)
        * [5\.1\.3 float类型](#513-float类型)
        * [5\.1\.4 bool类型](#514-bool类型)
        * [5\.1\.5 datetime类型](#515-datetime类型)
    * [5\.2 嵌套结构数据类型](#52-嵌套结构数据类型)
        * [5\.2\.1 dict类型](#521-dict类型)
        * [5\.2\.2 list类型](#522-list类型)
    * [5\.3 扩展数据类型](#53-扩展数据类型)
        * [5\.3\.1 email: 校验字符串是否为邮箱](#531-email-校验字符串是否为邮箱)
        * [5\.3\.2 ipv4: 校验字符串是否为ipv4地址](#532-ipv4-校验字符串是否为ipv4地址)
        * [5\.3\.3 ipv6: 校验字符串是否为ipv6地址](#533-ipv6-校验字符串是否为ipv6地址)
        * [5\.3\.4 phone: 校验字符串是否为电话号码](#534-phone-校验字符串是否为电话号码)
        * [5\.3\.5 addr: 校验字符串是否为链接地址](#535-addr-校验字符串是否为链接地址)

## 1 安装

```shell
pip install pyverify
```

## 2 使用

如何使用`pyverify`校验数据

```python
from pyverify import Verify, rule

params = dict(aaa=rule.float(default=1.23, digits=1))
data = {}
verified = Verify(data, params)
print(verified.params)
```

## 3 校验失败消息支持

### 3.1 如何改变报错返回的信息

- 默认为中文报错信息，如果想使用英文，则使用`message.english()`方法设置。

```python
from pyverify import rule
from pyverify.msg import message

message.english()

rule.phone().parse('tel', '123456')
```

- 自定义报错信息

```python
from pyverify import rule
from pyverify.msg import message


class NewMsg:
    phone = '{key}的值{value}并不是电话号码'


message.reload(NewMsg)

rule.phone().parse('tel', '123456')
```

## 4 框架支持

### 4.1 Flask

- 获取form参数并解析

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

- 获取json参数并解析，当设置`many=True`时，json参数应该为`[]`格式。

```python
...


@app.route('/index', methods=['POST'])
@assign(json=relus, many=True)
def index(params: Params):
    return params.json


...
```

- 获取query参数并解析。

```python
...


@app.route('/index', methods=['POST'])
@assign(query=relus)
def index(params: Params):
    return params.query


...
```

- 获取headers对应值并解析。

```python
...


@app.route('/index', methods=['POST'])
@assign(headers=relus)
def index(params: Params):
    return params.headers


...
```

- 也支持多次解析不同的规则，但是解析相同类型的参数的化，后者会覆盖前者的解析结果
    - 写法上可以这样写

    ```python
    ...
    
    
    @app.route('/index', methods=['POST'])
    @assign(query=query_rules, json=json_rules)
    def index(params: Params):
        return {'query': params.query, 'json': params.json}
    
    
    ...
    ```

    - 也可以这样写
    ```python
    ...
    
    
    @app.route('/index', methods=['POST'])
    @assign(query=query_rules)
    @assign(json=json_rules)
    def index(params: Params):
        return {'query': params.query, 'json': params.json}
    
    
    ...
    ```

## 5 类型以及校验规则

### 5.1 基本数据类型规则

#### 5.1.1 str类型

#### 5.1.2 int类型

| 规则            | 释义                                                | 初始值   |
|---------------|---------------------------------------------------|-------|
| default       | 默认值                                               | False |
| required      | 是否时必须的                                            | False |
| allow_none    | 值是否允许为空                                           | True  |
| multi         | 是否是多个值                                            | False |
| func          | 自定义函数                                             | None  |
| gt/gte/lt/lte | 数值大小比较                                            | None  |
| enum          | 数字枚举，传入list规则时，则判断是否在枚举范围内，传入dict规则之后会对在其中的枚举进行映射 | None  |

#### 5.1.3 float类型

| 规则            | 释义               | 初始值   |
|---------------|------------------|-------|
| default       | 默认值              | False |
| required      | 是否时必须的           | False |
| allow_none    | 值是否允许为空          | True  |
| multi         | 是否是多个值           | False |
| func          | 自定义函数            | None  |
| gt/gte/lt/lte | 数值大小比较           | None  |
| digits        | float类型保留小数位数    | None  |
| decimal       | 是否转化为decimal数据类型 | False |

#### 5.1.4 bool类型

| 规则         | 释义                                                         | 初始值   |
|------------|------------------------------------------------------------|-------|
| default    | 默认值                                                        | False |
| required   | 是否时必须的                                                     | False |
| allow_none | 值是否允许为空                                                    | True  |
| multi      | 是否是多个值                                                     | False |
| func       | 自定义函数                                                      | None  |
| convert    | 是否将字符串转化为bool类型，为True时会转化字符串的True，False转化为对应的bool类型，大小写不敏感 | True  |

#### 5.1.5 datetime/date类型

| 规则            | 释义          | 初始值                                          |
|---------------|-------------|----------------------------------------------|
| default       | 默认值         | False                                        |
| required      | 是否时必须的      | False                                        |
| allow_none    | 值是否允许为空     | True                                         |
| multi         | 是否是多个值      | False                                        |
| func          | 自定义函数       | None                                         |
| fmt           | 日期格式化样式     | datetime为`%Y-%m-%d %H:%M:%S`，date为`%Y-%m-%d` |
| gt/gte/lt/lte | 日期大小比较      | None                                         |
| enum          | 日期是否在指定的枚举中 | None                                         |

### 5.2 嵌套结构数据类型

#### 5.2.1 dict类型

| 规则         | 释义            | 初始值   |
|------------|---------------|-------|
| default    | 默认值           | False |
| required   | 是否时必须的        | False |
| allow_none | 值是否允许为空       | True  |
| multi      | 是否是多个值        | False |
| func       | 自定义函数         | None  |
| subset     | 定义的嵌套规则       |       |
| dest       | 忽略所有校验，直接获取原值 |       |

#### 5.2.2 list类型

| 规则         | 释义            | 初始值   |
|------------|---------------|-------|
| default    | 默认值           | False |
| required   | 是否时必须的        | False |
| allow_none | 值是否允许为空       | True  |
| multi      | 是否是多个值        | False |
| func       | 自定义函数         | None  |
| subset     | 定义的嵌套规则       |       |
| dest       | 忽略所有校验，直接获取原值 |       |

### 5.3 扩展数据类型

#### 5.3.1 email: 校验字符串是否为邮箱

| 规则         | 释义      | 初始值   |
|------------|---------|-------|
| default    | 默认值     | False |
| required   | 是否时必须的  | False |
| allow_none | 值是否允许为空 | True  |
| multi      | 是否是多个值  | False |
| func       | 自定义函数   | None  |

#### 5.3.2 ipv4: 校验字符串是否为ipv4地址

| 规则         | 释义      | 初始值   |
|------------|---------|-------|
| default    | 默认值     | False |
| required   | 是否时必须的  | False |
| allow_none | 值是否允许为空 | True  |
| multi      | 是否是多个值  | False |
| func       | 自定义函数   | None  |

#### 5.3.3 ipv6: 校验字符串是否为ipv6地址

| 规则         | 释义      | 初始值   |
|------------|---------|-------|
| default    | 默认值     | False |
| required   | 是否时必须的  | False |
| allow_none | 值是否允许为空 | True  |
| multi      | 是否是多个值  | False |
| func       | 自定义函数   | None  |

#### 5.3.4 phone: 校验字符串是否为电话号码

| 规则         | 释义      | 初始值   |
|------------|---------|-------|
| default    | 默认值     | False |
| required   | 是否时必须的  | False |
| allow_none | 值是否允许为空 | True  |
| multi      | 是否是多个值  | False |
| func       | 自定义函数   | None  |
| region     | 电话号码地区  | CN    |

#### 5.3.5 addr: 校验字符串是否为链接地址

| 规则         | 释义      | 初始值   |
|------------|---------|-------|
| default    | 默认值     | False |
| required   | 是否时必须的  | False |
| allow_none | 值是否允许为空 | True  |
| multi      | 是否是多个值  | False |
| func       | 自定义函数   | None  |