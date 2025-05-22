import json

from core.exceptions import BadRequestException
import logging
from ..database.db_operations.eval_repository import EvaluationRepository, EvaluationPromptRepository, EvaluationResponseRepository
from core.utils import SingletonDepends

logger = logging.getLogger(__name__)




class EvaluationResultService:

    def __init__(
        self,
        evaluation_repository: EvaluationRepository = SingletonDepends(EvaluationRepository),
        evaluation_prompt_repository: EvaluationPromptRepository = SingletonDepends(EvaluationPromptRepository),
        evaluation_response_repository: EvaluationResponseRepository = SingletonDepends(EvaluationResponseRepository)
    ):
        self.evaluation_repository = evaluation_repository
        self.evaluation_prompt_repository = evaluation_prompt_repository
        self.evaluation_response_repository = evaluation_response_repository

    async def get_eval_results_with_filters(self, *args):
        return await self.evaluation_repository.get_eval_results_with_filters(*args)

    async def get_evaluation(self, uuid):
        return await self.evaluation_repository.get_evaluations_by_field('eval_id', uuid)

    async def get_cumulative_results_by_uuid(self, uuid):
        model = await self.evaluation_repository.get_evaluations_by_field("eval_id", uuid)
        if model is None:
            raise BadRequestException(f"No results found for {uuid}")
        cumulative_result = model.cumulative_result
        if cumulative_result is None:
            raise BadRequestException(f"No results found for {uuid}")
        cumulative_result = json.loads(cumulative_result)
        resp_list = list()
        resp_dict = {}
        for result in cumulative_result:
            resp = dict()
            resp['application_name'] = result['provider']
            resp['passed'] = result['metrics']['testPassCount']
            resp['failed'] = result['metrics']['testFailCount']
            resp['error'] = result['metrics']['testErrorCount']
            resp['categories'] = result['metrics']['namedScores']
            resp['total_categories'] = result['metrics']['namedScoresCount']
            resp_list.append(resp)
        resp_dict['result'] = resp_list
        resp_dict['eval_id'] = model.eval_id
        resp_dict['report_name'] = model.name
        resp_dict['owner'] = model.owner
        resp_dict['create_time'] = model.create_time
        resp_dict["target_users"] = model.target_users
        return resp_dict

    async def get_detailed_results_by_uuid(self,
        *args
    ):
        return await self.evaluation_prompt_repository.get_detailed_results_by_uuid(*args)

    async def get_result_by_severity(self, uuid):
        rows = await self.evaluation_response_repository.get_result_by_severity(uuid)
        # Initialize all possible severity levels with 0
        severity_levels = {"HIGH": 0, "MEDIUM": 0, "LOW": 0, "CRITICAL": 0}
        result_dict = dict()
        # Update with actual values from the query result
        for severity, app_name, count in rows:
            severity_level = severity_levels
            if severity in severity_levels:
                severity_level[severity] = count
            result_dict[app_name] = severity_level
        return result_dict

    async def get_result_by_category(self, uuid):
        return await self.evaluation_response_repository.get_result_by_category(uuid)

    async def get_all_categories_from_result(self, uuid):
        return await self.evaluation_response_repository.get_all_categories_from_result(uuid)

    async def get_stats_matrix(self):
        """
        Get a matrix of evaluation statistics across different dimensions.

        Returns:
            Dict: A dictionary containing evaluation statistics including:
                - total_evaluations (int): Total number of evaluations performed
                - evaluations_by_status (Dict[str, int]): Count of evaluations by status
                - evaluations_by_severity (Dict[str, int]): Count of evaluations by severity level
                - evaluations_by_category (Dict[str, int]): Count of evaluations by category
                - evaluations_by_application (Dict[str, Dict]): Statistics per application
                - recent_evaluations (List[Dict]): List of recent evaluations
                - pass_fail_stats (Dict[str, float]): Overall pass/fail statistics
        """
        # TODO: Implement the actual logic to get the statistics
        stats = {
            "total_evaluations": 150,
            "evaluations_by_status": {
                "completed": 120,
                "in_progress": 20,
                "failed": 10
            },
            "evaluations_by_severity": {
                "CRITICAL": 15,
                "HIGH": 35,
                "MEDIUM": 45,
                "LOW": 55
            },
            "evaluations_by_category": {
                "Hallucination": 40,
                "Toxicity": 30,
                "Bias": 25,
                "Factual Accuracy": 35,
                "Privacy": 20
            },
            "evaluations_by_application": {
                "chatbot-app": {
                    "total_tests": 45,
                    "passed": 35,
                    "failed": 8,
                    "error": 2,
                    "avg_severity": "MEDIUM",
                    "categories": {
                        "Hallucination": 12,
                        "Toxicity": 8,
                        "Bias": 15,
                        "Factual Accuracy": 10
                    }
                },
                "qa-system": {
                    "total_tests": 38,
                    "passed": 30,
                    "failed": 6,
                    "error": 2,
                    "avg_severity": "LOW",
                    "categories": {
                        "Hallucination": 10,
                        "Toxicity": 5,
                        "Bias": 12,
                        "Factual Accuracy": 11
                    }
                },
                "content-generator": {
                    "total_tests": 42,
                    "passed": 32,
                    "failed": 7,
                    "error": 3,
                    "avg_severity": "HIGH",
                    "categories": {
                        "Hallucination": 15,
                        "Toxicity": 12,
                        "Bias": 8,
                        "Privacy": 7
                    }
                }
            },
            "recent_evaluations": [
                {
                    "eval_id": "eval-2024-03-15-001",
                    "application": "chatbot-app",
                    "timestamp": "2024-03-15T10:30:00Z",
                    "status": "completed",
                    "severity": "MEDIUM",
                    "pass_rate": 0.78
                },
                {
                    "eval_id": "eval-2024-03-14-002",
                    "application": "qa-system",
                    "timestamp": "2024-03-14T15:45:00Z",
                    "status": "completed",
                    "severity": "LOW",
                    "pass_rate": 0.85
                },
                {
                    "eval_id": "eval-2024-03-14-001",
                    "application": "content-generator",
                    "timestamp": "2024-03-14T09:15:00Z",
                    "status": "completed",
                    "severity": "HIGH",
                    "pass_rate": 0.65
                }
            ],
            "pass_fail_stats": {
                "overall_pass_rate": 0.76,
                "pass_rate_by_category": {
                    "Hallucination": 0.70,
                    "Toxicity": 0.85,
                    "Bias": 0.75,
                    "Factual Accuracy": 0.80,
                    "Privacy": 0.90
                },
                "pass_rate_by_severity": {
                    "CRITICAL": 0.60,
                    "HIGH": 0.65,
                    "MEDIUM": 0.75,
                    "LOW": 0.85
                }
            }
        }
        return stats