import textwrap
from abc import ABC

from data.sqlite_db_helper import SQLite3Helper


class DAO(ABC):
    """
    Implementação base para todos os objetos de acesso a dados.
    """

    def __init__(self, helper: SQLite3Helper):
        self.helper = helper

    @staticmethod
    def insert_break_line(text, text_wrap_limit=32):
        """
        Função utilizada para adicionar quebra de linha no texto caso o mesmo ultrapasse `text_wrap_limit`.

        :param text: Texto avaliado
        :param text_wrap_limit:  Quantidade de caracteres que define o momento de quebrar linha.
        """
        if len(text) <= text_wrap_limit:
            return text
        else:
            wrapped_text = textwrap.wrap(text, width=text_wrap_limit, break_long_words=False)
            return '<br>'.join(wrapped_text)

    @staticmethod
    def remove_break_lines(text):
        """
        Função utilizada para remover a quebra de linha em momentos onde ela possa atrapalhar. Por exemplo, ao realizar
        filtros.

        :param text: Texto que serão removidas as quebras de linha
        """
        return text.replace('<br>', ' ')