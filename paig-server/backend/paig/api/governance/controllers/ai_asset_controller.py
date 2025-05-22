from typing import List, Dict

from core.controllers.paginated_response import Pageable
from core.db_session import Transactional, Propagation
from api.governance.api_schemas.ai_asset import (
    AIAssetView,
    AIAssetFilter,
    CreateAIAssetView,
    UpdateAIAssetView
)
from api.governance.services.ai_asset_service import AIAssetService
from core.utils import SingletonDepends


class AIAssetController:
    """
    Controller class specifically for handling AI Asset entities.

    Args:
        ai_asset_service (AIAssetService): The service class for handling AI Asset entities.
    """

    def __init__(self,
                 ai_asset_service: AIAssetService = SingletonDepends(AIAssetService)):
        self.ai_asset_service = ai_asset_service

    async def list_ai_assets(self, asset_filter: AIAssetFilter, page_number: int, size: int,
                            sort: List[str]) -> Pageable:
        """
        List AI assets based on the provided filter, pagination, and sorting parameters.

        Args:
            asset_filter (AIAssetFilter): The filter object containing the search parameters.
            page_number (int): The page number to retrieve.
            size (int): The number of records to retrieve per page.
            sort (List[str]): The sorting parameters to apply.

        Returns:
            Pageable: The paginated response containing the list of AI assets.
        """
        return await self.ai_asset_service.list_ai_assets(
            filter=asset_filter,
            page_number=page_number,
            size=size,
            sort=sort
        )

    @Transactional(propagation=Propagation.REQUIRED)
    async def create_ai_asset(self, request: CreateAIAssetView) -> AIAssetView:
        """
        Create a new AI asset.

        Args:
            request (CreateAIAssetView): The view object representing the AI asset to create.

        Returns:
            AIAssetView: The created AI asset view object.
        """
        return await self.ai_asset_service.create_ai_asset(request)

    async def get_ai_asset_by_id(self, id: int) -> AIAssetView:
        """
        Retrieve an AI asset by its ID.

        Args:
            id (int): The ID of the AI asset to retrieve.

        Returns:
            AIAssetView: The AI asset view object corresponding to the ID.
        """
        return await self.ai_asset_service.get_ai_asset_by_id(id)

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_ai_asset(self, id: int, request: UpdateAIAssetView) -> AIAssetView:
        """
        Update an AI asset identified by its ID.

        Args:
            id (int): The ID of the AI asset to update.
            request (UpdateAIAssetView): The updated view object representing the AI asset.

        Returns:
            AIAssetView: The updated AI asset view object.
        """
        return await self.ai_asset_service.update_ai_asset(id, request)

    @Transactional(propagation=Propagation.REQUIRED)
    async def delete_ai_asset(self, id: int):
        """
        Delete an AI Asset by its ID.

        Args:
            id (int): The ID of the AI Asset to delete.
        """
        await self.ai_asset_service.delete_ai_asset(id)

    async def get_ai_asset_stats(self) -> Dict:
        """
        Get comprehensive statistics about AI Assets in the system.
        """
        return await self.ai_asset_service.get_ai_asset_stats()

    async def get_user_usage_stats(self) -> Dict:
        """
        Get statistics about AI Asset usage by users.
        """
        return await self.ai_asset_service.get_user_usage_stats()

    async def get_model_usage_stats(self) -> Dict:
        """
        Get statistics about AI Asset usage by model.
        """
        return await self.ai_asset_service.get_model_usage_stats()
