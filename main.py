from fastapi import FastAPI

from app.routers.user_router import router
from app.config.development_config import DevelopmentConfig
from app.config.production_config import ProductionConfig
import os

app = FastAPI(
    title="PET USER MANAGEMENT API",
    description=f'Login krne ke kaam aata h, {" ".join(["Jeevitha S", "Harshita", "Priyank"])}',
    version="0.0.1",
    terms_of_service="http://PET_LOGIN.com",
    Developer_Name= ["Jeevitha S", "Harshita", "Priyank"],
    contact={
        "Developer Name": ["Jeevitha S", "Harshita", "Priyank"],
        "website": "http://PET_LOGIN.com",
        "email": "python-folks@gmail.com"
    },
    license_info={
        "name": "LicenseName",
        "url": "http://PET_LOGIN.com"
    },
    docs_url="/docs", redoc_url=None
)

if os.getenv("ENVIRONMENT") == "production":
    config = ProductionConfig()
else:
    config = DevelopmentConfig()

app.include_router(router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
