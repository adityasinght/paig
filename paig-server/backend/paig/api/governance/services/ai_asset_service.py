from typing import List, Dict
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, and_, desc
from datetime import datetime, timedelta

from core.controllers.base_controller import BaseController
from core.controllers.paginated_response import Pageable
from core.exceptions import BadRequestException
from core.exceptions.error_messages_parser import get_error_message, ERROR_RESOURCE_ALREADY_EXISTS
from core.utils import validate_id, SingletonDepends
from api.governance.api_schemas.ai_asset import (
    AIAssetView,
    AIAssetFilter,
    CreateAIAssetView,
    UpdateAIAssetView
)
from api.governance.database.db_models.ai_asset_model import AIAsset
from api.governance.database.db_operations.ai_asset_repository import AIAssetRepository


class AIAssetService(BaseController[AIAsset, AIAssetView]):
    """
    Service class specifically for handling AI Asset entities.

    Args:
        ai_asset_repository (AIAssetRepository): The repository handling AI Asset database operations.
    """

    def __init__(self,
                 ai_asset_repository: AIAssetRepository = SingletonDepends(AIAssetRepository)):
        super().__init__(ai_asset_repository, AIAsset, AIAssetView)

    def get_repository(self) -> AIAssetRepository:
        """
        Get the AI Asset repository.

        Returns:
            AIAssetRepository: The AI Asset repository.
        """
        return self.repository

    async def list_ai_assets(self, filter: AIAssetFilter, page_number: int, size: int, sort: List[str]) -> Pageable:
        """
        Retrieve a paginated list of AI Assets.

        Args:
            filter (AIAssetFilter): Filtering criteria.
            page_number (int): Page number to retrieve.
            size (int): Number of records per page.
            sort (List[str]): List of fields to sort by.

        Returns:
            Pageable: A paginated response containing AI Asset view objects and metadata.
        """
        return await self.list_records(
            filter=filter,
            page_number=page_number,
            size=size,
            sort=sort
        )

    async def create_ai_asset(self, request: CreateAIAssetView) -> AIAssetView:
        """
        Create a new AI Asset.

        Args:
            request (CreateAIAssetView): The view object representing the AI Asset to create.

        Returns:
            AIAssetView: The created AI Asset view object.

        Raises:
            BadRequestException: If an AI Asset with the same name already exists.
        """
        try:
            return await self.create_record(request)
        except IntegrityError as e:
            if "ai_asset.name" in str(e):
                raise BadRequestException(get_error_message(ERROR_RESOURCE_ALREADY_EXISTS, "AI Asset", "name", [request.name]))
            raise

    async def get_ai_asset_by_id(self, id: int) -> AIAssetView:
        """
        Retrieve an AI Asset by its ID.

        Args:
            id (int): The ID of the AI Asset to retrieve.

        Returns:
            AIAssetView: The AI Asset view object corresponding to the ID.
        """
        validate_id(id, "AI Asset ID")
        return await self.get_record_by_id(id)

    async def update_ai_asset(self, id: int, request: UpdateAIAssetView) -> AIAssetView:
        """
        Update an AI Asset identified by its ID.

        Args:
            id (int): The ID of the AI Asset to update.
            request (UpdateAIAssetView): The updated view object representing the AI Asset.

        Returns:
            AIAssetView: The updated AI Asset view object.

        Raises:
            BadRequestException: If an AI Asset with the same name already exists.
        """
        validate_id(id, "AI Asset ID")
        
        try:
            return await self.update_record(id, request)
        except IntegrityError as e:
            if "ai_asset.name" in str(e):
                raise BadRequestException(get_error_message(ERROR_RESOURCE_ALREADY_EXISTS, "AI Asset", "name", [request.name]))
            raise

    async def delete_ai_asset(self, id: int):
        """
        Delete an AI Asset by its ID.

        Args:
            id (int): The ID of the AI Asset to delete.
        """
        validate_id(id, "AI Asset ID")
        await self.delete_record(id)

    async def get_ai_asset_stats(self) -> Dict:
        """
        Get comprehensive statistics about AI Assets in the system.

        This method gathers various metrics and counts about AI Assets by querying the database.
        It uses SQL aggregation functions to efficiently calculate statistics.

        Returns:
            Dict: A dictionary containing the following statistics:
                - total_count (int): Total number of AI Assets
                - by_asset_type (Dict[str, int]): Count of assets by type
                - by_location (Dict[str, int]): Count of assets by location
                - by_risk_level (Dict[str, int]): Count of assets by risk level
                - by_owner (Dict[str, int]): Count of assets by owner
                - by_source (Dict[str, int]): Count of assets by source
                - risk_score_stats (Dict[str, float]): Statistics about risk scores
                - application_assets (int): Count of assets linked to applications
        """
        # TODO: Implement the actual logic to get the statistics
        stats = {
            "total_count": 250,
            "by_asset_type": {
                "Model": 120,
                "Dataset": 80,
                "Pipeline": 50
            },
            "by_location": {
                "us-east-1": 100,
                "us-west-2": 70,
                "eu-central-1": 80
            },
            "by_risk_level": {
                "Low": 130,
                "Medium": 90,
                "High": 30
            },
            "by_owner": {
                "alice@example.com": 60,
                "bob@example.com": 70,
                "carol@example.com": 50,
                "dave@example.com": 70
            },
            "by_source": {
                "internal": 150,
                "third_party": 70,
                "open_source": 30
            },
            "risk_score_stats": {
                "min": 1.2,
                "max": 9.8,
                "avg": 5.6,
                "median": 5.4,
                "std_dev": 2.1
            },
            "application_assets": 110
        }
        return stats

    async def get_user_usage_stats(self) -> Dict:
        """
        Get statistics about AI Asset usage by users.

        Returns:
            Dict: A dictionary containing the following statistics:
                - total_users (int): Total number of unique users
                - active_users (int): Number of users who have used assets in the last 30 days
                - usage_by_user (Dict[str, Dict]): Usage statistics per user
                - top_users (List[Dict]): List of top users by usage
        """
        # TODO: Implement the actual logic to get the statistics
        stats = {
            "total_users": 45,
            "active_users": 32,
            "usage_by_user": {
                "alice@example.com": {
                    "asset_count": 25,
                    "last_used": "2024-03-15T10:30:00Z",
                    "asset_types": {
                        "Model": 15,
                        "Dataset": 8,
                        "Pipeline": 2
                    },
                    "risk_levels": {
                        "Low": 18,
                        "Medium": 5,
                        "High": 2
                    }
                },
                "bob@example.com": {
                    "asset_count": 30,
                    "last_used": "2024-03-14T15:45:00Z",
                    "asset_types": {
                        "Model": 20,
                        "Dataset": 7,
                        "Pipeline": 3
                    },
                    "risk_levels": {
                        "Low": 22,
                        "Medium": 6,
                        "High": 2
                    }
                },
                "carol@example.com": {
                    "asset_count": 18,
                    "last_used": "2024-03-13T09:15:00Z",
                    "asset_types": {
                        "Model": 10,
                        "Dataset": 5,
                        "Pipeline": 3
                    },
                    "risk_levels": {
                        "Low": 12,
                        "Medium": 4,
                        "High": 2
                    }
                }
            },
            "top_users": [
                {
                    "user_id": "bob@example.com",
                    "usage_count": 30,
                    "last_used": "2024-03-14T15:45:00Z"
                },
                {
                    "user_id": "alice@example.com",
                    "usage_count": 25,
                    "last_used": "2024-03-15T10:30:00Z"
                },
                {
                    "user_id": "carol@example.com",
                    "usage_count": 18,
                    "last_used": "2024-03-13T09:15:00Z"
                },
                {
                    "user_id": "dave@example.com",
                    "usage_count": 15,
                    "last_used": "2024-03-12T14:20:00Z"
                },
                {
                    "user_id": "eve@example.com",
                    "usage_count": 12,
                    "last_used": "2024-03-11T11:10:00Z"
                }
            ]
        }
        return stats

    async def get_model_usage_stats(self) -> Dict:
        """
        Get statistics about AI Asset usage by model.

        Returns:
            Dict: A dictionary containing the following statistics:
                - total_models (int): Total number of unique models
                - active_models (int): Number of models used in the last 30 days
                - usage_by_model (Dict[str, Dict]): Usage statistics per model
                - top_models (List[Dict]): List of top models by usage
                - model_distribution (Dict[str, int]): Distribution of models by type
        """
        # TODO: Implement the actual logic to get the statistics
        stats = {
            "total_models": 15,
            "active_models": 12,
            "usage_by_model": {
                "gpt-4": {
                    "usage_count": 45,
                    "last_used": "2024-03-15T10:30:00Z",
                    "user_count": 25,
                    "avg_risk_score": 6.8
                },
                "gpt-3.5-turbo": {
                    "usage_count": 38,
                    "last_used": "2024-03-14T15:45:00Z",
                    "user_count": 30,
                    "avg_risk_score": 5.2
                },
                "claude-3-opus": {
                    "usage_count": 25,
                    "last_used": "2024-03-13T09:15:00Z",
                    "user_count": 18,
                    "avg_risk_score": 7.1
                },
                "llama-2-70b": {
                    "usage_count": 20,
                    "last_used": "2024-03-12T14:20:00Z",
                    "user_count": 15,
                    "avg_risk_score": 4.9
                }
            },
            "top_models": [
                {
                    "model_name": "gpt-4",
                    "usage_count": 45,
                    "user_count": 25
                },
                {
                    "model_name": "gpt-3.5-turbo",
                    "usage_count": 38,
                    "user_count": 30
                },
                {
                    "model_name": "claude-3-opus",
                    "usage_count": 25,
                    "user_count": 18
                },
                {
                    "model_name": "llama-2-70b",
                    "usage_count": 20,
                    "user_count": 15
                },
                {
                    "model_name": "mistral-7b",
                    "usage_count": 15,
                    "user_count": 12
                }
            ],
            "model_distribution": {
                "LLM": 85,
                "Embedding": 45,
                "Classification": 30,
                "Generation": 25,
                "Other": 15
            }
        }
        return stats
