from fastapi import APIRouter
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

# http://127.0.0.1:8000/api/login Puerto FRONT
# http://127.0.0.1:8000/api/rlogin  Puerto BACK
# http://127.0.0.1:8000/register  Puerto FRONT

app = FastAPI()

from user import router1
from user import router2
from user import router3
from user import router4

app.include_router(router1)
app.include_router(router2)
app.include_router(router3)
app.include_router(router4)
