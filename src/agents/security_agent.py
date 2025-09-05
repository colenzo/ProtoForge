import random
from pydantic import BaseModel
from typing import List, Optional

class SecurityFinding(BaseModel):
    severity: str  # e.g., "critical", "high", "medium", "low"
    description: str
    location: str = None

class SecurityReport(BaseModel):
    status: str  # e.g., "passed", "failed", "warnings"
    overall_message: str
    findings: List[SecurityFinding]

async def run_security_scan(code: str) -> SecurityReport:
    """Placeholder for AI-driven security scanning logic (Aegis Protocol)."""
    print(f"Running security scan on generated code (first 100 chars): {code[:100]}...")
    
    # Simulate different outcomes
    outcome = random.choices(['passed', 'warnings', 'failed'], weights=[0.6, 0.3, 0.1], k=1)[0]
    
    findings = []
    overall_status = "passed"
    overall_message = "Security scan completed (placeholder)."

    if outcome == 'passed':
        findings.append(SecurityFinding(severity="low", description="No critical vulnerabilities found. Minor style issues detected.", location="N/A"))
    elif outcome == 'warnings':
        overall_status = "warnings"
        overall_message = "Security scan completed with warnings. Review recommended."
        findings.append(SecurityFinding(severity="medium", description="Potential insecure dependency detected.", location="requirements.txt"))
        findings.append(SecurityFinding(severity="low", description="Hardcoded sensitive information (e.g., API key placeholder).", location="main.py:15"))
    elif outcome == 'failed':
        overall_status = "failed"
        overall_message = "Security scan failed. Critical vulnerabilities found."
        findings.append(SecurityFinding(severity="critical", description="SQL Injection vulnerability detected in user input handling.", location="api/genesis.py:20"))
        findings.append(SecurityFinding(severity="high", description="Cross-Site Scripting (XSS) vulnerability in output rendering.", location="frontend/index.html:30"))

    return SecurityReport(
        status=overall_status,
        overall_message=overall_message,
        findings=findings
    )
