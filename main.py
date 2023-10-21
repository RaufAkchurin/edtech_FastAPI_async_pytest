import uvicorn
from fastapi import APIRouter
from fastapi import FastAPI

from api.handlers import user_router

# BLOCK WITH ROUTERS
#############################

# create instance of the app
app = FastAPI(title="luchanos-oxford-iniversity")


###########################################
# create main router who collect all routers
###########################################

main_api_router = APIRouter()
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
