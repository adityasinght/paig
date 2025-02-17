import pytest
from httpx import AsyncClient
import json
from core.security.authentication import get_auth_user
from fastapi import FastAPI
from unittest.mock import AsyncMock, patch

evaluation_services_base_route = "eval-service/api"


class TestConfigRouters:
    def setup_method(self):
        self.auth_user_obj = {
            "id": 1,
            "username": "admin",
            "firstName": "admin",
            "lastName": "user",
            "roles": ["OWNER"],
            "groups": [],
            "status": 1
        }

    def auth_user(self):
        return self.auth_user_obj


    @pytest.mark.asyncio
    async def test_eval_routes(self, client: AsyncClient, app: FastAPI):
        app.dependency_overrides[get_auth_user] = self.auth_user
        post_data = {
            "url": "string",
            "body": {},
            "headers": {},
            "method": "string",
            "transformResponse": "string",
            "name": "target_name",
            "ai_application_id": 0
        }
        # Create application
        post_response = await client.post(f"/{evaluation_services_base_route}/target/application", json=post_data)
        assert post_response.status_code == 200

        post_data = {
            "purpose": "string",
            "name": "string",
            "categories": ["string"],
            "custom_prompts": ["string"],
            "application_ids": "string",
            "report_name": "string"
        }

        with patch("paig_evaluation.PAIGEvaluator") as MockEvaluator, \
                patch("paig_evaluation.get_suggested_plugins",
                      return_value={"status": "success", "result": ["plugin1", "plugin2"]}), \
                patch("paig_evaluation.get_all_plugins",
                      return_value={"status": "success", "result": ["plugin1", "plugin2", "plugin3"]}):
            # Mock PAIGEvaluator instance methods
            mock_evaluator_instance = MockEvaluator.return_value
            mock_evaluator_instance.generate_prompts.return_value = {
                "status": "success",
                "result": {"generated_prompts": ["mocked_prompt"]}
            }
            mock_evaluator_instance.evaluate.return_value = {
                "status": "success",
                "result": {
                    "results": {
                        "prompts": [
                            {"metrics": {"testPassCount": 5, "testFailCount": 2, "testErrorCount": 1}}
                        ]
                    }
                }
            }

            # save and run evaluation
            post_response = await client.post(f"/{evaluation_services_base_route}/eval/save_and_run", json=post_data)

            assert post_response.status_code == 200

            # get evaluation list
            get_response = await client.get(f"/{evaluation_services_base_route}/eval/report/list")

            assert get_response.status_code == 200
            assert "content" in get_response.json()
            assert isinstance(get_response.json()["content"], list)

            # rerun evaluation

            post_data = {
                "report_name": "string"
            }
            rerun_response = await client.post(f"/{evaluation_services_base_route}/eval/1/rerun", json=post_data)
            assert rerun_response.status_code == 200

            # delete report
            delete_response = await client.delete(f"/{evaluation_services_base_route}/eval/report/1")
            assert delete_response.status_code == 200


            # get categories
            post_data = {
                "purpose": "string"
            }
            get_categories_response = await client.post(f"/{evaluation_services_base_route}/eval/categories", json=post_data)
            assert get_categories_response.status_code == 200

