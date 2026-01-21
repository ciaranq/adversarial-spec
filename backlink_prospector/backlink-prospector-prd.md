# PRD: Backlink Prospector - Scalable Keyword Discovery System

**Version:** 1.1  
**Created:** 2025-01-19  
**Updated:** 2025-01-19  
**Author:** Claude + Chatterbox  
**Status:** 🟡 Awaiting Final Review  

---

## 1. Problem Statement

### What problem are we solving?

Earned Media needs to identify backlink opportunities across thousands of domains by finding pages that contain specific anchor text keywords. The current solution works for small domain sets but faces critical limitations when scaling to 5000+ domains:

- **IP blocking risk** when crawling from office network
- **Slow WiFi** causing timeouts and delays
- **No batch processing** or ability to pause/resume
- **No progress tracking** across large domain sets
- **Manual result aggregation** across multiple runs

### Who experiences this problem?

SEO consultants and agencies who need to:
- Identify backlink opportunities at scale
- Qualify thousands of potential domains efficiently
- Avoid getting blocked by target websites
- Process large domain lists without babysitting the script

### Current pain points

- Running from office IP risks blacklisting entire network
- 5000 domains × 50 pages each = 250,000 pages to analyze (days of runtime)
- No way to track progress or resume if interrupted
- Difficult to filter/analyze results across multiple output files
- Slow WiFi makes local execution impractical

---

## 2. Goals & Objectives

### Primary Goal

Build a cloud-based, scalable system to crawl 5000+ domains, identify pages containing target keywords, and output qualified candidate domains for Phase 2 backlink analysis.

### Secondary Goals

- Adaptive crawling based on site size (auto-adjust depth)
- Multiple output formats for different use cases
- Batch processing with pause/resume capability
- Respectful crawling to avoid blocks (rate limiting, robots.txt)
- Easy cloud deployment without advanced DevOps knowledge

### Non-Goals (Explicitly NOT doing in Phase 1)

- Next.js dashboard (Phase 2)
- Real-time progress monitoring UI (Phase 2)
- Link analysis (checking if keyword is already a link) (Phase 2)
- Email notifications
- Authentication/multi-user support
- Proxy rotation services (may add later if needed)

---

## 3. User Stories

### Core User Stories

#### Story 1: Upload Domain List

- **As an** SEO consultant
- **I want to** provide a CSV file with 5000 domains
- **So that** the system can process them all without manual intervention
- **Acceptance Criteria:**
  - Accept CSV with one domain per line (e.g., `example.com`)
  - Validate domains (basic format check)
  - Auto-deduplicate domains on load
  - Support up to 10,000 domains

#### Story 2: Define Keywords

- **As an** SEO consultant
- **I want to** provide a list of target keywords/phrases
- **So that** the system searches for those specific terms
- **Acceptance Criteria:**
  - Accept TXT file with one keyword per line
  - Support both single words and phrases
  - Case-insensitive matching
  - Support up to 100 keywords

#### Story 3: Select Crawl Method

- **As an** SEO consultant
- **I want to** choose which crawl method to use per run
- **So that** I can test which gives best results for my domains
- **Acceptance Criteria:**
  - Support `direct` method (free, Cloud Run IP)
  - Support `scrapingbee` method (paid, all features enabled)
  - Support `hybrid` method (try direct, fallback to ScrapingBee)
  - Track which method was used per domain
  - Compare results across methods

#### Story 4: Adaptive Crawling

- **As an** SEO consultant
- **I want the** system to crawl differently based on site size
- **So that** small sites get full coverage and large sites don't take forever
- **Acceptance Criteria:**
  - Check sitemap.xml first to estimate site size
  - If site ≤ 300 pages → crawl all pages
  - If site > 300 pages → crawl homepage + key pages only
  - Threshold configurable via `.env`

#### Story 5: Batch Processing with Job Management

- **As an** SEO consultant
- **I want** to create jobs and process them in batches
- **So that** I can manage large domain lists over multiple sessions
- **Acceptance Criteria:**
  - Create named jobs with domains and keywords
  - Process configurable number of batches per run
  - Track progress per job (X/5000 domains, Y/50 batches)
  - View job status anytime
  - List all jobs with summary stats

