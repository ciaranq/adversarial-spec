# Product Requirements Document (PRD)
## Technical SEO Dashboard - IntelliAgent

**Version:** 1.0  
**Date:** January 19, 2026  
**Author:** Claude (for Chatterbox/IntelliAgent)

---

## 1. Problem Statement

### What problem are we solving?
IntelliAgent needs a professional, client-facing technical SEO dashboard that presents audit results from their Python-based SEO tools in a clean, visual format similar to industry tools like SEO It Is.

### Who experiences this problem?
- **Primary:** IntelliAgent's clients who need easy-to-understand SEO audit reports
- **Secondary:** IntelliAgent team members who need to deliver and explain technical SEO findings

### Current pain points and limitations
- Python scripts generate raw CSV/PDF reports that lack visual appeal
- No unified interface to view multiple SEO audit types
- Clients need to download and interpret technical reports manually
- No easy way to share live audit results via URL
- Each client requires manual script execution and report delivery

---

## 2. Goals & Objectives

### Primary Goal
Create a Next.js-based web dashboard that integrates existing Python SEO audit scripts with a professional, card-based UI inspired by SEO It Is, enabling client-specific audit views.

### Secondary Goals
- Provide instant visual feedback on SEO issues grouped by severity
- Enable one-click report generation and downloads
- Support client-specific URLs (e.g., `/client-a`) for easy sharing
- Create a scalable foundation for adding more SEO tools (27 total planned)

### Non-Goals (What we're explicitly NOT doing)
- User authentication/login system (MVP focuses on direct client URLs)
- Historical data tracking/database storage
- Real-time monitoring or scheduled audits
- Multi-tenancy with user accounts
- Payment/subscription system
- SSL/HTTPS checker (not yet developed)

---

## 3. User Stories

### Client User Stories

**Story 1: View Dashboard**

**As a client,** I want to visit my unique URL (e.g., `/client-a`) so that I can view my site's SEO audit results in a clean dashboard.

**Acceptance Criteria:**
- Client can access their dashboard via `/[client-slug]`
- Dashboard displays overall SEO score
- Results are organized in card format by tool/category
- Visual indicators show issue severity (Critical, Warning, Good)

**Story 2: Download Reports**

**As a client,** I want to download audit reports so that I can share them with my team or reference them offline.

**Acceptance Criteria:**
- Download buttons available for CSV and PDF formats
- Files include client name and timestamp in filename
- Reports contain same data visible in UI

**Story 3: Trigger New Audit**

**As a client,** I want to trigger a new audit if results don't exist so that I can get up-to-date analysis.

**Acceptance Criteria:**
- "Run Analysis" button appears when no reports exist
- Loading indicator shows progress
- Results display automatically after completion
- Error messages appear if analysis fails

### IntelliAgent Team User Stories

**Story 4: Add New Clients**

**As an IntelliAgent team member,** I want to add new clients easily so that I can quickly onboard them to the dashboard.

**Acceptance Criteria:**
- New clients configured via .env file
- Client folder structure auto-created
- No code changes needed to add clients

**Story 5: Manage Tool Status**

**As an IntelliAgent team member,** I want to see which tools are active vs. coming soon so that I can manage client expectations.

**Acceptance Criteria:**
- Active tools display real data in cards
- Coming soon tools show placeholder cards with "Coming Soon" badge
- Clear visual distinction between states

---

## 4. Technical Requirements

### Frontend Requirements

