# PRD: Backlink Prospector - Scalable Keyword Discovery System

**Version:** 4.0
**Created:** 2025-01-19
**Updated:** 2025-01-19 (Round 4 - Final Consensus)
**Author:** Product Team
**Status:** ✅ Ready for Engineering Review

---

## 1. Executive Summary

SEO professionals at agencies like Earned Media spend 20-30 hours per week manually identifying backlink opportunities across thousands of websites. Current tools—local scripts, browser extensions, or manual Google searches—cannot scale beyond a few hundred domains without IP blocking, data loss from interruptions, and fragmented results.

**Backlink Prospector** is a cloud-native, distributed system that automates large-scale keyword prospecting across 5,000-50,000 domains, delivering qualified backlink candidates in hours instead of days. By eliminating manual bottlenecks and IP blocking risks, it enables SEO teams to focus on high-value relationship building and content strategy rather than data collection.

**Key Design Principles:**
- **Distributed Architecture**: Asynchronous task distribution enables horizontal scaling from 1 to hundreds of workers
- **Fault-tolerant**: Individual failures don't crash the system
- **Cost-controlled**: Hard budget caps prevent surprises
- **Scalable**: Process 5,000+ domains per hour without manual intervention
- **Observable**: Clear visibility into what's happening and why things fail

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

Alex (our target persona) uploads a CSV of 5,000 domains Friday at 4pm, goes home, and has a clean, consolidated CSV of 800 qualified opportunities waiting for her Monday at 9am. She spends Monday building relationships, not parsing HTML.

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

**US-1.1: One-Command Job Start**
- **As** Alex
- **I want to** start a job with a single command
- **So that** I don't waste time on multi-step initialization
- **Acceptance Criteria:**
  - Single command accepts domains, keywords, and starts processing: `job run --name "Acme Q1" --domains domains.csv --keywords keywords.txt`
  - Validates inputs synchronously (returns error immediately if files invalid)
  - Auto-deduplicates domains (log: "Removed 127 duplicates, processing 4,873 unique domains")
  - Assigns unique job ID and starts processing automatically
  - **Advanced option:** `--no-auto-start` flag creates job without starting (for review)

**US-1.2: Define Target Keywords**
- **As** Alex
- **I want to** specify 10-100 keywords/phrases to search for
- **So that** I can find mentions of my client's brand, product names, and key topics
- **Acceptance Criteria:**
  - Accept plain text file with one keyword per line
  - Support single words ("Salesforce") and phrases ("CRM for small business")
  - Case-insensitive matching by default
  - Support up to 500 keywords (though typical use is 10-50)
  - Show keyword count after loading: "Loaded 23 keywords from keywords.txt"

**US-1.3: Control Cost vs Coverage Tradeoff**
- **As** Alex
- **I want to** choose how aggressively the system tries to access protected/JS-heavy sites
- **So that** I can balance my ScrapingBee budget against the risk of missing opportunities
- **Acceptance Criteria:**
  - Three modes: `free-only` (direct HTTP, no paid API), `premium-only` (all requests via ScrapingBee), `smart-hybrid` (try free, fallback to premium)
  - Before job starts, show estimated cost range: "Estimated 2,000-8,000 ScrapingBee credits ($20-$80) based on hybrid mode and historical data"
  - Default to `smart-hybrid`
  - Flag: `--mode hybrid|free-only|premium-only`

**US-1.4: Budget Protection**
- **As** Alex
- **I want to** set a hard limit on ScrapingBee spending per job
- **So that** I don't accidentally spend $500 when I budgeted $50
- **Acceptance Criteria:**
  - Flag: `--max-credits 5000` sets hard cap
  - When cap reached, job auto-pauses with alert: "Budget limit reached (5,000 credits used). Job paused. Resume with higher limit or export partial results."
  - Default cap: 10,000 credits ($100)
  - **Budget check timing:** Checked before issuing new work to workers. In-flight work allowed to complete (may exceed cap by up to one batch worth of credits).

### Epic 2: Job Execution & Reliability

**US-2.1: Fault Tolerance**
- **As** Alex
- **I want** individual domain failures to not crash the entire job
- **So that** I get results for 4,700 domains even if 300 fail (DNS errors, timeouts, etc.)
- **Acceptance Criteria:**
  - If a domain fails after 3 retries, mark it as "failed" and continue to next domain
  - At job completion, show: "4,573 succeeded, 300 failed (see error report)"
  - Generate a separate `failed_domains.csv` with failure reason for each
  - Failed domains don't count against budget (no ScrapingBee credits charged for DNS errors, etc.)

**US-2.2: Pause and Resume**
- **As** Alex
- **I want to** pause a running job and resume it hours or days later
- **So that** I can stop spending credits if I spot an issue, or spread the cost over multiple billing periods
- **Acceptance Criteria:**
  - `job pause <job_id>` command stops issuing new work to workers
  - In-flight work completes (to avoid wasting credits on incomplete requests)
  - Job status shows "Pausing..." while in-flight work completes, then "Paused"
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
    - Status: "Running" / "Pausing" / "Paused" / "Completed" / "Failed"
    - ETA: "~2.3 hours remaining" (based on current throughput)
    - Cost so far: "4,832 ScrapingBee credits used ($48.32)"
    - Throughput: "Averaging 287 domains/hour over last 15 minutes"
    - Last activity: "2 minutes ago"
  - Works whether job is running or paused
  - **Performance:** Status query returns in <2 seconds (uses cached progress metrics, not real-time DB count)

**US-2.4: Multi-Job Management**
- **As** Alex
- **I want to** run jobs for multiple clients without results getting mixed up
- **So that** I don't accidentally send Client A's prospect list to Client B
- **Acceptance Criteria:**
  - Each job has unique ID and user-provided name
  - `job list` shows all jobs with status:
    ```
    abc123  Acme Corp Q1     Completed  5000/5000  203 matches  $62.47  Jan 18
    def456  Beta Inc Dec     Running    1247/3000   47 matches  $18.20  Jan 19
    ```
  - Results stored separately per job (no chance of cross-contamination)
  - Jobs can run concurrently (subject to global concurrency limits)

### Epic 3: Crawling Intelligence

