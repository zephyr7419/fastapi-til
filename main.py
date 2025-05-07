from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from containers import Container
from user.interface.controllers.user_controller import router as user_routers

app = FastAPI()
app.container = Container()

app.include_router(user_routers)
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors()},
    )