#### Story 6: Pause and Resume Jobs

- **As an** SEO consultant
- **I want to** pause and resume jobs at any time
- **So that** I don't lose progress and can spread work over days
- **Acceptance Criteria:**
  - Pause mid-batch (current batch completes first)
  - Resume from exact stopping point
  - No duplicate processing of domains
  - State persisted in SQLite database

#### Story 7: Track ScrapingBee Credits

- **As an** SEO consultant
- **I want to** monitor my ScrapingBee credit usage
- **So that** I don't exceed my monthly limit
- **Acceptance Criteria:**
  - Track credits used per request
  - Track credits used per batch and job
  - Warning when approaching monthly limit (50k remaining)
  - Auto-pause if limit exceeded
  - View credit usage reports

#### Story 8: View Results

- **As an** SEO consultant
- **I want** results in multiple formats
- **So that** I can analyze them different ways
- **Acceptance Criteria:**
  - CSV export (for Excel)
  - JSON export (for programmatic use)
  - SQLite database (for querying)
  - Include: domain, URL, keyword matches, context snippets, frequency
  - Include: crawl method used, credits consumed

---

## 4. Technical Requirements

### Frontend (Phase 2 Only)

*Deferred to Phase 2 - Next.js dashboard*

### Backend

#### Crawl Methods (User Selectable)

The system supports multiple crawl methods, selectable per run:

| Method | Description | Cost | Best For |
|--------|-------------|------|----------|
| `direct` | Direct HTTP requests from Cloud Run | Free | Testing, low-risk domains |
| `scrapingbee` | All requests via ScrapingBee API | ~1-25 credits/page | Protected sites, guaranteed success |
| `hybrid` | Try direct first, fallback to ScrapingBee on failure | Variable | Production runs, cost-efficient |

```bash
# Usage examples
python main.py --method direct        # Free, risk of blocks
python main.py --method scrapingbee   # Paid, reliable
python main.py --method hybrid        # Best of both (recommended)
```

#### ScrapingBee Integration

**API Features Enabled (for best results):**
- ✅ **JavaScript rendering** - Handle JS-heavy sites (5 credits/request)
- ✅ **Premium proxies** - Bypass protection (10-25 credits/request)
- ✅ **Stealth mode** - Avoid bot detection
- ✅ **Custom headers** - Mimic real browsers
- ✅ **Automatic retries** - Built-in retry logic

**Configuration:**
```env
# ScrapingBee Settings
SCRAPINGBEE_API_KEY=your_api_key_here
SCRAPINGBEE_RENDER_JS=true
SCRAPINGBEE_PREMIUM_PROXY=true
SCRAPINGBEE_STEALTH_PROXY=true
SCRAPINGBEE_MONTHLY_LIMIT=250000
SCRAPINGBEE_CREDITS_WARNING=50000
```

**Credit Tracking:**
- Track credits used per batch
- Track credits used per job
- Warning when approaching monthly limit
- Auto-pause if limit exceeded

#### Core Crawler

- **Language:** Python 3.9+
- **HTML Parser:** Selectolax (primary), BeautifulSoup (fallback)
- **HTTP Client:** `requests` with session management
- **Keyword Matching:**
  - Case-insensitive
  - Word boundary detection for single words
  - Substring matching for phrases
  - Capture match count and context (±30 chars, configurable)

#### Batch Processing System

The system processes domains in configurable batches with full state tracking:

**Batch Workflow:**
```
Job (5000 domains)
  └── Batch 1 (domains 1-100)      ✅ Completed
  └── Batch 2 (domains 101-200)    ✅ Completed  
  └── Batch 3 (domains 201-300)    🔄 In Progress
  └── Batch 4 (domains 301-400)    ⏸️ Pending
  └── ... 
  └── Batch 50 (domains 4901-5000) ⏸️ Pending
```

**SQLite Database Tracking:**