**US-3.1: Adaptive Depth Based on Site Size**
- **As** Alex
- **I want** the system to crawl small sites fully but not waste time on massive sites
- **So that** I get complete coverage on niche blogs (50 pages) but don't spend 2 hours on enterprise sites (10,000 pages)
- **Acceptance Criteria:**
  - System attempts to detect site size (via sitemap.xml, robots.txt, or HTTP headers)
  - If site ≤ 500 pages: crawl all discoverable pages
  - If site > 500 pages: crawl homepage + top 50 pages (based on internal links, or homepage links)
  - Threshold configurable via flag: `--max-pages-per-domain 100`

**US-3.2: Avoid IP Blocks**
- **As** Alex
- **I want** the system to respect rate limits and avoid triggering anti-bot defenses
- **So that** I don't get blacklisted or banned mid-job
- **Acceptance Criteria:**
  - Respect `robots.txt` directives (fetch once per domain, cache for job duration)
  - Rate limit: max 1 request per second per domain (even if processing 50 domains in parallel)
  - Rotate User-Agent headers (3-5 common browsers)
  - Honor `Retry-After` headers (if server says "wait 30 seconds", wait 30 seconds)
  - Exponential backoff on retries: 1s, 2s, 4s before marking failed

**US-3.3: Handle JavaScript-Heavy Sites**
- **As** Alex
- **I want** the system to render JavaScript when necessary
- **So that** I don't miss opportunities on modern React/Vue/Next.js sites where content loads dynamically
- **Acceptance Criteria:**
  - When using `premium-only` mode, enable JavaScript rendering for all requests
  - In `hybrid` mode:
    - Initial request uses direct HTTP (no JS rendering)
    - If response has empty `<body>` or minimal text content, retry with ScrapingBee + JS rendering
    - **Fallback granularity:** Per-URL (if homepage succeeds direct but subpage fails, retry subpage with ScrapingBee)
  - Log which domains required JS rendering: "example.com: 3/47 pages required JS rendering"

### Epic 4: Results & Analysis

**US-4.1: Asynchronous Export Generation**
- **As** Alex
- **I want** to download my results without waiting for a synchronous file generation
- **So that** I can export large result sets (50,000 domains) without timeouts
- **Acceptance Criteria:**
  - `job export <job_id> --format csv` initiates background generation
  - Returns immediately: "Export started. Check status in ~2 minutes. Run 'job export-status <job_id>' to check progress."
  - When complete, provides download URL: "Export ready: https://storage.googleapis.com/.../results-abc123.csv (expires in 7 days)"
  - Export generation uses streaming writes (row-by-row from DB to cloud storage) to avoid memory exhaustion
  - **Performance:** Can generate 50,000-domain export without exceeding 1GB worker memory

**US-4.2: Multiple Export Formats**
- **As** Alex
- **I want** results in CSV (for Excel) and JSON (for scripts)
- **So that** I can analyze in Google Sheets or pipe into other tools
- **Acceptance Criteria:**
  - Supported formats: `csv`, `json`
  - CSV structure: `domain,url,keyword,frequency,context_snippet,crawl_method,timestamp,http_status`
  - JSON structure: Clean, domain-keyed dictionary (see Appendix A)
  - Files stored in cloud storage with 7-day expiration (user downloads to their own storage)

**US-4.3: Cost Transparency**
- **As** Alex
- **I want** detailed cost breakdowns per job
- **So that** I can invoice clients accurately and budget future campaigns
- **Acceptance Criteria:**
  - Job status and completion summary include:
    - "ScrapingBee credits used: 6,247 ($62.47)"
    - "Breakdown: Direct (free): 3,891 domains | ScrapingBee (standard): 1,924 domains | ScrapingBee (JS rendering): 432 domains"
  - Separate command: `job cost-report <job_id>` generates detailed CSV with per-domain costs
  - Cost report columns: `domain,urls_crawled,direct_requests,scrapingbee_requests,js_rendering_requests,total_credits,estimated_cost_usd`

**US-4.4: Error Visibility**
- **As** Alex
- **I want** to understand why specific domains failed
- **So that** I can manually investigate high-value targets that didn't work
- **Acceptance Criteria:**
  - Separate error report: `job errors <job_id>` shows failed domains
  - Error report columns: `domain,failure_reason,http_status,retry_count,last_attempt_timestamp`
  - Failure reasons are human-readable: "DNS resolution failed", "Timeout after 15s", "robots.txt disallowed", "HTTP 403 Forbidden"
  - Error report downloadable as CSV

### Epic 5: System Reliability

**US-5.1: Global Concurrency Control**
- **As a** system operator
- **I want** the system to respect account-level API limits
- **So that** multiple concurrent jobs don't breach ScrapingBee's rate limits and get the account banned
- **Acceptance Criteria:**
  - System maintains a global concurrency cap across all running jobs (e.g., max 500 concurrent requests to ScrapingBee system-wide)
  - If Job A is using 300 workers and Job B tries to start, Job B only gets 200 workers (until Job A finishes)
  - Global cap configurable via system config (not per-job)
  - If global cap is reached, new work is queued (not dropped)

**US-5.2: Data Lifecycle Management**
- **As a** system operator
- **I want** old job data to be automatically cleaned up
- **So that** the database doesn't grow unbounded and queries stay fast
- **Acceptance Criteria:**
  - Job results and crawl data automatically soft-deleted after 90 days
  - User warned when exporting: "This job will be auto-deleted on [date]. Download your results now."
  - Deleted jobs move to "archived" state (metadata retained, results purged)
  - Archived jobs show in `job list --include-archived` with note: "(Results deleted)"

**US-5.3: Observability**
- **As a** system operator
- **I want** detailed logs and metrics for debugging failures
- **So that** I can diagnose issues when jobs fail or slow down
- **Acceptance Criteria:**
  - All external API errors logged with full context: "ScrapingBee error for example.com/page: HTTP 429 Rate Limit Exceeded (job: abc123, worker: w-42)"
  - Throughput metrics tracked in real-time: domains/minute, requests/second, error rate percentage
  - Failed jobs log root cause: "Job failed: Database connection timeout after 30s (connection pool exhausted)"
  - Slow jobs automatically flagged: "Warning: Job abc123 throughput dropped 80% in last 10 minutes. Current: 45 domains/hour (expected: 250)"

