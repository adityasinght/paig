from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from core.db_models.BaseSQLModel import BaseSQLModel

class AIUsageEvent(BaseSQLModel):
    __tablename__ = "ai_usage_event"

    id = Column(Integer, primary_key=True)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    user_id = Column(Integer)  # Add ForeignKey if needed
    event_type = Column(String)
    message = Column(Text)
    ai_asset_id = Column(Integer)  # Add ForeignKey if needed
