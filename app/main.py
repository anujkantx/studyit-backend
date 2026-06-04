from fastapi import FastAPI
from contextlib import asynccontextmanager # Importing asynccontextmanager to manage the lifespan of the application, allowing us to perform startup and shutdown tasks such as seeding the database.

from app.db.session import SessionLocal # Importing the SessionLocal from the session module to create a session for interacting with the database.
from app.db.seed import seed_database # Importing the seed_database function from the seed module to seed the database with initial data.

from app.api.admin.users import router as users_router


@asynccontextmanager # only a decorator that allows us to define an asynchronous context manager, which is used to manage the lifespan of the application.

# function defination for the lifespan of the application, which will be called by the FastAPI framework when the application starts up and shuts down. It will seed the database with initial data when the application starts up.
async def lifespan(app):   
    print('''
═══════════════════════
    Starting App
═══════════════════════
''')
    async with SessionLocal() as db: # Creating a session for interacting with the database using the SessionLocal that we imported from the session module. This session will be used to seed the database with initial data.
        print('Seeding database with initial data...')
        await seed_database(db) # Calling the seed_database function that we imported from the seed module to seed the database with initial data. We pass the session that we created as an argument to the seed_database function so that it can interact with the database to seed the data.
        print('Database seeding completed.')
    yield # Yielding control back to the FastAPI framework to allow the application to run. The code after the yield statement will be executed when the application is shutting down, allowing us to perform any necessary cleanup tasks.
    print('''
═══════════════════════
    Shutting down App
═══════════════════════
''')

app = FastAPI(lifespan=lifespan) # Creating an instance of the FastAPI class and passing the lifespan function that we defined as an argument to the lifespan parameter. This will allow the FastAPI framework to call the lifespan function when the application starts up and shuts down, allowing us to perform startup and shutdown tasks such as seeding the database.


@app.get("/")
def root():
    return {"message": "Welcome to the Studyit API!"}


app.include_router(users_router)