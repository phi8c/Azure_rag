from app.repositories.conversation_repository import (

 ConversationRepository

)
class ConversationService:
    @staticmethod
    async def create(
        db,
        email
    ):
     return await (
         ConversationRepository.create(
             db,
             email
        
         )
     )
    
    @staticmethod
    async def get_all(
        db,
        email
    ):
        return await (
            ConversationRepository.get_by_email(
                db,
                email
            )
        )
    @staticmethod
    async def delete(
        db,
        id
    ):
        return await (
            ConversationRepository.delete(db, id)
        )
    
    @staticmethod
    async def rename(
        db,
        id,
        title
    ):
        return await (
            ConversationRepository.rename(db, id, title)
        )