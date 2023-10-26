import uvicorn
from fastapi import APIRouter
from fastapi import FastAPI

import settings
from api.handlers import user_router
from api.login_handler import login_router
from api.service import service_router

# BLOCK WITH ROUTERS
#############################

# create instance of the app
app = FastAPI(title="luchanos-oxford-iniversity")


###########################################
# create main router who collect all routers
###########################################

main_api_router = APIRouter()
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(login_router, prefix="/login", tags=["login"])
main_api_router.include_router(service_router, tags=["service"])
app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.APP_PORT)
