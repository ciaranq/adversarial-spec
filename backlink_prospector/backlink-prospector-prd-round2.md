# PRD: Backlink Prospector - Scalable Keyword Discovery System

**Version:** 2.0
**Created:** 2025-01-19
**Updated:** 2025-01-19 (Round 2)
**Author:** Product Team
**Status:** 🟡 Under Review (Round 2)

---

## 1. Executive Summary

SEO professionals at agencies like Earned Media spend 20-30 hours per week manually identifying backlink opportunities across thousands of websites. Current tools—local scripts, browser extensions, or manual Google searches—cannot scale beyond a few hundred domains without IP blocking, data loss from interruptions, and fragmented results.

**Backlink Prospector** is a cloud-native system that automates large-scale keyword prospecting across 5,000-50,000 domains, delivering qualified backlink candidates in hours instead of days. By eliminating manual bottlenecks and IP blocking risks, it enables SEO teams to focus on high-value relationship building and content strategy rather than data collection.

---

## 2. Problem Statement

### The Current Situation

SEO consultants need to identify websites that mention client-related keywords but don't yet link back to the client's site. This is foundational for backlink outreach campaigns. The current approach involves:
1. Compiling a list of potentially relevant domains (from competitor analysis, industry directories, etc.)
2. Manually or semi-automatically crawling each domain to find keyword mentions
3. Filtering results to identify high-value targets for outreach

### Why This is Painful

For small campaigns (50-100 domains), consultants use local Python scripts or browser automation. But for serious campaigns (5,000+ domains), this breaks down completely:

**Time Loss:**
- Sequential processing from a laptop: 5,000 domains × 2 minutes/domain = 167 hours
- Reality: Jobs crash overnight, lose progress, must restart from scratch
- Consultants spend 60-70% of campaign time on data collection vs. 30% on strategy

**IP Blocking:**
- Office/home IPs get blacklisted after ~500 requests
- VPNs are slow and unreliable
- Blacklisting disrupts other business operations

**No Progress Tracking:**
- If the script crashes on domain 4,847 of 5,000, all progress is lost
- No way to pause Friday afternoon and resume Monday morning
- Results scattered across multiple CSV files from partial runs

### Who Experiences This

**Primary:** SEO strategists at digital marketing agencies managing 5-7 client campaigns simultaneously

**Secondary:** In-house SEO teams at SaaS companies running ongoing link building programs

### What Success Looks Like

Alex (our target persona) uploads a CSV of 5,000 domains Friday at 4pm, goes home, and has a clean, consolidated CSV of 800 qualified opportunities in her inbox Monday at 9am. She spends Monday building relationships, not parsing HTML.

---

## 3. Target User Persona

**Name:** Alex Chen
**Role:** Senior SEO Strategist at mid-sized digital marketing agency
**Age:** 32
**Location:** Sydney, Australia

**Background:**
Alex manages SEO for 5-7 B2B SaaS clients simultaneously. Her agency measures success by client organic traffic growth and retention rate. She has a marketing degree and taught herself Python/SQL to automate repetitive tasks, but she's not a software engineer—she doesn't want to manage infrastructure or debug Docker containers.

**Goals:**
- Find 50-100 high-quality backlink opportunities per client per month
- Spend 70% of time on strategy and relationship building, 30% on execution
- Prove ROI to clients with clear before/after traffic metrics

**Frustrations:**
> "I have a Python script that works great for 100 domains, but when I try to run 5,000 domains for a new client, it always times out or gets our office IP blocked. Then I have to explain to IT why Wikipedia blacklisted us."

> "Last Friday I kicked off a crawl before leaving. My laptop restarted over the weekend for an OS update. I lost 48 hours of work and had to start over Monday morning. I needed those results for a client meeting Tuesday."

> "I pay for ScrapingBee to avoid blocks, but I have no idea how much a job will cost until it's done. Last month I got a $600 bill because one client had way more JS-heavy sites than I expected."