#### Technology Stack
- **Framework:** Next.js 15.x (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Components:** shadcn/ui
- **Icons:** Lucide React (from shadcn/ui)

#### UI/UX Requirements

**Layout Structure:**
```
┌─────────────────────────────────────┐
│         Header / Navigation         │
├─────────────────────────────────────┤
│     Hero Section with URL Input     │
│   (Optional - may be disabled for   │
│        client-specific pages)       │
├─────────────────────────────────────┤
│       Overall Score Display         │
│         (e.g., "Score: 85")         │
├─────────────────────────────────────┤
│                                     │
│     SEO Audit Cards Grid            │
│  ┌──────┐ ┌──────┐ ┌──────┐       │
│  │ Card │ │ Card │ │ Card │       │
│  │  1   │ │  2   │ │  3   │       │
│  └──────┘ └──────┘ └──────┘       │
│  ┌──────┐ ┌──────┐ ┌──────┐       │
│  │ Card │ │ Card │ │ Card │       │
│  │  4   │ │  5   │ │  6   │       │
│  └──────┘ └──────┘ └──────┘       │
│  ... (up to 27 cards total)        │
│                                     │
├─────────────────────────────────────┤
│    Export/Download Section          │
└─────────────────────────────────────┘
```

**Card Component Structure:**
Each audit card should include:
- Status badge (Critical/Warning/Good with color coding)
- Tool name/title
- Icon (relevant to the audit type)
- Brief description
- Key metrics/findings
- Expandable details section (optional)
- "Coming Soon" badge for inactive tools

**Color Coding:**
- **Critical:** Red (#EF4444 or similar)
- **Warning:** Yellow/Amber (#F59E0B)
- **Good:** Green (#10B981)
- **Coming Soon:** Gray (#6B7280)

**Responsive Design:**
- Mobile: 1 column
- Tablet: 2 columns
- Desktop: 3 columns
- Cards maintain consistent height within rows

#### Page Routes

```
/                          → Landing page with URL input
/[client-slug]            → Client-specific dashboard
/api/analyze              → Trigger Python scripts
/api/results/[client]     → Fetch existing results
```

#### State Management
- React hooks (useState, useEffect) for local state
- No Redux/Zustand needed for MVP
- Client-side data fetching using native fetch API

### Backend Requirements

#### API Endpoints

**1. POST /api/analyze**

```typescript
Request Body:
{
  "clientSlug": "client-a",
  "tools": ["schema", "core-web-vitals"], // optional, defaults to all
  "forceRefresh": false // optional, skip if results exist
}

Response:
{
  "success": true,
  "client": "client-a",
  "results": {
    "schema": { /* JSON output */ },
    "coreWebVitals": { /* JSON output */ }
  },
  "files": {
    "schema": {
      "csv": "/clients/client-a/schema_report.csv",
      "json": "/clients/client-a/schema_report.json"
    },
    "coreWebVitals": {
      "json": "/clients/client-a/cwv_report.json",
      "pdf": "/clients/client-a/cwv_report.pdf"
    }
  },
  "timestamp": "2026-01-19T10:30:00Z"
}

Error Response:
{
  "success": false,
  "error": "Python script execution failed",
  "details": "..."
}
```

**2. GET /api/results/[client]**

```typescript
Response:
{
  "success": true,
  "client": "client-a",
  "hasResults": true,
  "results": {
    "schema": { /* parsed JSON */ },
    "coreWebVitals": { /* parsed JSON */ }
  },
  "lastUpdated": "2026-01-19T10:30:00Z"
}

// If no results exist:
{
  "success": true,
  "client": "client-a",
  "hasResults": false,
  "message": "No audit results found. Click 'Run Analysis' to generate."
}
```

**3. GET /api/download/[client]/[tool]/[format]**

```typescript
// Direct file download
// Examples:
// /api/download/client-a/schema/csv
// /api/download/client-a/core-web-vitals/pdf
```

#### Python Script Integration

**Execution Method:**
- Next.js API routes use Node.js `child_process.spawn()` to execute Python scripts
- Scripts run synchronously (await completion)
- Capture stdout/stderr for logging
- Return exit codes for error handling

**Modified Python Scripts:**

**Schema Audit Script Modifications:**
```python
# ADD: JSON output option
def generate_json_output(audit_results: list, output_path: str):
    """Generate JSON format for web dashboard integration."""
    json_output = {
        "summary": {
            "total_pages": len(audit_results),
            "pages_with_schema": sum(1 for r in audit_results if r.get('schema_types')),
            "pages_without_schema": sum(1 for r in audit_results if not r.get('schema_types')),
            "total_schema_types": sum(len(r.get('schema_types', [])) for r in audit_results),
            "errors": sum(1 for r in audit_results if r.get('error'))
        },
        "pages": audit_results,
        "timestamp": datetime.now().isoformat()
    }
    
    with open(output_path, 'w') as f:
        json.dump(json_output, f, indent=2)
```

**Core Web Vitals Script:**
- Already supports JSON output
- No modifications needed
- Use existing `--format json` flag

**Script Execution Commands:**
```bash
# Schema Audit
python schema_audit.py \
  --url $CLIENT_URL \
  --output /clients/$CLIENT_SLUG/schema_report.csv \
  --format json  # NEW: output JSON alongside CSV

# Core Web Vitals
python main.py analyze $CLIENT_URL \
  --format json \
  --output /clients/$CLIENT_SLUG/cwv_report.json
```

#### Data Models

**Client Configuration (.env format):**
```env
# Client A
CLIENT_A_NAME="Client A Company"
CLIENT_A_SLUG="client-a"
CLIENT_A_URL="https://clienta.com"
CLIENT_A_ENABLED_TOOLS="schema,core-web-vitals"

# Client B
CLIENT_B_NAME="Client B Inc"
CLIENT_B_SLUG="client-b"
CLIENT_B_URL="https://clientb.com"
CLIENT_B_ENABLED_TOOLS="schema,core-web-vitals"

# Add more clients...
```

**TypeScript Interfaces:**
```typescript
interface Client {
  name: string;
  slug: string;
  url: string;
  enabledTools: string[];
}

interface AuditCard {
  id: string;
  title: string;
  description: string;
  status: 'critical' | 'warning' | 'good' | 'coming-soon';
  icon: string; // Lucide icon name
  metrics?: {
    label: string;
    value: string | number;
  }[];
  details?: string;
}

interface SchemaAuditResult {
  summary: {
    total_pages: number;
    pages_with_schema: number;
    pages_without_schema: number;
    total_schema_types: number;
    errors: number;
  };
  pages: Array<{
    url: string;
    schema_types: string[];
    suggestions: string[];
    error?: string;
  }>;
  timestamp: string;
}

interface CoreWebVitalsResult {
  url: string;
  strategy: 'mobile' | 'desktop';
  performance_score: number;
  metrics: {
    lcp: { value: number; rating: string };
    fid: { value: number; rating: string };
    cls: { value: number; rating: string };
  };
  recommendations: Array<{
    title: string;
    priority: string;
    impact: string;
  }>;
  timestamp: string;
}

interface DashboardData {
  client: Client;
  overallScore: number;
  cards: AuditCard[];
  downloadLinks: {
    tool: string;
    format: string;
    url: string;
  }[];
}
```

### Infrastructure Requirements

#### File Structure
```
technical-seo-dashboard/
├── app/
│   ├── page.tsx                    # Landing page
│   ├── [client]/
│   │   └── page.tsx                # Client dashboard
│   ├── api/
│   │   ├── analyze/
│   │   │   └── route.ts            # Trigger Python scripts
│   │   ├── results/
│   │   │   └── [client]/
│   │   │       └── route.ts        # Get results
│   │   └── download/
│   │       └── [client]/
│   │           └── [tool]/
│   │               └── [format]/
│   │                   └── route.ts
│   └── layout.tsx
├── components/
│   ├── ui/                         # shadcn/ui components
│   ├── audit-card.tsx
│   ├── score-display.tsx
│   ├── client-dashboard.tsx
│   └── download-section.tsx
├── lib/
│   ├── python-executor.ts          # Python script execution
│   ├── client-config.ts            # Load client configs
│   ├── data-transformer.ts         # Transform Python output to UI format
│   └── utils.ts
├── types/
│   └── index.ts                    # TypeScript interfaces
├── clients/                        # Client-specific data
│   ├── client-a/
│   │   ├── schema_report.csv
│   │   ├── schema_report.json
│   │   ├── cwv_report.json
│   │   └── cwv_report.pdf
│   └── client-b/
│       └── ...
├── python-scripts/                 # Python audit tools
│   ├── schema_audit.py
│   ├── main.py                     # CWV analyzer
│   └── src/
│       └── ...
├── .env.local
├── .env.example
├── package.json
├── tsconfig.json
├── tailwind.config.ts
└── README.md
```

#### Hosting Requirements
- **Development:** localhost:3000
- **Production:** Vercel (planned, not MVP)
- **Python Execution:** Local environment for MVP
- **File Storage:** Local filesystem (`/clients` directory)

#### Performance Requirements
- Page load time: < 2 seconds
- Python script execution: 30-120 seconds (acceptable for MVP)
- UI responsive during script execution (loading states)

#### Security Requirements
- Client slugs validated against configured clients only
- No arbitrary code execution
- File downloads restricted to client's own folder
- Python scripts run with limited permissions
- Input validation on all API endpoints
- SSRF protection (already in CWV script)

---

## 5. Success Metrics

### How will we measure success?

#### Primary Metrics
1. **Client Satisfaction:** Clients can view and understand their audit results without explanation
2. **Report Delivery Time:** Reduced from manual delivery to instant access via URL
3. **Adoption Rate:** Percentage of clients using the dashboard vs. requesting manual reports

#### Key Performance Indicators (KPIs)
- Dashboard load time < 2 seconds
- Python script success rate > 95%
- Zero client data cross-contamination incidents
- Client report downloads per week

#### User Acceptance Criteria
- Client can access their dashboard URL without assistance
- Client can interpret Critical/Warning/Good status without explanation
- Client can download reports in their preferred format
- IntelliAgent team can add new clients in < 5 minutes

---

## 6. Timeline & Phases

### Phase 1: Foundation (Week 1)
**Goal:** Basic Next.js app with static UI

**Tasks:**
- Initialize Next.js 15 project with TypeScript, Tailwind, shadcn/ui
- Create file structure and routing
- Build card components with mock data
- Implement responsive grid layout
- Design and implement 27 card placeholders (3 active, 24 coming soon)

**Deliverable:** Static dashboard displaying all 27 cards with mock data

**Estimated Effort:** 8-12 hours

---

### Phase 2: Python Integration (Week 2)
**Goal:** Connect Python scripts to Next.js API

**Tasks:**
- Create API routes for triggering scripts and fetching results
- Implement Python script executor in Node.js
- Add JSON output to Schema Audit script
- Test script execution from Next.js
- Implement file-checking logic (run vs. display existing)
- Add error handling and logging

**Deliverable:** Working API that executes Python scripts and returns results

**Estimated Effort:** 12-16 hours

**Dependencies:** 
- Python scripts must output JSON format
- Node.js can execute Python scripts locally

---

### Phase 3: Data Flow & Display (Week 3)
**Goal:** Transform Python output into UI cards

**Tasks:**
- Parse JSON outputs from both scripts
- Transform data into AuditCard format
- Calculate overall SEO score algorithm
- Implement dynamic card population
- Add status badge logic (Critical/Warning/Good)
- Connect API to dashboard UI

**Deliverable:** Dashboard displays real Python script results

**Estimated Effort:** 10-14 hours

**Dependencies:** Phase 2 complete

---

### Phase 4: Client System (Week 4)
**Goal:** Multi-client support with unique URLs

**Tasks:**
- Implement client configuration loading from .env
- Create `/[client]` dynamic route
- Build client folder structure creation
- Implement "Run Analysis" button functionality
- Add loading states during script execution
- Test with multiple client configurations

**Deliverable:** Multiple clients can access their own dashboards

**Estimated Effort:** 8-12 hours

**Dependencies:** Phase 3 complete

---

### Phase 5: Downloads & Polish (Week 5)
**Goal:** Download functionality and UI refinement

**Tasks:**
- Implement download API endpoints
- Add download buttons to UI
- Test CSV/PDF downloads
- Refine card styling to match SEO It Is aesthetic
- Add animations and transitions
- Implement error states and empty states
- Write README documentation

**Deliverable:** Production-ready MVP

**Estimated Effort:** 10-12 hours

**Dependencies:** Phase 4 complete

---

### Total Estimated Timeline: 4-5 weeks
**Total Effort:** 48-66 hours

---

## 7. Potential Risks & Mitigation Strategies

### Risk 1: Python Script Execution Failures
**Impact:** High  
**Probability:** Medium

**Mitigation:**
- Comprehensive error handling in API routes
- Script execution timeout (5 minutes max)
- Fallback to displaying last successful results
- Detailed error logging for debugging
- Retry mechanism (1 automatic retry)

---

### Risk 2: Long Script Execution Times
**Impact:** Medium  
**Probability:** High (30-120 seconds expected)

**Mitigation:**
- Clear loading indicators with progress messages
- Consider implementing queue system for future (not MVP)
- Set client expectations upfront ("Analysis takes 1-2 minutes")
- Cache results and only re-run when explicitly requested

---

### Risk 3: Client Data Isolation Issues
**Impact:** Critical  
**Probability:** Low

**Mitigation:**
- Strict client slug validation
- File path sanitization
- Separate folders per client
- Unit tests for path generation
- Code review focused on security

---

### Risk 4: Scaling Beyond Local Environment
**Impact:** Medium  
**Probability:** High (when moving to production)

**Mitigation:**
- Document known limitations of local execution
- Plan for containerization (Docker) in Phase 2
- Consider serverless Python execution (AWS Lambda) for future
- Keep client data structure cloud-ready (S3-compatible)

---

### Risk 5: Python Dependency Management
**Impact:** Medium  
**Probability:** Medium

**Mitigation:**
- Document all Python dependencies clearly
- Use virtual environment (venv)
- Provide setup instructions in README
- Consider Docker container for consistent environment

---

## 8. Open Questions

### Technical Unknowns

1. **Python Execution Environment:**
   - Should we use a virtual environment or system Python?
   - Do we need to install dependencies in Next.js project or keep separate?
   - **Decision needed by:** Phase 2 start

2. **Overall Score Calculation:**
   - How should we weight Schema Audit vs. Core Web Vitals in overall score?
   - Should "Coming Soon" tools affect the score or be excluded?
   - **Decision needed by:** Phase 3 start

3. **Client Onboarding:**
   - Should we provide a CLI tool to add new clients automatically?
   - Or is manual .env editing acceptable for MVP?
   - **Decision needed by:** Phase 4 start

### Decisions Needed

4. **Landing Page Content:**
   - Should `/` have actual functionality or just explain the tool?
   - Should we allow public URL input or restrict to configured clients only?
   - **Decision needed by:** Phase 1 start

5. **Card Details Expansion:**
   - Should cards be expandable to show full details?
   - Or link to separate detail pages?
   - Or always show full details?
   - **Decision needed by:** Phase 1 during design

6. **Error Handling UX:**
   - When a Python script fails, show generic error or specific technical details?
   - Should we allow manual retry or auto-retry?
   - **Decision needed by:** Phase 2

### Items Requiring Further Research

7. **Future SSL/HTTPS Tool Integration:**
   - What data format will the SSL checker output?
   - What metrics should be displayed in the card?
   - **Research needed:** Before adding SSL tool

8. **Additional 24 "Coming Soon" Tools:**
   - What are the planned tools?
   - Which should be prioritized after MVP?
   - **Research needed:** Post-MVP planning

---

## Appendix A: SEO It Is Analysis

### Key Features Observed
1. **Visual Hierarchy:**
   - Large hero section with prominent URL input
   - Clear score display (e.g., "Score: 92")
   - Cards grouped visually by severity

2. **Card Design:**
   - Icon + Title combination
   - Brief description (1-2 sentences)
   - Status badge (color-coded)
   - Expandable details (click to see more)

3. **Information Architecture:**
   - 27+ individual checks organized logically
   - Critical issues appear first
   - Export options prominently displayed

4. **Color Scheme:**
   - Clean, modern palette
   - Green/Yellow/Red for status indicators
   - Lots of white space
   - Dark mode option available

5. **User Flow:**
   - Paste URL → Instant analysis → Results display
   - Export options always visible
   - Share functionality available

### What We'll Replicate
- Card-based layout with status badges
- Similar color coding for issue severity
- Clean, modern design aesthetic
- Export/download functionality
- Overall score display

### What We'll Customize
- Client-specific URLs instead of open URL input
- 3 active tools + 24 coming soon (vs. all active)
- "Run Analysis" button when no results exist
- IntelliAgent branding and styling

---

## Appendix B: Example Data Structures

### Example Schema Audit JSON Output
```json
{
  "summary": {
    "total_pages": 47,
    "pages_with_schema": 35,
    "pages_without_schema": 12,
    "total_schema_types": 58,
    "errors": 2
  },
  "schema_types_found": [
    "Organization",
    "WebSite",
    "Article",
    "BreadcrumbList",
    "Person"
  ],
  "pages": [
    {
      "url": "https://example.com/",
      "schema_types": ["Organization", "WebSite"],
      "schema_count": 2,
      "suggestions": ["Consider adding FAQPage schema for homepage"],
      "error": null
    },
    {
      "url": "https://example.com/blog/post-1",
      "schema_types": ["Article", "BreadcrumbList"],
      "schema_count": 2,
      "suggestions": [],
      "error": null
    }
  ],
  "timestamp": "2026-01-19T10:30:00Z"
}
```

### Example Core Web Vitals JSON Output
```json
{
  "url": "https://example.com",
  "strategy": "mobile",
  "performance_score": 85,
  "metrics": {
    "lcp": {
      "value": 2.3,
      "unit": "s",
      "rating": "good"
    },
    "fid": {
      "value": 45,
      "unit": "ms",
      "rating": "good"
    },
    "cls": {
      "value": 0.08,
      "rating": "good"
    }
  },
  "recommendations": [
    {
      "title": "Enable text compression",
      "priority": "high",
      "impact": "Potential savings of 125 KiB"
    },
    {
      "title": "Properly size images",
      "priority": "medium",
      "impact": "Potential savings of 89 KiB"
    }
  ],
  "wordpress_detected": true,
  "timestamp": "2026-01-19T10:30:00Z"
}
```

### Example Overall Dashboard Response
```json
{
  "client": {
    "name": "Client A Company",
    "slug": "client-a",
    "url": "https://clienta.com"
  },
  "overallScore": 87,
  "cards": [
    {
      "id": "schema-audit",
      "title": "Schema Markup",
      "description": "Structured data implementation across your site",
      "status": "warning",
      "icon": "Code",
      "metrics": [
        { "label": "Pages with Schema", "value": "35/47" },
        { "label": "Schema Types", "value": 5 }
      ],
      "details": "12 pages missing schema markup"
    },
    {
      "id": "core-web-vitals",
      "title": "Core Web Vitals",
      "description": "Page performance and user experience metrics",
      "status": "good",
      "icon": "Gauge",
      "metrics": [
        { "label": "Performance Score", "value": "85/100" },
        { "label": "LCP", "value": "2.3s" },
        { "label": "CLS", "value": "0.08" }
      ]
    },
    {
      "id": "ssl-https",
      "title": "SSL/HTTPS",
      "description": "Security and encryption configuration",
      "status": "coming-soon",
      "icon": "Lock"
    }
  ],
  "downloadLinks": [
    {
      "tool": "schema",
      "format": "csv",
      "url": "/api/download/client-a/schema/csv"
    },
    {
      "tool": "schema",
      "format": "json",
      "url": "/api/download/client-a/schema/json"
    },
    {
      "tool": "core-web-vitals",
      "format": "json",
      "url": "/api/download/client-a/core-web-vitals/json"
    },
    {
      "tool": "core-web-vitals",
      "format": "pdf",
      "url": "/api/download/client-a/core-web-vitals/pdf"
    }
  ],
  "lastUpdated": "2026-01-19T10:30:00Z"
}
```

---

## Appendix C: List of 27 Planned SEO Tools

Based on SEO It Is's 27+ checks, here are the tools we plan to implement:

### Currently Active (3)
1. **Schema Markup** - Structured data detection and validation
2. **Core Web Vitals** - Page performance metrics (LCP, FID, CLS)
3. **SSL/HTTPS** - Security certificate validation (coming next)

### Coming Soon (24)
4. Title Tag Analysis
5. Meta Description Analysis
6. H1 Structure Check
7. Heading Hierarchy (H1-H6)
8. Internal Links Analysis
9. External Links Analysis
10. Image Optimization (alt text, formats)
11. Page Speed Analysis
12. Mobile Responsiveness
13. Open Graph Tags
14. Twitter Cards
15. Canonical URL Check
16. Robots.txt Validation
17. Sitemap Detection
18. URL Structure Analysis
19. Content Analysis (word count, readability)
20. Accessibility Checks
21. Meta Robots Tags
22. Hreflang Tags
23. Favicon Detection
24. Lazy Loading Check
25. Doctype Validation
26. Character Encoding
27. Keywords in URL

---

## Next Steps

1. **Review this PRD** and confirm all requirements are accurate
2. **Answer open questions** to finalize design decisions
3. **Set up development environment** (Next.js project, Python scripts)
4. **Begin Phase 1** with Claude Code to create the initial UI structure

---

**End of PRD**
