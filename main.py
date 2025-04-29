from fastapi import APIRouter
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

# http://127.0.0.1:8000/api/login Puerto FRONT
# http://127.0.0.1:8000/api/rlogin Puerto BACK
# http://127.0.0.1:8000/api/register Puerto FRONT
# http://127.0.0.1:8000/api/okregister Puerto FRONT
# http://127.0.0.1:8000/api/oficinas Puerto FRONT
# http://127.0.0.1:8000/api/availability Puerto FRONT
# http://127.0.0.1:8000/api/{id_user}/reserve Puerto FRONT
# http://127.0.0.1:8000/api/{id_user}/rreserve Puerto BACK


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from user import router1, router2, router3, router4
from offices import router5, router10
from availability import router6
from reservas import router7, router8, router9

app.include_router(router1)
app.include_router(router2)
app.include_router(router3)
app.include_router(router4)

app.include_router(router5)
app.include_router(router10)

app.include_router(router6)

app.include_router(router7)
app.include_router(router8)
app.include_router(router9)