**A Day in Alex's Life:**
- 9am: Check campaign dashboards, respond to client questions
- 10am: Outreach to 20 prospects identified last week (personalized emails)
- 12pm: Analyze competitor backlink profiles for new client
- 2pm: *Wants to start prospecting crawl but hesitates because it will monopolize her laptop for 8 hours*
- 3pm: Client call
- 4pm: Start building content partnerships for existing client
- 5pm: Check if crawl finished (it didn't, it's stuck on domain 847)

---

## 4. User Stories

### Epic 1: Job Initialization

**US-1.1: Upload Large Domain Lists**
- **As** Alex
- **I want to** upload a CSV with 5,000+ domains and start a job with one command
- **So that** I don't spend 30 minutes copy-pasting lists or formatting data
- **Acceptance Criteria:**
  - Accept CSV files up to 50,000 rows
  - Auto-detect and strip URL protocols/paths (e.g., `https://example.com/page` → `example.com`)
  - Auto-deduplicate domains (log: "Removed 127 duplicates, processing 4,873 unique domains")
  - Validate domain format (reject invalid entries with clear error: "Line 847: 'not-a-domain' is invalid")

**US-1.2: Define Target Keywords**
- **As** Alex
- **I want to** specify 10-100 keywords/phrases to search for
- **So that** I can find mentions of my client's brand, product names, and key topics
- **Acceptance Criteria:**
  - Accept plain text file with one keyword per line
  - Support single words ("Salesforce") and phrases ("CRM for small business")
  - Case-insensitive matching by default
  - Support up to 500 keywords (though typical use is 10-50)

**US-1.3: Control Cost vs Coverage Tradeoff**
- **As** Alex
- **I want to** choose how aggressively the system tries to access protected/JS-heavy sites
- **So that** I can balance my ScrapingBee budget against the risk of missing opportunities
- **Acceptance Criteria:**
  - Three modes: `free-only` (direct HTTP, no paid API), `premium-only` (all requests via ScrapingBee), `smart-hybrid` (try free, fallback to premium on failure)
  - Before job starts, show estimated cost range: "Estimated 2,000-8,000 ScrapingBee credits ($20-$80) based on hybrid mode"
  - Default to `smart-hybrid`

**US-1.4: Preview Before Running**
- **As** Alex
- **I want to** see a job summary before it starts processing
- **So that** I can catch mistakes (wrong keyword file, wrong domain list) before wasting time and credits
- **Acceptance Criteria:**
  - Show: "Job 'Acme Corp Q1' - 4,873 domains, 23 keywords, hybrid mode, estimated $45, ETA 6-8 hours"
  - Require explicit confirmation: "Type 'confirm' to start, or 'cancel' to abort"

### Epic 2: Job Execution & Reliability

**US-2.1: Fault Tolerance**
- **As** Alex
- **I want** individual domain failures to not crash the entire job
- **So that** I get results for 4,700 domains even if 300 fail (DNS errors, timeouts, etc.)
- **Acceptance Criteria:**
  - If a domain fails after 3 retries, mark it as "failed" and continue to next domain
  - At job completion, show: "4,573 succeeded, 300 failed (see error report)"
  - Generate a separate `failed_domains.csv` with failure reason for each

**US-2.2: Pause and Resume**
- **As** Alex
- **I want to** pause a running job and resume it hours or days later
- **So that** I can stop spending credits if I spot an issue, or spread the cost over multiple billing periods
- **Acceptance Criteria:**
  - `job pause <job_id>` command completes current batch (e.g., 100 domains) then stops
  - State persisted externally (survives system restart)
  - `job resume <job_id>` picks up exactly where it left off (no duplicate processing)
  - Show: "Paused at 2,400/5,000 domains (48%). Resume anytime with 'job resume abc123'"

**US-2.3: Progress Visibility**
- **As** Alex
- **I want to** check job status without SSH-ing into a server
- **So that** I can answer "Is it done yet?" from my client without technical overhead
- **Acceptance Criteria:**
  - `job status <job_id>` command shows:
    - Progress: "3,241/5,000 domains (65%)"
    - Status: "Running" / "Paused" / "Completed" / "Failed"
    - ETA: "~2.3 hours remaining"
    - Cost so far: "4,832 ScrapingBee credits used ($48.32)"
    - Last activity: "2 minutes ago"
  - Works whether job is running or paused

