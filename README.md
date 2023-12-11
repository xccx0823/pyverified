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