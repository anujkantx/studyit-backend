from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession # Importing create_async_engine to create an asynchronous engine for connecting to the database, and AsyncSession to create asynchronous sessions for interacting with the database.
from sqlalchemy.orm import sessionmaker # Importing sessionmaker to create a session factory that will be used to create sessions for interacting with the database.

from app.core.config import settings # Importing settings to get the DATABASE_URL from the .env file

engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True  # This option is used to check if the connection to the database is still alive before using it. If the connection is not alive, it will be replaced with a new one from the pool. This helps to prevent errors caused by stale connections in the connection pool.
)

# Till now we have created the engine, now we need to create a sessionmaker that will be used to create sessions for interacting with the database.
SessionLocal = sessionmaker(       
    bind=engine,    # This option is used to bind the sessionmaker to the engine that we created. This means that all the sessions created by this sessionmaker will use the same engine to connect to the database.
    class_= AsyncSession,    # This option is used to specify that the sessions created by this sessionmaker should be of type AsyncSession, which allows us to use asynchronous methods for interacting with the database.
    autocommit=False, # manual commit mode, which means that we need to manually call session.commit() to persist the changes to the database. This gives us more control over when the changes are committed to the database, allowing us to perform multiple operations in a single transaction if needed.
    autoflush=False # flush means that the session will automatically send any pending changes to the database before executing a query. By setting autoflush to False, we are disabling this behavior, which means that we need to manually call session.flush() to send the pending changes to the database before executing a query. This can be useful in certain situations where we want to control when the changes are sent to the database, such as when we want to perform multiple operations in a single transaction without flushing after each operation.
)