```sql
-- jobs table (tracks overall job)
CREATE TABLE jobs (
  id TEXT PRIMARY KEY,           -- UUID
  name TEXT,                      -- User-friendly name
  created_at TIMESTAMP,
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  status TEXT,                    -- pending/running/paused/completed/failed
  crawl_method TEXT,              -- direct/scrapingbee/hybrid
  total_domains INTEGER,
  processed_domains INTEGER,
  total_batches INTEGER,
  completed_batches INTEGER,
  scrapingbee_credits_used INTEGER
);

-- batches table (tracks each batch)
CREATE TABLE batches (
  id INTEGER PRIMARY KEY,
  job_id TEXT,
  batch_number INTEGER,
  status TEXT,                    -- pending/running/completed/failed
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  domains_in_batch INTEGER,
  domains_processed INTEGER,
  domains_succeeded INTEGER,
  domains_failed INTEGER,
  matches_found INTEGER,
  scrapingbee_credits_used INTEGER,
  error_message TEXT,
  FOREIGN KEY (job_id) REFERENCES jobs(id)
);

-- domains table (tracks each domain)
CREATE TABLE domains (
  id INTEGER PRIMARY KEY,
  job_id TEXT,
  batch_id INTEGER,
  domain TEXT,
  status TEXT,                    -- pending/in-progress/completed/failed
  crawl_method_used TEXT,         -- direct/scrapingbee
  pages_crawled INTEGER,
  matches_found INTEGER,
  error_message TEXT,
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  FOREIGN KEY (job_id) REFERENCES jobs(id),
  FOREIGN KEY (batch_id) REFERENCES batches(id)
);

-- results table (keyword matches)
CREATE TABLE results (
  id INTEGER PRIMARY KEY,
  job_id TEXT,
  domain_id INTEGER,
  url TEXT,
  keyword TEXT,
  frequency INTEGER,
  context TEXT,
  crawled_at TIMESTAMP,
  FOREIGN KEY (job_id) REFERENCES jobs(id),
  FOREIGN KEY (domain_id) REFERENCES domains(id)
);

-- errors table (detailed error tracking)
CREATE TABLE errors (
  id INTEGER PRIMARY KEY,
  job_id TEXT,
  domain_id INTEGER,
  batch_id INTEGER,
  error_type TEXT,
  error_message TEXT,
  url TEXT,
  occurred_at TIMESTAMP,
  FOREIGN KEY (job_id) REFERENCES jobs(id),
  FOREIGN KEY (domain_id) REFERENCES domains(id),
  FOREIGN KEY (batch_id) REFERENCES batches(id)
);

-- scrapingbee_usage table (credit tracking)
CREATE TABLE scrapingbee_usage (
  id INTEGER PRIMARY KEY,
  job_id TEXT,
  batch_id INTEGER,
  domain TEXT,
  url TEXT,
  credits_used INTEGER,
  timestamp TIMESTAMP,
  FOREIGN KEY (job_id) REFERENCES jobs(id),
  FOREIGN KEY (batch_id) REFERENCES batches(id)
);
```

**CLI Commands for Batch Management:**
```bash
# Create a new job
python main.py job create --name "January 2025 Run" --domains domains.csv --keywords keywords.txt

# Start/resume processing
python main.py job run <job_id> --method hybrid --batches 5

# Check job status
python main.py job status <job_id>

# List all jobs
python main.py job list

# Pause a running job
python main.py job pause <job_id>

# Resume a paused job
python main.py job resume <job_id> --batches 10

# Export results
python main.py job export <job_id> --format csv,json

# View ScrapingBee credit usage
python main.py credits status
python main.py credits usage --job <job_id>
```

**Batch Size:** 100 domains (configurable via `.env`)

#### Adaptive Crawling Logic

```python
# Pseudocode
if estimate_site_size(domain) <= PAGE_THRESHOLD:
    crawl_strategy = "full_site"
    max_pages = None
else:
    crawl_strategy = "selective"
    max_pages = PAGE_THRESHOLD

# .env variables:
# PAGE_THRESHOLD=300
# MAX_PAGES_PER_DOMAIN=50 (for selective crawling)
```

