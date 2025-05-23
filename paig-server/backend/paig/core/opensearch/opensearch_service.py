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

    async def get_field_counts(
        self,
        index: str,
        fields: List[str],
        from_time: Optional[str] = None,
        to_time: Optional[str] = None,
        time_field: str = "@timestamp"
    ) -> Dict[str, Any]:
        """
        Get counts for specified fields with optional time range filtering.
        
        Args:
            index: The name of the index
            fields: List of fields to get counts for (use dot notation for nested fields)
            from_time: Optional start time in ISO format
            to_time: Optional end time in ISO format
            time_field: Field name containing the timestamp (default: @timestamp)
            
        Returns:
            Dict containing counts for each field
        """
        # Build the query
        query = {
            "size": 0,  # We only want aggregations, not actual documents
            "query": {
                "bool": {
                    "must": []
                }
            },
            "aggs": {}
        }

        # Add time range if provided
        if from_time or to_time:
            range_filter = {"range": {time_field: {}}}
            if from_time:
                range_filter["range"][time_field]["gte"] = from_time
            if to_time:
                range_filter["range"][time_field]["lte"] = to_time
            query["query"]["bool"]["must"].append(range_filter)

        # Add aggregations for each field
        for field in fields:
            # Handle nested fields in labels
            if field.startswith('labels.'):
                nested_field = field.replace('labels.', '')
                agg_name = f"{nested_field}_count"
                query["aggs"][agg_name] = {
                    "terms": {
                        "field": f"labels.{nested_field}.keyword",  # Added .keyword for text fields
                        "size": 100  # Get top 100 values for each field
                    }
                }
            else:
                query["aggs"][f"{field}_count"] = {
                    "terms": {
                        "field": f"{field}.keyword" if field not in ["value", "@timestamp"] else field,  # Handle non-text fields
                        "size": 100
                    }
                }

        # If no time filters, use match_all
        if not query["query"]["bool"]["must"]:
            query["query"] = {"match_all": {}}

        try:
            print(f"Executing query: {query}")  # Debug log
            response = self.client.search(
                index=index,
                body=query
            )

            # Process the aggregation results
            result = {}
            for field in fields:
                # Get the appropriate aggregation key
                if field.startswith('labels.'):
                    field_name = field.split('.')[-1]
                    agg_key = f"{field_name}_count"
                else:
                    agg_key = f"{field}_count"

                if agg_key in response.get("aggregations", {}):
                    buckets = response["aggregations"][agg_key]["buckets"]
                    result[field] = {
                        "total": sum(bucket["doc_count"] for bucket in buckets),
                        "breakdown": {
                            bucket["key"]: bucket["doc_count"]
                            for bucket in buckets
                        }
                    }
                else:
                    result[field] = {"total": 0, "breakdown": {}}

            return result
        except Exception as e:
            print(f"Error executing search: {str(e)}")
            return {"error": str(e)}

    async def create_index_if_not_exists(self, index: str, mapping: Dict = None) -> None:
        """Create an index if it doesn't exist with optional mapping."""
        try:
            if not self.client.indices.exists(index=index):
                self.client.indices.create(
                    index=index,
                    body=mapping if mapping else {}
                )
        except Exception as e:
            print(f"Error creating index: {str(e)}")

    async def update_index_mapping(self, index: str, mapping: Dict) -> None:
        """Update the mapping of an existing index."""
        try:
            self.client.indices.put_mapping(
                index=index,
                body=mapping
            )
        except Exception as e:
            print(f"Error updating mapping: {str(e)}")

    def get_ai_usage_mapping(self) -> Dict:
        """Get the mapping for AI usage metrics index."""
        return {
            "mappings": {
                "properties": {
                    "@timestamp": {"type": "date"},
                    "metric_name": {"type": "keyword"},
                    "value": {"type": "float"},  # Changed from long to float
                    "labels": {
                        "properties": {
                            "function_name": {"type": "keyword"},
                            "model_name": {"type": "keyword"},
                            "warehouse_id": {"type": "long"}
                        }
                    }
                }
            }
        }

    async def ensure_ai_usage_index(self) -> None:
        """Ensure the AI usage metrics index exists with correct mapping."""
        index = self.settings.get('opensearch', {}).get('ai_usage_index', 'ai_usage_metrics')
        mapping = self.get_ai_usage_mapping()
        
        # Create index if it doesn't exist
        if not self.client.indices.exists(index=index):
            await self.create_index_if_not_exists(index, mapping)
        else:
            # Update mapping for existing index
            try:
                await self.update_index_mapping(index, mapping["mappings"])
            except Exception as e:
                print(f"Error updating mapping: {str(e)}")

    async def get_index_mapping(self, index: str) -> Dict:
        """Get the current mapping of an index."""
        try:
            return self.client.indices.get_mapping(index=index)
        except Exception as e:
            print(f"Error getting mapping: {str(e)}")
            return {}

    async def get_all_documents(self, index: str, size: int = 100) -> List[Dict]:
        """Get all documents from an index."""
        try:
            response = self.client.search(
                index=index,
                body={
                    "query": {"match_all": {}},
                    "size": size
                }
            )
            return [hit["_source"] for hit in response["hits"]["hits"]]
        except Exception as e:
            print(f"Error getting documents: {str(e)}")
            return []