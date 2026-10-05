from sqlalchemy import text

from app.core.database import engine


with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))
    print(result.scalar())

# uv run python -m app.scripts.test_database