---

## 5. Functional Requirements

### FR-1: Job Management

**FR-1.1:** System must accept domain lists (CSV, TXT, one domain per line) up to 50,000 entries

**FR-1.2:** System must accept keyword lists (TXT, one keyword/phrase per line) up to 500 entries

**FR-1.3:** System must validate and deduplicate domains synchronously before job starts (return error immediately if invalid)

**FR-1.4:** System must assign a unique ID (e.g., UUID) and user-provided name to each job

**FR-1.5:** System must persist job state (status, progress, configuration, results) in a persistent data store that survives system restarts/crashes. The data store must not reside on ephemeral container storage.

**FR-1.6:** System must support these job states: `pending`, `running`, `pausing`, `paused`, `completed`, `failed`, `archived`

**FR-1.7:** System must allow pausing and resuming jobs without data loss or duplicate processing

**FR-1.8:** System must enforce a 90-day retention policy: Job results automatically soft-deleted after 90 days from completion

**FR-1.9:** System must support concurrent jobs (multiple jobs can run simultaneously, subject to global concurrency limits)

### FR-2: Crawling & Keyword Detection

**FR-2.1:** System must crawl target domains to discover pages containing target keywords

**FR-2.2:** System must perform case-insensitive keyword matching with word boundaries (e.g., "CRM" matches "CRM software" but not "sCRaMble")

**FR-2.3:** For each match, system must capture:
- Domain name
- Full URL of page
- Keyword found
- Frequency (number of occurrences on page)
- Context snippet (configurable, default 150 chars before + after)
- Timestamp of crawl (ISO 8601 format)
- Crawl method used (direct, scrapingbee-standard, scrapingbee-js)
- HTTP status code

**FR-2.4:** System must respect `robots.txt` directives for all domains. If robots.txt disallows crawling, log as failure: "Robots.txt disallowed"

**FR-2.5:** System must support three crawl modes:
- `free-only`: Direct HTTP requests only (no paid API usage)
- `premium-only`: All requests via ScrapingBee (with JS rendering if needed)
- `smart-hybrid`: Try direct first; fallback to ScrapingBee per-URL on failure (HTTP 403, 429, 503, timeout, empty body)

**FR-2.6:** **Hybrid fallback granularity:** Fallback decisions made per-URL, not per-domain. If homepage succeeds with direct crawl but a subpage fails, only the subpage is retried with ScrapingBee.

**FR-2.7:** System must detect site size (via sitemap.xml, robots.txt, or HTTP headers) and adjust crawl depth:
- Small sites (≤ configurable threshold, default 500 pages): Crawl all discoverable pages
- Large sites (> threshold): Crawl homepage + top N pages (configurable, default 50)

**FR-2.8:** System must handle JavaScript-heavy sites:
- In `premium-only` mode: Enable JS rendering for all requests
- In `hybrid` mode: Retry with JS rendering if initial response has empty/minimal content

### FR-3: Distributed Task Processing

**FR-3.1: Asynchronous Task Distribution Architecture**

System must implement a distributed, asynchronous task processing architecture to enable horizontal scaling and fault tolerance. This architecture must support the following capabilities:

- **Task Decomposition:** When a job starts, the system must break the domain list into individual work units (tasks) that can be processed independently
- **Task Queuing:** Work units must be queued in a persistent, external task queue (not in-memory) that survives system restarts
- **Worker Independence:** Multiple stateless workers must be able to pull tasks from the queue and process them concurrently without coordinating with each other
- **Exactly-Once Processing:** The system must ensure that each task (domain + keywords) is processed successfully exactly once, even if workers crash mid-processing
- **Task Retry Mechanism:** If a task fails (worker crash, timeout), it must automatically be retried by a different worker (up to 3 attempts)
- **Poison Message Handling:** Tasks that fail repeatedly (>3 attempts) must be moved to a separate error queue for investigation, not retried indefinitely

**FR-3.2: Checkpoint Persistence**

System must persist progress checkpoints to external storage (not ephemeral container storage) at regular intervals:
- After every N completed tasks (configurable, default 100)
- When job is paused by user
- Before system shutdown (if graceful shutdown is possible)

Checkpoints must include:
- Job ID
- Total tasks queued
- Tasks completed successfully
- Tasks failed
- Last processed timestamp
- Current job state

**FR-3.3: Worker Fault Tolerance**

System must handle worker failures gracefully:
- If a worker crashes while processing a task, the task must be returned to the queue after a visibility timeout (e.g., 5 minutes)
- System must detect stuck workers (no heartbeat for >5 minutes) and reclaim their tasks
- New workers must be able to join the pool dynamically without restarting existing workers

### FR-4: Scalability & Concurrency

**FR-4.1:** System architecture must support horizontal scaling—capable of scaling from 1 worker to 500+ workers based on queue depth and available budget

**FR-4.2: Distributed Rate Limiting**

System must enforce per-domain rate limiting (max 1 request per second per unique domain) across all distributed workers, regardless of which physical servers they run on.

Implementation requirements:
- Rate limit enforcement must be coordinated across all workers (not local to each worker)
- System must prevent race conditions where multiple workers simultaneously request the same domain
- Rate limit state must be shared via a distributed coordination mechanism (e.g., distributed cache, centralized rate limiter)

**FR-4.3:** **System must enforce a global concurrency cap** across all running jobs to prevent exceeding ScrapingBee account-level limits. The global cap must be:
- Configurable via system config file (not hardcoded)
- Dynamically allocated across active jobs
- Example: Global cap = 500 workers. If Job A uses 300, Job B can use up to 200.
- Enforced before issuing new tasks to workers (not by killing in-flight workers)

**FR-4.4:** **Backpressure handling:** If database write throughput cannot keep up with crawl throughput, workers must:
- Slow down task processing rate (introduce delays between tasks)
- Buffer results in memory temporarily (up to configurable limit, default 100 results per worker)
- If buffer exceeds limit and DB still slow, pause job and alert operator

**FR-4.5: Connection Pooling**

System must manage database connections efficiently to prevent connection exhaustion:
- Workers must reuse database connections across multiple tasks (not open/close per task)
- Total number of active database connections must not exceed 80% of database connection limit
- System must monitor connection pool usage and alert if approaching limit

