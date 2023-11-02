from fastapi import FastAPI, HTTPException
from crud import get_all_note, get_by_id, add, delete, update
from sqlalchemy.ext.asyncio import async_sessionmaker
from db import engine
from schemas import NoteModel, NoteCreateModel
from typing import List
from models import Note

app = FastAPI(
    title="Postgresql",
    docs_url="/",
    description="Psql project to use database async",
)

session = async_sessionmaker(bind=engine, expire_on_commit=False)


@app.get("/notes", response_model=List[NoteModel])
async def get_all_notes():
    notes = await get_all_note(session)
    return notes


@app.get("/notes/{note_id}")
async def get_notes_by_id(note_id: int):
    note = await get_by_id(session, note_id)
    return note


@app.post("/notes/create")
async def create_note(request: NoteCreateModel):
    new_note = Note(title=request.title, content=request.content)
    note = await add(session, new_note)
    return note


@app.patch("/notes/{note_id}")
async def get_note_by_id_to_update(note_id: int, data: NoteCreateModel):
    note = await update(
        session, note_id, data={"title": data.title, "content": data.content}
    )

    return note


@app.delete("/notes/{note_id}")
async def get_note_delete(note_id: int):
    await delete(session, note_id)
    return "Deleted"
