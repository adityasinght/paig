from sqlalchemy.exc import NoResultFound

from core.exceptions import NotFoundException
from core.exceptions.error_messages_parser import get_error_message, ERROR_RESOURCE_NOT_FOUND
from core.factory.database_initiator import BaseOperations
from api.governance.database.db_models.ai_asset_model import AIAsset


class AIAssetRepository(BaseOperations[AIAsset]):
    """
    Repository class for handling database operations related to AI Asset models.

    Inherits from BaseOperations[AIAsset], providing generic CRUD operations.

    This class inherits all methods from BaseOperations[AIAsset].
    """

    def __init__(self):
        """
        Initialize the AIAssetRepository.

        Args:
            db_session (Session): The database session to use for operations.
        """
        super().__init__(AIAsset)

    async def get_ai_asset_by_name(self, name: str) -> AIAsset:
        """
        Retrieve an AI Asset by its name.

        Args:
            name (str): The name of the AI Asset to retrieve.

        Returns:
            AIAsset: The AI Asset with the specified name.

        Raises:
            NotFoundException: If no AI Asset with the specified name is found.
        """
        try:
            return await self.get_by(filters={"name": name}, unique=True)
        except NoResultFound as e:
            raise NotFoundException(get_error_message(ERROR_RESOURCE_NOT_FOUND, "AI Asset", "name", name))

    async def get_ai_asset_by_uuid(self, uuid: str) -> AIAsset:
        """
        Retrieve an AI Asset by its UUID.

        Args:
            uuid (str): The UUID of the AI Asset to retrieve.

        Returns:
            AIAsset: The AI Asset with the specified UUID.

        Raises:
            NotFoundException: If no AI Asset with the specified UUID is found.
        """
        try:
            return await self.get_by(filters={"uuid": uuid}, unique=True)
        except NoResultFound as e:
            raise NotFoundException(get_error_message(ERROR_RESOURCE_NOT_FOUND, "AI Asset", "uuid", uuid))
