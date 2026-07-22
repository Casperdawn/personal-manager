import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.database import engine, Base
from app.routes import auth, todo, finance, learning, health
from app.models.user import User
from app.utils.security import get_password_hash

app = FastAPI(title="Personal Manager", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(todo.router, prefix="/api/todo", tags=["Todo"])
app.include_router(finance.router, prefix="/api/finance", tags=["Finance"])
app.include_router(learning.router, prefix="/api/learning", tags=["Learning"])
app.include_router(health.router, prefix="/api/health", tags=["Health"])


if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
    if hasattr(sys, '_MEIPASS'):
        STATIC_DIR = os.path.join(sys._MEIPASS, 'static')
    else:
        STATIC_DIR = os.path.join(BASE_DIR, 'static')
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    STATIC_DIR = os.path.join(BASE_DIR, '..', 'frontend', 'dist')

print(f"Static files directory: {STATIC_DIR}")
print(f"Static files exist: {os.path.exists(STATIC_DIR)}")

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        file_path = os.path.join(STATIC_DIR, full_path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(STATIC_DIR, "index.html"))

    @app.get("/")
    async def root():
        return FileResponse(os.path.join(STATIC_DIR, "index.html"))
else:
    @app.get("/")
    def root():
        return {"message": "Welcome to Personal Manager API"}


def init_db():
    Base.metadata.create_all(bind=engine)
    from app.core.database import SessionLocal
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.username == "hzs").first()
        if not existing_user:
            hashed_password = get_password_hash("123")
            user = User(username="hzs", email="hzs@example.com", hashed_password=hashed_password)
            db.add(user)
            db.commit()
            print("默认用户创建成功: hzs / 123")
    finally:
        db.close()


init_db()

if __name__ == "__main__" or getattr(sys, 'frozen', False):
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
