from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import List, Optional
from auth.users import users
from auth.dependencies import get_current_user
from auth.jwt_handler import create_access_token
from services.data_loader import load_characters_from_json
from services.character_service import CharacterService
from db.database import init_db
from services.admin_service import AdminService

import os


app = FastAPI()
init_db()

characters_filepath = os.path.join("data", "characters.json")
characters = load_characters_from_json(characters_filepath)


character_service = CharacterService(characters)


class CharacterUpdateRequest(BaseModel):
    name: Optional[str] = None
    house: Optional[str] = None
    animal: Optional[str] = None
    symbol: Optional[str] = None
    nickname: Optional[str] = None
    role: Optional[str] = None
    age: Optional[int] = None
    death: Optional[int] = None
    strength: Optional[str] = None


class CharacterCreateRequest(BaseModel):
    name: str
    house: str
    animal: Optional[str] = None
    symbol: Optional[str] = None
    nickname: Optional[str] = None
    role: str
    age: int
    death: Optional[int] = None
    strength: Optional[str] = None


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


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users.get(form_data.username)
    if not user or user["password"] != form_data.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/characters")
def get_characters(
    limit: int = Query(0, ge=0),
    skip: int = Query(0, ge=0),
    name: Optional[str] = None,
    house: Optional[str] = None,
    role: Optional[str] = None,
    age: Optional[int] = None,
    age_more_than: Optional[int] = None,
    age_less_than: Optional[int] = None,
    sort_asc: Optional[str] = None,
    sort_desc: Optional[str] = None,
):
    try:
        result = character_service.get_all_characters(
            limit=limit,
            skip=skip,
            filters={
                "name": name,
                "house": house,
                "role": role,
                "age": age,
                "age_more_than": age_more_than,
                "age_less_than": age_less_than,
            },
            sort_asc=sort_asc,
            sort_desc=sort_desc,
        )
        return [char for char in result]
    except ValueError as e:
        return HTTPException(status_code=400, detail=str(e))


@app.get("/characters/{character_id}")
def get_character_by_id(character_id: int):
    character = character_service.get_character_by_id(character_id)
    if character:
        return character
    raise HTTPException(status_code=404, detail="Character not found")


@app.post("/characters", status_code=201, dependencies=[Depends(get_current_user)])
def create_character(request: CharacterCreateRequest):
    try:
        character_data = request.model_dump()
        existing_character = character_service.get_character_by_name(character_data["name"])
        if existing_character:
            raise HTTPException(status_code=400, detail="Character with this name already exists")
        character = character_service.add_character(character_data)
        return character
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except HTTPException as http_exc:
        raise http_exc  # bewusst geworfene HTTP Fehler nicht umbrechen!
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while creating the character.",
        )


@app.patch("/characters/{character_id}", dependencies=[Depends(get_current_user)])
def update_character(character_id: int, request: CharacterUpdateRequest):
    try:
        updated_data = request.model_dump(
            exclude_unset=True
        )  # Nur Felder, die wirklich gesendet wurden
        print(updated_data, character_id)
        character = character_service.update_character(character_id, updated_data)
        if character:
            return character
        raise HTTPException(status_code=404, detail="Character not found")

    except HTTPException as http_exc:
        raise http_exc  # bewusst geworfene HTTP Fehler nicht umbrechen!
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while updating the character.",
        )


@app.delete("/characters/{character_id}", dependencies=[Depends(get_current_user)])
def delete_character(character_id: int):
    try:
        success = character_service.delete_character(character_id)
        if success:
            return {"message": "Character successfully deleted."}
        raise HTTPException(status_code=404, detail="Character not found")
    except HTTPException as http_exc:
        raise http_exc  # bewusst geworfene HTTP Fehler nicht umbrechen!
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while deleting the character.",
        )


@app.post("/admin/load-json", dependencies=[Depends(get_current_user)])
def load_json_to_db(user: dict = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")

    AdminService.load_json_into_db()
    return {"message": "Characters loaded successfully into database."}
