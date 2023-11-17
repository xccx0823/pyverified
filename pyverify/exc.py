from typing import TypedDict, List


class ErrorInfo(TypedDict):
    """错误信息结构"""
    key: str
    msg: str


class Error:
    """异常信息类"""

    def __init__(self):
        self.errors: List[ErrorInfo] = []

    def isnull(self):
        return not bool(self.errors)

    def push(self, key: str, msg: str):
        err_info = {'key': key, 'msg': msg}
        if err_info not in self.errors:
            self.errors.append({'key': key, 'msg': msg})


class VerifyError(Exception):
    """参数校验失败"""

    def __init__(self, err: Error):
        self.err = err

    def __str__(self):
        error_msg = ''
        for error in self.err.errors:
            key = error['key']
            msg = error['msg']
            error_msg += f'\n  {key}: {msg}'
        return error_msg
