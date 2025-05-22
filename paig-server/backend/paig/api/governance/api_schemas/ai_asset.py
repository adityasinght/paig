from core.factory.database_initiator import BaseAPIFilter
from core.api_schemas.base_view import BaseView
from datetime import datetime
from typing import Optional, Dict, List
from pydantic import Field, BaseModel, constr


class AIAssetView(BaseView):
    """
    A model representing an AI Asset.

    Inherits from:
        BaseView: The base model containing common fields.

    Attributes:
        id (Optional[int]): The unique identifier of the AI Asset.
        name (str): The unique name of the AI Asset.
        description (Optional[str]): The description of the AI Asset.
        asset_type (str): The type of the AI Asset.
        meta_data (Optional[Dict]): Additional metadata for the AI Asset.
        created_by (Optional[str]): The user who created the AI Asset.
        updated_by (Optional[str]): The user who last updated the AI Asset.
        created_at (Optional[str]): The timestamp when the AI Asset was created.
        updated_at (Optional[str]): The timestamp when the AI Asset was last updated.
        uuid (Optional[str]): The unique UUID of the AI Asset.
        location (Optional[str]): The location of the AI Asset.
        status (Optional[str]): The current status of the AI Asset.
        owner (Optional[str]): The owner of the AI Asset.
        source (Optional[str]): The source of the AI Asset.
        risk_score (Optional[int]): The risk score associated with the AI Asset.
        risk_level (Optional[str]): The risk level of the AI Asset.
        ai_model (Optional[str]): The AI model associated with the Asset.
    """
    id: Optional[int] = Field(None, description="The unique identifier of the AI Asset")
    name: str = Field(..., description="The unique name of the AI Asset", pattern=r"^[^~!@#$%^&*(),|\"']+$")
    description: Optional[str] = Field(None, description="The description of the AI Asset", max_length=4000)
    asset_type: str = Field(..., description="The type of the AI Asset", alias="assetType")
    meta_data: Optional[Dict] = Field(None, description="Additional metadata for the AI Asset")
    created_by: Optional[str] = Field(None, description="The user who created the AI Asset")
    updated_by: Optional[str] = Field(None, description="The user who last updated the AI Asset")
    created_at: Optional[str] = Field(None, description="The timestamp when the AI Asset was created")
    updated_at: Optional[str] = Field(None, description="The timestamp when the AI Asset was last updated")
    uuid: Optional[str] = Field(None, description="The unique UUID of the AI Asset")
    location: Optional[str] = Field(None, description="The location of the AI Asset")
    status: Optional[int] = Field(None, description="The current status of the AI Asset")
    owner: Optional[str] = Field(None, description="The owner of the AI Asset")
    source: Optional[str] = Field(None, description="The source of the AI Asset")
    risk_score: Optional[int] = Field(None, description="The risk score associated with the AI Asset", alias="riskScore")
    risk_level: Optional[str] = Field(None, description="The risk level of the AI Asset", alias="riskLevel")
    ai_model: Optional[str] = Field(None, description="The AI model associated with the Asset", alias="aiModel")
    ai_application_id: Optional[int] = Field(None, description="The AI application ID associated with the Asset", alias="aiApplicationId")

    model_config = BaseView.model_config

class CreateAIAssetView(BaseModel):
    """
    A model for creating a new AI Asset.

    Attributes:
        name (str): The name of the AI asset.
        location (str): The location of the AI asset.
        asset_type (str): The type of the AI asset.
        owner (str): The owner of the AI asset.
        ai_model (str): The AI model associated with the asset.
        description (Optional[str]): The description of the AI asset.
        risk_score (Optional[int]): The risk score associated with the AI asset.
        risk_level (Optional[str]): The risk level of the AI asset.
        meta_data (Optional[dict]): Additional metadata for the AI asset.
    """
    name: str = Field(..., description="The unique name of the AI Asset", pattern=r"^[^~!@#$%^&*(),|\"']+$")
    location: str = Field(None, description="The location of the AI asset")
    asset_type: str = Field(..., description="The type of the AI asset", alias="assetType")
    owner: str = Field(..., description="The owner of the AI asset")
    ai_model: str = Field(None, description="The AI model associated with the asset", alias="aiModel")
    description: Optional[str] = Field(None, description="The description of the AI asset", max_length=4000)
    risk_score: Optional[int] = Field(default=None, description="The risk score associated with the AI asset", alias="riskScore")
    risk_level: Optional[str] = Field(default=None, description="The risk level of the AI asset", alias="riskLevel")
    meta_data: Optional[Dict] = Field(None, description="Additional metadata for the AI asset")
    ai_application_id: Optional[int] = Field(None, description="The AI application ID associated with the Asset", alias="aiApplicationId")
    
    model_config = BaseView.model_config

class UpdateAIAssetView(BaseModel):
    """
    A model for updating an existing AI Asset.

    Attributes:
        name (Optional[str]): The name of the AI asset.
        location (Optional[str]): The location of the AI asset.
        asset_type (Optional[str]): The type of the AI asset.
        owner (Optional[str]): The owner of the AI asset.
        status (Optional[str]): The current status of the AI asset.
        ai_model (Optional[str]): The AI model associated with the asset.
        description (Optional[str]): The description of the AI asset.
        risk_score (Optional[int]): The risk score associated with the AI asset.
        risk_level (Optional[str]): The risk level of the AI asset.
        meta_data (Optional[dict]): Additional metadata for the AI asset.
    """
    name: Optional[str] = Field(None, description="The unique name of the AI Asset", pattern=r"^[^~!@#$%^&*(),|\"']+$")
    location: Optional[str] = Field(None, description="The location of the AI asset")
    asset_type: Optional[str] = Field(None, description="The type of the AI asset", alias="assetType")
    owner: Optional[str] = Field(None, description="The owner of the AI asset")
    status: Optional[int] = Field(None, description="The status of the AI Asset (1 for active, 0 for inactive)")
    ai_model: Optional[str] = Field(None, description="The AI model associated with the asset", alias="aiModel")
    description: Optional[str] = Field(None, description="The description of the AI asset", max_length=4000)
    risk_score: Optional[int] = Field(default=None, description="The risk score associated with the AI asset", alias="riskScore")
    risk_level: Optional[str] = Field(default=None, description="The risk level of the AI asset", alias="riskLevel")
    meta_data: Optional[Dict] = Field(None, description="Additional metadata for the AI asset")
    ai_application_id: Optional[int] = Field(None, description="The AI application ID associated with the Asset", alias="aiApplicationId")
    model_config = BaseView.model_config

class AIAssetFilter(BaseAPIFilter):
    """
    Filter class for AI Asset queries.

    Attributes:
        id (Optional[int]): Filter by AI Asset ID.
        name (Optional[str]): Filter by AI Asset name.
        asset_type (Optional[str]): Filter by AI Asset type.
        exact_match (Optional[bool]): Whether to perform exact matching.
    """
    id: Optional[int] = Field(None, description="Filter by AI Asset ID")
    name: Optional[str] = Field(None, description="Filter by AI Asset name")
    asset_type: Optional[str] = Field(None, description="Filter by AI Asset type")
    exact_match: Optional[bool] = Field(False, description="Whether to perform exact matching")

    model_config = BaseView.model_config