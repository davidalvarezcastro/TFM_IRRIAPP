"""
    Custom exceptions -> DATABASE
"""


class ExceptionDatabase(Exception):

    def __init__(self, type: str, msg: str, *args):
        super().__init__(args)
        self.type = type
        self.msg = msg

    def __str__(self):
        return f'Database error [{self.type}] => {self.msg}'
