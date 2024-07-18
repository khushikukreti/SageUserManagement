from fastapi import FastAPI
from app.controllers import auth_controller

app = FastAPI()

# Include the router from the auth_controller
app.include_router(auth_controller.router)
