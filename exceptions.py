class FioTestError(Exception):
    """Общее исключение для ошибок тестирования fio."""
    pass


class FioParseError(Exception):
    """Исключение для ошибок парсинга fio-вывода."""
    pass


class GnuplotError(Exception):
    """Общее исключение для ошибок, связанных с gnuplot."""
    pass


class GnuplotScriptError(Exception):
    """Исключение для ошибок при генерации скрипта gnuplot."""
    pass


class FioOutputParseError(Exception):
    """Исключение, возникающее при ошибке парсинга вывода fio."""
