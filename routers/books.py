from fastapi import APIRouter
from starlette import status

from database import SessionDep
from repositories.books import BookRepository
from schemas.books import *

books_router = APIRouter(
    prefix="/books",
    tags=["Книги"]
)


@books_router.post("", response_model=SBook, status_code=status.HTTP_201_CREATED)
async def create_book(
        book: SBookAdd,
        session: SessionDep
):
    """Создаёт книгу"""
    return await BookRepository.add_one(book, session)


@books_router.get("", response_model=list[SBook])
async def get_books(
        session: SessionDep,
):
    """Возвращает все книги"""
    return await BookRepository.get_all(session)


@books_router.get("/{book_id}", response_model=SBook)
async def get_book(
        book_id: int,
        session: SessionDep
):
    """Возвращает книгу по ID"""
    return await BookRepository.get_one(book_id, session)

@books_router.put("/{book_id}", response_model=SBook)
async def update_book(
        book_id: int,
        book: SBookAdd,
        session: SessionDep
):
    """Изменяет книгу"""
    return await BookRepository.update_one(book_id, book, session)

@books_router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
        book_id: int,
        session: SessionDep
):
    """Удаляет книгу"""
    return await BookRepository.delete_one(book_id, session)
