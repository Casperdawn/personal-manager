import os
import sys
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    DATABASE_TYPE: str = "sqlite"
    
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "password"
    MYSQL_DB: str = "personal_manager"

    class Config:
        env_file = ".env"

    @property
    def database_url(self):
        if self.DATABASE_TYPE == "mysql":
            return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"
        if getattr(sys, 'frozen', False):
            db_path = os.path.join(os.path.dirname(sys.executable), "personal_manager.db")
        else:
            db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "personal_manager.db")
        return f"sqlite:///{db_path}"


settings = Settings()
