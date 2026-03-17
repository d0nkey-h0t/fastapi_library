from fastapi import HTTPException
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config import MSG_NOT_FOUND
from models.books import BookModel
from schemas.books import SBookAdd


class BookRepository:
    @classmethod
    async def add_one(cls, data: SBookAdd, session: AsyncSession) -> BookModel:
        # 1. Превращаем данные из Pydantic в словарь
        book_dict = data.model_dump()

        # 2. Создаем объект модели
        book = BookModel(**book_dict)

        # 3. Добавляем и сохраняем
        session.add(book)
        await session.commit()
        await session.refresh(book)

        # 4. Возвращаем созданный объект
        return book

    @classmethod
    async def get_all(cls, session: AsyncSession):
        # 1. Готовим запрос
        query = select(BookModel)

        # 2. Выполняем
        result = await session.execute(query)

        # 3. Возвращаем список объектов
        return result.scalars().all()

    @classmethod
    async def get_one(cls, book_id: int, session: AsyncSession) -> type[BookModel]:
        book = await session.get(BookModel, book_id)
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=MSG_NOT_FOUND)

        # 3. Возвращаем объект
        return book

    @classmethod
    async def update_one(cls, book_id: int, data: SBookAdd, session: AsyncSession) -> type[BookModel] | None:
        book = await session.get(BookModel, book_id)
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=MSG_NOT_FOUND)

        # 1. Готовим запрос
        query = update(BookModel).where(BookModel.id == book_id).values(**data.model_dump())

        # 2. Выполняем
        await session.execute(query)

        # 4. Возвращаем обновлённый объект
        await session.refresh(book)
        return book

    @classmethod
    async def delete_one(cls, book_id: int, session: AsyncSession):
        book = await session.get(BookModel, book_id)
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=MSG_NOT_FOUND)

        # 1. Готовим запрос
        query = delete(BookModel).where(BookModel.id == book_id)

        # 2. Выполняем
        await session.execute(query)
