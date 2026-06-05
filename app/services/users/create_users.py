from app.models.users import User, Role, UserRole, StudentProfile
from app.services.users.get_users import get_users

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

class create_users:
    @staticmethod
    async def create_by_google_info(db: AsyncSession, google_info: dict):
        role = await db.execute(select(Role).where(Role.name == UserRole.STUDENT.value))
        role = role.scalar_one_or_none()
        if not role:
            raise ValueError("Default student role not found in database")

        email = google_info.get("email")
        name = google_info.get("name")
        google_id = google_info.get("sub")
        avatar_url = google_info.get("picture")
        role_id = role.id


        if not email or not name or not google_id:
            raise ValueError("Google info must include email, name, sub (google_id)")

        new_user = User(
            email=email,
            name=name,
            google_id=google_id,
            avatar_url=avatar_url,
            role_id=role_id
        )
        db.add(new_user)
        await db.flush()  # Ensure the new user gets an ID

        profile = StudentProfile(
            user_id=new_user.id,
        )
        db.add(profile)
        await db.commit()
        await db.refresh(new_user)
        return new_user