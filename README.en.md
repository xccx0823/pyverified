<img src="https://github.com/xccx0823/pyverified/blob/main/icon.png" alt="Pyverified" style="width: 100%; display: block; margin: 0 auto;">

<p align="center">
    <em>A parameter validation framework implemented in Python</em>
</p>

<p align="center">
    <a href="#" target="_blank">
        <img src="https://img.shields.io/badge/python-3.6+-blue.svg" alt="Python 3.6+">
    </a>
    <a href="https://opensource.org/licenses/MIT" target="_blank">
        <img src="https://img.shields.io/badge/license-MIT-brightgreen.svg" alt="MIT license">
    </a>
    <a href="https://github.com/xccx0823/pyverified/releases" target="_blank">
        <img src="https://img.shields.io/github/v/release/xccx0823/pyverified" alt="GitHub release">
    </a>
</p>

## Index

* [Validation Failure Message Support](#validation-failure-message-support)
* [Framework Support](#framework-support)
* [Types and Validation Rules](#types-and-validation-rules)

## Installation

```shell
pip install pyverified
```

## Usage

How to use `pyverified` to validate data

```python
from pyverified import Verify, rule

params = dict(aaa=rule.float(default=1.23, digits=1))
data = {}
verified = Verify(data, params)
print(verified.params)
```

## Validation Failure Message Support

### How to change the error message returned

- The default error messages are in Chinese. To use English messages, use the `message.english()` method.

```python
from pyverified import rule
from pyverified.msg import message

message.english()

rule.phone().parse('tel', '123456')
```

- Custom error messages

```python
from pyverified import rule
from pyverified.msg import message


class NewMsg:
    phone = '{key}的值{value}并不是电话号码'


message.reload(NewMsg)

rule.phone().parse('tel', '123456')
```

## Framework Support

### Flask

- Get and parse form parameters

```python
from flask import Flask, jsonify

from pyverified import rule, message, ValidationError
from pyverified.frame.base import Params
from pyverified.frame.flask import assign

app = Flask(__name__)
message.english()

relus = dict(
    username=rule.str(required=True, isalnum=True, minLength=1, maxLength=20),
    password=rule.str(required=True, isalnum=True, minLength=1, maxLength=20)
)


# Intercept the ValidationError exception from pyverified and customize the return message format.
@app.errorhandler(ValidationError)
def handler_exception(error):
    response = jsonify({'error': error.msg})
    response.status_code = 400
    return response


@app.route('/index', methods=['POST'])
@assign(form=relus)  # Must be below the app.route decorator
def index(params: Params):
    return params.form


if __name__ == '__main__':
    app.run()
```

- To obtain and parse JSON parameters, when setting many=True, the JSON parameters should be in the [] format.

```python
...


@app.route('/index', methods=['POST'])
@assign(json=relus, many=True)
def index(params: Params):
    return params.json


...
```

- To retrieve and parse query parameters.

```python
...


@app.route('/index', methods=['POST'])
@assign(query=relus)
def index(params: Params):
    return params.query


...
```

- To fetch and parse the values corresponding to headers.

```python
...


@app.route('/index', methods=['POST'])
@assign(headers=relus)
def index(params: Params):
    return params.headers


...
```

- Also supports multiple parsing with different rules. However, when parsing parameters of the same type, the latter
  will override the parsing results of the former.

    - In terms of syntax, it can be written like this:

  ```python
  ...


  @app.route('/index', methods=['POST'])
  @assign(query=query_rules, json=json_rules)
  def index(params: Params):
      return {'query': params.query, 'json': params.json}


  ...
  ```

    - Alternatively, you can express it this way:

  ```python
  ...


  @app.route('/index', methods=['POST'])
  @assign(query=query_rules)
  @assign(json=json_rules)
  def index(params: Params):
      return {'query': params.query, 'json': params.json}


  ...
  ```

## ypes and Validation Rules

### Basic Data Type Rules

#### str

| Rule         | Description                                                                                                                                                      | Default |
|--------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
| default      | Default value                                                                                                                                                    | False   |
| required     | Whether it is required                                                                                                                                           | False   |
| allow_none   | Whether the value is allowed to be empty                                                                                                                         | True    |
| multi        | Whether it is a multi-value                                                                                                                                      | False   |
| func         | Custom function                                                                                                                                                  | None    |
| minLength    | Minimum length of the string                                                                                                                                     | None    |
| maxLength    | Maximum length of the string                                                                                                                                     | None    |
| enum         | String enumeration. When a list rule is passed, it checks if the value is within the enum range. When a dict rule is passed, it maps enumerated values within it | None    |
| strip        | Whether to remove specified characters from both ends of the string                                                                                              | False   |
| lstrip       | Whether to remove specified characters from the left end of the string                                                                                           | False   |
| rstrip       | Whether to remove specified characters from the right end of the string                                                                                          | False   |
| strip_chars  | Used in conjunction with strip, specifies the characters to be removed                                                                                           | None    |
| lstrip_chars | Used in conjunction with lstrip, specifies the characters to be removed                                                                                          | None    |
| rstrip_chars | Used in conjunction with rstrip, specifies the characters to be removed                                                                                          | None    |
| startswith   | Checks if the string starts with the specified string                                                                                                            | None    |
| endswith     | Checks if the string ends with the specified string                                                                                                              | None    |
| isalnum      | Checks if the string consists of letters and numbers                                                                                                             | False   |
| isalpha      | Checks if the string consists only of letters                                                                                                                    | False   |
| isdecimal    | Checks if the string contains only decimal characters                                                                                                            | False   |
| isdigit      | Checks if the string contains only numeric characters                                                                                                            | False   |
| isidentifier | Checks if the string is a valid identifier                                                                                                                       | False   |
| islower      | Checks if all the letters in the string are lowercase                                                                                                            | False   |
| isupper      | Checks if all the letters in the string are uppercase                                                                                                            | False   |
| isprintable  | Checks if the string is printable                                                                                                                                | False   |
| isspace      | Checks if the string contains only whitespace characters                                                                                                         | False   |
| istitle      | Checks if each word in the string starts with an uppercase letter, and the rest are lowercase                                                                    | False   |
| include      | Checks if the string contains the specified string                                                                                                               | None    |
| exclude      | Checks if the string does not contain the specified string                                                                                                       | None    |
| replace      | Whether to replace specified strings in the string with others                                                                                                   | False   |
| replace_args | Used in conjunction with replace                                                                                                                                 | ()      |
| capitalize   | Converts the first character of the string to uppercase, and the rest to lowercase                                                                               | False   |
| title        | Converts the first letter of each word in the string to uppercase, and the rest to lowercase                                                                     | False   |
| swapcase     | Swaps the case of each letter in the string                                                                                                                      | False   |
| lower        | Converts all letters in the string to lowercase                                                                                                                  | False   |
| upper        | Converts all letters in the string to uppercase                                                                                                                  | False   |
| casefold     | Similar to lower(), but more powerful. Converts all characters to lowercase and handles special characters for case-insensitive comparison                       | False   |
| split        | Splits the string by the specified character. Note: The result obtained after using this feature is of type list                                                 | None    |
| split2type   | Converts elements in the split data to the specified data type                                                                                                   | None    |
| regex        | Performs regex matching on the string                                                                                                                            | None    |

#### int

| Rule          | Description                                                                                                                                                       | Default |
|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
| default       | Default value                                                                                                                                                     | False   |
| required      | Whether it is required                                                                                                                                            | False   |
| allow_none    | Whether the value is allowed to be empty                                                                                                                          | True    |
| multi         | Whether it is a multi-value                                                                                                                                       | False   |
| func          | Custom function                                                                                                                                                   | None    |
| gt/gte/lt/lte | Numeric comparison for greater than/equal to/less than/less than or equal to                                                                                      | None    |
| enum          | Numeric enumeration. When a list rule is passed, it checks if the value is within the enum range. When a dict rule is passed, it maps enumerated values within it | None    |

#### float

| Rule          | Description                             | Default |
|---------------|-----------------------------------------|---------|
| default       | Default value                           | False   |
| required      | Whether it is required                  | False   |
| allow_none    | Whether the value can be empty          | True    |
| multi         | Whether it is a multi-value             | False   |
| func          | Custom function                         | None    |
| gt/gte/lt/lte | Numeric comparison                      | None    |
| digits        | Number of decimal places for float type | None    |
| decimal       | Whether to convert to decimal data type | False   |

#### bool

| Rule       | Description                                                                                                                           | Default |
|------------|---------------------------------------------------------------------------------------------------------------------------------------|---------|
| default    | Default value                                                                                                                         | False   |
| required   | Whether it is required                                                                                                                | False   |
| allow_none | Whether the value can be empty                                                                                                        | True    |
| multi      | Whether it is a multi-value                                                                                                           | False   |
| func       | Custom function                                                                                                                       | None    |
| convert    | Whether to convert the string to a bool type. When True, it converts "True" to True, "False" to False as bool types, case-insensitive | True    |

#### datetime/date

| Rule          | Description                                                                                    | Default |
|---------------|------------------------------------------------------------------------------------------------|---------|
| default       | Default value                                                                                  | False   |
| required      | Whether it is required                                                                         | False   |
| allow_none    | Whether the value can be empty                                                                 | True    |
| multi         | Whether it is a multi-value                                                                    | False   |
| func          | Custom function                                                                                | None    |
| fmt           | Date formatting style. For datetime, it is `%Y-%m-%d %H:%M:%S`, and for date, it is `%Y-%m-%d` | None    |
| gt/gte/lt/lte | Date comparison                                                                                | None    |
| enum          | Whether the date is in the specified enumeration                                               | None    |

### Nested structured data types

#### dict

| Rule       | Description                                                   | Default |
|------------|---------------------------------------------------------------|---------|
| default    | Default value                                                 | False   |
| required   | Whether it is required                                        | False   |
| allow_none | Whether the value can be empty                                | True    |
| multi      | Whether it is a multi-value                                   | False   |
| func       | Custom function                                               | None    |
| subset     | Defined nested rules                                          |         |
| dest       | Ignore all validations and directly obtain the original value |         |

#### list

| Rule       | Description                                                   | Default |
|------------|---------------------------------------------------------------|---------|
| default    | Default value                                                 | False   |
| required   | Whether it is required                                        | False   |
| allow_none | Whether the value can be empty                                | True    |
| multi      | Whether it is a multi-value                                   | False   |
| func       | Custom function                                               | None    |
| subset     | Defined nested rules                                          |         |
| dest       | Ignore all validations and directly obtain the original value |         |

### Extended Data Types

#### email

Validate whether the string is an email address.

| Rule       | Description                    | Default |
|------------|--------------------------------|---------|
| default    | Default value                  | False   |
| required   | Whether it is required         | False   |
| allow_none | Whether the value can be empty | True    |
| multi      | Whether it is a multi-value    | False   |
| func       | Custom function                | None    |

#### ipv4

Validate whether the string is an IPv4 address.

| Rule       | Description                    | Default |
|------------|--------------------------------|---------|
| default    | Default value                  | False   |
| required   | Whether it is required         | False   |
| allow_none | Whether the value can be empty | True    |
| multi      | Whether it is a multi-value    | False   |
| func       | Custom function                | None    |

#### ipv6

Validate whether the string is an IPv6 address.

| Rule       | Description                    | Default |
|------------|--------------------------------|---------|
| default    | Default value                  | False   |
| required   | Whether it is required         | False   |
| allow_none | Whether the value can be empty | True    |
| multi      | Whether it is a multi-value    | False   |
| func       | Custom function                | None    |

#### phone

Validate whether the string is a phone number.

| Rule       | Description                    | Default |
|------------|--------------------------------|---------|
| default    | Default value                  | False   |
| required   | Whether it is required         | False   |
| allow_none | Whether the value can be empty | True    |
| multi      | Whether it is a multi-value    | False   |
| func       | Custom function                | None    |
| region     | Phone number region            | CN      |

#### addr

Validate whether the string is a URL.

| Rule       | Description                    | Default |
|------------|--------------------------------|---------|
| default    | Default value                  | False   |
| required   | Whether it is required         | False   |
| allow_none | Whether the value can be empty | True    |
| multi      | Whether it is a multi-value    | False   |
| func       | Custom function                | None    |

