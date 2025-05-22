from typing import List
from sqlalchemy.exc import IntegrityError

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
