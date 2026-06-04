from sqlalchemy.ext.asyncio import AsyncSession # here used to type hint the session that we will use to interact with the database in the seed functions.
from app.db.seeds.users import seed_roles, seed_users # Importing the seed_roles and seed_users functions from the seeds.users module to seed the roles and users tables with initial data.


async def seed_database(db: AsyncSession):  # getting the session as an argument to interact with the database
    await seed_roles(db) # Calling the seed_roles function to seed the roles table with initial data. We pass the session that we created as an argument to the seed_roles function so that it can interact with the database to seed the data.
    await seed_users(db)

# this session has been created by main.py and passed to the seed_database function to seed the database with initial data when the application starts up. The seed_database function will call the seed_roles and seed_users functions to seed the roles and users tables with initial data.

# single session is used to seed all the tables in the database, which is more efficient than creating a new session for each table. This allows us to perform all the seeding operations in a single transaction, which can help to improve performance and reduce the number of database transactions.