### FR-5: Cost Management

**FR-5.1:** System must track ScrapingBee API usage (credits consumed) per:
- Individual domain
- Job total
- System-wide (across all jobs)

**FR-5.2:** Before job starts, system must provide estimated cost range based on:
- Selected crawl mode (free/premium/hybrid)
- Historical data (if available): "Similar jobs used 5,000-8,000 credits"
- Display as: "Estimated cost: $50-$80 (5,000-8,000 credits)"

**FR-5.3:** System must support user-defined budget caps per job:
- Flag: `--max-credits N`
- When budget reached, pause job (stop issuing new work; allow in-flight work to complete)
- Alert user: "Budget limit reached. Job paused. Resume with higher limit or export partial results."

**FR-5.4:** System must generate detailed cost reports:
- Per-job summary: Total credits, breakdown by method (direct/standard/JS), estimated cost
- Per-domain detail (optional): CSV with credits used per domain

### FR-6: Output & Export

**FR-6.1:** System must export results in CSV and JSON formats

**FR-6.2:** Export generation must be asynchronous and use streaming writes to avoid memory exhaustion:
- Command `job export <id>` initiates background task
- Returns immediately: "Export started. Check status with 'job export-status <id>'"
- Streams results row-by-row from database to cloud storage (never load full dataset into memory)
- When complete, provides download URL with 7-day expiration

**FR-6.3:** CSV structure: `domain,url,keyword,frequency,context_snippet,crawl_method,timestamp,http_status`

**FR-6.4:** JSON structure: Domain-keyed dictionary with nested keywords (see Appendix A)

**FR-6.5:** System must generate these reports:
- **Results export**: Successful matches (CSV or JSON)
- **Error report**: Failed domains with failure reasons (CSV)
- **Cost report**: Per-domain credit usage (CSV)

**FR-6.6:** Exported files must be stored in cloud storage (e.g., S3, GCS) with:
- 7-day retention (auto-delete after 7 days)
- Signed URLs for secure download (no public access)

### FR-7: Observability & Logging

**FR-7.1:** System must log all external API errors with full context:
- Timestamp (ISO 8601)
- Job ID and worker ID
- Domain and URL being processed
- Error type and message
- HTTP status code (if applicable)
- Example: `2025-01-19T14:23:45Z [ERROR] Job:abc123 Worker:w-42 URL:example.com/page ScrapingBee: HTTP 429 Rate Limit Exceeded`

**FR-7.2:** System must track and expose real-time throughput metrics:
- Domains processed per minute (per job and system-wide)
- Requests per second to ScrapingBee
- Error rate percentage (failed requests / total requests)
- Database write rate (results written per minute)
- Queue depth (pending tasks in queue)

**FR-7.3:** System must detect and alert on anomalies:
- If job throughput drops >50% in 10 minutes: "Warning: Job abc123 throughput dropped from 250 to 45 domains/hour"
- If error rate exceeds 20% in 5 minutes: "Alert: High error rate detected (23% failures). Check API status."
- If database writes are slow (>5s per write): "Warning: Database write latency high (8.2s average)"
- If queue depth grows unbounded: "Alert: Queue depth growing faster than processing rate (12,000 pending tasks)"

**FR-7.4:** Failed jobs must log root cause in human-readable format:
- "Job failed: Database connection timeout after 30s (connection pool exhausted)"
- "Job failed: ScrapingBee API returned 503 Service Unavailable for 10 consecutive requests"
- "Job failed: Task queue unreachable (network connectivity issue)"

---

## 6. Non-Functional Requirements

### NFR-1: Scalability

**NFR-1.1:** System must be designed to meet throughput and job size targets without requiring manual intervention or configuration changes for typical workloads

**NFR-1.2:** System must handle jobs up to 50,000 domains

**NFR-1.3:** **Target throughput: 5,000+ domains per hour** (measured across all concurrent jobs running at steady state)

**NFR-1.4:** **Architecture capacity: System architecture must be capable of scaling to 20,000+ domains per hour** when provided sufficient infrastructure budget and API credits. Phase 1 deployment will target 5,000 domains/hour; the architecture must not have bottlenecks that prevent future scaling to 20,000+.

**NFR-1.5:** System must support horizontal scaling: Architecture must allow adding more workers to increase throughput linearly (not limited to single-machine performance)

**NFR-1.6: Database Performance at Scale**

System must maintain acceptable query performance as data volume grows:
- Database schema must support efficient querying even with 100M+ result rows (across all jobs over 90 days)
- Export generation queries must complete in <5 minutes for 50,000-domain jobs
- Job status queries must return in <2 seconds regardless of result count
- **Recommended approach:** Use database partitioning (by job ID or date) to isolate large datasets, though specific implementation is at engineering's discretion

### NFR-2: Reliability

**NFR-2.1:** System availability: 99% uptime (excludes scheduled maintenance)

**NFR-2.2:** Data durability: 0% data loss on system crash/restart (job state and results persisted externally)

**NFR-2.3:** Individual domain failure rate: <5% for valid, accessible domains (excludes intentionally blocked/unavailable domains)

**NFR-2.4:** Job resumption: 100% success rate (paused jobs always resumable without data loss or duplicate processing)

### NFR-3: Performance

**NFR-3.1:** Job creation latency: <5 seconds to validate and start a job with 10,000 domains

**NFR-3.2:** Status check latency: <2 seconds to retrieve current job status (uses cached progress metrics, updated every 30-60 seconds)

**NFR-3.3:** Target job completion time: Process 5,000 domains in under 1.5 hours (avg 3,333 domains/hour at scale)

**NFR-3.4:** Export generation: Support generating exports for 50,000-domain jobs without exceeding 1GB worker memory (via streaming writes)

**NFR-3.5:** Cold start: From a "zero workers" state, system must ramp up to target processing capacity (5,000 domains/hour) within 5 minutes of job start

### NFR-4: Security

**NFR-4.1:** All API keys and credentials must be stored in a secure secrets manager or environment variables (never hardcoded in source code)

**NFR-4.2:** Database credentials must use least-privilege access (read/write only to required tables)

**NFR-4.3:** Exported files must not be publicly accessible (use signed URLs with expiration, or require authentication)

### NFR-5: Usability

