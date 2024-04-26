from fastapi import FastAPI, HTTPException
import random
import json
import os
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Literal, Optional
from uuid import uuid4

app = FastAPI()

class Book(BaseModel):
    name: str
    price: float

    id: Optional[str]=uuid4().hex
    genre: Literal["Fiction","Non-Fiction"]

BOOK_FILE ="books.json" 
BOOK_DATABASE = []

@app.get("/")
async def home():
    return "Bem vindos a loja de livros."
 
@app.get("/list-books")
async def list_books():
    return {
        "books":BOOK_DATABASE
    }

if os.path.exists(BOOK_FILE):
    with open(BOOK_FILE,"r") as f:
        BOOK_DATABASE = json.load(f)

@app.get("/list-book-by-index/{index}")

async def list_book_by_index(index:int):
    if index < 0 or index >=len(BOOK_DATABASE):
        raise HTTPException(404,"Index out of range")
    else:
        return {
            "books":BOOK_DATABASE[index]
    }

@app.get("/get-randon-book")
async def get_randon_book():
    if (len(BOOK_DATABASE) != 0):
        book = random.choice(BOOK_DATABASE)
        return{
            "book":book
        }
    else:
        return{
            "No books"
        }

@app.post("/add-book")
async def add_book(book:Book):
    book.id=uuid4().hex
    json_book = jsonable_encoder(book)
    BOOK_DATABASE.append(json_book)

    with open(BOOK_FILE,"w") as f:
        json.dump(BOOK_DATABASE, f)
    return {
        "message":f"Seu livro {book} foi adicionado!"
    }

@app.delete("/remove-book")
async def remove_book(book:int):
    BOOK_DATABASE.pop(book) 
    with open(BOOK_FILE,"w") as f:
        json.dump(BOOK_DATABASE, f)
    return {
        f"Livro removido: {book}"
    }
    
