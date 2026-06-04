from passlib.context import CryptContext # Importing to hash the passwords before storing them. The CryptContext allows us to specify the hashing algorithm and other options for hashing the passwords. In this case, we are using bcrypt as the hashing algorithm.
from sqlalchemy import select # Importing select to perform select queries on the database to check if the roles and users already exist before seeding them. This helps to prevent duplicate entries in the database when seeding the data multiple times.
from sqlalchemy.ext.asyncio import AsyncSession # Importing AsyncSession to type hint the session that we will use to interact with the database in the seed functions. This allows us to use asynchronous methods for interacting with the database, which can help to improve performance by allowing us to perform multiple operations concurrently without blocking the main thread.

from app.models.users import Role, User # Importing the Role and User models to create instances of these models when seeding the roles and users tables with initial data. We will use these models to create new role and user objects and add them to the database session for seeding the data.


roles_list = [
    {
        "name": "admin",
        "description": "Administrator with full access to all resources and management capabilities."
    },
    {
        "name": "student",
        "description": "Student with limited access to course materials and assignments."
    }
]

users_list = [
    {
        "name": "Admin",
        "email": "admin@gmail.com",
        "phone": "",
        "password": "admin1234",
        "role": "admin"
    },
    {
        "name": "Student",
        "email": "student@gmail.com",
        "phone": "0987654321",
        "password": "student123",
        "role": "student"
    }
]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Creating an instance of the CryptContext with the bcrypt hashing algorithm. This will be used to hash the passwords before storing them in the database. The deprecated="auto" option is used to automatically mark any hashing algorithms that are considered weak or outdated as deprecated, which can help to improve security by encouraging the use of stronger hashing algorithms. In this case, bcrypt is a strong hashing algorithm that is widely used for hashing passwords, so it will not be marked as deprecated.


# This function is used to hash the passwords before storing them in the database. We will use this function in the seed_users function to hash the passwords of the users before adding them to the database session for seeding the data.
def _hash_password(password: str) -> str:
    return pwd_context.hash(password)


async def seed_roles(db: AsyncSession): # taking the session as an argument to interact with the database.

    # looping through the list of roles and checking if the role already exists in the database before seeding it. If the role does not already exist, we create a new Role object with the name of the role and add it to the database session for seeding the data. This helps to prevent duplicate entries in the database when seeding the data multiple times.
    for role_data in roles_list:
        role_name = role_data["name"]
        role_description = role_data["description"]
        existing_role = (
            await db.execute(select(Role).where(Role.name == role_name)) 
        ).scalar_one_or_none() # This method is used to execute the query and return a single result or None if no result is found. If a role with the same name already exists in the database, it will return that role object. If no role with the same name is found, it will return None.

        if not existing_role:
            new_role = Role(name=role_name, description=role_description) # If the existing role is None, we create a new Role object
            db.add(new_role) 

    await db.commit()


async def seed_users(db: AsyncSession):
    role_rows = await db.execute(select(Role))
    roles_by_name = {
        str(getattr(role.name, "value", role.name)): role
        for role in role_rows.scalars().all()
    }

    for user_data in users_list:
        existing_user = (await db.execute(
            select(User).where(User.email == user_data["email"])
        )).scalar_one_or_none()

        if existing_user:
            continue

        role = roles_by_name.get(user_data["role"])
        if not role:
            continue

        db.add(
            User(
                role_id=role.id,
                name=user_data["name"],
                email=user_data["email"],
                phone=user_data["phone"],
                password_hash=_hash_password(user_data["password"]),
            )
        )

    await db.commit()