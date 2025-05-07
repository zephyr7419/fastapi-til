from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, EmailStr

from common.auth import CurrentUser, get_current_user
from containers import Container

router = APIRouter(prefix="/users")

class CreateUserBody(BaseModel):
    name: str = Field(min_length=2, max_length=32)
    email: EmailStr = Field(max_length=64)
    password: str = Field(min_length=8, max_length=32)

class UpdateUser(BaseModel):
    name: str | None = Field(min_length=2, max_length=32, default=None)
    password: str | None = Field(min_length=8, max_length=32, default=None)

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: str
    updated_at: str

class GetUsersResponse(BaseModel):
    total_count: int
    page: int
    users: list[UserResponse]

class UpdateUserBody(BaseModel):
    name: str | None = Field(min_length=2, max_length=32, default=None)
    password: str | None = Field(min_length=8, max_length=32, default=None)

@router.post("", status_code=201, response_model=UserResponse)
@inject
def register_user(
        user: CreateUserBody,
        user_service = Depends(Provide[Container.user_service]),
):
    new_user = user_service.create_user(
        name = user.name,
        email = user.email,
        password = user.password,
    )

    return new_user

@router.get("/{email}", status_code=200)
@inject
def get_user(
        email: str,
        user_service = Depends(Provide[Container.user_service]),
):
    user = user_service.find_user(email)
    return user

@router.put("/{user_id}", status_code=200, response_model=UserResponse)
@inject
def update_user(
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
        body: UpdateUserBody,
        user_service = Depends(Provide[Container.user_service]),
):
    new_user = user_service.update_user(
        user_id = current_user.id,
        name = body.name,
        password = body.password,
    )

    return UserResponse(
        id=new_user.id,
        name=new_user.name,
        email=new_user.email,
        created_at=new_user.created_at.isoformat(),
        updated_at=new_user.updated_at.isoformat()
    )

@router.get("", status_code=200)
@inject
def get_users(
        page: int = 1,
        items_per_page: int = 10,
        user_service = Depends(Provide[Container.user_service]),
) -> GetUsersResponse:
    total_count, users = user_service.get_users(page, items_per_page)

    user_responses = [
        UserResponse(
            id = user.id,
            name = user.name,
            email = user.email,
            created_at = user.created_at.isoformat(),
            updated_at = user.updated_at.isoformat(),
        )
        for user in users
    ]

    return GetUsersResponse(
        total_count = total_count,
        page = page,
        users = user_responses,
    )

@router.delete("", status_code=204)
@inject
def delete_user(
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
        user_service = Depends(Provide[Container.user_service]),
):
    user_service.delete_user(current_user.id)


@router.post("/login", status_code=200)
@inject
def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_service = Depends(Provide[Container.user_service]),
):
    access_token = user_service.login(
        email = form_data.username,
        password = form_data.password,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
