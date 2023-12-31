from models import Note,User
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from passlib.context import CryptContext


async def get_all_note(async_session: async_sessionmaker[AsyncSession]):
    async with async_session() as session:
        statement = select(Note).order_by(Note.id)
        result = await session.execute(statement)
    return result.scalars()


async def add(async_session: async_sessionmaker[AsyncSession], note: Note):
    async with async_session() as session:
        session.add(note)
        await session.commit()
    return note


async def get_by_id(async_session: async_sessionmaker[AsyncSession], note_id: int):
    async with async_session() as session:
        statement = select(Note).filter(Note.id == note_id)
        try:
            result = await session.execute(statement)
            return result.scalars().one()

        except:
            raise HTTPException(
                status_code=404, detail=f"Note with id {note_id} not found."
            )


async def update(async_session: async_sessionmaker[AsyncSession], note_id: int, data):
    async with async_session() as session:
        statement = select(Note).filter(Note.id == note_id)
        try:
            result = await session.execute(statement)
            note = result.scalars().one()
            note.title = data["title"]
            note.content = data["content"]
            await session.commit()
            return note

        except:
            raise HTTPException(
                status_code=404, detail=f"Note with id {note_id} not found."
            )


async def delete(async_session: async_sessionmaker[AsyncSession], note_id: int):
    async with async_session() as session:
        statement = select(Note).filter(Note.id == note_id)
        try:
            result = await session.execute(statement)
            note = result.scalars().one()
            await session.delete(note)
            await session.commit()
        except:
            raise HTTPException(
                status_code=404, detail=f"Note with id {note_id} not found."
            )



pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

async def hash_password(password:str):
    return pwd_context.hash(password)

async def create_user(async_session:async_sessionmaker[AsyncSession],user:User):
    async with async_session() as session:
        session.add(user)
        await session.commit()
        return user

async def get_users(async_session:async_sessionmaker[AsyncSession]):
    async with async_session() as session:
        statement = select(User).order_by(User.id)
        result = await session.execute(statement)
        return result.scalars()
    
async def get_user_by_id(async_session:async_sessionmaker[AsyncSession],user_id:str):
    async with async_session() as session:
        statement = select(User).filter(User.id == user_id)
        try:
            result = await session.execute(statement)
            return result.scalars().one()
        except:
            raise HTTPException(status_code=404, detail=f"User with this id {user_id} Not found")
