"""API execution tool"""
from typing import List
from ..models import ExecutionRequest, ExecutionResponse
from ..services import ExecutionService


async def execute_apis_tool(
    app_id: str,
    execution_service: ExecutionService,
    executions: List[ExecutionRequest]
) -> ExecutionResponse:
    """
    Execute multiple API calls

    Args:
        app_id: Application identifier
        execution_service: Execution service instance
        executions: List of API execution requests

    Returns:
        Execution results for all APIs
    """
    results = await execution_service.execute_apis(app_id, executions)

    return ExecutionResponse(results=results)
