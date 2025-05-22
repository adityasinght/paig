from sqlalchemy import Column, Integer, String, DateTime, Text, JSON
from core.db_models.BaseSQLModel import BaseSQLModel
import uuid


class AIAsset(BaseSQLModel):
    __tablename__ = "ai_asset"

    name = Column(String(255), index=True, unique=True, nullable=False)
    created_by = Column(String(255), nullable=True)
    updated_by = Column(String(255), nullable=True)
    uuid = Column(String(36), default=lambda: str(uuid.uuid4()))
    location = Column(String(255), nullable=True)
    owner = Column(String(255), nullable=False)
    asset_type = Column(String(255), nullable=False)
    source = Column(String(255), nullable=True)
    risk_score = Column(Integer, nullable=True)
    risk_level = Column(String, nullable=True)
    ai_model = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    meta_data = Column(JSON, nullable=True)
    ai_application_id = Column(Integer, nullable=True)
