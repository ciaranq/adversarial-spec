# Adversarial Spec Process Summary

## Technical SEO Dashboard - Earned Media

**Date:** January 20, 2026
**Process:** Adversarial Spec Development
**Facilitator:** Claude (Opus 4.5)
**Opponent Models:** gemini/gemini-2.0-flash

---

## Overview

This document summarizes the adversarial specification development process used to create the Product Requirements Document (PRD) and Technical Specification for the Earned Media Technical SEO Dashboard project.

The adversarial spec process involves multiple AI models critiquing and refining a specification document until all participants reach consensus, ensuring comprehensive coverage and identifying gaps that a single reviewer might miss.

---

## Documents Created

| Document | Version | File |
|----------|---------|------|
| Product Requirements Document | v1.5 (FINAL) | `technical-seo-dashboard-prd-v1.4-FINAL.md` |
| Technical Specification | v1.2 (FINAL) | `technical-seo-dashboard-tech-spec-v1.2-FINAL.md` |

---

## PRD Development Process

### Starting Point
- Initial PRD (v1.0) created by Claude based on user requirements
- Company: Originally "IntelliAgent", corrected to "Earned Media"
- Reference: SEO It Is (seoitis.com) for UI inspiration

### Debate Rounds

| Round | Model | Result | Key Changes |
|-------|-------|--------|-------------|
| 1 | gemini/gemini-2.0-flash | Critiqued | Added quantified problem statement, improved personas, moved audit triggering from clients to Account Managers |
| 2 | gemini/gemini-2.0-flash | Critiqued | Defined "actively using" metric, flagged score weights as assumptions, added contact info to error messages |
| 3 | gemini/gemini-2.0-flash | Critiqued | Added open-ended survey question, refined success metrics |
| 4 | gemini/gemini-2.0-flash | **AGREED** | Consensus reached |

### Key PRD Refinements

