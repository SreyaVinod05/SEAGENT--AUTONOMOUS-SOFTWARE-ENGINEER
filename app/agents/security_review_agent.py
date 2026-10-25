import logging
from typing import List, Optional, Any
from app.agents.base import BaseAgent
from app.models.schemas import (
    RequirementAnalysisResult,
    ArchitectureResult,
    GeneratedFile,
    TestExecutionReport,
    SecurityReviewResult,
)

logger = logging.getLogger("seagent.agent.security")


class SecurityReviewAgent(BaseAgent):
    """
    Security Review Agent:
    Specialized Application Security Engineer that inspects the generated source code
    and architecture for OWASP Top 10 vulnerabilities, CWE compliance, hardcoded secrets,
    injection attacks, and weak input validations. Produces an objective security score
    and actionable remediation advice.
    """

    SYSTEM_INSTRUCTION = """You are a Principal Application Security Architect and Lead Penetration Tester in SEAGENT.
Your role is to conduct a rigorous automated security review of the generated codebase and system design.

Audit Criteria:
1. OWASP Top 10 & CWE standards:
   - Injection risks (SQL, Command, LDAP, NoSQL).
   - Broken authentication & session flaws.
   - Sensitive data exposure or hardcoded API keys/passwords.
   - Broken access controls or insecure direct object references (IDOR).
   - Security misconfigurations (permissive CORS, debug flags, missing headers).
   - Vulnerable dependencies or unsafe deserialization (e.g., pickle).
   - Server-Side Request Forgery (SSRF) and Path Traversal.
2. Code Hygiene:
   - Input validation and parameterized queries.
   - Safe error handling without leaking internal stack traces.
3. Scoring & Status:
   - Assign security_score from 1 to 100 (90-100: robust, 70-89: minor warnings, <70: needs remediation).
   - Set status to 'PASSED', 'WARNINGS_DETECTED', or 'NEEDS_REMEDIATION'.
4. Return structured output strictly conforming to the SecurityReviewResult schema.
"""

    def __init__(
        self,
        provider: Optional[Any] = None,
        use_mock: bool = False,
        provider_name: Optional[str] = None,
    ):
        super().__init__(provider=provider, use_mock=use_mock, provider_name=provider_name)

    def review(
        self,
        requirements: RequirementAnalysisResult,
        architecture: ArchitectureResult,
        files: List[GeneratedFile],
        test_report: Optional[TestExecutionReport] = None,
    ) -> SecurityReviewResult:
        files_preview = "\n\n".join(
            f"--- FILE: {f.path} ---\n{f.content[:2000]}" for f in files
        )

        prompt = f"""Conduct a thorough application security review of the following project:

Project Name: {requirements.project_name}
Architecture Style: {architecture.architecture_style}
Security Considerations Specified: {', '.join(architecture.security_considerations)}

Codebase to Audit:
{files_preview}

Audit the code for security vulnerabilities, assign a security score (1-100), identify any vulnerabilities with remediation steps, and check OWASP compliance.
"""
        return self.run_prompt(
            prompt=prompt,
            schema=SecurityReviewResult,
            system_instruction=self.SYSTEM_INSTRUCTION,
            temperature=0.1,
        )
