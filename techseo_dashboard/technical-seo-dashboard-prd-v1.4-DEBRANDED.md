# Product Requirements Document (PRD)
## Technical SEO Dashboard

**Version:** 1.4 (De-branded)
**Date:** January 20, 2026
**Author:** Claude (Adversarial Spec Process)
**Adversarial Review:** 4 rounds with gemini/gemini-2.0-flash

---

## 1. Executive Summary

[Agency Name], an SEO agency, is losing valuable time and resources to manual SEO report creation. Account Managers spend an estimated **2-3 hours per client per month** compiling, formatting, and explaining reports, costing the agency approximately **100-150 hours/month**. This prevents them from focusing on high-value strategic consulting, impacting revenue and client satisfaction.

This client-facing Technical SEO Dashboard will automate report delivery, slashing report creation time from days to minutes, eliminating manual formatting, and providing clients with 24/7 self-service access to their SEO audit results.

**Key Deliverable:** A Next.js web application that integrates existing Python SEO audit scripts with a professional dashboard UI, accessible via client-specific URLs (e.g., `/client-name`).

---

## 2. Problem Statement

### What problem are we solving?
[Agency Name] needs to eliminate the manual effort required to deliver and explain technical SEO audit results to clients, freeing up Account Managers to focus on strategic consulting and improving client satisfaction.

### Quantified Impact of Current State
- **Time Cost:** ~2-3 hours per client per month on report compilation and delivery
- **Scale:** 50+ active clients = 100-150 hours/month of manual work
- **Opportunity Cost:** Reduced time for strategic SEO consulting, impacting revenue and client retention
- **Quality Issues:** Inconsistent report formatting across tools and clients leads to a perception of lower quality
- **Client Friction:** Clients struggle to understand technical reports, requiring scheduled calls and creating a dependency on Account Managers

### Who experiences this problem?
- **Primary:** [Agency Name]'s clients who need easy-to-understand, actionable insights into their website's SEO performance
- **Secondary:** [Agency Name] Account Managers who need to efficiently deliver and explain technical SEO findings, and want to focus on higher-value activities

### Current Pain Points
1. Python scripts generate raw CSV/PDF reports that lack visual appeal and are difficult for clients to understand
2. There is no unified interface to view multiple SEO audit types, forcing clients to piece together information from different sources
3. Clients must download and interpret technical reports manually, leading to confusion and frustration
4. There's no easy way to share live audit results via URL, requiring email attachments and manual distribution
5. Each client requires manual script execution and report delivery, creating a bottleneck for Account Managers
6. Inconsistent formatting across different tools creates a disjointed and unprofessional experience

---

## 3. Goals & Objectives

### Primary Goal
Create a client-facing web dashboard that integrates existing Python SEO audit scripts with a professional, card-based UI, enabling client-specific audit views with agency branding, targeting a **50% reduction in Account Manager time spent on reporting**.

### Success Criteria
- Report delivery time reduced from 2-3 days to < 5 minutes
- 80% of clients actively using the dashboard within 30 days of launch (defined as viewing the dashboard at least twice OR downloading at least one report)
- Account Manager reporting time reduced by 50%

### Secondary Goals
- Provide instant visual feedback on SEO issues grouped by severity
- Enable one-click report generation and downloads (CSV, JSON)
- Support client-specific URLs for easy sharing
- Create a scalable foundation for adding more SEO tools (27 total planned)
- Present a professional, branded experience matching the agency's visual identity

### Non-Goals (What we're explicitly NOT doing in MVP)
- User authentication/login system (MVP uses direct client URLs)
- Historical data tracking/database storage
- Real-time monitoring or scheduled audits
- Multi-tenancy with user accounts
- Payment/subscription system
- Configurable score weighting per client
- PDF export with custom branding
- Public URL input (anyone can enter a URL to audit)

---

## 4. Target Users / Personas

### Persona 1: Sarah Chen - The Marketing Director
**Role:** Marketing Director at a mid-sized e-commerce company (50 employees, $10M revenue)
**Company:** "Style Australia" - online apparel retailer selling primarily to Australian women 25-45

**Technical Level:**
- ✅ Understands: ROI, conversion rates, Google Analytics basics, email campaign metrics
- ✅ Tools used: Google Analytics, Mailchimp, Shopify admin
- ❌ Does not understand: Canonical tags, schema markup, crawl budget, HTTP status codes, structured data

