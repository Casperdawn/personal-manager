from fastapi import FastAPI
from app.core.database import engine, Base
from app.routes import auth, todo, finance, learning

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal Manager", version="1.0.0")

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(todo.router, prefix="/api/todo", tags=["Todo"])
app.include_router(finance.router, prefix="/api/finance", tags=["Finance"])
app.include_router(learning.router, prefix="/api/learning", tags=["Learning"])


@app.get("/")
def root():
    return {"message": "Welcome to Personal Manager API"}
