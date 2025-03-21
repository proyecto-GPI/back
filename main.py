from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware

# http://127.0.0.1:8000/login Puerto FRONT
# http://127.0.0.1:8000/rlogin  Puerto BACK
# http://127.0.0.1:8000/register  Puerto FRONT

app = FastAPI()

from user import router1
from user import router2

app.include_router(router1)
app.include_router(router2)

