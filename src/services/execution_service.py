"""API execution service"""
import asyncio
from typing import List
from ..models import ExecutionRequest, ExecutionResult, SessionContext
from ..data_access import DataProvider


class ExecutionService:
    """Service for executing APIs"""

    def __init__(self, data_provider: DataProvider):
        """
        Initialize execution service

        Args:
            data_provider: Data provider instance
        """
        self._data_provider = data_provider

    async def execute_apis(
        self, context: SessionContext, executions: List[ExecutionRequest]
    ) -> List[ExecutionResult]:
        """
        Execute multiple APIs concurrently

        Args:
            context: Session context
            executions: List of execution requests

        Returns:
            List of execution results
        """
        # Execute all APIs concurrently
        tasks = [
            self._execute_single(context, execution)
            for execution in executions
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Convert exceptions to error results
        final_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                final_results.append(ExecutionResult(
                    api_name=executions[i].api_name,
                    success=False,
                    error=str(result)
                ))
            else:
                final_results.append(result)

        return final_results

    async def _execute_single(
        self, context: SessionContext, execution: ExecutionRequest
    ) -> ExecutionResult:
        """
        Execute a single API

        Args:
            context: Session context
            execution: Execution request

        Returns:
            Execution result
        """
        try:
            return await self._data_provider.execute_api(context.app_id, execution)
        except Exception as e:
            return ExecutionResult(
                api_name=execution.api_name,
                success=False,
                error=str(e)
            )
