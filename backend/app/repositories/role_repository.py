from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.role import Role

class RoleRepository:
    
    @staticmethod
    async def create(
        db: AsyncSession,
        name: str,
        description: str | None = None
    ):
        role = Role(
            name=name,
            description=description
        )
        
        db.add(role)
        await db.commit()
        await db.refresh(role)
        
        
        return role
    
    @staticmethod
    async def get_all(db: AsyncSession ):
        result = await db.execute(
            select(Role)
        )
        return result.scalars().all()
        