#### Rate Limiting & Politeness

- Respect `robots.txt`
- Delay between requests: 1-2 seconds (configurable)
- User-Agent: `Mozilla/5.0 (compatible; BacklinkProspector/1.0)`
- Timeout: 15 seconds per request
- Retry logic: 3 attempts with exponential backoff
- Max concurrent requests per domain: 1

#### Output Formats

**CSV Structure:**
```csv
domain,url,keyword,frequency,context,crawl_date,status
example.com,https://example.com/page,SEO services,3,"...best SEO services in Australia...",2025-01-19T10:30:00,success
```

**JSON Structure:**
```json
{
  "job_id": "uuid",
  "started_at": "2025-01-19T10:00:00",
  "completed_at": "2025-01-19T12:30:00",
  "total_domains": 5000,
  "processed_domains": 5000,
  "matches_found": 847,
  "results": [
    {
      "domain": "example.com",
      "url": "https://example.com/page",
      "keywords": {
        "SEO services": {
          "count": 3,
          "contexts": ["...best SEO services in...", "..."]
        }
      },
      "crawl_date": "2025-01-19T10:30:00"
    }
  ]
}
```

**SQLite Schema:**

See "Batch Processing System" section above for complete database schema including:
- `jobs` - Overall job tracking
- `batches` - Batch-level tracking  
- `domains` - Per-domain status
- `results` - Keyword matches
- `errors` - Error logging
- `scrapingbee_usage` - Credit tracking

### Infrastructure

#### GCP Cloud Run Deployment

- **Service:** Cloud Run (containerized)
- **Region:** australia-southeast1 (Sydney)
- **Memory:** 2GB
- **CPU:** 1 vCPU
- **Timeout:** 3600 seconds (1 hour max per execution)
- **Concurrency:** 1 (process one job at a time)
- **Autoscaling:** 0-1 instances (scale to zero when idle)

#### Storage

- **Cloud Storage Bucket:** For inputs (domains.csv, keywords.txt) and outputs
- **Local SQLite:** For progress tracking (stored in container, backed up to Cloud Storage)

#### Configuration (.env)

```env
# ===========================================
# CRAWL METHOD SETTINGS
# ===========================================
# Options: direct, scrapingbee, hybrid
DEFAULT_CRAWL_METHOD=hybrid

# ===========================================
# DIRECT CRAWLING SETTINGS
# ===========================================
PAGE_THRESHOLD=300
MAX_PAGES_PER_DOMAIN=50
CRAWL_DELAY=1.5
REQUEST_TIMEOUT=15
MAX_RETRIES=3
CONTEXT_LENGTH=30
USER_AGENT=Mozilla/5.0 (compatible; BacklinkProspector/1.0)

# ===========================================
# SCRAPINGBEE SETTINGS
# ===========================================
SCRAPINGBEE_API_KEY=your_api_key_here
SCRAPINGBEE_RENDER_JS=true
SCRAPINGBEE_PREMIUM_PROXY=true
SCRAPINGBEE_STEALTH_PROXY=true
SCRAPINGBEE_MONTHLY_LIMIT=250000
SCRAPINGBEE_CREDITS_WARNING=50000
SCRAPINGBEE_TIMEOUT=30

# ===========================================
# BATCH SETTINGS
# ===========================================
BATCH_SIZE=100
AUTO_SAVE_INTERVAL=10

# ===========================================
# OUTPUT SETTINGS
# ===========================================
OUTPUT_DIR=./output
SAVE_CSV=true
SAVE_JSON=true
SAVE_SQLITE=true

# ===========================================
# GCP SETTINGS (for Cloud Run)
# ===========================================
GCS_BUCKET=backlink-prospector-results
GCP_PROJECT_ID=your-project-id
GCP_REGION=australia-southeast1

# ===========================================
# OPTIONAL: GOOGLE DRIVE EXPORT
# ===========================================
GOOGLE_DRIVE_ENABLED=false
GOOGLE_DRIVE_FOLDER_ID=
```

---

## 5. Success Metrics

### Performance Metrics

