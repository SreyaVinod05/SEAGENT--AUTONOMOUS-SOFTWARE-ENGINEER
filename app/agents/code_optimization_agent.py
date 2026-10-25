import logging
from typing import List, Optional, Any
from app.agents.base import BaseAgent
from app.models.schemas import (
    RequirementAnalysisResult,
    ArchitectureResult,
    GeneratedFile,
    CodeOptimizationResult,
)

logger = logging.getLogger("seagent.agent.optimization")


class CodeOptimizationAgent(BaseAgent):
    """
    Code Optimization Agent:
    Specialized Performance and Algorithmic Optimization Engineer.
    Refines the codebase to improve execution speed, reduce time/space complexity,
    eliminate redundant logic, and elevate maintainability without altering intended functionality.
    """

    SYSTEM_INSTRUCTION = """You are a Principal Performance Engineer and Code Optimization Specialist in SEAGENT.
Your role is to analyze the generated source code and refactor it for maximum runtime efficiency,
clean architecture, and minimal Big-O complexity.

Optimization Objectives:
1. Algorithmic Complexity:
   - Identify nested loops, suboptimal lookups (O(N) in lists -> O(1) in dicts/sets).
   - Optimize sorting, searching, and traversal operations.
2. Memory & Resource Efficiency:
   - Replace redundant collections with generators/iterators where appropriate.
   - Prevent unnecessary object allocations and caching bottlenecks.
3. Code Quality & Modularity:
   - Eliminate dead code, deduplicate logic (DRY principle).
   - Enhance function readability and docstring clarity.
4. Non-breaking Guarantee:
   - You MUST preserve all function signatures, REST API endpoints, and business behaviors so all tests remain valid.
5. Return structured output strictly conforming to the CodeOptimizationResult schema, including optimized_files with complete improved code.
"""

    def __init__(
        self,
        provider: Optional[Any] = None,
        use_mock: bool = False,
        provider_name: Optional[str] = None,
    ):
        super().__init__(provider=provider, use_mock=use_mock, provider_name=provider_name)

    def optimize(
        self,
        requirements: RequirementAnalysisResult,
        architecture: ArchitectureResult,
        files: List[GeneratedFile],
    ) -> CodeOptimizationResult:
        files_dump = "\n\n".join(
            f"=== FILE: {f.path} ===\n{f.content}" for f in files
        )

        prompt = f"""Review the following software codebase and optimize it for computational efficiency, Big-O complexity, and maintainability:

Project: {requirements.project_name}
Architecture: {architecture.architecture_style}

Current Codebase:
{files_dump}

Analyze algorithmic complexity (Big-O before and after), apply performance refactoring, and return the optimized files with non-breaking improvements.
"""
        return self.run_prompt(
            prompt=prompt,
            schema=CodeOptimizationResult,
            system_instruction=self.SYSTEM_INSTRUCTION,
            temperature=0.2,
        )
