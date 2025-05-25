from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.readers import Reader
from app.schemas.readers import UpdateReader, GetReader, CreateReader
from app.core.database import is_existing
from app.core.exceptions import NotFoundError, AlreadyExistsError

def get_readers(session: Session):
    result = session.execute(select(Reader))
    return result.scalars().all()


def get_reader(session: Session, reader_id: int):
    reader = session.get(Reader, reader_id)

    if reader is None:
        raise NotFoundError("Reader not found")
    
    return reader


def create_reader(session: Session, reader_in: CreateReader):
    reader = Reader(**reader_in.model_dump())

    if is_existing(session, Reader, email=reader_in.email):
        raise AlreadyExistsError("Email already in use")
    
    session.add(reader)
    session.commit()
    session.refresh(reader)
    return reader


def update_reader(session: Session, reader_id: int, reader_in: UpdateReader):
    reader = session.get(Reader, reader_id)

    if reader is None:
        raise NotFoundError("Reader not found")
    
    if reader_in.email is not None and reader_in.email != reader.email:
        if is_existing(session, Reader, email=reader_in.email):
            raise AlreadyExistsError("Email already in use")

    for field, value in reader_in.model_dump(exclude_unset=True).items():
        setattr(reader, field, value)

    session.commit()
    session.refresh(reader)
    return reader


def delete_reader(session: Session, reader_id: int):
    reader = session.get(Reader, reader_id)

    if reader is None:
        raise NotFoundError("Reader not found")

    session.delete(reader)
    session.commit()
    return reader
