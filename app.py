from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import List
from services.data_loader import load_characters_from_json
from services.character_service import CharacterService
import os


app = FastAPI()

characters_filepath = os.path.join('data', 'characters.json')
characters = load_characters_from_json(characters_filepath)


character_service = CharacterService(characters)


# Exception-Handler
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": "Invalid request parameters", "details": exc.errors()},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "details": str(exc)},
    )

@app.get("/characters")
def get_characters(limit: int = Query(0, ge= 0) ,skip : int = Query(0, ge=0)):
    result = character_service.get_all_characters(limit=limit, skip=skip)
    return [char.to_dict() for char in result]


@app.get("/characters/{character_id}")
def get_character_by_id(character_id : int):
    character = character_service.get_character_by_id(character_id)
    if character:
        return character.to_dict()
    raise HTTPException(status_code=404, detail="Character not found")




# Hinweis: Starte die App über Uvicorn: uvicorn app:app --reload --host 0.0.0.0 --port 8000
