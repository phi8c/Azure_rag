from sqlalchemy.ext.asyncio import (

 AsyncSession

)

from sqlalchemy import case, select
from sqlalchemy.dialects.postgresql import insert
from uuid import UUID
from typing import Optional

from app.models.conversation import (
    

 Conversation
 

)


class ConversationRepository:
    @staticmethod
    async def increment_chat_request_count(db: AsyncSession, conversation_id: UUID) -> int:
        """Atomically increment the public chat counter, rolling over after three."""
        insert_stmt = insert(Conversation).values(
            id=conversation_id,
            # Legacy DBs may still enforce NOT NULL on user_email.
            user_email="",
            title="Landing page chat",
            request_count=1,
        )
        stmt = insert_stmt.on_conflict_do_update(
            index_elements=[Conversation.id],
            set_={
                "request_count": case(
                    (Conversation.request_count >= 2, 0),
                    else_=Conversation.request_count + 1,
                )
            },
        ).returning(Conversation.request_count)
        count = (await db.execute(stmt)).scalar_one()
        await db.commit()
        return count

    @staticmethod
    async def create(
        db: AsyncSession,
        conversation_id: UUID,
        title: str,
        email: Optional[str] = None,
        
    ):
     item = Conversation( 
                         
        id=conversation_id,
                         
        title=title,
                         
        user_email = email  
                         )
     db.add(item)
     await db.commit()
     await db.refresh(item)
     return item
    
    
    @staticmethod
    async def get_by_email(
        db: AsyncSession,
        email: str,
        
    ):
        query = await db.execute(
        select(
            Conversation
        )
        .where(
            Conversation.user_email == email
        )
    )
        return (

        query

        .scalars()

        .all()

        )
        
    @staticmethod
    async def rename(
        db: AsyncSession,
        id,
        title: str
        
    ):
        query = await db.execute(
            select(
                Conversation
            )
            .where(
                Conversation.id == id
            )
        )
        item = query.scalar_one_or_none()
        if not item:
            return None
        item.title = title
        
        await db.commit()
        await db.refresh(item)
        return item
    @staticmethod
    async def delete(

        db:AsyncSession,

        id

        ):


        query= await db.execute(

        select(

            Conversation

        )

        .where(

            Conversation.id

            ==

            id

        )

        )


        item=query.scalar_one_or_none()


        if not item:

            return False


        await db.delete(

        item

        )


        await db.commit()


        return True
    
    @staticmethod
    async def get_or_create_by_email(
        db: AsyncSession,
        email: str
    ):

        query = await db.execute(
            select(
                Conversation
            )
            .where(
                Conversation.user_email == email
            )
            .order_by(
                Conversation.created_at.asc()
            )
        )

        item = query.scalar_one_or_none()

        if item:
            return item

        item = Conversation(
            user_email=email
        )

        db.add(item)

        await db.commit()

        await db.refresh(item)

        return item
    
    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        conversation_id: UUID,
    ) -> Conversation | None:
        result = await db.execute(
            select(Conversation).where(
                Conversation.id == conversation_id
            )
        )

        return result.scalar_one_or_none()

                
