from fastapi import FastAPI
from app.database.models import Base
from app.database.dbSession import engine
from fastapi import FastAPI
from app.routes.api import router as api_router
from app.exception_handlers import InvalidFileTypeException, invalid_file_type_handler, ResourceNotFoundException, resource_not_found_handler
from app.exception_handlers import InternalServerError, internal_server_error_handler, BadRequestException, bad_request_handler
from app.exception_handlers import unhandled_exception_handler
from fastapi.exceptions import HTTPException as FastAPIHTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.exception_handlers import http_exception_handler

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Attaching exception handlers
app.add_exception_handler(FastAPIHTTPException, http_exception_handler)
app.add_exception_handler(ResourceNotFoundException, resource_not_found_handler)
app.add_exception_handler(InvalidFileTypeException, invalid_file_type_handler)
app.add_exception_handler(InternalServerError, internal_server_error_handler)
app.add_exception_handler(BadRequestException, bad_request_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)

Base.metadata.create_all(bind=engine)


app.include_router(api_router, prefix="/api/v1")