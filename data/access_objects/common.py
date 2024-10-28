import textwrap
from abc import ABC

from data.sqlite_db_helper import SQLite3Helper


class DAO(ABC):

    def __init__(self, helper: SQLite3Helper):
        self.helper = helper

    @staticmethod
    def insert_break_line(text, text_wrap_limit=32):
        if len(text) <= text_wrap_limit:
            return text
        else:
            wrapped_text = textwrap.wrap(text, width=text_wrap_limit, break_long_words=False)
            return '<br>'.join(wrapped_text)

    @staticmethod
    def remove_break_lines(text):
        return text.replace('<br>', ' ')