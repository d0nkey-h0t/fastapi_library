import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from routers.books import books_router
from database import engine, Model
from models.books import BookModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- КОД ПРИ СТАРТЕ ---
    # Мы обращаемся к движку и просим создать все таблицы
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

    print("База данных готова к работе")

    yield  # Разделяет старт и выключение

    # --- КОД ПРИ ВЫКЛЮЧЕНИИ ---
    print("Выключение сервера")


# Передаем lifespan в приложение
app = FastAPI(
    lifespan=lifespan,
    title="Library Manager API",
    description="Учебное приложение для курса по FastAPI",
    version="1.0.0"
)
app.include_router(books_router)

if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8080, reload=True)