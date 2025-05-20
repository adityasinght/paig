# ai_asset.py

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AIAsset(Base):
    __tablename__ = "ai_asset"

    id = Column(Integer, primary_key=True)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    created_by = Column(String)
    updated_by = Column(String)
    name = Column(String)
    uuid = Column(String, unique=True)
    location = Column(String)
    status = Column(String)
    owner = Column(String)
    type = Column(String)
    discovered_on = Column(String)  # Or use Date
    risk_score = Column(Integer)
    risk_level = Column(String)
    ai_model = Column(String)
    description = Column(Text)
    meta_data = Column(JSONB)
