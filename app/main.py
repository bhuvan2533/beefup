from fastapi import FastAPI
from app.database.models import Base
from app.database.dbSession import engine
from fastapi import FastAPI
from app.routes.api import router as api_router

from app.exception_handlers import general_exception_handler, not_found_exception_handler, http_exception_handler, NotFoundException, HTTPException

app = FastAPI()

#Attaching exception handlers
app.add_exception_handler(Exception, general_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(NotFoundException, not_found_exception_handler)

Base.metadata.create_all(bind=engine)


app.include_router(api_router, prefix="/api")