- **Throughput:** Process 100+ domains per hour
- **Completion Rate:** Successfully crawl >90% of domains
- **Error Rate:** <10% failed requests per batch
- **Time to Completion:** 5000 domains in <48 hours

### Quality Metrics

- **No IP blocks** during entire run
- **Accurate keyword matching:** 100% precision (no false positives)
- **Resume success rate:** 100% (can always resume from checkpoint)

### User Acceptance Criteria

- ✅ Upload 5000 domains, get results in 3 formats
- ✅ Can pause and resume without data loss
- ✅ Results clearly show domain, URL, keyword matches, context
- ✅ No manual intervention required during run
- ✅ Deployment to GCP takes <30 minutes following README

---

## 6. Timeline & Phases

### Phase 1A: Core Backend (Week 1)

**Duration:** 3-5 days

**Deliverables:**
1. ✅ `main.py` - CLI interface with job management commands
2. ✅ `crawler.py` - Direct crawling engine (reuse `crawl_live_selectolax.py`)
3. ✅ `scrapingbee_client.py` - ScrapingBee API integration with all features
4. ✅ `batch_manager.py` - Batch processing with pause/resume
5. ✅ `job_manager.py` - Job CRUD and state management
6. ✅ `database.py` - SQLite schema and operations
7. ✅ `config.py` - Environment variable management
8. ✅ `storage.py` - Multi-format output (CSV, JSON, SQLite, optional GDrive)
9. ✅ `sitemap_parser.py` - Sitemap parsing for site size estimation
10. ✅ `utils.py` - Keyword search, domain parsing, deduplication

**Dependencies:**
- Existing scripts: `crawl_live_selectolax.py`, `crawl_live_soup.py`
- Core libraries: selectolax, beautifulsoup4, requests, python-dotenv
- CLI library: click (recommended) or argparse
- Optional: google-auth, google-api-python-client (for GDrive)

### Phase 1B: Cloud Deployment (Week 1)

**Duration:** 2-3 days

**Deliverables:**
1. ✅ `Dockerfile` - Container definition
2. ✅ `requirements.txt` - Python dependencies
3. ✅ `.env.example` - Template configuration
4. ✅ `README.md` - Setup and deployment guide
5. ✅ `deploy.sh` - One-command deployment script

**Dependencies:**
- GCP account with Cloud Run enabled
- Docker installed locally (for testing)

### Phase 1C: Testing & Documentation (Week 1)

**Duration:** 1-2 days

**Deliverables:**
1. ✅ Test with 100 domains
2. ✅ Test pause/resume functionality
3. ✅ Verify all output formats
4. ✅ Document deployment process
5. ✅ Create troubleshooting guide

### Phase 2: Next.js Dashboard (Week 2-3)

**Duration:** 1-2 weeks

**Features:**
- Upload domains/keywords via UI
- Trigger crawl jobs
- Real-time progress monitoring
- View/filter/export results
- Job history

**Tech Stack:**
- Next.js 15.x (App Router)
- TypeScript
- Tailwind CSS
- shadcn/ui components
- Vercel deployment

---

## 7. Open Questions & Decisions

### Technical Decisions ✅ RESOLVED

1. ✅ **Site size estimation:** Check sitemap.xml first
   - **Decision:** Parse sitemap.xml to count URLs
   - **Fallback:** If no sitemap, crawl up to MAX_PAGES_PER_DOMAIN (50)
   - **Implementation:** Try sitemap.xml, then sitemap_index.xml, then default to selective crawl

2. ✅ **Cloud Run timeout:** 1-hour max execution per request
   - **Decision:** Split into multiple jobs
   - **Implementation:** 
     - Process in batches of 100 domains
     - Each batch checkpoint saved to SQLite
     - Can manually re-invoke Cloud Run to continue
     - Future: Add Cloud Scheduler for automatic continuation

3. ✅ **Output storage:** Cloud Storage vs Google Drive
   - **Decision:** Both options supported
   - **Implementation:**
     - Primary: Cloud Storage for automated storage
     - Optional: Export to Google Drive via API (user provides credentials)
     - Local download always available