**NFR-5.1:** Phase 1 interface: Command-line interface (CLI) with intuitive, single-command workflows

**NFR-5.2:** All CLI commands must provide helpful error messages with actionable next steps
- Bad: "Error: invalid input"
- Good: "Error: Domain file not found at 'domainz.csv'. Check file path. Expected format: CSV with one domain per line."

**NFR-5.3:** Documentation must include:
- Quick start guide (0 to first job in <10 minutes)
- CLI reference (all commands with examples)
- Troubleshooting guide (common errors and solutions)
- Architecture overview (for operators/DevOps)

**NFR-5.4:** Deployment to cloud platform must be achievable in <60 minutes following documentation (for users with basic cloud experience: familiarity with GCP Console, gcloud CLI, or AWS Console)

### NFR-6: Cost Efficiency

**NFR-6.1:** Cloud infrastructure must scale to zero when idle (no jobs running) to minimize costs

**NFR-6.2:** Target infrastructure cost: <$0.10 per 1,000 domains processed (excluding ScrapingBee fees)

**NFR-6.3:** Workers must have strict memory limits (e.g., 512MB-1GB) to prevent runaway costs from memory-heavy operations

---

## 7. Success Metrics

### Business Outcomes

**BM-1: Time Saved**
- **Metric:** Average time to generate 500 qualified prospects
- **Baseline:** 16 hours (manual process)
- **Target:** <2 hours (87% reduction)
- **Measurement:** Track job duration from creation to completed export for jobs targeting ~500 results

**BM-2: Campaign Capacity (Product-Led Metric)**
- **Metric:** Number of distinct jobs completed per week by Earned Media team
- **Baseline:** 2-3 jobs/week (limited by manual bottleneck)
- **Target:** 8-10 jobs/week
- **Measurement:** Count of completed jobs per week from database (automated, no surveys)

**BM-3: Cost per Opportunity**
- **Metric:** Fully-loaded cost (infrastructure + APIs) per qualified prospect identified
- **Target:** <$0.40 per prospect
- **Measurement:** (Total monthly cost) / (Total prospects identified across all jobs)

### System Performance

**PM-1: Throughput**
- **Metric:** Domains processed per hour (system-wide, all jobs)
- **Target Phase 1:** 5,000+ domains/hour at scale
- **Target Phase 2:** 20,000+ domains/hour at scale
- **Measurement:** Log processing rate every minute, aggregate to hourly average

**PM-2: Queue Processing Latency**
- **Metric:** Average time a task waits in queue before being picked up by a worker
- **Target:** <10 seconds (when system is not at max concurrency)
- **Measurement:** Timestamp when task added to queue vs. when worker picks it up

**PM-3: Completion Rate**
- **Metric:** Percentage of jobs that complete successfully (not paused by user or failed)
- **Target:** >95%
- **Measurement:** `completed_jobs / total_non_paused_jobs` from database

**PM-4: Domain Success Rate**
- **Metric:** Percentage of domains successfully crawled (within completed jobs)
- **Target:** >90% for valid, accessible domains
- **Measurement:** `(successful_domains / total_domains) * 100` excluding domains with permanent failures (DNS error, robots.txt disallowed)

**PM-5: Resumption Success**
- **Metric:** Percentage of paused jobs that resume without errors
- **Target:** 100%
- **Measurement:** Track resume attempts vs. successful resumes (no duplicate processing, no data loss)

**PM-6: Global Concurrency Compliance**
- **Metric:** Percentage of time system stays within configured global concurrency cap
- **Target:** 100% (never exceed cap)
- **Measurement:** Log concurrency every minute; alert if cap breached

**PM-7: Database Write Performance**
- **Metric:** P95 latency for inserting crawl results into database
- **Target:** <100ms per batch insert (batch size = 100 results)
- **Measurement:** Database performance monitoring, application logs

### Quality Metrics

**QM-1: Keyword Matching Accuracy**
- **Metric:** False positive rate (keywords reported but not actually on page)
- **Target:** <1%
- **Measurement:** Manual audit of 100 random results per month

**QM-2: Data Integrity**
- **Metric:** Duplicate entries in results (same domain+URL+keyword appears multiple times)
- **Target:** 0%
- **Measurement:** Automated deduplication check on all exports

**QM-3: Error Message Quality**
- **Metric:** Percentage of user-reported issues resolved without engineering intervention
- **Target:** >80% (users can self-diagnose from error messages and docs)
- **Measurement:** Track support tickets vs. self-resolved issues (qualitative)

---

## 8. Scope & Phasing

### Phase 1: Core CLI Tool (In Scope)

**Goal:** Functional CLI tool deployed to cloud, usable by Earned Media team

**Features:**
- ✅ CLI-based job management (run, pause, resume, status, export)
- ✅ CSV/TXT file inputs (domains, keywords)
- ✅ Three crawl modes (free, premium, hybrid) with per-URL fallback
- ✅ Distributed task processing architecture (asynchronous queue-based)
- ✅ Persistent job state in external database (Cloud SQL, Firestore, or equivalent)
- ✅ Horizontal scaling support (1 to 500+ workers)
- ✅ ScrapingBee integration with credit tracking and budget caps
- ✅ Asynchronous CSV/JSON export generation with streaming writes
- ✅ Comprehensive observability (logs, metrics, error reports)
- ✅ Global concurrency control across all jobs
- ✅ Distributed rate limiting coordination
- ✅ 90-day data retention policy with automatic cleanup

**Success Criteria:**
- Earned Media team successfully runs 5 jobs in first week
- At least one job processes 5,000+ domains without manual intervention
- Team reports >50% time savings vs. previous method
- Zero duplicate results or data loss incidents
- System achieves 5,000+ domains/hour throughput during peak load

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

**A-2:** ScrapingBee (or equivalent service) provides sufficient API capacity for our volume (10K-50K requests/day) and account-level concurrency cap is ≥500 concurrent requests

**A-3:** Target domains are publicly accessible (not behind authentication)

**A-4:** Majority of target domains do not aggressively block well-behaved crawlers that respect robots.txt and reasonable rate limits

**A-5:** Users are comfortable with command-line interfaces (no GUI required for Phase 1)

**A-6:** 90-day data retention is sufficient for user workflows (users export results within 90 days of job completion)

