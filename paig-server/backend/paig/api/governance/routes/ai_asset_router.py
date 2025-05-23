from typing import List, Dict, Optional
from fastapi import APIRouter, Depends, status, Query
from core.controllers.paginated_response import Pageable
from api.governance.api_schemas.ai_asset import (
    AIAssetView,
    AIAssetFilter,
    CreateAIAssetView,
    UpdateAIAssetView
)
from api.governance.controllers.ai_asset_controller import AIAssetController
from core.utils import SingletonDepends
from core.utils import alias_field_to_column_name
from core.exceptions.base import BadRequestException

ai_asset_router = APIRouter()
stats_router = APIRouter()

ai_asset_controller_instance = Depends(SingletonDepends(AIAssetController, called_inside_fastapi_depends=True))


@ai_asset_router.get("", response_model=Pageable)
async def list_ai_assets(
        asset_filter: AIAssetFilter = Depends(),
        page: int = Query(0, description="The page number to retrieve"),
        size: int = Query(10, description="The number of items per page"),
        sort: List[str] = Query([], description="The sort options"),
        ai_asset_controller: AIAssetController = ai_asset_controller_instance
) -> Pageable:
    """
    List all AI assets with optional filtering and pagination.
    
    Args:
        asset_filter: Filter criteria for AI assets
        page: Page number for pagination
        size: Number of items per page
        sort: List of fields to sort by
        ai_asset_controller: Controller instance for AI asset operations
    
    Returns:
        Pageable response containing the list of AI assets
    """
    sort = alias_field_to_column_name(sort, AIAssetView)
    return await ai_asset_controller.list_ai_assets(asset_filter, page, size, sort)


@ai_asset_router.post("", response_model=AIAssetView, status_code=status.HTTP_201_CREATED)
async def create_ai_asset(
        create_asset_request: CreateAIAssetView,
        ai_asset_controller: AIAssetController = ai_asset_controller_instance
) -> AIAssetView:
    """
    Create a new AI asset.
    
    Args:
        create_asset_request: Data for creating the new AI asset
        ai_asset_controller: Controller instance for AI asset operations
    
    Returns:
        The created AI asset
    """
    return await ai_asset_controller.create_ai_asset(create_asset_request)


@ai_asset_router.get("/{id}", response_model=AIAssetView)
async def get_ai_asset(
        id: int,
        ai_asset_controller: AIAssetController = ai_asset_controller_instance
) -> AIAssetView:
    """
    Get an AI asset by ID.
    
    Args:
        id: The ID of the AI asset to retrieve
        ai_asset_controller: Controller instance for AI asset operations
    
    Returns:
        The requested AI asset
    """
    return await ai_asset_controller.get_ai_asset_by_id(id)


@ai_asset_router.put("/{id}", response_model=AIAssetView)
async def update_ai_asset(
        id: int,
        update_asset_request: UpdateAIAssetView,
        ai_asset_controller: AIAssetController = ai_asset_controller_instance
) -> AIAssetView:
    """
    Update an existing AI asset.
    
    Args:
        id: The ID of the AI asset to update
        update_asset_request: Updated data for the AI asset
        ai_asset_controller: Controller instance for AI asset operations
    
    Returns:
        The updated AI asset
    """
    return await ai_asset_controller.update_ai_asset(id, update_asset_request)


@ai_asset_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ai_asset(
        id: int,
        ai_asset_controller: AIAssetController = ai_asset_controller_instance
) -> None:
    """
    Delete an AI asset by ID.
    
    Args:
        id: The ID of the AI asset to delete
        ai_asset_controller: Controller instance for AI asset operations
    """
    await ai_asset_controller.delete_ai_asset(id)

@ai_asset_router.get("/stats/assets_usage", response_model=Dict, status_code=status.HTTP_200_OK)
async def get_ai_asset_stats(
        ai_asset_controller: AIAssetController = ai_asset_controller_instance
) -> Dict:
    """
    Get comprehensive statistics about AI Assets in the system.
    This endpoint provides various metrics and counts about AI Assets.
    """
    return await ai_asset_controller.get_ai_asset_stats()



@stats_router.get("/user_usage", response_model=Dict)
async def get_user_usage_stats(
    controller: AIAssetController = ai_asset_controller_instance
) -> Dict:
    """
    Get statistics about AI Asset usage by users.
    """
    return await controller.get_user_usage_stats()

@stats_router.get("/model_usage", response_model=Dict)
async def get_model_usage_stats(
    controller: AIAssetController = ai_asset_controller_instance
) -> Dict:
    """
    Get statistics about AI Asset usage by model.
    """
    return await controller.get_model_usage_stats()


@stats_router.get("/count", response_model=Dict)
async def get_counts(
    fields: str,
    from_time: Optional[str] = None,
    to_time: Optional[str] = None,
    index: Optional[str] = None,
    controller: AIAssetController = ai_asset_controller_instance
) -> Dict:
    """
    Get field counts from OpenSearch with optional time range filtering.

    Args:
        fields (str): Comma-separated list of fields to get counts for
        from_time (str, optional): Start time in ISO format (e.g., 2024-03-15T00:00:00Z)
        to_time (str, optional): End time in ISO format (e.g., 2024-03-15T23:59:59Z)
        index (str, optional): OpenSearch index to query (defaults to eval_runs)

    Returns:
        Dict: Counts for each requested field with breakdowns
    """
    # Split the comma-separated fields
    field_list = [field.strip() for field in fields.split(',') if field.strip()]
    
    if not field_list:
        raise BadRequestException("At least one field must be specified")
        
    return await controller.get_count(
        fields=field_list,
        from_time=from_time,
        to_time=to_time,
        index=index
    )