### Product Decisions ✅ RESOLVED

4. ✅ **Duplicate handling:** Sanitize domain list first
   - **Decision:** Automatically deduplicate on load
   - **Implementation:**
     - Load domains into set (auto-deduplicates)
     - Log: "Removed X duplicate domains"
     - Continue with unique list

5. ✅ **Partial failures:** Mark as failed, continue
   - **Decision:** Mark as failed and continue to next domain
   - **Implementation:**
     - Track failed domains in SQLite errors table
     - Continue processing remaining domains
     - Generate failure report at end
     - Option to retry failed domains separately

6. ✅ **Context snippet length:** ±30 characters, configurable
   - **Decision:** Default 30 chars before/after (60 total), configurable
   - **Implementation:**
     - `.env` variable: `CONTEXT_LENGTH=30`
     - Adjustable from 10-200 characters
     - Stored in output for each match

---

## 8. Dependencies & Constraints

### External Dependencies

- **GCP Account:** Required for Cloud Run deployment
- **Domain Availability:** Target domains must be publicly accessible (no auth)
- **robots.txt Compliance:** Some sites may disallow crawling

### Technical Constraints

- **Cloud Run Timeout:** 1 hour max per execution
- **Memory Limits:** 2GB max memory per container
- **Rate Limits:** Must respect target site rate limits (self-imposed: 1 req/sec)

### Budget Constraints

- **GCP Costs:** ~$5-20 for 5000-domain job (estimated)
- **Development Time:** 1 week for Phase 1 (backend + deployment)

---

## 9. Risks & Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **IP blocking despite cloud deployment** | High - Job fails partway | Low | Implement aggressive rate limiting, respect robots.txt, add proxy rotation if needed |
| **Cloud Run timeout (1 hour) insufficient** | High - Can't complete job | Medium | Design for multiple invocations, checkpointing every 100 domains |
| **Site estimation inaccurate** | Low - Inefficient crawling | Medium | Use conservative heuristics, allow manual override per domain |
| **Memory overflow on large sites** | Medium - Container crash | Low | Set hard limits on pages/domain, implement memory monitoring |
| **Failed domain retry loops** | Low - Wasted resources | Low | Limit retries to 3, mark as permanently failed after |

---

## 10. Reusable Components from Existing Scripts

### From `crawl_live_selectolax.py` ✅ REUSE

```python
# These functions can be copied directly:
- load_target_sites()          # Read domains from file
- load_word_list()              # Read keywords from file
- search_keywords_in_text()     # Keyword matching logic
- fetch_and_analyze_url()       # Core crawling function
- discover_urls_from_site()     # Link discovery
```

### From `crawl_live_soup.py` ✅ REUSE AS FALLBACK

```python
# Use as fallback if Selectolax fails:
- BeautifulSoup parsing logic
- Text extraction and cleaning
```

### From `common_crawl.py` ⚠️ REFERENCE ONLY

```python
# Good patterns to reference:
- Output formatting (markdown, JSON)
- Progress tracking display
- Error handling patterns
# But Common Crawl API itself not used in Phase 1
```

### From `crawl_live_scrapy.py` ❌ NOT REUSING

```python
# Scrapy framework too complex for cloud deployment
# Stick with requests + selectolax for simplicity
```

### From `dataforseo_sandbox.py` 💡 FUTURE INTEGRATION

```python
# Could integrate in Phase 3 for:
- Backlink verification
- Domain authority checking
- Competitor analysis
```

### New Components Needed 🆕

```python
# main.py
- CLI interface using argparse or click
- Job management commands
- Credit tracking commands

# crawler.py (enhanced)
- Direct crawling with Selectolax
- BeautifulSoup fallback
- Configurable per-request settings

# scrapingbee_client.py 🆕
- ScrapingBee API wrapper
- Credit tracking per request
- JS rendering support
- Premium proxy support
- Stealth mode configuration

# batch_manager.py
- Batch orchestration
- Progress tracking
- Pause/resume logic

# job_manager.py 🆕
- Job CRUD operations
- Job state management
- Multi-job support

# database.py 🆕
- SQLite connection management
- Schema initialization
- Query helpers

# storage.py
- Multi-format export (CSV, JSON, SQLite)
- Cloud Storage integration
- Optional Google Drive export

# config.py
- Environment variable parsing
- Validation
- Method-specific configs

# sitemap_parser.py
- Parse sitemap.xml to estimate site size
- Handle sitemap_index.xml
- Fallback logic

# utils.py
- Keyword search with context extraction
- Domain parsing and deduplication
- URL normalization
```