1. **Company Branding**
   - Changed from IntelliAgent to Earned Media
   - Added brand colors from earnedmedia.com.au (#EA401D, #031C38, #009BD8, etc.)
   - Added correct logo reference

2. **Problem Statement**
   - Added quantified impact: 100-150 hours/month of manual work
   - Added opportunity cost analysis

3. **User Stories**
   - Moved "Trigger Audit" capability from clients to Account Managers only
   - Added specific acceptance criteria with checkboxes

4. **Personas**
   - Made generic personas specific (Sarah Chen, Tom Nguyen, Emily Torres)
   - Added company context ("Style Australia")
   - Added specific tools they use

5. **Score Calculation**
   - Added explicit formula with weights (CWV 35%, Schema 25%, SSL 25%, Title Tags 15%)
   - Flagged as assumptions to validate post-launch
   - Added penalty system for Critical issues

6. **Error Handling**
   - Added specific error messages with contact information
   - Added degraded mode for partial API failures
   - Added data retention policy (keep 3 audits)

7. **Success Metrics**
   - Defined "actively using" as 2+ views OR 1+ download
   - Added specific survey questions
   - Added measurement methodology

---

## Technical Specification Process

### Debate Rounds

| Round | Model | Result | Key Changes |
|-------|-------|--------|-------------|
| 1 | gemini/gemini-2.0-flash | Critiqued | Added tool-specific detail interfaces, improved error handling, added API key rotation procedure |
| 2 | gemini/gemini-2.0-flash | Critiqued | Added E2E test scenarios, Railway volume sizing, CLI cleanup implementation, concurrent audit notes |
| 3 | gemini/gemini-2.0-flash | **AGREED** | Consensus reached |

### Key Tech Spec Refinements

1. **Architecture**
   - Split architecture: Vercel (Next.js) + Railway (Python/FastAPI)
   - File-based JSON storage with 10GB SSD volume
   - API key authentication between services

2. **Data Models**
   - Added specific detail interfaces for each tool (SchemaDetails, CWVDetails, SSLDetails, TitleTagDetails)
   - Changed errors from single string to array per tool
   - Aligned TypeScript and Python models

3. **Security**
   - Added monthly API key rotation procedure
   - Added emergency rotation for compromised keys
   - Added SSRF protection, path traversal protection, rate limiting
   - Added CORS configuration

4. **Error Handling**
   - Added retry logic with exponential backoff (3 attempts)
   - Added graceful degradation when Python server unavailable
   - Added structured JSON logging format

5. **Infrastructure**
   - Specified Railway volume size (10GB SSD)
   - Added cost estimates (~$30/month total)
   - Added CI/CD pipeline details

6. **Testing**
   - Added comprehensive E2E test scenarios
   - Added security test checklist
   - Added coverage targets (90%+)

---

## Final Outputs

### PRD Contents (17 Sections)
1. Executive Summary
2. Problem Statement
3. Goals & Objectives
4. Target Users / Personas
5. User Stories / Use Cases
6. Functional Requirements
7. Non-Functional Requirements
8. Success Metrics / KPIs
9. Scope
10. Dependencies
11. Risks and Mitigations
12. Open Questions
13. Appendix
14. Technical Architecture Summary
15. Implementation Roadmap (6 Phases)
16. Handoff Checklist
17. Post-MVP Roadmap

### Tech Spec Contents (15 Sections)
1. Overview
2. Goals and Non-Goals
3. API Design
4. Data Models
5. Component Design
6. Security
7. Error Handling
8. Performance
9. Observability
10. Testing Strategy
11. CI/CD Pipeline
12. Infrastructure
13. File Cleanup / Retention
14. Scalability Considerations
15. Open Questions

---

## Process Statistics

| Metric | PRD | Tech Spec | Total |
|--------|-----|-----------|-------|
| Debate Rounds | 4 | 3 | 7 |
| Model Used | gemini/gemini-2.0-flash | gemini/gemini-2.0-flash | - |
| Initial Version | 1.0 | 1.0 | - |
| Final Version | 1.5 | 1.2 | - |
| Consensus | Round 4 | Round 3 | - |

---

## Claude's Contributions

As an active participant in the debate (not just orchestrator), Claude contributed:

### PRD Contributions
- Identified that audit triggering should be Account Manager only
- Added quantified problem statement
- Created specific personas with concrete examples
- Designed score calculation formula
- Added data retention policy
- Added degraded mode requirements

### Tech Spec Contributions
- Designed Vercel + Railway split architecture
- Created retry logic with exponential backoff
- Defined tool-specific detail interfaces
- Added API key rotation procedures
- Created CLI for manual file cleanup
- Documented post-MVP scalability path

---

## Files in Repository

```
/techseo_dashboard/
├── technical-seo-dashboard-prd.md                    # Original PRD (v1.0)
├── technical-seo-dashboard-prd-v1.4-FINAL.md         # Final PRD with implementation guide
├── technical-seo-dashboard-tech-spec-v1.2-FINAL.md   # Final Technical Specification
├── EM_Logo.png                                       # Earned Media logo
└── ADVERSARIAL-SPEC-SUMMARY.md                       # This summary document
```

---

## Lessons Learned

1. **Multi-round critique catches gaps** - Round 1 identified major issues (client triggering audits) that would have caused problems in development

2. **Specific > Generic** - Generic personas and metrics were repeatedly challenged until made concrete

3. **Assumptions should be flagged** - Score weights were arbitrary until flagged as "assumptions to validate post-launch"

4. **Error handling needs detail** - Initial "error messages appear" was too vague; needed specific messages with contact info

5. **Security needs procedures** - API key rotation needed not just mention but step-by-step procedure including emergency scenarios

---

## Next Steps for Project Team

1. Review PRD and Tech Spec documents
2. Resolve open questions (landing page, card expansion, title tag script)
3. Gather pre-development requirements (logo, API keys, accounts)
4. Begin Phase 1: Project Setup & Foundation

---

**Process completed:** January 20, 2026
**Ready for development handoff**
