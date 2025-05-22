from typing import Dict, List, Optional
from core.opensearch.opensearch_service import OpenSearchService
from core.opensearch.eval_indices import (
    EVAL_RUN_INDEX,
    EVAL_PROMPT_INDEX,
    EVAL_RESPONSE_INDEX,
    get_eval_run_mapping,
    get_eval_prompt_mapping,
    get_eval_response_mapping
)

class EvalOpenSearchService:
    def __init__(self, opensearch_service: OpenSearchService):
        self.opensearch = opensearch_service

    async def init_indices(self):
        """Initialize all evaluation-related indices if they don't exist."""
        # Create indices with their mappings
        await self.opensearch.create_index_if_not_exists(EVAL_RUN_INDEX, get_eval_run_mapping())
        await self.opensearch.create_index_if_not_exists(EVAL_PROMPT_INDEX, get_eval_prompt_mapping())
        await self.opensearch.create_index_if_not_exists(EVAL_RESPONSE_INDEX, get_eval_response_mapping())

    async def insert_eval_run(self, eval_run: Dict) -> Dict:
        """Insert evaluation run details."""
        return await self.opensearch.insert_document(EVAL_RUN_INDEX, eval_run, eval_run.get('eval_id'))

    async def insert_eval_prompt(self, prompt: Dict) -> Dict:
        """Insert evaluation prompt."""
        return await self.opensearch.insert_document(EVAL_PROMPT_INDEX, prompt, prompt.get('prompt_uuid'))

    async def insert_eval_response(self, response: Dict) -> Dict:
        """Insert evaluation response."""
        return await self.opensearch.insert_document(EVAL_RESPONSE_INDEX, response)

    async def bulk_insert_eval_prompts(self, prompts: List[Dict]) -> None:
        """Bulk insert evaluation prompts."""
        for prompt in prompts:
            await self.insert_eval_prompt(prompt)

    async def bulk_insert_eval_responses(self, responses: List[Dict]) -> None:
        """Bulk insert evaluation responses."""
        for response in responses:
            await self.insert_eval_response(response)

    async def get_eval_run(self, eval_id: str) -> Optional[Dict]:
        """Get evaluation run by ID."""
        return await self.opensearch.get_document(EVAL_RUN_INDEX, eval_id)

    async def search_eval_runs(self, query: Dict, size: int = 10) -> List[Dict]:
        """Search evaluation runs."""
        return await self.opensearch.search_documents(EVAL_RUN_INDEX, query, size)

    async def search_eval_responses(self, query: Dict, size: int = 10) -> List[Dict]:
        """Search evaluation responses."""
        return await self.opensearch.search_documents(EVAL_RESPONSE_INDEX, query, size)

    async def update_eval_run(self, eval_id: str, update_data: Dict) -> Dict:
        """Update evaluation run."""
        return await self.opensearch.update_document(EVAL_RUN_INDEX, eval_id, update_data) 