**Current Workflow:**
1. Receives monthly SEO report as PDF email attachment from Account Manager
2. Skims report, highlights items that seem important
3. Forwards to web developer with "Can you look at this?"
4. Schedules 30-min call with agency to ask questions
5. Creates summary for CEO based on call notes

**Goals:**
- Quickly understand overall SEO health at a glance
- Share results with CEO without needing to explain technical details
- Demonstrate ROI on SEO investment

**Pain Points:**
- "I don't know what 'missing canonical tags' means or why it matters"
- "I spend 30 minutes every month just getting up to speed before client calls"
- "My CEO wants a simple answer: 'Are we doing better or worse?'"

**What She Needs:**
- Traffic-light system (Red/Yellow/Green) she can understand instantly
- Plain-English explanations of what each issue means
- One number (overall score) to track progress

---

### Persona 2: Tom Nguyen - The Technical Lead
**Role:** Senior Web Developer / Tech Lead at Style Australia
**Reports to:** Head of Engineering (works closely with Sarah Chen's team)

**Technical Level:**
- Expert in HTML/CSS/JavaScript, React, PHP (WordPress)
- Tools used: VS Code, Git, Jira, Chrome DevTools
- Familiar with SEO basics but not deep expertise
- Can implement fixes but needs specific guidance

**Current Workflow:**
1. Receives forwarded PDF from Sarah with "Can you fix these?"
2. Spends 1-2 hours parsing PDF to create actionable tasks
3. Googles SEO terms he doesn't understand
4. Implements fixes based on best guesses
5. Has no way to verify fixes work until next month's report

**Goals:**
- Get specific, actionable tasks (URL X has issue Y, fix with Z)
- Prioritize by impact (what moves the needle most?)
- Verify fixes without waiting for next audit

**Pain Points:**
- "The PDF says 'improve page speed' but doesn't tell me WHICH pages or HOW"
- "I need URLs, not general advice"
- "I fixed something last month but have no idea if it worked"

**What Tom Needs:**
- Expandable details with specific URLs and code examples
- Raw data export (CSV/JSON) for import into issue tracker
- Technical recommendations per issue

---

### Persona 3: Emily Torres - Account Manager
**Role:** Senior Account Manager at [Agency Name]
**Portfolio:** Manages 12 client accounts

**Technical Level:**
- Can explain SEO concepts to non-technical clients
- Runs Python scripts via command line (follows documented steps)
- Cannot debug Python errors or modify code

**Current Workflow:**
1. Runs Python audit scripts for each client (10-15 min each)
2. Opens CSV outputs, reformats into client-friendly report (30-45 min)
3. Writes summary email explaining findings (15-20 min)
4. Schedules call to walk through results (30 min)
5. Answers follow-up questions via email (15-30 min)
Total: ~2-3 hours per client per month

**Goals:**
- Onboard new clients quickly and efficiently
- Share results via URL instead of attachments
- Reduce time explaining reports (let dashboard explain itself)
- Look professional and modern to clients

**Pain Points:**
- "I spend more time formatting reports than analyzing them"
- "Every client asks the same questions about what the numbers mean"
- "I wish clients could see this themselves without me walking them through it"

**What Emily Needs:**
- One-click audit initiation
- Shareable URL per client
- Dashboard that explains itself (so she doesn't have to)

---

## 5. User Stories / Use Cases

### Account Manager Stories

**Story 1: Initiate Client Audit**
**As an Account Manager,** I want to initiate an SEO audit for a client with a single click so that I can quickly get up-to-date analysis of their website's performance and identify areas for improvement.

**Acceptance Criteria:**
- [ ] Account Manager can trigger audit via internal admin interface (not client-facing)
- [ ] Clear visual loading indicator shows script execution progress
- [ ] Dashboard automatically refreshes and displays results upon audit completion
- [ ] Informative error messages are displayed for any failed audits (see FR-11)

---

**Story 2: View Client Dashboard**
**As an Account Manager,** I want to view a client's SEO dashboard via their unique URL so that I can review the results and prepare talking points before sharing with the client.

**Acceptance Criteria:**
- [ ] Dashboard is accessible at `/[client-slug]`
- [ ] Overall SEO score (0-100) is prominently displayed
- [ ] Results are organized into clearly labeled cards with severity badges
- [ ] Agency branding (logo, colors) is visible
- [ ] Loading state is displayed if an audit is in progress

---

**Story 3: Download Client Reports**
**As an Account Manager,** I want to download audit reports in multiple formats so that I can share them with clients via email or import the data into other reporting tools.

**Acceptance Criteria:**
- [ ] CSV download is available for each tool
- [ ] JSON download is available for each tool
- [ ] Files are named: `{client}_{tool}_{date}.{format}`
- [ ] Download buttons are clearly visible on each card and in export section

---

**Story 4: Onboard a New Client**
**As an Account Manager,** I want to quickly onboard a new client to the dashboard so that I can immediately start tracking their SEO performance.

**Acceptance Criteria:**
- [ ] New clients added via `clients.json` configuration file
- [ ] Required fields: `name`, `slug`, `url`, `enabledTools`
- [ ] Client folder auto-created on first audit
- [ ] No code deployment required to add clients

---

**Story 5: Handle Audit Errors**
**As an Account Manager,** I want to quickly understand and resolve audit errors so that I can ensure clients receive accurate results.

**Acceptance Criteria:**
- [ ] Failed audits display specific, actionable error messages
- [ ] Common errors include suggested resolutions
- [ ] Last successful results shown with "Data may be outdated" warning
- [ ] Errors logged with timestamp for debugging

---

### Client Stories

**Story 6: View My Dashboard**
**As a client,** I want to visit my unique URL to view my SEO audit results so that I can easily understand my website's SEO health.

**Acceptance Criteria:**
- [ ] Dashboard loads at `/[my-company-slug]`
- [ ] Overall score visible within 1 second of page load
- [ ] Cards display Critical (red), Warning (amber), Good (green) status
- [ ] No login required
- [ ] Agency branding visible

---

**Story 7: Understand SEO Issues**
**As a client,** I want to easily understand what each SEO issue means so that I can discuss them with my team and prioritize fixes.

**Acceptance Criteria:**
- [ ] Each card has a plain-English description (no jargon)
- [ ] "Why it matters" explanation on each card
- [ ] Expandable section for technical details
- [ ] Severity indicated with color AND text label

---

**Story 8: Download Reports**
**As a client,** I want to download audit reports so that I can share them with my internal team.

**Acceptance Criteria:**
- [ ] CSV and JSON downloads available
- [ ] Clear download buttons visible
- [ ] Files include company name and date

---

## 6. Functional Requirements

### 6.1 Dashboard Display

**FR-1: Overall Score Display**
- Display aggregate SEO score (0-100) prominently at top of dashboard
- Score calculation:
  - Base score = Weighted average of individual tool scores
  - Weights: Core Web Vitals (35%), Schema (25%), SSL/HTTPS (25%), Title Tags (15%)
  - Penalty: Subtract 5 points for each Critical issue (max penalty: 25 points)
  - Floor: Minimum score is 0
- *Note: Weights are initial assumptions to be validated post-launch by correlating scores with client SEO performance.*
- Each tool defines its own scoring methodology, documented in tool configuration.

**FR-2: Card Grid Layout**
- Responsive grid: Mobile (1 col), Tablet (2 cols), Desktop (3 cols)
- Cards maintain consistent height within rows
- Visual grouping by status (Criticals first, then Warnings, then Good)

**FR-3: Card Content Requirements**
Each active card displays:
- Tool name and icon (Lucide React)
- Status badge: Critical (Red), Warning (Amber/Gold), Good (Teal/Green)
- One-line description (plain English, no jargon)
- Key metric summary (e.g., "85/100", "3 issues found")
- "Why it matters" tooltip or subtitle
- Expandable details for full results

**FR-4: Coming Soon Cards**
- Display placeholder cards for inactive tools
- "Coming Soon" badge in gray
- Brief description of what the tool will check
- No expandable content

### 6.2 Client Management

**FR-5: Client Configuration**
- Clients defined in `clients.json` file
- Schema:
```json
{
  "clients": [
    {
      "name": "Client Company Name",
      "slug": "client-slug",
      "url": "https://clientsite.com",
      "enabledTools": ["schema", "cwv", "ssl", "title-tags"]
    }
  ]
}
```

**FR-6: URL Routing**
- Valid client slugs serve dashboard at `/[slug]`
- Invalid slugs return branded 404 page
- Slugs validated against `clients.json` allowlist

### 6.3 Audit Execution

**FR-7: Audit Initiation**
- Account Managers trigger audits via internal mechanism (API endpoint or admin page)
- Clients cannot trigger audits (view-only access)
- Audit runs all enabled tools for the client

**FR-8: Result Caching**
- Results cached as JSON files in `/clients/[slug]/` directory
- Cached results displayed if available
- Cache invalidated when new audit runs
- Cache retention: Keep last 3 audit results per client

**FR-9: Execution Timeouts**
- Individual script timeout: 2 minutes
- Total audit timeout: 5 minutes
- Timeout triggers error state, partial results not displayed

### 6.4 Export Functionality

**FR-10: Download Formats**
- CSV: Human-readable spreadsheet format
- JSON: Machine-readable for API/integration
- File naming: `{client-slug}_{tool}_{YYYY-MM-DD}.{format}`

### 6.5 Error Handling

**FR-11: Error States**
Error messages should be user-friendly and actionable. Content determined by UX writing. Examples:
- **Script timeout:** "The audit took too long. Please try again or contact support@[agency-domain]."
- **Script crash:** "An error occurred while running [Tool Name]. Our team has been notified."
- **Network error:** "Unable to reach [client URL]. Please verify the URL is accessible."
- **Partial failure:** Show successful results with error badge on failed cards

**FR-12: Degraded Mode**
- If external API unavailable, affected card shows "Temporarily unavailable"
- Other tools continue to display normally
- Warning banner: "Some tools are temporarily unavailable"

### 6.6 Data Retention

**FR-13: Data Retention Policy**
- Keep last 3 successful audit results per client
- Older results automatically deleted on new audit completion
- Manual trigger only in MVP (no scheduled audits)

---

## 7. Non-Functional Requirements

### 7.1 Performance
- Page load time: < 2 seconds for cached results (desktop, broadband connection)
- Time to interactive: < 3 seconds
- Audit execution timeout: 5 minutes max
- UI remains responsive during execution (loading states)

### 7.2 Security
- Client slugs validated against allowlist only
- No arbitrary code/command execution
- File downloads restricted to client's own directory
- Path traversal protection on all file operations
- Python scripts run with minimal permissions
- Input validation on all API endpoints
- SSRF protection in URL-fetching operations

### 7.3 Accessibility
- WCAG 2.1 Level AA compliance
- Text contrast ratio: minimum 4.5:1
- Color is not the only indicator (icons + text + color for status)
- Keyboard navigable
- Screen reader compatible (semantic HTML, ARIA labels)

### 7.4 Branding
- **Primary CTA:** Primary Brand Color (Orange/Red)
- **Header/Footer:** Dark Brand Color (Navy/Dark Blue)
- **Secondary Accent:** Secondary Brand Color (Blue/Cyan)
- **Good Status:** Success Green (Teal)
- **Warning Status:** Warning Amber (Gold)
- **Critical Status:** Error Red
- **Coming Soon:** Neutral Gray
- **Light Backgrounds:** Light Gray/Blue
- **Font:** Modern Sans-Serif (e.g., Inter, System UI)
- **Logo:** Agency logo in header

---

## 8. Success Metrics / KPIs

### Primary Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Account Manager Time Savings | 50% reduction in reporting time | Pre/post timesheets. Sample 5 Account Managers, track 4 weeks before and after launch. |
| Client Dashboard Adoption | 80% of clients active within 30 days | Analytics: unique `/[slug]` views. "Active" = 2+ views OR 1+ download. |
| Client Satisfaction Score | 4.5/5 average | Post-launch survey at 30 days. Questions: (1) Ease of use, (2) Helpfulness, (3) Likelihood to recommend, (4) Open: "What would you improve?" |

### Secondary Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Page Load Time | < 2 seconds (p95) | Vercel Analytics |
| Audit Success Rate | > 95% | Log analysis |
| Report Downloads | Track volume | API endpoint logging |
| Support Requests | 30% reduction in "explain report" tickets | Support ticket tracking |

---

## 9. Scope

### In Scope (MVP)
- Next.js dashboard with agency branding
- **4 active SEO tools:** Schema Markup, Core Web Vitals, SSL/HTTPS, Title Tag Analysis
- Client-specific URLs (`/[slug]`)
- Card-based results with severity indicators
- CSV and JSON exports
- Python script integration
- Basic landing page (marketing/informational)
- Error states with user-friendly messages
- Degraded mode for partial API failures
- Data retention (last 3 audits per client)

### Out of Scope (MVP)
- User authentication/login
- Historical data visualization/trending
- Database storage (file-based only)
- Real-time monitoring
- Scheduled/automated audits
- Multi-language support
- White-labeling for other agencies
- PDF export
- Public URL input
- Client self-service audit triggering

---

## 10. Dependencies

### Internal Dependencies
| Dependency | Owner | Status | Fallback |
|------------|-------|--------|----------|
| Python scripts output JSON | Dev Team | Required | CSV-to-JSON wrapper script |
| Agency logo (high-res) | Marketing | Required | Text logo placeholder |
| Title Tag analysis script | Dev Team | Required | Launch with 3 tools + "Coming Soon" placeholder; prioritize for Sprint 2 |

### External Dependencies
| Dependency | Provider | Impact of Unavailability |
|------------|----------|--------------------------|
| Google PageSpeed API | Google | CWV card shows "unavailable", other tools work |
| SSL certificate checking | Python ssl library | SSL card shows "unavailable", other tools work |

---

## 11. Risks and Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Python script execution failures | High | Medium | Error handling, 5-min timeout, fallback to last results with warning |
| Long script execution (>2 min) | Medium | High | Loading indicators, expectation setting, result caching |
| Client data isolation breach | Critical | Low | Slug allowlist, path sanitization, separate folders, security tests |
| Scaling beyond local execution | Medium | High (post-MVP) | Document limitations, plan Docker/cloud migration |
| API key exposure | Critical | Low | Server-side only, never bundled, rotation runbook |
| External API outage | Medium | Low | Graceful degradation per tool, warning banner |

---

## 12. Open Questions

### Decisions Required Before Development

1. **Landing Page Content**
   - Marketing content vs redirect to contact page?
   - **Recommendation:** Marketing content with "Contact for Access" CTA
   - **Decision Owner:** Marketing

2. **Card Expansion Behavior**
   - Inline expand, modal, or detail page?
   - **Recommendation:** Inline expand
   - **Decision Owner:** Product/Design

3. **Title Tag Script Availability**
   - Ready for MVP?
   - **Decision Required By:** Development kickoff
   - **Fallback:** 3 tools + placeholder; deliver in Sprint 2

---

## 13. Appendix

### A. Brand Guidelines (Template)
| Element | Value | Notes |
|---------|-------|-------|
| Primary CTA | [Primary Color] | Use for main action buttons |
| Header/Footer | [Dark Color] | Navigation and footer background |
| Secondary Accent | [Secondary Color] | Links, highlights |
| Good Status | [Success Green] | Positive results |
| Warning | [Warning Amber] | Moderate issues |
| Critical | [Error Red] | Urgent issues |
| Coming Soon | [Neutral Gray] | Placeholder state |
| Light Background | [Light Gray/Blue] | Page backgrounds |
| Font | [Sans-Serif Font] | Primary typography |
| Website | [agency-domain.com] | Company website |

### B. SEO Tool Feature Reference (27 Checks)
1. Title Tag Analysis
2. Meta Description
3. Heading Structure (H1-H6)
4. Internal Links
5. External Links
6. Image Alt Text
7. Schema Markup
8. Core Web Vitals
9. Mobile Responsiveness
10. SSL/HTTPS
11. Open Graph Tags
12. Twitter Cards
13. Canonical URLs
14. Robots.txt
15. XML Sitemap
16. URL Structure
17. Content Analysis
18. Accessibility
19. Meta Robots
20. Hreflang
21. Favicon
22. Lazy Loading
23. Doctype
24. Character Encoding
25. Keywords in URL
26. Page Speed
27. Security Headers

### C. MVP Tool Breakdown

**Active (4):**
1. Schema Markup Audit
2. Core Web Vitals (via Google PageSpeed API)
3. SSL/HTTPS Checker
4. Title Tag Analysis

**Coming Soon (23):** All remaining tools from list B

### D. Example Card Content

**Schema Markup Card (Good):**
- **Title:** Schema Markup
- **Icon:** Code
- **Status:** Good (green)
- **Summary:** "5 schema types found across 12 pages"
- **Why it matters:** "Schema helps search engines understand your content and may earn rich snippets."
- **Details:** Pages with schema, pages missing schema

**Core Web Vitals Card (Warning):**
- **Title:** Core Web Vitals
- **Icon:** Gauge
- **Status:** Warning (amber)
- **Summary:** "Performance score: 68/100"
- **Why it matters:** "Google uses Core Web Vitals as a ranking factor."
- **Details:** LCP, FID, CLS values, top recommendations

---

## 14. Technical Architecture Summary

### 14.1 System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENTS (Browser)                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    VERCEL (Next.js 15)                          │
│  Dashboard Pages │ API Routes │ Static Assets                   │
│  Region: [Preferred Region]                                     │
└─────────────────────────────────────────────────────────────────┘
                              │ HTTPS + API Key
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                  RAILWAY (Python/FastAPI)                        │
│  Audit Endpoints │ Script Executor │ Result Storage             │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  Python SEO Scripts (schema, cwv, ssl, title-tags)          ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FILE STORAGE (10GB SSD)                       │
│         /clients/{slug}/audit_{timestamp}.json                   │
└─────────────────────────────────────────────────────────────────┘
```

### 14.2 Technology Stack

| Layer | Technology | Hosting |
|-------|------------|---------|
| Frontend | Next.js 15 (App Router), TypeScript, Tailwind CSS, shadcn/ui | Vercel |
| Backend | Python 3.11, FastAPI | Railway |
| Storage | File-based JSON | Railway Volume (10GB SSD) |
| External APIs | Google PageSpeed API | Google Cloud |

### 14.3 Key Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Frontend hosting | Vercel | Native Next.js support, edge network, easy deployment |
| Backend hosting | Railway | Simple Python deployment, persistent storage, affordable |
| Storage | JSON files | Simple for MVP, no database overhead, easy migration to S3 later |
| Auth (internal) | API key | Simple, secure for server-to-server communication |
| Auth (clients) | None (URL-based) | Unguessable slugs provide security without login friction |

### 14.4 Infrastructure Costs

| Service | Purpose | Monthly Cost |
|---------|---------|--------------|
| Vercel Pro | Next.js hosting | $20 |
| Railway | Python server + 10GB storage | $10 |
| UptimeRobot | Health monitoring | Free |
| Google PageSpeed API | Core Web Vitals data | Free (25k requests/day) |
| **Total** | | **~$30/month** |

---

## 15. Implementation Roadmap

### Phase 1: Project Setup & Foundation
**Deliverable:** Working Next.js app with agency branding

**Tasks:**
- [ ] Initialize Next.js 15 project with TypeScript
- [ ] Configure Tailwind CSS with brand colors
- [ ] Install and configure shadcn/ui components
- [ ] Create base layout with header (logo) and footer
- [ ] Set up `clients.json` configuration file with test client
- [ ] Implement slug validation and 404 page
- [ ] Deploy to Vercel (preview environment)

**Acceptance Criteria:**
- Landing page displays at `/` with agency branding
- `/test-client` shows placeholder dashboard
- `/invalid-slug` shows branded 404 page

---

### Phase 2: Dashboard UI Components
**Deliverable:** Complete dashboard UI with mock data

**Tasks:**
- [ ] Build ScoreDisplay component (circular progress indicator)
- [ ] Build AuditCard component with all states (good/warning/critical/coming-soon)
- [ ] Build CardGrid with responsive layout (1/2/3 columns)
- [ ] Build DownloadSection with export buttons
- [ ] Implement card expansion (accordion for details)
- [ ] Add loading skeleton component
- [ ] Test with mock audit data

**Acceptance Criteria:**
- Dashboard displays all 4 MVP tool cards + 23 "Coming Soon" cards
- Cards show correct colors for each status
- Grid is responsive at mobile/tablet/desktop breakpoints
- Cards expand to show detailed content

---

### Phase 3: Python Server Setup
**Deliverable:** FastAPI server deployed on Railway

**Tasks:**
- [ ] Initialize Python project with FastAPI
- [ ] Create `/health` endpoint
- [ ] Create `/audit/{slug}` endpoint (stub)
- [ ] Create `/results/{slug}` endpoint (stub)
- [ ] Implement API key authentication middleware
- [ ] Implement CORS configuration
- [ ] Set up file storage service (`/clients/{slug}/`)
- [ ] Create Dockerfile and deploy to Railway
- [ ] Configure environment variables

**Acceptance Criteria:**
- `/health` returns server status
- API key validation works correctly
- File storage creates/reads JSON files

---

### Phase 4: Python Script Integration
**Deliverable:** Working audit execution with real scripts

**Tasks:**
- [ ] Integrate Schema Markup audit script
- [ ] Integrate SSL/HTTPS checker script
- [ ] Integrate Core Web Vitals script (PageSpeed API)
- [ ] Implement script executor with timeouts (2 min per script, 5 min total)
- [ ] Implement partial failure handling
- [ ] Implement score calculation logic
- [ ] Test end-to-end audit execution

**Acceptance Criteria:**
- Triggering audit runs all enabled scripts
- Results saved to JSON file
- Partial failures don't block other tools
- Overall score calculated correctly

---

### Phase 5: Vercel ↔ Python Integration
**Deliverable:** Full data flow from trigger to display

**Tasks:**
- [ ] Create Next.js API route: `POST /api/audit/[slug]`
- [ ] Create Next.js API route: `GET /api/results/[slug]`
- [ ] Create Next.js API route: `GET /api/download/[slug]/[tool]/[format]`
- [ ] Implement Python client with 3 retries and exponential backoff
- [ ] Implement graceful degradation (server unavailable state)
- [ ] Connect dashboard to real API data
- [ ] Test error scenarios

**Acceptance Criteria:**
- Dashboard displays real audit results
- Downloads work for CSV and JSON
- Graceful error handling when Python server down

---

### Phase 6: Polish & Launch Prep
**Deliverable:** Production-ready application

**Tasks:**
- [ ] Implement error banners and user-friendly messages
- [ ] Add "Why it matters" explanations to all cards
- [ ] Implement data retention (auto-delete old audits)
- [ ] Set up UptimeRobot monitoring
- [ ] Configure production environment variables
- [ ] Write admin documentation (how to trigger audits, add clients)
- [ ] Perform security review (SSRF, path traversal, rate limiting)
- [ ] Run E2E tests with Playwright
- [ ] Deploy to production

**Acceptance Criteria:**
- All acceptance criteria from PRD user stories pass
- Security tests pass
- Documentation complete
- Monitoring active

---

## 16. Handoff Checklist

### Pre-Development Requirements

| Item | Owner | Status |
|------|-------|--------|
| Agency logo (PNG, high-res) | Marketing | Required |
| Brand color specifications | Marketing | Required |
| Test client URL for development | Account Team | Required |
| Google PageSpeed API key | Dev Team | Required |
| Railway account setup | Dev Team | Required |
| Vercel account setup | Dev Team | Required |
| Python SEO scripts (Schema, SSL) | Dev Team | Required |

### Decisions Required

| Decision | Options | Recommendation | Owner |
|----------|---------|----------------|-------|
| Landing page content | Marketing page vs. redirect | Marketing page with "Contact for Access" | Marketing |
| Card expansion style | Inline vs. modal vs. detail page | Inline accordion | Product/Design |
| Title Tag script | Ready for MVP vs. Coming Soon | Confirm availability | Dev Team |

### Documentation Provided

| Document | Location |
|----------|----------|
| Product Requirements (this document) | `technical-seo-dashboard-prd-v1.4-DEBRANDED.md` |
| Technical Specification | TBD |
| Agency Logo | TBD |

### Key Contacts

| Role | Responsibility |
|------|----------------|
| Product Owner | Requirements clarification, priority decisions |
| Marketing | Brand assets, landing page content |
| Dev Team | Implementation, script integration |
| Account Team | Test client selection, UAT feedback |

---

## 17. Post-MVP Roadmap

### Near-Term Enhancements (Sprint 2-3)
- [ ] Title Tag Analysis tool (if not in MVP)
- [ ] PDF export functionality
- [ ] Historical audit comparison view
- [ ] Email notifications on audit completion

### Medium-Term Enhancements (Months 2-3)
- [ ] Scheduled/automated audits (weekly/monthly)
- [ ] Additional SEO tools (Meta Description, Heading Structure)
- [ ] Client self-service: request new audit
- [ ] Admin dashboard for Account Managers

### Long-Term Roadmap (Months 4+)
- [ ] User authentication and multi-tenant support
- [ ] Database storage (PostgreSQL) for scale
- [ ] All 27 SEO tools from reference list
- [ ] White-label option for partner agencies
- [ ] API access for client integrations

---

**End of PRD v1.4 (DE-BRANDED)**
