class NotFoundError(Exception):
    """Вызывается, когда объект не найден в базе."""
    pass

class AlreadyExistsError(Exception):
    """Вызывается, когда объект уже существует."""
    pass

class NoCopiesAvailable(Exception):
    """Вызывается, когда нет копий книги для выдачи."""
    pass

class ReaderAlreadyHasThisBook(Exception):
    """Вызывается, когда пользователь уже взял эту книгу."""
    pass

class ReaderLimit(Exception):
    """Вызывается, когда пользователь уже взял 3 книги."""
    pass

class AlreadyReturned(Exception):
    """Вызывается, когда пользователь уже вернул эту книгу"""
    pass