**US-2.4: Multi-Job Management**
- **As** Alex
- **I want to** run jobs for multiple clients without results getting mixed up
- **So that** I don't accidentally send Client A's prospect list to Client B
- **Acceptance Criteria:**
  - Each job has unique ID and user-provided name: `job create --name "Acme Corp Q1 2025"`
  - `job list` shows all jobs with status: `abc123 | Acme Corp Q1 | Completed | 5000/5000 | Jan 18`
  - Results stored separately per job (no chance of cross-contamination)

### Epic 3: Crawling Intelligence

**US-3.1: Adaptive Depth Based on Site Size**
- **As** Alex
- **I want** the system to crawl small sites fully but not waste time on massive sites
- **So that** I get complete coverage on niche blogs (50 pages) but don't spend 2 hours on enterprise sites (10,000 pages)
- **Acceptance Criteria:**
  - System attempts to detect site size (e.g., via sitemap.xml, robots.txt)
  - If site ≤ 500 pages: crawl all discoverable pages
  - If site > 500 pages: crawl homepage + top 50 pages (most linked-to, or user-configurable heuristic)
  - Threshold configurable per job

**US-3.2: Avoid IP Blocks**
- **As** Alex
- **I want** the system to respect rate limits and avoid triggering anti-bot defenses
- **So that** I don't get blacklisted or banned mid-job
- **Acceptance Criteria:**
  - Respect `robots.txt` directives
  - Rate limit: max 1 request per second per domain (even if processing 50 domains in parallel)
  - Rotate User-Agent headers
  - Honor `Retry-After` headers (if server says "wait 30 seconds", wait 30 seconds)

**US-3.3: Handle JavaScript-Heavy Sites**
- **As** Alex
- **I want** the system to render JavaScript when necessary
- **So that** I don't miss opportunities on modern React/Vue/Next.js sites where content loads dynamically
- **Acceptance Criteria:**
  - When using premium mode (ScrapingBee), enable JavaScript rendering
  - In hybrid mode, if initial request returns empty `<body>`, retry with JS rendering
  - Log which domains required JS rendering (helps Alex understand costs)

### Epic 4: Results & Analysis

**US-4.1: Consolidated Output**
- **As** Alex
- **I want** one clean CSV file with all results
- **So that** I don't manually merge outputs from 50 batches
- **Acceptance Criteria:**
  - Single `results.csv` with columns: `domain`, `url`, `keyword`, `frequency`, `context_snippet`, `crawl_method_used`, `crawl_timestamp`
  - Context snippet: 150 characters before + keyword + 150 after (configurable)
  - Results sorted by domain, then by keyword frequency (most mentions first)

**US-4.2: Multiple Export Formats**
- **As** Alex
- **I want** results in CSV (for Excel) and JSON (for scripts)
- **So that** I can analyze in Google Sheets or pipe into other tools
- **Acceptance Criteria:**
  - `job export <job_id> --format csv,json` generates both files
  - JSON structure nested by domain: `{"example.com": {"keywords": {"Salesforce": {"count": 5, "pages": [...]}}}}`
  - Files stored in cloud storage (not just locally) for remote access

**US-4.3: Cost Transparency**
- **As** Alex
- **I want** detailed cost breakdowns per job
- **So that** I can invoice clients accurately and budget future campaigns
- **Acceptance Criteria:**
  - Final report includes: "ScrapingBee credits used: 6,247 ($62.47)"
  - Breakdown: "Direct requests: 3,891 (free), ScrapingBee JS rendering: 432 ($43.20), ScrapingBee premium proxy: 1,924 ($19.24)"
  - Exportable cost report: `job export <job_id> --cost-report`

**US-4.4: Quality Scoring (Future Enhancement Noted)**
- **As** Alex
- **I want** results ranked by opportunity quality (domain authority, relevance, etc.)
- **So that** I prioritize high-value outreach targets first
- **Acceptance Criteria:**
  - *Out of scope for Phase 1 (noted as Phase 2 feature)*
  - Phase 1 exports raw results; Alex uses external tools (Ahrefs, Moz) to enrich

