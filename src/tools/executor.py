"""API execution tool"""
from typing import List
from ..models import SessionContext, ExecutionRequest, ExecutionResponse
from ..services import SessionService, ExecutionService


async def execute_apis_tool(
    session_ctx: SessionContext,
    session_service: SessionService,
    execution_service: ExecutionService,
    executions: List[ExecutionRequest]
) -> ExecutionResponse:
    """
    Execute multiple API calls

    Args:
        session_ctx: Session context
        session_service: Session service instance
        execution_service: Execution service instance
        executions: List of API execution requests

    Returns:
        Execution results for all APIs
    """
    session_service.validate_session(session_ctx)

    results = await execution_service.execute_apis(session_ctx, executions)

    return ExecutionResponse(results=results)