**A-7:** Cloud provider's message queue service (Pub/Sub, SQS) supports required throughput (5,000+ tasks/minute) and task visibility timeout features

---

## 10. Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **Widespread IP Blocking** | High - Job fails before completion | Medium | Primary: Use ScrapingBee for protected sites via hybrid mode. Secondary: Aggressive rate limiting (1 req/sec/domain) and User-Agent rotation for direct crawls. Tertiary: Integrate residential proxy pool if needed (Phase 2). |
| **ScrapingBee Budget Overrun** | High - Unexpected $500+ bill | Medium | **Mandatory:** Cost estimation before job starts. Hard budget caps per job (default $100). Real-time credit tracking with alerts. Budget check before issuing new work (in-flight work may exceed cap by up to one batch). |
| **Global Concurrency Limit Breach** | Critical - ScrapingBee account banned | Medium | Implement strict global concurrency cap enforced via centralized coordination (distributed cache). Log concurrency metrics every minute. Alert if cap exceeded. Dynamically throttle new job starts if cap is reached. |
| **Cloud Infrastructure Costs** | Medium - Monthly bill exceeds $200 | Low | Design for scale-to-zero when idle. Use serverless compute (Cloud Run, Lambda) with per-second billing. Set billing alerts at $150/month. Monitor per-job costs; optimize inefficient jobs. |
| **External Service Downtime** | Medium - ScrapingBee/Cloud SQL unavailable | Low | Graceful degradation: If ScrapingBee down for >5 minutes, pause job and alert user (don't silently fail all domains). Retry logic with exponential backoff for transient errors. For DB downtime: buffer results in memory (up to 100 per worker) and retry writes. |
| **Database Connection Exhaustion** | Critical - All jobs fail | Medium | Implement connection pooling (workers reuse connections). Enforce hard limit on max concurrent workers (must be < DB max connections / 2). Monitor active connections; alert at 80% of max. |
| **Task Queue Poison Messages** | Medium - Workers crash repeatedly | Low | Implement Dead Letter Queue (DLQ) after 3 failed processing attempts. Isolate crashing tasks for engineering investigation. Monitor DLQ depth daily. |
| **Export Memory Overflow** | High - Users can't download results | Low | Mandate streaming writes for export generation (row-by-row from DB to cloud storage). Never load full dataset into memory. Test with 50,000-domain exports to ensure <1GB memory usage. |
| **Database Write Throughput Bottleneck** | High - Processing slows dramatically | Medium | Use batch inserts (100 results per transaction). Consider database partitioning by job ID or date for large datasets (100M+ rows). Monitor write latency (target <100ms per batch). |
| **Distributed Rate Limiting Failure** | High - DDoS multiple target sites | Low | Use distributed cache (Redis/Memcached) with TTL for rate limit locks. Implement fallback: if cache unavailable, use conservative local rate limiting (0.5 req/sec) rather than failing completely. |
| **Inaccurate Site Size Estimation** | Low - Waste time crawling irrelevant pages | Medium | Start with conservative heuristics (sitemap.xml primary source). Allow per-job override of crawl depth via `--max-pages-per-domain`. Log actual pages crawled per domain to tune heuristics over time. |
| **Memory Overflow on Large Sites** | Medium - Worker crashes mid-domain | Low | Implement strict per-domain limits: max 500 pages, max 10MB HTML per page. If limits exceeded, mark domain as "partially crawled" and continue. Use workers with memory limits (512MB-1GB) and automatic restarts on OOM. |
| **False Keyword Matches** | Low - Irrelevant results frustrate user | Low | Use word-boundary matching (not substring). Capture context snippets so users can manually verify. Log match count vs. page count (if keyword appears 200 times on one page, likely spam/footer). |
| **Low Adoption (Too Complex)** | High - Team doesn't use tool | Low | Invest in documentation: 5-minute quickstart video. 1-hour hands-on training with Earned Media team. Simplify CLI workflow (single command to start job). Collect feedback weekly for first month. |
| **Data Loss on System Crash** | Critical - Users lose job progress | Low | All job state and results persisted to external database (Cloud SQL, Firestore). Checkpoints after every batch. Test crash recovery: kill workers mid-job, verify resume succeeds without data loss. |
| **Queue Depth Growing Unbounded** | High - System overwhelmed | Low | Monitor queue depth in real-time. Alert if queue depth > 50,000 tasks. Implement auto-pause: if queue depth exceeds threshold and not shrinking after 10 minutes, pause new job starts until queue drains. |

---

## 11. Dependencies

### Internal Dependencies

**D-1:** Earned Media team availability for requirements validation and user acceptance testing (est. 5 hours over 2 weeks)

**D-2:** Cloud platform admin access for initial deployment (GCP project with Cloud Run, Cloud SQL, Cloud Storage, Pub/Sub enabled)

**D-3:** Decision on external database technology (Cloud SQL PostgreSQL vs. Firestore) - affects FR-1.5, FR-3.2, FR-4.4

### External Dependencies

**D-4:** ScrapingBee API account with:
- Minimum $100/month subscription
- Account-level concurrency cap documented and ≥500 concurrent requests
- API documentation for credit tracking and error codes

**D-5:** Cloud storage service (GCS or S3) for:
- Exported result files (CSV/JSON)
- Checkpoint data backups
- Log archival

**D-6: Distributed Cache (Redis or Memcached) - CRITICAL**
- **Purpose:** Global concurrency limiting, distributed rate limiting coordination
- **Requirements:**
  - Sub-millisecond latency for lock acquisition
  - Support for TTL (time-to-live) on keys
  - High availability (99.9%+ uptime)
- **Recommended:** Managed service (Cloud Memorystore, ElastiCache)

**D-7: Message Queue Service - CRITICAL**
- **Purpose:** Asynchronous task distribution for horizontal scaling
- **Requirements:**
  - Support for message visibility timeout (task retry on worker crash)
  - Dead Letter Queue (DLQ) for poison messages
  - Throughput: 5,000+ messages/minute
  - FIFO not required (order doesn't matter)
- **Examples:** Google Cloud Pub/Sub, AWS SQS, RabbitMQ
- **Recommended:** Managed service (Pub/Sub, SQS) for operational simplicity

---

## 12. Open Questions

**Q-1:** Should we support other scraping services (Bright Data, Oxylabs) in addition to ScrapingBee, or standardize on one provider?
- **Decision needed by:** Week 1 (affects architecture)
- **Recommendation:** Start with ScrapingBee only (most popular, good documentation). Design abstraction layer to add more providers in Phase 2 if needed.

**Q-2:** What happens if a user starts a job, forgets about it, and it runs for 72 hours costing $500?
- **Decision needed by:** Week 1 (cost protection)
- **Recommendation:** Implement global timeout (default 48 hours) in addition to hard budget cap. Jobs auto-pause at timeout and require manual resume. Alert user: "Job running for 48 hours. Auto-paused to prevent runaway costs."

**Q-3:** Should we cache successful crawls to avoid re-crawling the same domain within X days?
- **Decision needed by:** Week 2 (performance optimization)
- **Recommendation:** Not for Phase 1 (adds complexity). Evaluate in Phase 2 if users report frequent re-crawls of same domains. Could save credits but adds state management complexity.

**Q-4:** How do we handle domains with CAPTCHAs or login requirements?
- **Decision needed by:** Week 1 (crawling strategy)
- **Recommendation:** Out of scope for Phase 1. ScrapingBee's stealth mode may bypass some CAPTCHAs. For domains requiring login, mark as failed: "Login required (HTTP 401/403)". Document workaround: user can manually verify these domains.

**Q-5:** What message queue technology should we use?
- **Decision needed by:** Week 1 (architecture)
- **Recommendation:** Use cloud provider's managed service: Google Cloud Pub/Sub (if GCP) or AWS SQS (if AWS). Avoid self-hosted RabbitMQ/Kafka for Phase 1 (operational overhead).

---

## 13. Compliance & Legal Considerations

**L-1: Web Scraping Legality**
- **Requirement:** System must respect `robots.txt` and website Terms of Service
- **Rationale:** Avoid legal exposure from aggressive/unauthorized crawling
- **Implementation:** Parse and honor robots.txt before crawling any domain. Do not provide "bypass robots.txt" option.

**L-2: Data Retention & Deletion**
- **Requirement:** Crawled content (HTML, text) must not be stored longer than necessary for analysis
- **Rationale:** Minimize copyright and privacy risk
- **Implementation:** Extract keyword matches and context snippets; discard full HTML immediately. Do not build a persistent crawl archive. Auto-delete job results after 90 days.

**L-3: Privacy (GDPR/CCPA)**
- **Requirement:** If crawled pages contain PII (unlikely but possible), do not store it
- **Rationale:** Compliance with data protection regulations
- **Implementation:** System only extracts keyword matches and surrounding text (max 300 chars). No personal data fields parsed or stored. If user discovers PII in results, provide data deletion endpoint.

**L-4: ScrapingBee Terms of Service**
- **Requirement:** Verify that our use case complies with ScrapingBee's acceptable use policy
- **Rationale:** Avoid account suspension
- **Implementation:** Review ScrapingBee ToS during Week 1. Ensure we're not violating any prohibited use cases (e.g., scraping social media profiles, bypassing paywalls, copyright infringement).

**L-5: Rate Limiting as Good Citizenship**
- **Requirement:** System must not perform actions that resemble a DDoS attack
- **Rationale:** Ethical responsibility and legal risk mitigation
- **Implementation:** Enforce 1 req/sec per domain. Respect Retry-After headers. Rotate User-Agents to avoid appearing as a bot army from single source.

---

## 14. Out of Scope (Explicitly Not Doing)

**OS-1:** Real-time crawling (jobs must be batch-oriented, not live monitoring)

**OS-2:** Content extraction beyond keyword matching (e.g., extracting contact emails, phone numbers, structured data)

**OS-3:** Automated outreach (sending emails to prospects)

**OS-4:** Integration with CRM systems (Salesforce, HubSpot)

**OS-5:** Multi-tenancy or user authentication (Phase 1 is single-user CLI tool deployed per team)

**OS-6:** Mobile app or browser extension

**OS-7:** Competitor analysis or domain authority scoring (use external tools like Ahrefs, Moz for enrichment)

**OS-8:** Historical data storage beyond 90 days (users must export to their own storage for long-term retention)

---

## Appendix A: Example JSON Export Schema

```json
{
  "results": {
    "example.com": {
      "CRM software": [
        {
          "url": "https://example.com/blog/best-crm-tools",
          "frequency": 7,
          "context": "...Looking for the best CRM software for your small business? We compared 15 tools...",
          "crawl_method": "direct",
          "timestamp": "2025-01-19T16:15:32Z",
          "http_status": 200
        }
      ],
      "small business CRM": [
        {
          "url": "https://example.com/guides/crm-comparison",
          "frequency": 3,
          "context": "...Top 5 small business CRM platforms for 2025...",
          "crawl_method": "scrapingbee-standard",
          "timestamp": "2025-01-19T16:17:48Z",
          "http_status": 200
        }
      ]
    },
    "another-example.net": {
      "CRM software": [
        {
          "url": "https://another-example.net/",
          "frequency": 2,
          "context": "...We integrate with popular CRM software like Salesforce and HubSpot...",
          "crawl_method": "direct",
          "timestamp": "2025-01-19T16:22:10Z",
          "http_status": 200
        }
      ]
    }
  }
}
```

**Notes:**
- Top-level `results` object contains domains as keys
- Each domain contains keywords as keys
- Each keyword contains array of page matches
- Flat structure for easy programmatic parsing
- No redundant summary data (use `job status` command for summaries)

---

## Appendix B: CLI Command Reference

```bash
# ============================================
# PRIMARY COMMAND: Run a new job
# ============================================
backlink-prospector job run \
  --name "Acme Corp Q1 2025" \
  --domains domains.csv \
  --keywords keywords.txt \
  --mode hybrid \
  --max-credits 5000 \
  --max-pages-per-domain 100

# Optional: Create job without auto-starting (for review)
backlink-prospector job run \
  --name "Beta Inc Test" \
  --domains domains.csv \
  --keywords keywords.txt \
  --no-auto-start

# Start a previously created job
backlink-prospector job start <job_id>

# ============================================
# JOB MANAGEMENT
# ============================================

# Check status of a running job
backlink-prospector job status <job_id>

# Pause a running job
backlink-prospector job pause <job_id>

# Resume a paused job
backlink-prospector job resume <job_id>

# List all jobs
backlink-prospector job list

# List including archived jobs (results deleted)
backlink-prospector job list --include-archived

# ============================================
# EXPORT & REPORTS
# ============================================

# Export results (asynchronous)
backlink-prospector job export <job_id> --format csv
backlink-prospector job export <job_id> --format json
backlink-prospector job export <job_id> --format csv,json

# Check export status
backlink-prospector job export-status <job_id>

# View cost report
backlink-prospector job cost-report <job_id>

# View error report
backlink-prospector job errors <job_id>

# ============================================
# SYSTEM MONITORING (for operators)
# ============================================

# View system-wide metrics
backlink-prospector system metrics

# View active workers and concurrency
backlink-prospector system workers

# View global credit usage
backlink-prospector system credits

# View task queue status
backlink-prospector system queue-status
```

---

## Appendix C: Architecture Overview Diagram

```
┌─────────────┐
│   User CLI  │
└──────┬──────┘
       │ job run
       ▼
┌──────────────────────────────────────────────────┐
│           Job Manager (Stateless)                │
│  - Validates inputs                              │
│  - Creates job in DB                             │
│  - Decomposes job into tasks (1 task per domain)│
│  - Pushes tasks to Message Queue                 │
└────────────────────┬─────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │   Message Queue        │
        │  (Pub/Sub / SQS)       │
        │  - Task: {domain, kws} │
        └───────┬────────────────┘
                │
     ┌──────────┴──────────┬──────────┐
     ▼                     ▼          ▼
┌─────────┐          ┌─────────┐  ┌─────────┐
│Worker 1 │          │Worker 2 │  │Worker N │
│(stateless)         │(stateless) │(stateless)
└────┬────┘          └────┬────┘  └────┬────┘
     │                    │            │
     │ Check distributed rate limit    │
     ▼                    ▼            ▼
┌────────────────────────────────────────┐
│     Distributed Cache (Redis)          │
│  - Rate limit locks per domain         │
│  - Global concurrency tokens           │
└────────────────────────────────────────┘
     │                    │            │
     │ Crawl domain       │            │
     ▼                    ▼            ▼
┌────────────────────────────────────────┐
│        ScrapingBee API                 │
│  (or direct HTTP for free mode)        │
└────────────────────────────────────────┘
     │                    │            │
     │ Write results      │            │
     ▼                    ▼            ▼
┌────────────────────────────────────────┐
│     Database (Cloud SQL / Firestore)   │
│  - Job state                           │
│  - Results (keyword matches)           │
│  - Checkpoints                         │
└────────────────────────────────────────┘
     │
     │ User requests export
     ▼
┌────────────────────────────────────────┐
│     Export Worker (Async)              │
│  - Streams results from DB             │
│  - Writes to Cloud Storage             │
└────────┬───────────────────────────────┘
         │
         ▼
┌────────────────────────────────────────┐
│     Cloud Storage (S3 / GCS)           │
│  - Exported CSV/JSON files             │
│  - 7-day retention                     │
└────────────────────────────────────────┘
```

**Key Architectural Principles:**
1. **Stateless Workers:** Workers can be killed/restarted without data loss
2. **Task Queue as Single Source of Work:** All workers pull from queue (no master/worker coordination)
3. **Distributed Coordination:** Rate limits and concurrency enforced via Redis (shared state)
4. **Persistent State:** All progress saved to external database (not in-memory or ephemeral storage)
5. **Horizontal Scaling:** Add more workers → increase throughput linearly

---

## Appendix D: Glossary

| Term | Definition |
|------|------------|
| **Backlink** | A hyperlink from one website to another. A key factor in SEO rankings. |
| **Anchor Text** | The clickable text in a hyperlink. |
| **Prospecting** | The process of identifying websites that mention relevant keywords but don't yet link to your site. |
| **Qualified Prospect** | A domain where keyword mentions suggest a good backlink opportunity (high relevance, potentially good authority). |
| **Adaptive Crawling** | Adjusting crawl depth based on site size (full crawl for small sites, selective for large sites). |
| **Hybrid Mode** | Crawl strategy that tries free direct requests first, falls back to premium proxy service on per-URL failure. |
| **Batch** | A subset of domains processed together (e.g., 100 domains). Progress checkpointed after each batch. Deprecated in v4.0 in favor of per-task processing. |
| **Task** | A single unit of work in the system: one domain + associated keywords to crawl. |
| **Job** | A complete prospecting request: one domain list, one keyword list, processed to completion. |
| **Worker** | A stateless compute instance (container, VM, serverless function) that pulls tasks from queue and processes them. |
| **Message Queue** | Distributed system for asynchronous task distribution (e.g., Pub/Sub, SQS). Enables horizontal scaling. |
| **Fault Tolerance** | System's ability to continue operating even when individual components (workers, domains) fail. |
| **Horizontal Scaling** | Adding more workers to process tasks in parallel (vs. vertical scaling = bigger/faster single worker). |
| **Global Concurrency Cap** | System-wide limit on total concurrent requests across all jobs, to prevent exceeding external API rate limits. |
| **Distributed Rate Limiting** | Coordinating rate limits across multiple workers using shared state (e.g., Redis locks). |
| **Backpressure** | When downstream components (e.g., database) cannot keep up with upstream components (e.g., crawlers), requiring throttling. |
| **Streaming Export** | Generating export files by writing row-by-row from database to storage, never loading full dataset into memory. |
| **Checkpoint** | Persistent snapshot of job progress, allowing resume after crash or pause. |
| **Dead Letter Queue (DLQ)** | Separate queue for tasks that fail repeatedly (>3 times), preventing infinite retry loops. |
| **Poison Message** | A task that causes workers to crash (e.g., malformed data, triggers a bug). Moved to DLQ after max retries. |
| **Soft Delete** | Marking data as deleted (invisible to users) but retaining in database temporarily, vs. hard delete (permanent removal). |
| **Connection Pooling** | Reusing database connections across multiple operations instead of opening/closing per operation. Prevents connection exhaustion. |

---

**END OF PRD v4.0**
