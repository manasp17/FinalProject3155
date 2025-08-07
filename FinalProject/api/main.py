import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .routers import index as indexRoute
from .models import model_loader
from .dependencies.config import conf
from fastapi import FastAPI
from routers import sandwiches
from fastapi import FastAPI




app = FastAPI()
app.include_router(sandwiches.router)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model_loader.index()
indexRoute.load_routes(app)





if __name__ == "__main__":
    uvicorn.run(app, host=conf.app_host, port=conf.app_port)


    @app.get("/")
    def root():
        return {"message": "Welcome to the Sandwich Maker API!"}