### Epic 5: Operational Safety

**US-5.1: Budget Caps**
- **As** Alex
- **I want to** set a hard limit on ScrapingBee spending per job
- **So that** I don't accidentally spend $500 when I budgeted $50
- **Acceptance Criteria:**
  - `job create --max-credits 5000` sets hard cap
  - When cap reached, job auto-pauses with alert: "Budget limit reached (5,000 credits). Job paused. Resume with higher limit or export partial results."
  - Default cap: 10,000 credits ($100)

**US-5.2: Failure Alerts**
- **As** Alex
- **I want to** know if a job fails catastrophically (not just individual domains)
- **So that** I don't wait 8 hours for results that will never come
- **Acceptance Criteria:**
  - If >50% of domains fail in first 100 processed, auto-pause with error: "High failure rate detected. Check connectivity or domain list quality."
  - If external service (ScrapingBee, Cloud Storage) is unreachable, pause and log clear error

---

## 5. Functional Requirements

### FR-1: Job Management

**FR-1.1:** System must accept domain lists (CSV, TXT, one domain per line) up to 50,000 entries

**FR-1.2:** System must accept keyword lists (TXT, one keyword/phrase per line) up to 500 entries

**FR-1.3:** System must validate and deduplicate domains before job execution begins

**FR-1.4:** System must assign a unique ID and user-provided name to each job

**FR-1.5:** System must persist job state (status, progress, configuration, results) in a **persistent, external data store** that survives system restarts/crashes

**FR-1.6:** System must support these job states: `pending`, `running`, `paused`, `completed`, `failed`

**FR-1.7:** System must allow pausing and resuming jobs without data loss or duplicate processing

### FR-2: Crawling & Keyword Detection

**FR-2.1:** System must crawl target domains to discover pages containing target keywords

**FR-2.2:** System must perform case-insensitive keyword matching with word boundaries (e.g., "CRM" matches "CRM software" but not "sCRaMble")

**FR-2.3:** For each match, system must capture:
- Domain name
- Full URL of page
- Keyword found
- Frequency (number of times keyword appears on page)
- Context snippet (configurable, default 150 chars before + after)
- Timestamp of crawl
- Crawl method used (direct, premium, JS-rendered)

**FR-2.4:** System must respect `robots.txt` directives for all domains

**FR-2.5:** System must support three crawl modes:
- **Free-only:** Direct HTTP requests (no paid API usage)
- **Premium-only:** All requests via third-party scraping service (e.g., ScrapingBee)
- **Smart-hybrid:** Try free first; fallback to premium if:
  - HTTP status 403, 429, 503
  - Timeout after 15 seconds
  - Empty response body (likely bot challenge)
  - Cloudflare/anti-bot challenge detected

**FR-2.6:** System must detect site size (via sitemap.xml or other heuristic) and adjust crawl depth:
- Small sites (≤500 pages): Crawl all discoverable pages
- Large sites (>500 pages): Crawl homepage + top N pages (configurable, default 50)

**FR-2.7:** System must handle JavaScript-heavy sites by using headless browser rendering when necessary (via premium service)

### FR-3: Reliability & Fault Tolerance

**FR-3.1:** System must process domains in batches (configurable size, default 100 domains per batch)

**FR-3.2:** System must checkpoint progress after each batch completion (persist to external storage)

**FR-3.3:** If an individual domain fails after 3 retry attempts, system must log the failure and continue processing remaining domains

**FR-3.4:** System must implement exponential backoff for transient errors (e.g., network timeouts)