---

## 11. File Structure for New Project

```
backlink-prospector/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── Dockerfile
├── deploy.sh
│
├── src/
│   ├── __init__.py
│   ├── main.py              # Entry point, CLI interface
│   ├── crawler.py           # Core crawler (direct method)
│   ├── scrapingbee_client.py # ScrapingBee API integration
│   ├── batch_manager.py     # Batch processing + job management
│   ├── job_manager.py       # Job CRUD operations
│   ├── config.py            # Config management
│   ├── storage.py           # Output handlers (CSV, JSON, SQLite, GCS, GDrive)
│   ├── sitemap_parser.py    # Sitemap.xml parsing for size estimation
│   ├── database.py          # SQLite database operations
│   └── utils.py             # Shared utilities (keyword search, dedup, etc.)
│
├── tests/
│   ├── test_crawler.py
│   ├── test_scrapingbee_client.py
│   ├── test_batch_manager.py
│   ├── test_storage.py
│   └── test_sitemap_parser.py
│
├── docs/
│   ├── DEPLOYMENT.md        # GCP deployment guide
│   ├── ARCHITECTURE.md      # System design
│   ├── CLI_REFERENCE.md     # CLI commands documentation
│   └── TROUBLESHOOTING.md   # Common issues
│
├── scripts/                 # Original scripts for reference
│   ├── crawl_live_selectolax.py
│   ├── crawl_live_soup.py
│   ├── common_crawl.py
│   └── crawl_live_scrapy.py
│
├── data/                    # Input data (gitignored except examples)
│   ├── domains.csv.example
│   └── keywords.txt.example
│
└── output/                  # Results (gitignored)
    ├── jobs.db              # SQLite database
    ├── results.csv
    ├── results.json
    └── reports/
        └── job_<id>_report.md
```

---

## 12. Next Steps

### Immediate Actions

1. ✅ **Review & Approve PRD** - Get sign-off on scope and approach
2. 🔜 **Create New Project Repository** - Set up Git repo with structure above
3. 🔜 **Copy Reusable Scripts** - Move `crawl_live_selectolax.py` to `scripts/` for reference
4. 🔜 **Start Development** - Begin Phase 1A (Core Backend)

### All Decisions Made ✅

- ✅ **Site size estimation:** Check sitemap.xml first, fallback to selective crawl
- ✅ **Cloud Run strategy:** Split into multiple 100-domain jobs
- ✅ **Output storage:** Cloud Storage + optional Google Drive export
- ✅ **Duplicate handling:** Auto-deduplicate on load
- ✅ **Retry strategy:** Mark as failed, continue, optional retry at end
- ✅ **Context length:** 30 characters (configurable)

---

## PRD Approval

**Reviewers:**
- [ ] Chatterbox (Product Owner)
- [ ] Claude (Technical Implementation)

**Approval Signatures:**

| Name | Role | Date | Signature |
|------|------|------|-----------|
| Chatterbox | Product Owner | | |
| Claude | Technical Lead | | |

---

## Appendix A: Example Usage

### Initial Setup
```bash
# Clone and setup
git clone <repo>
cd backlink-prospector
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your ScrapingBee API key and settings
```

### Create a Job
```bash
# Create a new job with 5000 domains
python src/main.py job create \
  --name "January 2025 Backlink Research" \
  --domains data/domains.csv \
  --keywords data/keywords.txt

# Output: Created job abc123 with 5000 domains (50 batches)
```

