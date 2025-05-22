from typing import Dict

EVAL_RUN_INDEX = "eval_runs"
EVAL_PROMPT_INDEX = "eval_prompts"
EVAL_RESPONSE_INDEX = "eval_responses"

def get_eval_run_mapping() -> Dict:
    return {
        "mappings": {
            "properties": {
                "eval_id": {"type": "keyword"},
                "eval_run_id": {"type": "keyword"},
                "config_id": {"type": "keyword"},
                "tenant_id": {"type": "keyword"},
                "owner": {"type": "keyword"},
                "status": {"type": "keyword"},
                "purpose": {"type": "text"},
                "config_name": {"type": "keyword"},
                "report_name": {"type": "keyword"},
                "application_names": {"type": "keyword"},
                "target_users": {"type": "keyword"},
                "base_run_id": {"type": "keyword"},
                "create_time": {"type": "date"},
                "update_time": {"type": "date"},
                "passed": {"type": "keyword"},
                "failed": {"type": "keyword"},
                "cumulative_result": {"type": "object"},
                "total_prompts": {"type": "integer"},
                "total_passed": {"type": "integer"},
                "total_failed": {"type": "integer"},
                "execution_time": {"type": "float"}
            }
        }
    }

def get_eval_prompt_mapping() -> Dict:
    return {
        "mappings": {
            "properties": {
                "prompt_uuid": {"type": "keyword"},
                "eval_id": {"type": "keyword"},
                "eval_run_id": {"type": "keyword"},
                "tenant_id": {"type": "keyword"},
                "prompt": {"type": "text"},
                "create_time": {"type": "date"}
            }
        }
    }

def get_eval_response_mapping() -> Dict:
    return {
        "mappings": {
            "properties": {
                "eval_result_prompt_uuid": {"type": "keyword"},
                "eval_id": {"type": "keyword"},
                "eval_run_id": {"type": "keyword"},
                "tenant_id": {"type": "keyword"},
                "application_name": {"type": "keyword"},
                "response": {"type": "text"},
                "failure_reason": {"type": "text"},
                "category_score": {"type": "object"},
                "status": {"type": "keyword"},
                "category": {"type": "keyword"},
                "category_type": {"type": "keyword"},
                "category_severity": {"type": "keyword"},
                "create_time": {"type": "date"}
            }
        }
    } 