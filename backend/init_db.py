from app.core.database import engine, Base
from app.models.user import User
from app.models.todo import Todo
from app.models.finance import Finance
from app.models.learning import Learning

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created successfully!")
print("Tables: users, todos, finance, learning")
