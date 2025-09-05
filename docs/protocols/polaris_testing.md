# Testing Protocol: Project Genesis

## Core Principles
- **Test-Driven Development (TDD):** New features should ideally be developed using a TDD approach (write tests first, then code).
- **Comprehensive Coverage:** Strive for high test coverage across all layers (unit, integration, end-to-end).
- **Automated Testing:** Prioritize automated tests over manual testing wherever possible.
- **Performance Testing:** Critical paths and new features must include performance benchmarks and tests.
- **Security Testing:** Integrate automated security testing (SAST/DAST) into the CI/CD pipeline.

## Test Types & Requirements
- **Unit Tests:**
  - Granular, fast-executing tests for individual functions/components.
  - Required for all new code.
  - Minimum 80% code coverage.
- **Integration Tests:**
  - Verify interactions between different modules or services.
  - Required for all API endpoints and service integrations.
- **End-to-End (E2E) Tests:**
  - Simulate real user scenarios across the entire application.
  - Focus on critical user journeys.
- **Performance Tests:**
  - Load testing, stress testing, and scalability testing for critical services.
  - Benchmarks defined in PRD.
- **Security Tests:**
  - Static Application Security Testing (SAST) on code commits.
  - Dynamic Application Security Testing (DAST) on deployed environments.

## Test Environment
- Dedicated test environments that mirror production as closely as possible.
- Data anonymization/masking for sensitive data in non-production environments.

## CI/CD Integration
- All tests must run automatically as part of the CI/CD pipeline.
- PRs cannot be merged if tests fail or coverage requirements are not met.

## Bug Reporting
- All bugs found during testing must be reported using the `incident_report.md` template.
- Root cause analysis required for all critical bugs.