**FR-3.5:** System must detect and handle external service failures:
- If ScrapingBee API is unreachable, pause job and alert user (don't silently fail)
- If cloud storage is unreachable, buffer results in memory and retry upload

**FR-3.6:** If more than 50% of first 100 domains fail, system must auto-pause and alert user to investigate

### FR-4: Scalability & Performance

**FR-4.1:** System architecture must support horizontal scaling—capable of processing multiple domains concurrently

**FR-4.2:** System must use a distributed task queue or job scheduler to enable parallel processing across multiple workers

**FR-4.3:** System must enforce per-domain rate limiting (max 1 request/second per domain) regardless of number of parallel workers

**FR-4.4:** System must be capable of processing 5,000 domains in under 8 hours (target: 625+ domains/hour)

### FR-5: Cost Management

**FR-5.1:** System must track API usage (e.g., ScrapingBee credits) per domain, per batch, and per job

**FR-5.2:** Before job starts, system must provide estimated cost range based on selected crawl mode and historical data

**FR-5.3:** System must support user-defined budget caps per job; auto-pause when cap is reached

**FR-5.4:** System must generate detailed cost reports showing breakdown by crawl method (direct vs premium vs JS rendering)

### FR-6: Output & Export

**FR-6.1:** System must export results in CSV and JSON formats

**FR-6.2:** CSV structure: `domain,url,keyword,frequency,context,crawl_method,timestamp,http_status`

**FR-6.3:** JSON structure: Nested by domain, then by keyword (see Appendix A for schema)

**FR-6.4:** System must generate a summary report including:
- Total domains processed
- Success/failure counts
- Total matches found
- Credits consumed
- Estimated cost

**FR-6.5:** System must generate a separate error report (`failed_domains.csv`) listing failed domains with failure reasons

**FR-6.6:** Results and reports must be stored in persistent cloud storage (not just locally)

---

## 6. Non-Functional Requirements

### NFR-1: Scalability

**NFR-1.1:** System must support horizontal scaling—architecture cannot rely on single-instance processing

**NFR-1.2:** System must handle jobs up to 50,000 domains

**NFR-1.3:** Target throughput: 1,000+ domains per hour at scale (across all workers)

### NFR-2: Reliability

**NFR-2.1:** System availability: 99% uptime (excludes scheduled maintenance)

**NFR-2.2:** Data durability: 0% data loss on system crash/restart (job state persisted externally)

**NFR-2.3:** Individual domain failure rate: <5% for valid, accessible domains

**NFR-2.4:** Job resumption: 100% success rate (paused jobs always resumable)

### NFR-3: Performance

**NFR-3.1:** Job creation latency: <5 seconds to validate and create a job with 10,000 domains

**NFR-3.2:** Status check latency: <2 seconds to retrieve current job status

**NFR-3.3:** Export latency: <30 seconds to generate CSV/JSON for a 5,000-domain job

### NFR-4: Security

**NFR-4.1:** All API keys and credentials must be stored in secure environment variables or secrets manager (never hardcoded)

**NFR-4.2:** Database credentials must use least-privilege access (read/write only to required tables)

**NFR-4.3:** Exported files containing potentially sensitive data must not be publicly accessible (require authentication or signed URLs)

### NFR-5: Usability

**NFR-5.1:** Phase 1 interface: Command-line interface (CLI) with intuitive commands

**NFR-5.2:** All CLI commands must provide helpful error messages (e.g., "Domain list not found at path/to/domains.csv. Check file path.")

**NFR-5.3:** Documentation must include:
- Quick start guide (0 to first job in <10 minutes)
- CLI reference (all commands with examples)
- Troubleshooting guide (common errors and fixes)

**NFR-5.4:** Deployment to cloud platform must be achievable in <60 minutes following documentation (for users with basic cloud experience)

### NFR-6: Cost Efficiency

**NFR-6.1:** Cloud infrastructure must scale to zero when idle (no jobs running)

**NFR-6.2:** Target cost: <$0.10 per 1,000 domains for direct crawling (excluding ScrapingBee fees)

**NFR-6.3:** System must minimize waste: don't re-crawl domains that recently succeeded (optional caching layer)

---

## 7. Success Metrics

### Business Outcomes

**BM-1: Time Saved**
- **Metric:** Average time to generate 500 qualified prospects
- **Baseline:** 16 hours (manual process)
- **Target:** <3 hours (80% reduction)
- **Measurement:** Track job duration from creation to completed export

**BM-2: Campaign Capacity**
- **Metric:** Number of concurrent client campaigns Alex can manage
- **Baseline:** 3-4 campaigns/month (time-limited by manual prospecting)
- **Target:** 7-8 campaigns/month
- **Measurement:** Survey Earned Media team after 1 month

**BM-3: Cost per Opportunity**
- **Metric:** Fully-loaded cost (infrastructure + APIs) per qualified prospect identified
- **Target:** <$0.50 per prospect
- **Measurement:** Total monthly spend / total prospects identified across all jobs

### System Performance

**PM-1: Throughput**
- **Metric:** Domains processed per hour (system-wide)
- **Target:** 1,000+ domains/hour at scale
- **Measurement:** Log processing rate per batch, aggregate

**PM-2: Completion Rate**
- **Metric:** Percentage of jobs that complete successfully (not paused/failed)
- **Target:** >95%
- **Measurement:** `completed_jobs / total_jobs` from database

**PM-3: Domain Success Rate**
- **Metric:** Percentage of domains successfully crawled (within completed jobs)
- **Target:** >90% for valid, accessible domains
- **Measurement:** `(successful_domains / total_domains) * 100`

**PM-4: Resumption Success**
- **Metric:** Percentage of paused jobs that resume without errors
- **Target:** 100%
- **Measurement:** Track resume attempts vs. successful resumes

### Quality Metrics

**QM-1: Keyword Matching Accuracy**
- **Metric:** False positive rate (keywords reported but not actually on page)
- **Target:** <1%
- **Measurement:** Manual audit of 100 random results per month

**QM-2: Data Integrity**
- **Metric:** Duplicate entries in results (same domain+URL+keyword appears multiple times)
- **Target:** 0%
- **Measurement:** Automated deduplication check on all exports

---

## 8. Scope & Phasing

### Phase 1: Core CLI Tool (In Scope)

**Goal:** Functional CLI tool deployed to cloud, usable by Earned Media team

**Features:**
- ✅ CLI-based job management (create, run, pause, resume, status, export)
- ✅ CSV/TXT file inputs (domains, keywords)
- ✅ Three crawl modes (free, premium, hybrid)
- ✅ Persistent job state (external database/storage)
- ✅ Batch processing with checkpoints
- ✅ ScrapingBee integration with cost tracking
- ✅ CSV/JSON exports to cloud storage
- ✅ Basic observability (logs, error reports)

**Success Criteria:**
- Earned Media team successfully runs 5 jobs in first week
- At least one job processes 5,000+ domains without manual intervention
- Team reports >50% time savings vs. previous method

### Phase 2: Web Dashboard (Future)

**Out of Scope for Initial Launch:**
- Web-based UI for job management
- Real-time progress visualization
- User authentication and multi-user support
- Scheduled/recurring jobs
- Email/Slack notifications
- Integration with Ahrefs/Moz for domain authority scoring

**Rationale:** Phase 1 validates core functionality with internal users. Phase 2 adds UX polish for broader rollout.

### Phase 3: Advanced Analytics (Future)

**Out of Scope for Initial Launch:**
- Link analysis (check if keyword is already a link, analyze anchor text)
- Sentiment analysis of keyword context
- Competitor comparison (benchmark client mentions vs. competitors)
- Historical trending (track keyword mentions over time)

---

## 9. Key Assumptions

**A-1:** Earned Media team has access to a cloud provider account (GCP or AWS) with billing enabled

**A-2:** ScrapingBee (or equivalent service) provides sufficient API capacity for our volume (10K-50K requests/day)

**A-3:** Target domains are publicly accessible (not behind authentication)

**A-4:** Majority of target domains do not aggressively block well-behaved crawlers (respect robots.txt, reasonable rate limits)

**A-5:** Users are comfortable with command-line interfaces (no GUI required for Phase 1)

---

## 10. Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **Widespread IP Blocking** | High - Job fails before completion | Medium | Primary: Use ScrapingBee for protected sites. Secondary: Aggressive rate limiting (1 req/sec/domain) and User-Agent rotation for direct crawls. Fallback: Integrate residential proxy pool if needed. |
| **ScrapingBee Budget Overrun** | High - Unexpected $500+ bill | Medium | Mandatory: Cost estimation before job starts. Hard budget caps per job (default $100). Real-time credit tracking with alerts at 50%, 80%, 100% of budget. |
| **Cloud Infrastructure Costs** | Medium - Monthly bill exceeds $200 | Low | Design for scale-to-zero when idle. Use serverless compute (Cloud Run, Lambda). Set billing alerts at $150/month. Monitor per-job costs; optimize inefficient jobs. |
| **External Service Downtime** | Medium - ScrapingBee/Cloud SQL unavailable | Low | Graceful degradation: If ScrapingBee down, pause job and alert user (don't silently fail all domains). Retry logic with exponential backoff for transient errors. |
| **Inaccurate Site Size Estimation** | Low - Waste time crawling irrelevant pages | Medium | Start with conservative heuristics (sitemap.xml primary source). Allow per-job override of crawl depth. Log actual pages crawled per domain to tune heuristics. |
| **Memory Overflow on Large Sites** | Medium - Worker crashes mid-domain | Low | Implement strict per-domain limits: max 500 pages, max 10MB HTML per page. If limits exceeded, mark as "partially crawled" and continue. |
| **False Keyword Matches** | Low - Irrelevant results frustrate user | Low | Use word-boundary matching (not substring). Capture context snippets so users can manually verify. Log match count vs. page count (if keyword appears 200 times on one page, likely spam/footer). |
| **Low Adoption (Too Complex)** | High - Team doesn't use tool | Low | Invest in documentation: 5-minute quickstart video. 1-hour hands-on training with Earned Media team. Collect feedback weekly for first month. |

---

## 11. Dependencies

### Internal Dependencies

**D-1:** Earned Media team availability for requirements validation and user acceptance testing (est. 5 hours over 2 weeks)

**D-2:** Cloud platform admin access for initial deployment (GCP project with Cloud Run, Cloud SQL, Cloud Storage enabled)

### External Dependencies

**D-3:** ScrapingBee API account with minimum $100/month subscription (or equivalent service)

**D-4:** Stable internet connectivity for cloud deployment (one-time setup, not ongoing)

---

## 12. Open Questions

**Q-1:** Should we support other scraping services (Bright Data, Oxylabs) in addition to ScrapingBee, or standardize on one provider?
- **Decision needed by:** Week 1 (affects architecture)
- **Recommendation:** Start with ScrapingBee only (most popular, good documentation). Design abstraction layer to add more providers in Phase 2.

**Q-2:** What's the data retention policy? How long do we keep job results and crawled content?
- **Decision needed by:** Week 1 (affects storage costs and legal compliance)
- **Recommendation:** Keep results for 90 days, then auto-delete. Users can export to their own storage if needed longer. Logs retained for 30 days.

**Q-3:** Should we cache successful crawls to avoid re-crawling the same domain within X days?
- **Decision needed by:** Week 2 (performance optimization)
- **Recommendation:** Not for Phase 1 (adds complexity). Evaluate in Phase 2 if users report frequent re-crawls of same domains.

**Q-4:** What happens if a user starts a job, forgets about it, and it runs for 72 hours costing $500?
- **Decision needed by:** Week 1 (cost protection)
- **Recommendation:** Implement global timeout (default 48 hours) + hard budget cap (default $100). Jobs auto-pause at timeout/budget and require manual resume.

---

## 13. Compliance & Legal Considerations

**L-1: Web Scraping Legality**
- **Requirement:** System must respect `robots.txt` and website Terms of Service
- **Rationale:** Avoid legal exposure from aggressive/unauthorized crawling
- **Implementation:** Parse and honor robots.txt before crawling any domain. Do not provide "bypass robots.txt" option.

**L-2: Data Retention**
- **Requirement:** Crawled content (HTML, text) must not be stored longer than necessary for analysis
- **Rationale:** Minimize copyright and privacy risk
- **Implementation:** Extract keyword matches and context snippets; discard full HTML immediately. Do not build a persistent crawl archive.

**L-3: Privacy (GDPR/CCPA)**
- **Requirement:** If crawled pages contain PII (unlikely but possible), do not store it
- **Rationale:** Compliance with data protection regulations
- **Implementation:** System only extracts keyword matches and surrounding text (max 300 chars). No personal data fields parsed or stored. If user discovers PII in results, provide data deletion endpoint.

**L-4: ScrapingBee Terms of Service**
- **Requirement:** Verify that our use case complies with ScrapingBee's acceptable use policy
- **Rationale:** Avoid account suspension
- **Implementation:** Review ScrapingBee ToS during Week 1. Ensure we're not violating any prohibited use cases (e.g., scraping social media profiles, bypassing paywalls).

---

## 14. Out of Scope (Explicitly Not Doing)

**OS-1:** Real-time crawling (jobs must be batch-oriented, not live monitoring)

**OS-2:** Content extraction beyond keyword matching (e.g., extracting contact emails, phone numbers)

**OS-3:** Automated outreach (sending emails to prospects)

**OS-4:** Integration with CRM systems (Salesforce, HubSpot)

**OS-5:** Multi-tenancy or user authentication (Phase 1 is single-user CLI tool)

**OS-6:** Mobile app or browser extension

**OS-7:** Competitor analysis or domain authority scoring (use external tools like Ahrefs for this)

---

## Appendix A: Example JSON Export Schema

```json
{
  "job_id": "abc123",
  "job_name": "Acme Corp Q1 2025",
  "created_at": "2025-01-19T16:00:00Z",
  "completed_at": "2025-01-20T02:15:00Z",
  "total_domains": 5000,
  "processed_domains": 4987,
  "failed_domains": 13,
  "total_matches": 1247,
  "scrapingbee_credits_used": 6832,
  "estimated_cost_usd": 68.32,
  "results": [
    {
      "domain": "example.com",
      "matches": [
        {
          "keyword": "CRM software",
          "pages": [
            {
              "url": "https://example.com/blog/best-crm-tools",
              "frequency": 7,
              "context": "...Looking for the best CRM software for your small business? We compared 15 tools...",
              "crawl_method": "direct",
              "crawled_at": "2025-01-19T16:15:32Z",
              "http_status": 200
            }
          ]
        }
      ]
    }
  ],
  "failed": [
    {
      "domain": "example-broken.com",
      "error": "DNS resolution failed after 3 retries",
      "attempted_at": "2025-01-19T18:42:10Z"
    }
  ]
}
```

---

## Appendix B: CLI Command Reference (Draft)

```bash
# Create a new job
backlink-prospector job create \
  --name "Acme Corp Q1" \
  --domains domains.csv \
  --keywords keywords.txt \
  --mode hybrid \
  --max-credits 5000

# Start processing
backlink-prospector job run <job_id>

# Check status
backlink-prospector job status <job_id>

# Pause a running job
backlink-prospector job pause <job_id>

# Resume a paused job
backlink-prospector job resume <job_id>

# List all jobs
backlink-prospector job list

# Export results
backlink-prospector job export <job_id> --format csv,json

# View cost report
backlink-prospector job cost-report <job_id>

# View failed domains
backlink-prospector job errors <job_id>
```

---

## Appendix C: Glossary

| Term | Definition |
|------|------------|
| **Backlink** | A hyperlink from one website to another. A key factor in SEO rankings. |
| **Anchor Text** | The clickable text in a hyperlink. |
| **Prospecting** | The process of identifying websites that mention relevant keywords but don't yet link to your site. |
| **Qualified Prospect** | A domain where keyword mentions suggest a good backlink opportunity (high relevance, good authority). |
| **Adaptive Crawling** | Adjusting crawl depth based on site size (full crawl for small sites, selective for large sites). |
| **Hybrid Mode** | Crawl strategy that tries free direct requests first, falls back to premium proxy service on failure. |
| **Batch** | A subset of domains processed together (e.g., 100 domains). Progress checkpointed after each batch. |
| **Job** | A complete prospecting task: one domain list, one keyword list, processed to completion. |
| **Worker** | A compute instance (container, VM, serverless function) that processes domains in parallel. |
| **Fault Tolerance** | System's ability to continue operating even when individual components (domains, workers) fail. |
| **Horizontal Scaling** | Adding more workers to process domains in parallel (vs. vertical scaling = bigger/faster workers). |

---

**END OF PRD**
