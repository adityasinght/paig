from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from core.db_models.BaseSQLModel import BaseSQLModel

class AIUser(BaseSQLModel):

    __tablename__ = "ai_user"

    id = Column(Integer, primary_key=True)
    create_time = Column(DateTime)
    last_used = Column(DateTime)
    ai_asset_uuid = Column(String)  # You can set up ForeignKey later
    location = Column(String)
    tenant_id = Column(String)
    username = Column(String)
    email = Column(String)
