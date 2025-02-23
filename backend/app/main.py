
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from .routes.users_route import router as users_router

app = FastAPI()
app.include_router(users_router, prefix='/users', tags=["Users"])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    msg = exc.errors()[0]["msg"]
    return JSONResponse({"detail": msg}, status_code=400)


@app.get("/")
async def home():
    return PlainTextResponse("Hello, World!")


app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
