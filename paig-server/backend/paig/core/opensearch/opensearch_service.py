from typing import Any, Dict, List, Optional
from opensearchpy import OpenSearch
from core.config import get_settings

class OpenSearchService:
    def __init__(self):
        self.settings = get_settings()
        self.client = self._create_client()

    def _create_client(self) -> OpenSearch:
        """Create and return an OpenSearch client instance."""
        config = self.settings.get('opensearch', {})
        endpoint = config.get('endpoint', 'https://localhost:9200')
        client = OpenSearch(
            hosts=[endpoint],
            http_auth=(config.get('username', 'admin'), config.get('secret', 'admin')),
            use_ssl=config.get('use_ssl', True),
            verify_certs=config.get('verify_certs', False),
            ssl_show_warn=False
        )
        return client

    async def insert_document(self, index: str, document: Dict[str, Any], document_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Insert a document into OpenSearch.
        
        Args:
            index: The name of the index
            document: The document to insert
            document_id: Optional document ID. If not provided, OpenSearch will generate one.
            
        Returns:
            Dict containing the response from OpenSearch
        """
        response = self.client.index(
            index=index,
            body=document,
            id=document_id,
            refresh=True
        )
        return response

    async def get_document(self, index: str, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a document by its ID.
        
        Args:
            index: The name of the index
            document_id: The ID of the document to retrieve
            
        Returns:
            The document if found, None otherwise
        """
        try:
            response = self.client.get(
                index=index,
                id=document_id
            )
            return response['_source']
        except Exception:
            return None

    async def search_documents(self, index: str, query: Dict[str, Any], size: int = 10) -> List[Dict[str, Any]]:
        """
        Search for documents using a query.
        
        Args:
            index: The name of the index
            query: The search query
            size: Maximum number of results to return
            
        Returns:
            List of matching documents
        """
        response = self.client.search(
            index=index,
            body=query,
            size=size
        )
        return [hit['_source'] for hit in response['hits']['hits']]

    async def update_document(self, index: str, document_id: str, document: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a document by its ID.
        
        Args:
            index: The name of the index
            document_id: The ID of the document to update
            document: The new document data
            
        Returns:
            Dict containing the response from OpenSearch
        """
        response = self.client.update(
            index=index,
            id=document_id,
            body={'doc': document},
            refresh=True
        )
        return response

    async def delete_document(self, index: str, document_id: str) -> Dict[str, Any]:
        """
        Delete a document by its ID.
        
        Args:
            index: The name of the index
            document_id: The ID of the document to delete
            
        Returns:
            Dict containing the response from OpenSearch
        """
        response = self.client.delete(
            index=index,
            id=document_id,
            refresh=True
        )
        return response 