### Run Batches
```bash
# Run 5 batches using hybrid method (recommended)
python src/main.py job run abc123 --method hybrid --batches 5

# Output:
# Batch 1/50: Processing domains 1-100...
#   ✓ 87 succeeded (direct: 72, scrapingbee: 15)
#   ✗ 13 failed
#   📊 42 matches found
#   💳 ScrapingBee credits used: 375
# Batch 2/50: Processing domains 101-200...
# ...
# ✅ Completed 5 batches. Progress: 500/5000 (10%)
# 💳 Total ScrapingBee credits used this session: 1,847
```

### Check Status
```bash
# View job status
python src/main.py job status abc123

# Output:
# Job: January 2025 Backlink Research (abc123)
# Status: Paused
# Progress: 500/5000 domains (10%)
# Batches: 5/50 completed
# Matches found: 203
# ScrapingBee credits used: 1,847
# Last run: 2025-01-19 14:30:00
```

### Resume Processing
```bash
# Resume and run 10 more batches
python src/main.py job resume abc123 --batches 10

# Or run until complete (not recommended for large jobs)
python src/main.py job run abc123 --method hybrid --all
```

### Check ScrapingBee Credits
```bash
# View credit usage
python src/main.py credits status

# Output:
# ScrapingBee Monthly Usage
# ─────────────────────────
# Monthly limit: 250,000
# Used this month: 12,847
# Remaining: 237,153
# 
# Usage by job:
#   abc123 (January 2025 Run): 1,847 credits
#   def456 (December Test): 11,000 credits
```

### Export Results
```bash
# Export job results
python src/main.py job export abc123 --format csv,json

# Output:
# Exported to:
#   output/abc123_results.csv
#   output/abc123_results.json
```

### List All Jobs
```bash
python src/main.py job list

# Output:
# ID       Name                    Status    Progress    Matches  Created
# ─────────────────────────────────────────────────────────────────────────
# abc123   January 2025 Run        Paused    500/5000    203      2025-01-19
# def456   December Test           Complete  100/100     47       2024-12-15
# ghi789   November Analysis       Complete  2000/2000   892      2024-11-20
```

### Cloud Run Execution
```bash
# Deploy to GCP Cloud Run
./deploy.sh

# Trigger via HTTP (for automated/scheduled runs)
curl -X POST https://backlink-prospector-xxx.run.app/job/run \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
  -d '{
    "job_id": "abc123",
    "method": "hybrid",
    "batches": 10
  }'
```

---

## Appendix B: Technology Stack Summary

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Language | Python | 3.9+ | Core application |
| HTML Parser | Selectolax | Latest | Fast HTML parsing |
| Fallback Parser | BeautifulSoup4 | Latest | Robust HTML parsing |
| HTTP Client | Requests | Latest | Direct HTTP requests |
| Proxy Service | ScrapingBee | API | Anti-block crawling |
| Database | SQLite | 3.x | Job/batch/progress tracking |
| CLI Framework | Click | Latest | Command-line interface |
| Config | python-dotenv | Latest | Environment variables |
| Container | Docker | Latest | Cloud deployment |
| Cloud Platform | GCP Cloud Run | - | Serverless compute |
| Storage | GCP Cloud Storage | - | File storage |
| Optional | Google Drive API | - | Export to Drive |

---

## Appendix C: Glossary

| Term | Definition |
|------|------------|
| **Backlink** | A link from one website to another |
| **Anchor Text** | The clickable text in a hyperlink |
| **Prospecting** | The process of identifying potential backlink opportunities |
| **Adaptive Crawling** | Adjusting crawl depth/strategy based on site characteristics |
| **Batch** | A group of domains (default 100) processed together |
| **Job** | A complete crawl task containing all domains and keywords |
| **Direct Crawling** | Fetching pages directly from Cloud Run IP |
| **ScrapingBee** | Third-party proxy service for anti-block crawling |
| **Hybrid Method** | Try direct first, fallback to ScrapingBee on failure |
| **Cloud Run** | Google Cloud Platform's serverless container service |
| **Selectolax** | Fast Python HTML parser using C bindings |
| **Sitemap** | XML file listing all URLs on a website |

---

**End of PRD**
