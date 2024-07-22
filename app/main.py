from fastapi import FastAPI
from app.controllers import auth_controller
from fastapi.responses import RedirectResponse

app = FastAPI(
    title="PET USER MANAGEMENT API",
    description=f'Login krne ke kaam aata h, \nDevelopers: {" ".join(["Jeevitha S", "Harshita", "Priyank"])}',
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


# Include the router from the auth_controller
app.include_router(auth_controller.router)

@app.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse(url="/docs")
