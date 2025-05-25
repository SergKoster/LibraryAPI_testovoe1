from datetime import datetime, timezone

from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.books import Book
from app.models.readers import Reader
from app.models.borrows import Borrow
from app.schemas.borrows import UpdateBorrow, GetBorrow, CreateBorrow
from app.core.exceptions import NotFoundError, ReaderAlreadyHasThisBook, NoCopiesAvailable, ReaderLimit, AlreadyReturned


def get_borrows(session: Session):
    result = result = session.execute(select(Borrow))
    return result.scalars().all()


def get_borrow(session:Session, borrow_id: int):
    borrow = session.get(Borrow, borrow_id)

    if not borrow:
        raise NotFoundError("Borrow not found")
    
    return borrow


def create_borrow(session: Session, borrow_in: CreateBorrow):
    book = session.get(Book, borrow_in.book_id)
    reader = session.get(Reader, borrow_in.reader_id)

    if book is None or reader is None:
        raise NotFoundError("Book or reader not found")

    if not is_book_available(session, borrow_in.book_id):
        raise NoCopiesAvailable("No copies available")

    if reader_has_book(session, borrow_in.reader_id, borrow_in.book_id):
        raise ReaderAlreadyHasThisBook("This book is already borrowed by this reader")

    if reader_active_borrow_count(session, borrow_in.reader_id) >= 3:
        raise ReaderLimit("Reader has reached the borrowing limit (3 books)")

    
    borrow = Borrow(
        book_id=borrow_in.book_id,
        reader_id=borrow_in.reader_id,
        borrow_date=borrow_in.borrow_date or datetime.now(timezone.utc),
        return_date=None,
    )
    session.add(borrow)
    book.copies -= 1
    session.commit()
    session.refresh(borrow)
    return borrow


def update_borrow(session: Session, borrow_id: int, borrow_in: UpdateBorrow):
    borrow = session.get(Borrow, borrow_id)
    if borrow is None:
        raise NotFoundError("Borrow not found")

    for field, value in borrow_in.model_dump(exclude_unset=True).items():
        setattr(borrow, field, value)

    session.commit()
    session.refresh(borrow)
    return borrow


def delete_borrow(session: Session, borrow_id: int):
    borrow = session.get(Borrow, borrow_id)

    if borrow is None:
        raise NotFoundError("Borrow not found")

    session.delete(borrow)
    session.commit()
    return borrow


def get_active_books_by_reader(session: Session, reader_id: int):
    from app.models.books import Book
    from app.models.borrows import Borrow

    # Получаем все книги, которые этот reader взял и ещё не вернул
    result = (
        session.query(Book)
        .join(Borrow, Borrow.book_id == Book.id)
        .filter(Borrow.reader_id == reader_id, Borrow.return_date == None)
        .all()
    )
    return result


def return_borrow(session: Session, borrow_id: int, return_date: datetime = None):
    borrow = session.get(Borrow, borrow_id)
    if borrow is None:
        raise NotFoundError("Borrow not found")
    if borrow.return_date is not None:
        raise AlreadyReturned("Book already returned")
    borrow.return_date = return_date or datetime.now(timezone.utc)
    book = session.get(Book, borrow.book_id)
    if book:
        book.copies += 1
    session.commit()
    session.refresh(borrow)
    return borrow


# Бизнес логика 


def reader_active_borrow_count(session: Session, reader_id: int) -> int:
    """Проверка, сколько у читателя взято книг в данный момент"""
    borrows = session.execute(
        select(Borrow).where(
            Borrow.reader_id == reader_id,
            Borrow.return_date == None,
        )
    ).scalars().all()
    return len(borrows)


def reader_has_book(session: Session, reader_id: int, book_id: int) -> bool:
    """Проверка, есть ли данная книга уже у читателя"""
    borrow = session.execute(
        select(Borrow)
        .where(
            Borrow.reader_id == reader_id,
            Borrow.book_id == book_id,
            Borrow.return_date == None,
        )
    ).scalar_one_or_none()
    return borrow is not None


def is_book_available(session: Session, book_id: int) -> bool:
    """Проверка, есть ли в наличии нужная книга 
    (кол-во на складе больше 0)"""
    book = session.get(Book, book_id)
    return book is not None and book.copies > 0


