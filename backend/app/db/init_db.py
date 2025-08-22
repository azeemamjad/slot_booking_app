from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User, UserRole
from app.models.department import Department
from app.core.security import get_password_hash


async def init_db(db: AsyncSession) -> None:
    """Initialize database with default data (if needed)."""

    # Ensure at least one Department exists
    result = await db.execute(select(Department))
    department = result.scalars().first()
    if not department:
        department = Department(title="General", description="Default Department")
        db.add(department)
        await db.commit()
        await db.refresh(department)

    # Ensure superuser exists
    result = await db.execute(select(User).filter(User.role == UserRole.ADMIN))
    admin_user = result.scalars().first()
    if not admin_user:
        user = User(
            email="admin@example.com",
            username="admin",
            password=get_password_hash("admin123"),  # hashed!
            role=UserRole.ADMIN,
            department_id=department.id,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
