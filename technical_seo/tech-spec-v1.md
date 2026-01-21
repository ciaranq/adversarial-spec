# Technical Specification: Technical SEO Audit System

## Document Information

**Version**: 1.0
**Status**: Draft - Awaiting Stakeholder Review
**Last Updated**: 2026-01-16
**Based on PRD**: prd-final.md v3.0
**Authors**: Development Team

## Executive Summary

This Technical Specification defines the implementation architecture for the Technical SEO Audit System, a Python-based CLI tool that analyzes websites for technical SEO issues and generates comprehensive reports in multiple formats (PDF, JSON, Markdown, HTML).

The system will be built using Python 3.9+, distributed via PyPI, and leverage industry-standard tools including Google Lighthouse (via Playwright), BeautifulSoup for HTML parsing, and a custom crawling engine. The architecture prioritizes cross-platform compatibility, maintainability, and extensibility while meeting the performance target of 1-3 minutes for typical sites (5-10 pages).

## 1. System Architecture

### 1.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         CLI Interface                        │
│                    (Click + Rich for UI)                     │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Configuration Manager                      │
│              (Load YAML/JSON, validate settings)             │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     Orchestration Layer                      │
│        (Coordinate crawl → analysis → report flow)           │
└───────────┬───────────────┬─────────────────┬───────────────┘
            │               │                 │
            ▼               ▼                 ▼
    ┌───────────┐   ┌──────────────┐  ┌─────────────┐
    │  Crawler  │   │   Analyzer   │  │   Reporter  │
    │  Engine   │   │   Engine     │  │   Engine    │
    └─────┬─────┘   └──────┬───────┘  └──────┬──────┘
          │                │                  │
          ▼                ▼                  ▼
    ┌─────────────────────────────────────────────┐
    │             Data Models & Storage            │
    │        (In-memory during analysis)           │
    └─────────────────────────────────────────────┘
```

**Architecture Principles:**
1. **Modularity**: Separate concerns (crawl, analyze, report) for maintainability
2. **Sequential Processing**: Single-threaded execution for simplicity and determinism
3. **In-Memory Processing**: No persistent storage; all data held in memory during execution
4. **Error Resilience**: Continue on error, log issues, produce partial results when possible
5. **Cross-Platform**: Avoid platform-specific dependencies; test on Windows, macOS, Linux

### 1.2 Component Breakdown

#### 1.2.1 CLI Interface
- **Framework**: Click (argument parsing, command structure)
- **Progress Display**: Rich library (progress bars, tables, formatted output)
- **Responsibilities**:
  - Parse command-line arguments and flags
  - Load configuration file (YAML/JSON)
  - Display minimal progress indicators (current step only, no percentage)
  - Show errors to stderr
  - Invoke orchestration layer
  - Exit with appropriate codes (0=success, 1=error)

#### 1.2.2 Configuration Manager
- **Format**: YAML (primary) or JSON (fallback)
- **Location**: `~/.config/seo-audit/config.yaml` or project-local `.seo-audit.yaml`
- **Responsibilities**:
  - Load and validate configuration
  - Merge CLI flags with config file (CLI overrides file)
  - Provide defaults for missing values
  - Validate ranges and types

#### 1.2.3 Orchestration Layer
- **Pattern**: Coordinator/Mediator
- **Responsibilities**:
  - Validate input URL
  - Initialize crawler with config
  - Execute crawl phase
  - Pass crawl results to analyzer
  - Execute analysis phase
  - Pass analysis results to reporter
  - Handle errors and produce partial results
  - Manage resource cleanup (browser instances, temp files)

#### 1.2.4 Crawler Engine
- **Core Library**: Playwright (Python)
- **HTML Parser**: BeautifulSoup4 (lxml parser)
- **Responsibilities**:
  - Fetch and render target URL
  - Extract internal links
  - Respect robots.txt
  - Discover pages (breadth-first up to depth limit)
  - Parse sitemap.xml if present
  - Collect raw HTML, headers, metadata
  - Measure basic page metrics (load time, response codes)
  - Return structured crawl data

#### 1.2.5 Analyzer Engine
- **Sub-Analyzers**:
  1. **Performance Analyzer**: Lighthouse (via Playwright) + custom checks
  2. **Crawlability Analyzer**: robots.txt, canonical, redirects, broken links
  3. **On-Page Analyzer**: Title, meta, headings, alt text, HTTPS
  4. **Structured Data Analyzer**: JSON-LD validation, schema detection
- **Responsibilities**:
  - Run all sub-analyzers on crawl data
  - Collect issues from each analyzer
  - Apply false positive filtering (FR-7.6)
  - Assign severity levels (Critical, High, Medium, Low)
  - Calculate overall health score (0-100)
  - Return structured analysis results

#### 1.2.6 Reporter Engine
- **Output Formats**:
  1. **PDF**: WeasyPrint (HTML → PDF conversion)
  2. **HTML**: Jinja2 templates + static CSS
  3. **JSON**: Native Python json module
  4. **Markdown**: Custom template renderer
- **Responsibilities**:
  - Prioritize issues (severity → affected page % → alphabetical)
  - Limit to top 15-20 issues for PDF (all issues for JSON/Markdown)
  - Render report template with analysis data
  - Generate output file(s)
  - Return file paths

### 1.3 Data Flow

```
1. User Input
   ├─ URL: https://example.com
   ├─ CLI Flags: --depth 3 --pages 100 --format pdf,json
   └─ Config File: crawl_delay: 500ms

2. Validation
   └─ URL format check, accessibility test

3. Crawl Phase (Crawler Engine)
   ├─ Fetch homepage
   ├─ Discover links (BFS to depth 3)
   ├─ Parse sitemap.xml
   ├─ Respect robots.txt
   └─ Collect: HTML, headers, status codes, load times

4. Analysis Phase (Analyzer Engine)
   ├─ Performance Analyzer
   │  ├─ Run Lighthouse on key pages
   │  ├─ Measure LCP, CLS, FID/INP, TTFB
   │  └─ Detect oversized resources
   ├─ Crawlability Analyzer
   │  ├─ Parse robots.txt
   │  ├─ Check canonical tags
   │  └─ Detect redirect chains, broken links
   ├─ On-Page Analyzer
   │  ├─ Extract title, meta, headings
   │  ├─ Check HTTPS, mixed content
   │  └─ Validate alt text
   ├─ Structured Data Analyzer
   │  ├─ Extract JSON-LD
   │  ├─ Validate against schema.org
   │  └─ Detect errors
   ├─ False Positive Filtering
   ├─ Severity Assignment
   └─ Health Score Calculation

5. Report Phase (Reporter Engine)
   ├─ Prioritize issues
   ├─ Render HTML report template
   ├─ Convert to PDF (if requested)
   ├─ Generate JSON (if requested)
   ├─ Generate Markdown (if requested)
   └─ Save to output directory

6. Output
   └─ Files: audit-report.pdf, audit-report.json, audit-report.md, audit-report.html
```

## 2. Technology Stack

### 2.1 Core Technologies

| Component | Technology | Version | Justification |
|-----------|-----------|---------|---------------|
| **Runtime** | Python | 3.9+ | Balance of modern features and compatibility; asyncio support; excellent library ecosystem |
| **CLI Framework** | Click | 8.x | Industry standard; intuitive API; automatic help generation; supports nested commands |
| **Progress UI** | Rich | 13.x | Beautiful terminal output; progress bars; tables; error formatting |
| **Browser Automation** | Playwright | 1.4x | Cross-platform; bundles Chromium; better Windows support than Puppeteer; async support |
| **HTML Parsing** | BeautifulSoup4 | 4.12+ | Robust HTML parsing; handles malformed HTML; simple API |
| **HTML Parser Backend** | lxml | 5.x | Fast C-based parser; full XPath support |
| **Performance Analysis** | Lighthouse | 11.x (via Playwright) | Industry standard; comprehensive metrics; official Google tool |
| **HTTP Client** | httpx | 0.27+ | Modern async HTTP; follows redirects; excellent error handling; HTTP/2 support |
| **Configuration** | PyYAML | 6.x | YAML parsing; safe loading; clear syntax |
| **PDF Generation** | WeasyPrint | 60.x | HTML/CSS → PDF; excellent typography; cross-platform; no external dependencies |
| **HTML Templating** | Jinja2 | 3.1+ | Django-style templates; safe by default; powerful filters |
| **Schema Validation** | jsonschema | 4.x | Validate JSON-LD against schema.org; standard implementation |
| **Testing Framework** | pytest | 8.x | De facto standard; excellent fixtures; parametrization; plugins |
| **Logging** | Python logging | stdlib | Standard library; configurable; multiple handlers |

### 2.2 Development & Distribution

| Purpose | Technology | Version | Notes |
|---------|-----------|---------|-------|
| **Package Management** | pip + setuptools | Latest | Standard Python packaging |
| **Distribution** | PyPI | N/A | Public package repository |
| **Entry Point** | Console scripts | setuptools | Install creates `seo-audit` command |
| **Version Management** | setuptools-scm | 8.x | Automatic versioning from git tags |
| **Dependency Pinning** | requirements.txt | N/A | Pin exact versions for reproducibility |
| **Code Formatting** | Black | 24.x | (Optional) Consistent code style |
| **Linting** | Ruff | 0.3+ | (Optional) Fast Python linter |

### 2.3 Third-Party Services (Optional)

| Service | Purpose | Usage | Fallback |
|---------|---------|-------|----------|
| PageSpeed Insights API | Field performance data | Optional via `--use-psi` flag | Local Lighthouse only |
| None | N/A | No other external services | N/A |

## 3. Detailed Component Design

### 3.1 CLI Interface

#### 3.1.1 Command Structure

```bash
seo-audit <URL> [OPTIONS]
```

**Options:**

```
URL
  Required. Target website URL to audit (e.g., https://example.com)

--depth <1-5>
  Crawl depth (default: 3). How many link levels to follow from homepage.

--pages <1-500>
  Maximum pages to crawl (default: 100). Limits scope for large sites.

--output <path>
  Output directory (default: ./reports). Reports saved as audit-report.*

--format <pdf|html|json|md>
  Output formats (default: pdf). Comma-separated for multiple (pdf,json).

--config <path>
  Configuration file path (default: ~/.config/seo-audit/config.yaml)

--timeout <60-1800>
  Maximum audit duration in seconds (default: 900 / 15 minutes)

--user-agent <string>
  Custom user agent (default: "SEOAuditBot/1.0 (+https://github.com/user/seo-audit)")

--crawl-delay <ms>
  Delay between requests in milliseconds (default: 500)

--ignore-robots
  Ignore robots.txt restrictions (use with caution)

--no-headless
  Disable headless browser mode (for debugging rendering issues)

--verbose, -v
  Enable verbose logging (default: errors only)

--version
  Show version and exit

--help, -h
  Show help message and exit
```

**Examples:**

```bash
# Basic audit (PDF output)
seo-audit https://example.com

# Multiple formats with custom output
seo-audit https://example.com --format pdf,json,html --output ./my-reports/

# Deep crawl with verbose logging
seo-audit https://example.com --depth 5 --pages 250 --verbose

# Quick audit for debugging
seo-audit https://example.com --pages 10 --no-headless
```

#### 3.1.2 Exit Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 0 | Success | Audit completed successfully |
| 1 | General Error | Unhandled exception or critical failure |
| 2 | Invalid Input | Malformed URL or invalid configuration |
| 3 | Network Error | Cannot reach target URL (DNS, timeout, connection refused) |
| 4 | Timeout | Audit exceeded maximum duration |
| 5 | Permission Denied | Blocked by robots.txt (when not using --ignore-robots) |

#### 3.1.3 Progress Display

**Minimal Error-Only Output (Default):**
```
Auditing https://example.com...
Error: Failed to crawl https://example.com/page1 (404 Not Found)
Report saved: ./reports/audit-report.pdf
```

**Verbose Output (-v):**
```
[INFO] Loading configuration from ~/.config/seo-audit/config.yaml
[INFO] Starting audit for https://example.com
[INFO] Crawl depth: 3, Max pages: 100
[INFO] Fetching homepage...
[INFO] Discovered 45 internal links
[INFO] Crawling https://example.com/about (1/45)
[INFO] Crawling https://example.com/contact (2/45)
...
[INFO] Crawl complete. 45 pages analyzed.
[INFO] Running Performance Analyzer...
[INFO] Running Lighthouse on 5 key pages...
[INFO] Performance analysis complete (3 issues found)
[INFO] Running Crawlability Analyzer...
[INFO] Crawlability analysis complete (8 issues found)
[INFO] Running On-Page Analyzer...
[INFO] On-page analysis complete (12 issues found)
[INFO] Running Structured Data Analyzer...
[INFO] Structured data analysis complete (2 issues found)
[INFO] Applying false positive filtering...
[INFO] 25 total issues, 22 after filtering
[INFO] Health Score: 67/100 (Fair)
[INFO] Generating PDF report...
[INFO] Generating JSON report...
[INFO] Reports saved to ./reports/
[INFO] Audit complete in 2m 34s
```

### 3.2 Configuration Manager

#### 3.2.1 Configuration File Format

**Default Location**: `~/.config/seo-audit/config.yaml`
**Project Override**: `./.seo-audit.yaml` (in current directory)
**CLI Override**: `--config /path/to/config.yaml`

**Priority Order**: CLI flags > Project config > User config > Defaults

**Example config.yaml:**

```yaml
# Technical SEO Audit System Configuration

# Crawl Settings
crawl:
  depth: 3                    # Link depth to follow (1-5)
  max_pages: 100              # Maximum pages to crawl (1-500)
  delay_ms: 500               # Delay between requests in milliseconds
  timeout_per_page: 30        # Timeout per page in seconds
  respect_robots: true        # Respect robots.txt (boolean)
  user_agent: "SEOAuditBot/1.0 (+https://github.com/user/seo-audit)"

# Browser Settings
browser:
  headless: true              # Run browser in headless mode
  viewport_width: 1920        # Browser viewport width
  viewport_height: 1080       # Browser viewport height
  wait_until: "networkidle"   # Wait condition: load|domcontentloaded|networkidle

# Analysis Settings
analysis:
  run_lighthouse: true        # Run Lighthouse for performance metrics
  lighthouse_pages: 5         # Number of pages to run Lighthouse on
  validate_schema: true       # Validate structured data
  check_broken_links: true    # Check for broken internal links

# Performance Settings
performance:
  max_audit_duration: 900     # Maximum audit time in seconds (15 min)
  max_memory_mb: 2048         # Maximum memory usage in MB

# Output Settings
output:
  directory: "./reports"      # Output directory for reports
  formats:                    # Output formats to generate
    - pdf
    - json
  filename_template: "audit-report-{domain}-{timestamp}"
  pdf_single_page: true       # Fit PDF to single page (truncate issues if needed)
  max_issues_pdf: 20          # Maximum issues to show in PDF

# Logging Settings
logging:
  level: "ERROR"              # ERROR | INFO | DEBUG
  file: null                  # Log file path (null = stdout only)
  format: "[{levelname}] {message}"

# False Positive Filtering
filters:
  exclude_url_patterns:       # URL patterns to exclude from issues
    - "/admin/"
    - "/login/"
    - "/checkout/"
    - "/cart/"
    - "/wp-admin/"
  exclude_noindex_admin: true # Ignore noindex on admin pages
  min_thin_content_words: 200 # Minimum words to not flag as thin content

# Severity Thresholds (from PRD FR-7)
severity:
  critical:
    noindex_threshold: 0.9     # > 90% of pages
    failed_cwv_threshold: 0.5  # > 50% of pages
    no_https_threshold: 0.8    # > 80% of pages
  high:
    duplicate_titles_threshold: 0.5    # > 50% of pages
    redirect_chains_threshold: 0.1     # > 10% of pages
    broken_links_threshold: 0.2        # > 20% of pages
  medium:
    missing_meta_desc_threshold: 0.3   # > 30% of pages
    oversized_images_threshold: 0.4    # > 40% of pages
    heading_issues_threshold: 0.25     # > 25% of pages
  low:
    missing_schema_threshold: 0.25     # > 25% of pages
    thin_content_threshold: 0.1        # > 10% of pages
```

#### 3.2.2 Configuration Validation

The Configuration Manager validates:
- **Types**: Integers, floats, booleans, strings, lists as expected
- **Ranges**: depth (1-5), max_pages (1-500), timeouts (60-1800), etc.
- **Paths**: Output directory is writable
- **URLs**: User agent format is valid
- **Formats**: Output formats are supported (pdf, html, json, md)

**Error Handling**: If configuration is invalid, exit with code 2 and clear error message.

### 3.3 Crawler Engine

#### 3.3.1 Crawler Architecture

**Class: `WebsiteCrawler`**

```python
class WebsiteCrawler:
    """
    Crawls a website and collects page data for analysis.

    Uses Playwright for rendering JavaScript-heavy sites and
    BeautifulSoup for HTML parsing.
    """

    def __init__(self, config: CrawlConfig):
        """Initialize crawler with configuration."""
        self.config = config
        self.browser = None
        self.visited_urls = set()
        self.pages = []
        self.robots_txt = None

    async def crawl(self, start_url: str) -> CrawlResult:
        """
        Crawl website starting from start_url.

        Returns:
            CrawlResult containing all discovered pages and metadata
        """
        # 1. Validate and normalize URL
        # 2. Fetch robots.txt
        # 3. Launch browser
        # 4. Crawl homepage
        # 5. Discover and crawl internal links (BFS)
        # 6. Fetch and parse sitemap.xml
        # 7. Close browser
        # 8. Return CrawlResult

    async def fetch_page(self, url: str) -> PageData:
        """Fetch and parse a single page."""
        # 1. Check robots.txt
        # 2. Wait crawl_delay
        # 3. Navigate to URL with Playwright
        # 4. Wait for page load (networkidle)
        # 5. Extract HTML, headers, status code
        # 6. Parse with BeautifulSoup
        # 7. Extract links, images, meta tags
        # 8. Return PageData

    def extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract and normalize internal links."""
        # Find all <a> tags
        # Resolve relative URLs
        # Filter to same domain only
        # Remove fragments and query params (optional)
        # Deduplicate

    def fetch_robots_txt(self, base_url: str) -> RobotsTxt:
        """Fetch and parse robots.txt."""

    def fetch_sitemap(self, base_url: str) -> Sitemap:
        """Fetch and parse sitemap.xml."""
```

**Data Models:**

```python
@dataclass
class PageData:
    """Data collected for a single page."""
    url: str
    status_code: int
    final_url: str  # After redirects
    html: str
    headers: Dict[str, str]
    load_time_ms: int
    response_size_bytes: int

    # Parsed elements
    title: Optional[str]
    meta_description: Optional[str]
    meta_robots: Optional[str]
    canonical: Optional[str]
    h1_tags: List[str]
    h2_tags: List[str]
    images: List[ImageData]
    links: List[LinkData]
    scripts: List[str]
    stylesheets: List[str]
    structured_data: List[Dict]  # JSON-LD objects

    # Metrics
    word_count: int
    has_https: bool
    has_mixed_content: bool

    # Errors
    errors: List[str]

@dataclass
class CrawlResult:
    """Result of website crawl."""
    start_url: str
    pages: List[PageData]
    robots_txt: Optional[RobotsTxt]
    sitemap: Optional[Sitemap]
    crawl_duration_seconds: float
    total_pages_discovered: int
    total_pages_crawled: int
    errors: List[CrawlError]
```

#### 3.3.2 Crawl Algorithm

**Strategy**: Breadth-First Search (BFS) with depth limit

```
1. Initialize queue with [start_url] at depth 0
2. While queue not empty AND pages_crawled < max_pages:
   a. Dequeue (url, depth)
   b. If url visited OR depth > max_depth: skip
   c. If robots.txt disallows url AND respect_robots: skip
   d. Fetch and parse page
   e. Add to visited_urls
   f. If depth < max_depth:
      - Extract links
      - Enqueue links at depth + 1
   g. Store PageData
3. Return CrawlResult
```

**Performance Optimizations:**
- **Sequential execution**: Simple, deterministic, avoids rate limiting issues
- **Crawl delay**: Configurable delay (default 500ms) between requests
- **Early termination**: Stop if max_pages reached
- **Timeout per page**: Skip pages that hang (default 30s timeout)

#### 3.3.3 Robots.txt Handling

**Parser**: Use `robotexclusionrulesparser` library or custom implementation

```python
class RobotsTxtParser:
    def __init__(self, robots_txt_content: str):
        # Parse Disallow, Allow, Crawl-delay directives
        # Match user agent (SEOAuditBot or *)

    def is_allowed(self, url: str) -> bool:
        """Check if URL is allowed for our user agent."""

    def get_crawl_delay(self) -> Optional[float]:
        """Get crawl delay for our user agent (if specified)."""
```

**Behavior:**
- Fetch `robots.txt` from `<domain>/robots.txt`
- If 404: Assume no restrictions
- If 5xx: Log warning, proceed cautiously (assume allowed)
- If `--ignore-robots` flag: Skip robots.txt checks entirely

#### 3.3.4 Sitemap Handling

**Parser**: Use `xml.etree.ElementTree` (stdlib)

```python
def parse_sitemap(xml_content: str) -> List[str]:
    """Parse sitemap.xml and return list of URLs."""
    # Parse XML
    # Extract <loc> elements
    # Support <sitemapindex> (nested sitemaps)
    # Return URLs
```

**Discovery:**
1. Check `<domain>/sitemap.xml`
2. Check robots.txt for `Sitemap:` directive
3. Check common locations: `/sitemap_index.xml`, `/sitemap1.xml`

**Usage:**
- Supplement crawled URLs with sitemap URLs
- Prioritize sitemap URLs if crawl hits page limit
- Report sitemap presence/absence as issue

### 3.4 Analyzer Engine

#### 3.4.1 Analyzer Architecture

**Class: `SEOAnalyzer`**

```python
class SEOAnalyzer:
    """Coordinates all sub-analyzers and produces analysis result."""

    def __init__(self, config: AnalysisConfig):
        self.config = config
        self.performance_analyzer = PerformanceAnalyzer(config)
        self.crawlability_analyzer = CrawlabilityAnalyzer(config)
        self.onpage_analyzer = OnPageAnalyzer(config)
        self.schema_analyzer = SchemaAnalyzer(config)
        self.false_positive_filter = FalsePositiveFilter(config)

    def analyze(self, crawl_result: CrawlResult) -> AnalysisResult:
        """Run all analyzers and return issues."""
        issues = []

        # Run sub-analyzers
        issues.extend(self.performance_analyzer.analyze(crawl_result))
        issues.extend(self.crawlability_analyzer.analyze(crawl_result))
        issues.extend(self.onpage_analyzer.analyze(crawl_result))
        issues.extend(self.schema_analyzer.analyze(crawl_result))

        # Filter false positives
        issues = self.false_positive_filter.filter(issues, crawl_result)

        # Assign severity
        issues = self.assign_severity(issues, crawl_result)

        # Calculate health score
        health_score = self.calculate_health_score(issues)

        return AnalysisResult(
            issues=issues,
            health_score=health_score,
            total_pages=len(crawl_result.pages),
            analysis_duration_seconds=time.time() - start_time
        )
```

**Data Models:**

```python
@dataclass
class Issue:
    """Represents a detected SEO issue."""
    id: str  # Unique identifier (e.g., "missing-meta-description")
    title: str  # Display title
    category: str  # Performance | Crawlability | OnPage | StructuredData
    severity: str  # Critical | High | Medium | Low
    description: str  # Client-friendly explanation
    remediation: str  # How to fix
    affected_pages: List[str]  # URLs affected
    affected_count: int
    affected_percentage: float
    details: Dict[str, Any]  # Additional context

@dataclass
class AnalysisResult:
    """Result of SEO analysis."""
    issues: List[Issue]
    health_score: int  # 0-100
    total_pages: int
    analysis_duration_seconds: float
```

#### 3.4.2 Performance Analyzer

**Responsibilities** (FR-3):
- Measure Core Web Vitals (LCP, CLS, FID/INP, TTFB)
- Detect oversized resources (images > 100KB, scripts > 50KB)
- Identify render-blocking resources
- Check image optimization (format, compression, lazy loading)

**Implementation:**

```python
class PerformanceAnalyzer:
    def analyze(self, crawl_result: CrawlResult) -> List[Issue]:
        issues = []

        # Select pages for Lighthouse (default: 5 key pages)
        key_pages = self.select_key_pages(crawl_result)

        # Run Lighthouse on key pages
        lighthouse_results = []
        for page in key_pages:
            result = self.run_lighthouse(page.url)
            lighthouse_results.append(result)

        # Analyze Core Web Vitals
        issues.extend(self.check_core_web_vitals(lighthouse_results))

        # Check resource sizes (all pages)
        issues.extend(self.check_resource_sizes(crawl_result.pages))

        # Check image optimization
        issues.extend(self.check_image_optimization(crawl_result.pages))

        # Check render-blocking resources
        issues.extend(self.check_render_blocking(lighthouse_results))

        return issues

    def run_lighthouse(self, url: str) -> Dict:
        """Run Lighthouse via Playwright."""
        # Use Playwright's Lighthouse integration
        # Or subprocess call to `lighthouse` CLI
        # Return metrics: LCP, CLS, FID, TTFB, scores

    def select_key_pages(self, crawl_result: CrawlResult) -> List[PageData]:
        """Select pages to run Lighthouse on."""
        # Priority: Homepage, highest traffic (from sitemap priority), key templates
        # Default: Homepage + 4 random pages
```

**Lighthouse Integration:**

Two options:
1. **Playwright + Lighthouse CLI** (subprocess):
   ```python
   subprocess.run([
       "lighthouse", url,
       "--output=json",
       "--chrome-flags='--headless'",
       "--only-categories=performance"
   ])
   ```

2. **lighthouse-python library** (if available):
   ```python
   from lighthouse import run_lighthouse
   result = run_lighthouse(url, headless=True)
   ```

**Metrics Collected:**
- **LCP** (Largest Contentful Paint): Target < 2.5s (Good), < 4.0s (Needs Improvement), > 4.0s (Poor)
- **CLS** (Cumulative Layout Shift): Target < 0.1 (Good), < 0.25 (Needs Improvement), > 0.25 (Poor)
- **FID/INP** (First Input Delay / Interaction to Next Paint): Target < 100ms (Good), < 300ms (Needs Improvement), > 300ms (Poor)
- **TTFB** (Time to First Byte): Target < 800ms (Good), < 1800ms (Needs Improvement), > 1800ms (Poor)

**Issue Detection Examples:**

| Issue ID | Condition | Severity Threshold (from config) |
|----------|-----------|----------------------------------|
| `failed-lcp` | LCP > 4.0s on X% of pages | Critical if > 50%, High if > 25% |
| `failed-cls` | CLS > 0.25 on X% of pages | Critical if > 50%, High if > 25% |
| `oversized-images` | Images > 100KB on X% of pages | Medium if > 40% |
| `no-lazy-loading` | Below-fold images without lazy attr | Medium if > 30% |
| `render-blocking-resources` | Blocking CSS/JS detected | High if > 20% of pages |

#### 3.4.3 Crawlability Analyzer

**Responsibilities** (FR-4):
- Parse robots.txt
- Detect noindex/nofollow directives
- Validate canonical tags
- Check XML sitemap presence
- Detect orphaned pages
- Identify redirect chains and loops
- Find broken internal links

**Implementation:**

```python
class CrawlabilityAnalyzer:
    def analyze(self, crawl_result: CrawlResult) -> List[Issue]:
        issues = []

        # Robots.txt analysis
        issues.extend(self.check_robots_txt(crawl_result))

        # Meta robots
        issues.extend(self.check_meta_robots(crawl_result.pages))

        # Canonical tags
        issues.extend(self.check_canonicals(crawl_result.pages))

        # Sitemap
        issues.extend(self.check_sitemap(crawl_result))

        # Orphaned pages
        issues.extend(self.check_orphaned_pages(crawl_result))

        # Redirects
        issues.extend(self.check_redirects(crawl_result.pages))

        # Broken links
        issues.extend(self.check_broken_links(crawl_result.pages))

        return issues

    def check_meta_robots(self, pages: List[PageData]) -> List[Issue]:
        """Detect pages with noindex/nofollow."""
        noindex_pages = [p for p in pages if 'noindex' in (p.meta_robots or '')]

        if len(noindex_pages) / len(pages) > 0.9:
            # Critical: Site-wide noindex
            return [Issue(
                id='site-wide-noindex',
                title='Site-Wide Noindex Detected',
                category='Crawlability',
                severity='Critical',
                description='Over 90% of pages have noindex meta tag, preventing indexing.',
                remediation='Remove noindex tags unless pages are intentionally excluded.',
                affected_pages=[p.url for p in noindex_pages[:10]],
                affected_count=len(noindex_pages),
                affected_percentage=len(noindex_pages) / len(pages)
            )]
        elif len(noindex_pages) > 0:
            # Informational: Some pages noindex (may be intentional)
            return [Issue(
                id='noindex-pages',
                title='Pages with Noindex Tag',
                category='Crawlability',
                severity='Low',
                description=f'{len(noindex_pages)} pages have noindex (verify intentional).',
                remediation='Review pages and remove noindex if unintended.',
                affected_pages=[p.url for p in noindex_pages],
                affected_count=len(noindex_pages),
                affected_percentage=len(noindex_pages) / len(pages)
            )]

        return []

    def check_redirects(self, pages: List[PageData]) -> List[Issue]:
        """Detect redirect chains."""
        # Build redirect graph: original_url -> final_url
        # Detect chains > 2 redirects
        # Detect loops (cycle detection)
```

**Redirect Chain Detection:**

```
Example redirect chain:
  A -> B -> C -> D (3 redirects, problematic)

Detection:
  1. Track redirect history during crawl
  2. Count hops from original URL to final URL
  3. Flag if hops > 2
```

**Orphaned Page Detection:**

```
Algorithm:
  1. Build link graph: page_url -> [linked_urls]
  2. Find pages in crawl_result.pages not in any linked_urls list
  3. Exclude homepage (always linked externally)
```

#### 3.4.4 On-Page Analyzer

**Responsibilities** (FR-5):
- Extract and evaluate title tags (length, uniqueness)
- Extract and evaluate meta descriptions (length, uniqueness)
- Analyze heading structure (H1 presence, hierarchy)
- Detect missing alt text
- Check HTTPS usage and mixed content
- Detect duplicate content
- Identify thin content pages

**Implementation:**

```python
class OnPageAnalyzer:
    def analyze(self, crawl_result: CrawlResult) -> List[Issue]:
        issues = []

        pages = crawl_result.pages

        # Title tags
        issues.extend(self.check_titles(pages))

        # Meta descriptions
        issues.extend(self.check_meta_descriptions(pages))

        # Heading structure
        issues.extend(self.check_headings(pages))

        # Alt text
        issues.extend(self.check_alt_text(pages))

        # HTTPS
        issues.extend(self.check_https(pages))

        # Duplicate content
        issues.extend(self.check_duplicates(pages))

        # Thin content
        issues.extend(self.check_thin_content(pages))

        return issues

    def check_titles(self, pages: List[PageData]) -> List[Issue]:
        """Check title tag quality."""
        issues = []

        # Missing titles
        missing = [p for p in pages if not p.title or p.title.strip() == '']
        if missing:
            issues.append(Issue(
                id='missing-title',
                title='Missing Title Tags',
                category='OnPage',
                severity='High' if len(missing) / len(pages) > 0.5 else 'Medium',
                description=f'{len(missing)} pages missing title tags.',
                remediation='Add descriptive title tags to all pages.',
                affected_pages=[p.url for p in missing],
                affected_count=len(missing),
                affected_percentage=len(missing) / len(pages)
            ))

        # Duplicate titles
        title_counts = {}
        for page in pages:
            if page.title:
                title_counts[page.title] = title_counts.get(page.title, 0) + 1

        duplicates = {title: count for title, count in title_counts.items() if count > 1}
        if duplicates and len(duplicates) / len(pages) > 0.5:
            issues.append(Issue(
                id='duplicate-titles',
                title='Duplicate Title Tags',
                category='OnPage',
                severity='High',
                description=f'{len(duplicates)} duplicate title tags found.',
                remediation='Ensure each page has a unique title tag.',
                affected_pages=[],  # List would be too long
                affected_count=sum(duplicates.values()),
                affected_percentage=sum(duplicates.values()) / len(pages)
            ))

        # Title length
        too_short = [p for p in pages if p.title and len(p.title) < 30]
        too_long = [p for p in pages if p.title and len(p.title) > 60]
        # ... similar Issue creation

        return issues

    def check_thin_content(self, pages: List[PageData]) -> List[Issue]:
        """Identify thin content pages (< 200 words)."""
        thin_pages = [p for p in pages if p.word_count < 200]

        # Apply false positive filtering early
        # Exclude admin/checkout/cart pages
        thin_pages = [
            p for p in thin_pages
            if not any(pattern in p.url for pattern in ['/admin/', '/login/', '/checkout/', '/cart/'])
        ]

        if len(thin_pages) / len(pages) > 0.1:  # > 10%
            return [Issue(
                id='thin-content',
                title='Thin Content Pages',
                category='OnPage',
                severity='Low',
                description=f'{len(thin_pages)} pages have less than 200 words.',
                remediation='Add more substantive content or consolidate pages.',
                affected_pages=[p.url for p in thin_pages],
                affected_count=len(thin_pages),
                affected_percentage=len(thin_pages) / len(pages)
            )]

        return []
```

**Title Tag Guidelines:**
- **Optimal Length**: 50-60 characters (Google typically displays first 50-60 chars)
- **Uniqueness**: Each page should have unique title
- **Presence**: All pages must have title

**Meta Description Guidelines:**
- **Optimal Length**: 150-160 characters
- **Uniqueness**: Preferred but not critical
- **Presence**: All pages should have meta description

**Heading Structure:**
- **H1**: Exactly one per page (SEO best practice)
- **Hierarchy**: No skipped levels (H1 -> H3 without H2 is violation)

#### 3.4.5 Structured Data Analyzer

**Responsibilities** (FR-6):
- Detect structured data formats (JSON-LD, Microdata, RDFa)
- Validate JSON-LD against schema.org
- Identify schema types used
- Detect syntax errors
- Check for key schema types on relevant pages

**Implementation:**

```python
class SchemaAnalyzer:
    def __init__(self, config: AnalysisConfig):
        self.config = config
        # Load schema.org JSON-LD schemas for validation
        self.validator = jsonschema.Draft7Validator

    def analyze(self, crawl_result: CrawlResult) -> List[Issue]:
        issues = []

        pages = crawl_result.pages

        # Detect presence
        pages_with_schema = [p for p in pages if p.structured_data]

        if len(pages_with_schema) == 0:
            issues.append(Issue(
                id='no-structured-data',
                title='No Structured Data Detected',
                category='StructuredData',
                severity='Medium',
                description='No structured data found on any page.',
                remediation='Add JSON-LD schema markup for better search visibility.',
                affected_pages=[],
                affected_count=len(pages),
                affected_percentage=1.0
            ))

        # Validate syntax
        for page in pages_with_schema:
            for schema_obj in page.structured_data:
                validation_errors = self.validate_schema(schema_obj)
                if validation_errors:
                    issues.append(Issue(
                        id='invalid-schema-syntax',
                        title='Invalid Structured Data Syntax',
                        category='StructuredData',
                        severity='High',
                        description=f'Schema errors on {page.url}',
                        remediation='Fix JSON-LD syntax errors using schema.org validator.',
                        affected_pages=[page.url],
                        affected_count=1,
                        affected_percentage=1 / len(pages),
                        details={'errors': validation_errors}
                    ))

        # Check for key schema types
        # Example: Product pages should have Product schema
        # This requires heuristics or configuration

        return issues

    def validate_schema(self, schema_obj: Dict) -> List[str]:
        """Validate JSON-LD against schema.org."""
        errors = []

        # Basic JSON-LD structure checks
        if '@context' not in schema_obj:
            errors.append('Missing @context')

        if '@type' not in schema_obj:
            errors.append('Missing @type')

        # Type-specific validation
        schema_type = schema_obj.get('@type')
        if schema_type == 'Organization':
            if 'name' not in schema_obj:
                errors.append('Organization missing required "name" property')
        elif schema_type == 'Product':
            if 'name' not in schema_obj:
                errors.append('Product missing required "name" property')
            if 'offers' not in schema_obj:
                errors.append('Product missing required "offers" property')
        # ... more types

        return errors
```

**Supported Schema Types (Priority):**
1. **Organization**: Company info
2. **Product**: E-commerce products
3. **Article**: Blog posts, news
4. **LocalBusiness**: Local businesses
5. **Breadcrumb**: Navigation breadcrumbs
6. **FAQ**: Frequently asked questions
7. **Review**: Product/service reviews

**Validation Strategy:**
- **JSON-LD**: Parse JSON, validate structure against schema.org specs (local validation)
- **Microdata/RDFa**: Extract with `extruct` library (more complex parsing)
- **Priority**: JSON-LD preferred (simplest to validate); Microdata/RDFa detection only

#### 3.4.6 False Positive Filtering

**Purpose**: Reduce noise by excluding common non-issues (FR-7.6)

**Filter Rules** (from PRD):
1. **Intentional noindex**: Exclude admin/login/checkout pages from noindex Critical issues
2. **URL pattern exclusions**: `/admin/`, `/login/`, `/checkout/`, `/cart/`, `/wp-admin/`
3. **Thin content exceptions**: Utility pages with low word count are expected
4. **Redirect chains for tracking**: Verify consistent redirect patterns (harder, v2 feature)

**Implementation:**

```python
class FalsePositiveFilter:
    def __init__(self, config: AnalysisConfig):
        self.exclude_patterns = config.filters.exclude_url_patterns

    def filter(self, issues: List[Issue], crawl_result: CrawlResult) -> List[Issue]:
        """Remove false positive issues."""
        filtered = []

        for issue in issues:
            if self.is_false_positive(issue, crawl_result):
                continue  # Skip this issue

            # Filter affected pages
            issue.affected_pages = [
                url for url in issue.affected_pages
                if not self.is_excluded_url(url)
            ]
            issue.affected_count = len(issue.affected_pages)
            issue.affected_percentage = len(issue.affected_pages) / len(crawl_result.pages)

            # If no affected pages remain, skip issue
            if issue.affected_count == 0:
                continue

            filtered.append(issue)

        return filtered

    def is_false_positive(self, issue: Issue, crawl_result: CrawlResult) -> bool:
        """Determine if issue is a false positive."""

        # Rule 1: Noindex on admin pages is expected
        if issue.id == 'site-wide-noindex':
            # Check if all noindex pages match exclude patterns
            noindex_pages = issue.affected_pages
            excluded = [p for p in noindex_pages if self.is_excluded_url(p)]
            if len(excluded) == len(noindex_pages):
                return True  # All noindex pages are admin/utility pages

        # Rule 2: Thin content on utility pages is expected
        if issue.id == 'thin-content':
            # Already filtered in OnPageAnalyzer.check_thin_content()
            pass

        return False

    def is_excluded_url(self, url: str) -> bool:
        """Check if URL matches exclude patterns."""
        return any(pattern in url for pattern in self.exclude_patterns)
```

#### 3.4.7 Severity Assignment

**Severity Levels**: Critical, High, Medium, Low

**Assignment Logic** (FR-7 from PRD):

| Severity | Criteria |
|----------|----------|
| **Critical** | - Site-wide noindex (> 90% of pages)<br>- Broken homepage<br>- Failed Core Web Vitals (> 50% of pages)<br>- Missing HTTPS (> 80% of pages) |
| **High** | - Missing XML sitemap<br>- Widespread duplicate titles (> 50%)<br>- Redirect chains (> 10%)<br>- Broken internal links (> 20%) |
| **Medium** | - Missing meta descriptions (> 30%)<br>- Oversized images (> 40%)<br>- Heading hierarchy issues (> 25%)<br>- Missing structured data on key pages |
| **Low** | - Missing schema (< 25% of pages)<br>- Thin content on non-critical pages (< 10%)<br>- Suboptimal image formats (< 30%) |

**Implementation:**

```python
def assign_severity(self, issues: List[Issue], crawl_result: CrawlResult) -> List[Issue]:
    """Assign severity based on thresholds."""

    thresholds = self.config.severity

    for issue in issues:
        percentage = issue.affected_percentage

        # Use issue-specific thresholds from config
        if issue.id == 'site-wide-noindex':
            if percentage > thresholds.critical.noindex_threshold:
                issue.severity = 'Critical'
        elif issue.id == 'duplicate-titles':
            if percentage > thresholds.high.duplicate_titles_threshold:
                issue.severity = 'High'
        # ... more rules

        # Default severity based on category and percentage
        if not issue.severity:
            issue.severity = self.default_severity(issue, percentage)

    return issues
```

#### 3.4.8 Health Score Calculation

**Formula** (from PRD FR-8.9):

```
Score = 100 - (Critical × 15) - (High × 8) - (Medium × 3) - (Low × 1)
Minimum: 0, Maximum: 100
```

**Grade Mapping:**
- **90-100**: Excellent (Green)
- **70-89**: Good (Yellow-Green)
- **50-69**: Fair (Orange)
- **0-49**: Poor (Red)

**Implementation:**

```python
def calculate_health_score(self, issues: List[Issue]) -> int:
    """Calculate overall health score (0-100)."""

    critical_count = sum(1 for i in issues if i.severity == 'Critical')
    high_count = sum(1 for i in issues if i.severity == 'High')
    medium_count = sum(1 for i in issues if i.severity == 'Medium')
    low_count = sum(1 for i in issues if i.severity == 'Low')

    score = 100 - (critical_count * 15) - (high_count * 8) - (medium_count * 3) - (low_count * 1)

    return max(0, min(100, score))  # Clamp to 0-100
```

### 3.5 Reporter Engine

#### 3.5.1 Reporter Architecture

**Class: `ReportGenerator`**

```python
class ReportGenerator:
    """Generates reports in multiple formats."""

    def __init__(self, config: ReportConfig):
        self.config = config
        self.template_env = self.setup_jinja_env()

    def generate_reports(self, analysis_result: AnalysisResult, crawl_result: CrawlResult) -> List[str]:
        """Generate all requested report formats."""
        output_files = []

        formats = self.config.formats

        if 'json' in formats:
            output_files.append(self.generate_json(analysis_result, crawl_result))

        if 'md' in formats or 'markdown' in formats:
            output_files.append(self.generate_markdown(analysis_result, crawl_result))

        if 'html' in formats:
            output_files.append(self.generate_html(analysis_result, crawl_result))

        if 'pdf' in formats:
            output_files.append(self.generate_pdf(analysis_result, crawl_result))

        return output_files

    def generate_json(self, analysis: AnalysisResult, crawl: CrawlResult) -> str:
        """Generate JSON report."""
        # Serialize to JSON
        # Include all issues (no truncation)
        # Include metadata

    def generate_markdown(self, analysis: AnalysisResult, crawl: CrawlResult) -> str:
        """Generate Markdown report."""
        # Use Markdown template
        # Include all issues

    def generate_html(self, analysis: AnalysisResult, crawl: CrawlResult) -> str:
        """Generate HTML report."""
        # Use Jinja2 template
        # Embed CSS (no external dependencies)
        # Include all issues with collapsible sections

    def generate_pdf(self, analysis: AnalysisResult, crawl: CrawlResult) -> str:
        """Generate PDF report."""
        # Generate HTML first (using PDF-specific template)
        # Convert to PDF with WeasyPrint
        # Fit to single page (limit to top 15-20 issues)
```

#### 3.5.2 Issue Prioritization

**Prioritization Rules** (from PRD FR-7.5):
1. **By Severity**: Critical > High > Medium > Low
2. **By Affected %**: Higher percentage first (within same severity)
3. **By Title**: Alphabetical (tie-breaker)

**Implementation:**

```python
def prioritize_issues(issues: List[Issue]) -> List[Issue]:
    """Sort issues by priority."""

    severity_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}

    return sorted(issues, key=lambda i: (
        severity_order[i.severity],
        -i.affected_percentage,  # Negative for descending order
        i.title
    ))
```

**PDF Truncation:**
- Limit to top 15-20 issues (configurable via `max_issues_pdf`)
- Include note: "Showing top 20 issues. Full list available in JSON/HTML report."

#### 3.5.3 JSON Report Format

**Structure:**

```json
{
  "meta": {
    "tool_name": "Technical SEO Audit System",
    "tool_version": "1.0.0",
    "audit_timestamp": "2026-01-16T14:23:45Z",
    "audit_duration_seconds": 154.3
  },
  "target": {
    "start_url": "https://example.com",
    "final_url": "https://www.example.com",
    "domain": "example.com"
  },
  "crawl_summary": {
    "total_pages_discovered": 45,
    "total_pages_crawled": 45,
    "crawl_depth": 3,
    "crawl_duration_seconds": 67.2,
    "robots_txt_present": true,
    "sitemap_present": true,
    "errors": []
  },
  "analysis_summary": {
    "health_score": 67,
    "health_grade": "Fair",
    "total_issues": 22,
    "critical_issues": 1,
    "high_issues": 5,
    "medium_issues": 10,
    "low_issues": 6,
    "analysis_duration_seconds": 87.1
  },
  "issues": [
    {
      "id": "site-wide-noindex",
      "title": "Site-Wide Noindex Detected",
      "category": "Crawlability",
      "severity": "Critical",
      "description": "Over 90% of pages have noindex meta tag, preventing indexing.",
      "remediation": "Remove noindex tags unless pages are intentionally excluded.",
      "affected_count": 42,
      "affected_percentage": 0.933,
      "affected_pages": [
        "https://example.com/page1",
        "https://example.com/page2"
      ],
      "details": {}
    }
  ],
  "pages": [
    {
      "url": "https://example.com",
      "status_code": 200,
      "title": "Example Domain",
      "meta_description": "Example domain for testing.",
      "word_count": 450,
      "load_time_ms": 1234,
      "has_https": true,
      "h1_tags": ["Welcome to Example"],
      "issues": ["missing-meta-description"]
    }
  ]
}
```

#### 3.5.4 Markdown Report Format

**Structure:**

```markdown
# Technical SEO Audit Report

**Audited Site:** https://example.com
**Audit Date:** 2026-01-16 14:23:45 UTC
**Tool Version:** 1.0.0

---

## Summary

- **Health Score:** 67/100 (Fair)
- **Total Issues:** 22 (1 Critical, 5 High, 10 Medium, 6 Low)
- **Pages Crawled:** 45
- **Audit Duration:** 2m 34s

---

## Issues

### Critical Issues (1)

#### 1. Site-Wide Noindex Detected

**Category:** Crawlability
**Affected Pages:** 42 (93.3%)

**Description:** Over 90% of pages have noindex meta tag, preventing indexing.

**Remediation:** Remove noindex tags unless pages are intentionally excluded.

**Affected URLs:**
- https://example.com/page1
- https://example.com/page2
- ... (see JSON report for full list)

---

### High Issues (5)

#### 2. Duplicate Title Tags
...
```

#### 3.5.5 HTML Report Format

**Template Structure** (Jinja2):

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO Audit Report - {{ target_url }}</title>
    <style>
        /* Embed CSS directly (no external files) */
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
        .health-score { font-size: 48px; font-weight: bold; }
        .score-excellent { color: #10b981; }
        .score-good { color: #84cc16; }
        .score-fair { color: #f59e0b; }
        .score-poor { color: #ef4444; }
        .severity-badge { padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 600; }
        .severity-critical { background: #fecaca; color: #991b1b; }
        .severity-high { background: #fed7aa; color: #9a3412; }
        .severity-medium { background: #fef3c7; color: #92400e; }
        .severity-low { background: #e5e7eb; color: #374151; }
        .issue { margin-bottom: 24px; padding: 16px; border: 1px solid #e5e7eb; border-radius: 8px; }
        .issue-title { font-size: 18px; font-weight: 600; margin-bottom: 8px; }
        details { margin-top: 8px; }
    </style>
</head>
<body>
    <header>
        <h1>Technical SEO Audit Report</h1>
        <p><strong>Audited Site:</strong> {{ target_url }}</p>
        <p><strong>Audit Date:</strong> {{ audit_timestamp }}</p>
    </header>

    <section class="summary">
        <h2>Summary</h2>
        <div class="health-score score-{{ health_grade|lower }}">
            {{ health_score }}/100
        </div>
        <p><strong>Grade:</strong> {{ health_grade }}</p>
        <p><strong>Total Issues:</strong> {{ total_issues }}
           ({{ critical_count }} Critical, {{ high_count }} High,
            {{ medium_count }} Medium, {{ low_count }} Low)</p>
        <p><strong>Pages Crawled:</strong> {{ total_pages }}</p>
    </section>

    <section class="issues">
        <h2>Issues</h2>

        {% for issue in issues %}
        <div class="issue">
            <div class="issue-header">
                <span class="severity-badge severity-{{ issue.severity|lower }}">
                    {{ issue.severity }}
                </span>
                <span class="issue-title">{{ loop.index }}. {{ issue.title }}</span>
            </div>
            <p><strong>Category:</strong> {{ issue.category }}</p>
            <p><strong>Affected Pages:</strong> {{ issue.affected_count }} ({{ (issue.affected_percentage * 100)|round(1) }}%)</p>
            <p><strong>Description:</strong> {{ issue.description }}</p>
            <p><strong>Remediation:</strong> {{ issue.remediation }}</p>

            <details>
                <summary>Affected URLs ({{ issue.affected_pages|length }} shown)</summary>
                <ul>
                {% for url in issue.affected_pages[:50] %}
                    <li><code>{{ url }}</code></li>
                {% endfor %}
                {% if issue.affected_pages|length > 50 %}
                    <li><em>... and {{ issue.affected_pages|length - 50 }} more (see JSON report)</em></li>
                {% endif %}
                </ul>
            </details>
        </div>
        {% endfor %}
    </section>

    <footer>
        <p><small>Generated by Technical SEO Audit System v{{ tool_version }} |
        <a href="https://github.com/user/seo-audit">View on GitHub</a></small></p>
    </footer>
</body>
</html>
```

**Features:**
- **Self-contained**: All CSS embedded (no external files)
- **Responsive**: Mobile-friendly layout
- **Interactive**: Collapsible affected URLs with `<details>`
- **Color-coded**: Health score and severity badges

#### 3.5.6 PDF Report Format

**Generation Strategy:**
1. Render HTML using PDF-specific Jinja2 template
2. Apply CSS optimized for single-page printing
3. Convert HTML → PDF using WeasyPrint
4. Limit to top 15-20 issues (configurable)

**PDF Template Differences from HTML:**
- **Single column layout** (no multi-column for simpler layout)
- **Compact spacing** (reduce margins, padding)
- **Truncate affected URLs** (show only 3-5 URLs per issue)
- **Page break control** (CSS `page-break-inside: avoid` on issues)
- **Footer on bottom** (not sticky, just at end)

**WeasyPrint Usage:**

```python
from weasyprint import HTML, CSS

def generate_pdf(html_content: str, output_path: str):
    """Convert HTML to PDF."""

    # Custom CSS for PDF rendering
    pdf_css = CSS(string='''
        @page {
            size: Letter;
            margin: 0.5in;
        }
        body {
            font-size: 10pt;
        }
        .issue {
            page-break-inside: avoid;
        }
    ''')

    HTML(string=html_content).write_pdf(
        output_path,
        stylesheets=[pdf_css]
    )
```

**Single-Page Constraint:**
- **Font size**: 10pt (readable but compact)
- **Margins**: 0.5in all sides
- **Issue limit**: Top 15-20 issues (configurable, default 20)
- **Note if truncated**: "Showing top 20 issues. Full list in JSON/HTML report."

## 4. Data Models

### 4.1 Configuration Models

```python
@dataclass
class CrawlConfig:
    depth: int = 3
    max_pages: int = 100
    delay_ms: int = 500
    timeout_per_page: int = 30
    respect_robots: bool = True
    user_agent: str = "SEOAuditBot/1.0"
    ignore_robots: bool = False

@dataclass
class BrowserConfig:
    headless: bool = True
    viewport_width: int = 1920
    viewport_height: int = 1080
    wait_until: str = "networkidle"

@dataclass
class AnalysisConfig:
    run_lighthouse: bool = True
    lighthouse_pages: int = 5
    validate_schema: bool = True
    check_broken_links: bool = True

@dataclass
class ReportConfig:
    directory: str = "./reports"
    formats: List[str] = field(default_factory=lambda: ["pdf"])
    filename_template: str = "audit-report-{domain}-{timestamp}"
    max_issues_pdf: int = 20
```

### 4.2 Crawl Models

```python
@dataclass
class PageData:
    url: str
    status_code: int
    final_url: str
    html: str
    headers: Dict[str, str]
    load_time_ms: int
    response_size_bytes: int

    # Parsed elements
    title: Optional[str] = None
    meta_description: Optional[str] = None
    meta_robots: Optional[str] = None
    canonical: Optional[str] = None
    h1_tags: List[str] = field(default_factory=list)
    h2_tags: List[str] = field(default_factory=list)
    images: List[Dict] = field(default_factory=list)
    links: List[Dict] = field(default_factory=list)
    scripts: List[str] = field(default_factory=list)
    stylesheets: List[str] = field(default_factory=list)
    structured_data: List[Dict] = field(default_factory=list)

    word_count: int = 0
    has_https: bool = False
    has_mixed_content: bool = False

    errors: List[str] = field(default_factory=list)

@dataclass
class CrawlResult:
    start_url: str
    pages: List[PageData]
    robots_txt: Optional[str] = None
    sitemap: Optional[Dict] = None
    crawl_duration_seconds: float = 0.0
    total_pages_discovered: int = 0
    total_pages_crawled: int = 0
    errors: List[str] = field(default_factory=list)
```

### 4.3 Analysis Models

```python
@dataclass
class Issue:
    id: str
    title: str
    category: str  # Performance | Crawlability | OnPage | StructuredData
    severity: str  # Critical | High | Medium | Low
    description: str
    remediation: str
    affected_pages: List[str]
    affected_count: int
    affected_percentage: float
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AnalysisResult:
    issues: List[Issue]
    health_score: int
    health_grade: str  # Excellent | Good | Fair | Poor
    total_pages: int
    analysis_duration_seconds: float

    @property
    def critical_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == 'Critical')

    @property
    def high_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == 'High')

    @property
    def medium_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == 'Medium')

    @property
    def low_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == 'Low')
```

## 5. File Structure

```
seo-audit/
├── README.md
├── LICENSE
├── setup.py                    # Package configuration
├── requirements.txt            # Dependencies
├── requirements-dev.txt        # Dev dependencies (pytest, black, ruff)
├── pyproject.toml             # Modern Python packaging metadata
├── .gitignore
│
├── src/
│   └── seo_audit/
│       ├── __init__.py
│       ├── __main__.py         # Entry point: python -m seo_audit
│       ├── cli.py              # CLI interface (Click commands)
│       ├── config.py           # Configuration management
│       ├── orchestrator.py     # Orchestration layer
│       │
│       ├── crawler/
│       │   ├── __init__.py
│       │   ├── crawler.py      # WebsiteCrawler class
│       │   ├── robots.py       # Robots.txt parser
│       │   └── sitemap.py      # Sitemap parser
│       │
│       ├── analyzer/
│       │   ├── __init__.py
│       │   ├── analyzer.py     # SEOAnalyzer coordinator
│       │   ├── performance.py  # PerformanceAnalyzer
│       │   ├── crawlability.py # CrawlabilityAnalyzer
│       │   ├── onpage.py       # OnPageAnalyzer
│       │   ├── schema.py       # SchemaAnalyzer
│       │   ├── filters.py      # FalsePositiveFilter
│       │   └── scoring.py      # Health score calculation
│       │
│       ├── reporter/
│       │   ├── __init__.py
│       │   ├── reporter.py     # ReportGenerator
│       │   ├── json_report.py  # JSON reporter
│       │   ├── md_report.py    # Markdown reporter
│       │   ├── html_report.py  # HTML reporter
│       │   └── pdf_report.py   # PDF reporter
│       │
│       ├── models/
│       │   ├── __init__.py
│       │   ├── config.py       # Configuration dataclasses
│       │   ├── crawl.py        # Crawl dataclasses
│       │   └── analysis.py     # Analysis dataclasses
│       │
│       ├── templates/
│       │   ├── report.html.j2  # HTML report template
│       │   ├── report-pdf.html.j2  # PDF report template
│       │   └── report.md.j2    # Markdown report template
│       │
│       └── utils/
│           ├── __init__.py
│           ├── url.py          # URL utilities
│           ├── logging.py      # Logging setup
│           └── validation.py   # Input validation
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures
│   ├── fixtures/               # Test HTML fixtures
│   │   ├── simple-page.html
│   │   ├── spa-page.html
│   │   └── schema-examples.json
│   │
│   ├── test_crawler.py
│   ├── test_analyzer.py
│   ├── test_performance.py
│   ├── test_crawlability.py
│   ├── test_onpage.py
│   ├── test_schema.py
│   ├── test_reporter.py
│   └── test_cli.py
│
├── docs/
│   ├── user-guide.md
│   ├── configuration.md
│   ├── architecture.md
│   └── api-reference.md
│
└── config/
    └── config.example.yaml     # Example configuration
```

## 6. Dependencies

### 6.1 Runtime Dependencies

```
# Core
python>=3.9,<4.0

# CLI & UI
click>=8.1.0
rich>=13.0.0

# HTTP & Browser
playwright>=1.40.0
httpx>=0.27.0

# HTML Parsing
beautifulsoup4>=4.12.0
lxml>=5.0.0

# Configuration
pyyaml>=6.0

# Structured Data
jsonschema>=4.0.0

# PDF Generation
weasyprint>=60.0

# Templating
jinja2>=3.1.0

# Utilities
python-dateutil>=2.8.0
```

### 6.2 Development Dependencies

```
# Testing
pytest>=8.0.0
pytest-asyncio>=0.23.0
pytest-cov>=4.1.0

# Code Quality (optional)
black>=24.0.0
ruff>=0.3.0
mypy>=1.8.0

# Type Stubs
types-beautifulsoup4
types-pyyaml
```

### 6.3 Dependency Installation

**setup.py:**

```python
from setuptools import setup, find_packages

setup(
    name="seo-audit",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Technical SEO Audit System CLI tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/user/seo-audit",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "click>=8.1.0",
        "rich>=13.0.0",
        "playwright>=1.40.0",
        "httpx>=0.27.0",
        "beautifulsoup4>=4.12.0",
        "lxml>=5.0.0",
        "pyyaml>=6.0",
        "jsonschema>=4.0.0",
        "weasyprint>=60.0",
        "jinja2>=3.1.0",
        "python-dateutil>=2.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-asyncio>=0.23.0",
            "pytest-cov>=4.1.0",
            "black>=24.0.0",
            "ruff>=0.3.0",
            "mypy>=1.8.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "seo-audit=seo_audit.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
```

## 7. Testing Strategy

### 7.1 Test Types

**Unit Tests**: Test individual functions/classes in isolation
- Crawler link extraction
- Analyzer issue detection logic
- Severity assignment
- Health score calculation
- Report formatting

**Integration Tests**: Test component interactions
- Crawler → Analyzer flow
- Analyzer → Reporter flow
- End-to-end: URL → Report

**Fixture Tests**: Test against saved HTML samples
- Mock HTTP responses with fixture HTML
- No network dependency
- Fast, deterministic

### 7.2 Test Fixtures

**Sample HTML Fixtures** (in `tests/fixtures/`):

1. **simple-page.html**: Basic page with title, meta, headings, links
2. **missing-elements.html**: Page missing title, meta description, alt text
3. **duplicate-titles.html**: Multiple pages with same title
4. **schema-valid.html**: Page with valid JSON-LD
5. **schema-invalid.html**: Page with malformed JSON-LD
6. **redirects.html**: Pages with redirect chains
7. **noindex.html**: Pages with noindex meta tag
8. **thin-content.html**: Page with < 200 words

### 7.3 Test Coverage Goals

- **Unit Tests**: > 80% code coverage
- **Integration Tests**: Cover main user flows (US-1, US-2, US-3)
- **Edge Cases**: Invalid URLs, network errors, malformed HTML, timeout scenarios

### 7.4 Example Test

```python
# tests/test_onpage.py
import pytest
from seo_audit.analyzer.onpage import OnPageAnalyzer
from seo_audit.models.crawl import PageData

@pytest.fixture
def missing_title_page():
    return PageData(
        url="https://example.com/page1",
        status_code=200,
        final_url="https://example.com/page1",
        html="<html><body>Content</body></html>",
        headers={},
        load_time_ms=500,
        response_size_bytes=1024,
        title=None,  # Missing title
        meta_description="A description",
        word_count=250
    )

def test_detects_missing_title(missing_title_page):
    analyzer = OnPageAnalyzer()
    issues = analyzer.check_titles([missing_title_page])

    assert len(issues) == 1
    assert issues[0].id == "missing-title"
    assert issues[0].severity == "High"
    assert issues[0].affected_count == 1
```

## 8. Performance Requirements

### 8.1 Targets (from PRD NFR-1)

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Audit Duration** | < 10 minutes for < 100 pages | User interview target: 1-3 minutes for 5-10 pages |
| **Concurrent Audits** | 2 concurrent without > 20% degradation | Sequential execution (no concurrency planned) |
| **PDF Generation** | < 5 seconds | WeasyPrint performance |
| **Memory Usage** | < 2GB | Playwright + data structures |

### 8.2 Performance Optimizations

**Crawler:**
- Sequential processing (no threading complexity)
- Early termination on page limit
- Configurable crawl delay (balance speed vs. politeness)
- Skip heavy resources (videos, large downloads) during crawl

**Analyzer:**
- Lighthouse on subset of pages (default: 5 key pages)
- Parallel Lighthouse runs not planned (sequential simpler)
- In-memory processing (no disk I/O)

**Reporter:**
- HTML template caching (Jinja2)
- PDF generation last step (only if requested)

### 8.3 Performance Testing

**Test Scenarios:**
1. Small site (5 pages): Target < 1 minute
2. Medium site (50 pages): Target < 5 minutes
3. Large site (100 pages): Target < 10 minutes

**Profiling:**
- Use Python `cProfile` to identify bottlenecks
- Monitor Playwright memory usage
- Track Lighthouse execution time (slowest component)

## 9. Error Handling

### 9.1 Error Categories

| Category | Examples | Handling Strategy |
|----------|----------|-------------------|
| **Invalid Input** | Malformed URL, invalid config | Exit with code 2, clear error message |
| **Network Errors** | DNS failure, timeout, connection refused | Exit with code 3, suggest checking URL |
| **Crawl Errors** | Robots.txt blocks, 404s, timeouts | Continue crawl, log errors, report partial results |
| **Analysis Errors** | Lighthouse crash, schema validation error | Continue analysis, skip failed checks, note in report |
| **Report Errors** | Cannot write file, PDF generation fails | Exit with code 1, suggest checking permissions |

### 9.2 Error Logging

**Minimal Mode (default)**:
- Show only critical errors that prevent audit completion
- Example: `Error: Cannot reach https://example.com (DNS resolution failed)`

**Verbose Mode (-v)**:
- Show all errors and warnings
- Log crawl errors per page
- Log analysis check failures
- Example:
  ```
  [ERROR] Failed to crawl https://example.com/page1 (404 Not Found)
  [WARNING] Lighthouse timeout on https://example.com/slow-page (skipping)
  [INFO] Skipping schema validation (no structured data found)
  ```

### 9.3 Partial Results

**Continue on Error (User-Selected Behavior)**:
- If page crawl fails: Skip page, continue with others
- If Lighthouse times out: Skip performance metrics for that page, note in report
- If schema validation fails: Report as issue, continue with other checks
- Always produce report with available data

**Report Error Summary:**
- Include "Errors Encountered" section in report
- List URLs that failed to crawl
- Note missing checks (e.g., "Lighthouse skipped on 2 pages due to timeouts")

## 10. Security Considerations

### 10.1 Input Validation

**URL Validation:**
- Validate URL format (protocol, domain)
- Reject `file://`, `javascript:`, `data:` schemes
- Sanitize URLs before passing to Playwright

**Configuration Validation:**
- Validate numeric ranges (depth, pages, timeouts)
- Sanitize file paths (prevent directory traversal)
- Reject dangerous user-agent strings (e.g., containing newlines)

### 10.2 Data Handling

**No Sensitive Data Collection:**
- Do not collect authentication credentials
- Do not store user data beyond audit results
- Do not transmit audit data to third parties (except optional PageSpeed Insights API)

**Temporary Data:**
- HTML content stored in memory only (cleared after audit)
- No disk caching of crawled pages

### 10.3 Third-Party API Security

**PageSpeed Insights API (Optional):**
- Only send target URL (no content)
- Use HTTPS
- Document in privacy policy

**Schema Validation:**
- Prefer local validation (no external API calls)
- If using external validator, sanitize JSON-LD before sending

### 10.4 User Responsibilities (from PRD)

**Authorization:**
- User must have permission to audit target website
- Documentation includes disclaimer
- Respect robots.txt by default

**Compliance:**
- User responsible for GDPR/CCPA compliance
- Tool does not extract PII from audited sites

## 11. Deployment & Distribution

### 11.1 PyPI Package Distribution

**Package Name**: `seo-audit` (or `seo-audit-cli` if taken)

**Installation:**

```bash
pip install seo-audit
```

**Post-Install:**
- Install Playwright browsers:
  ```bash
  playwright install chromium
  ```

**Entry Point:**
```bash
seo-audit https://example.com
```

### 11.2 PyPI Metadata

**setup.py / pyproject.toml:**

```toml
[project]
name = "seo-audit"
version = "1.0.0"
description = "Technical SEO Audit System CLI tool"
authors = [{name = "Your Name", email = "your.email@example.com"}]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.9"
keywords = ["seo", "audit", "lighthouse", "technical-seo", "cli"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Topic :: Internet :: WWW/HTTP :: Site Management",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
]

[project.urls]
Homepage = "https://github.com/user/seo-audit"
Repository = "https://github.com/user/seo-audit"
Documentation = "https://seo-audit.readthedocs.io"

[project.scripts]
seo-audit = "seo_audit.cli:main"

[project.optional-dependencies]
dev = ["pytest>=8.0.0", "pytest-asyncio", "pytest-cov", "black", "ruff", "mypy"]
```

### 11.3 Docker Support (Optional)

**Dockerfile:**

```dockerfile
FROM python:3.11-slim

# Install system dependencies for Playwright & WeasyPrint
RUN apt-get update && apt-get install -y \
    chromium \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install seo-audit
RUN pip install seo-audit

# Install Playwright browsers
RUN playwright install chromium

# Set working directory
WORKDIR /workspace

# Entry point
ENTRYPOINT ["seo-audit"]
```

**Usage:**

```bash
docker run --rm -v $(pwd):/workspace seo-audit https://example.com
```

### 11.4 Cross-Platform Testing

**CI/CD Strategy:**
- GitHub Actions matrix: Ubuntu, macOS, Windows
- Test Python 3.9, 3.10, 3.11, 3.12
- Run full test suite on all platforms
- Build platform-specific wheels

**Known Platform Issues:**
- **Windows**: Path separators, browser installation paths
- **macOS**: Chromium permissions, system fonts for WeasyPrint
- **Linux**: Various distros, system library versions

**Mitigation:**
- Playwright handles cross-platform browser binaries
- WeasyPrint uses system fonts (fallback to Liberation fonts)
- Path handling via `pathlib.Path` (cross-platform)

## 12. Success Metrics (from PRD Section 7)

### 12.1 Adoption Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Weekly Active Users | 20 within 3 months | Opt-in telemetry (none planned, user survey fallback) |
| Audits per User/Week | 5+ | User survey |
| User Retention | 60% conduct 2+ audits in first month | User survey |

### 12.2 Performance Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Audit Completion Rate | 95% success | Log analysis (if telemetry enabled) |
| Audit Duration | < 10 min for < 100 pages | Built-in timing, reported in verbose mode |
| Accuracy | < 5% false positive rate | Manual validation by 3 SEO experts on 50 sample reports |

### 12.3 Business Impact

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Time Savings | 90% reduction (2-4 hrs → < 10 min) | User survey |
| Client Satisfaction | 8+/10 on report quality | User survey |

## 13. Future Enhancements (Out of Scope for v1.0)

**Post-v1.0 Roadmap** (from PRD Out of Scope):

1. **v1.1 (2-3 weeks)**: Lightweight web-based report viewer
   - Drag-and-drop JSON upload
   - Client-side rendering (no server required)
   - Mirrors PDF report layout

2. **v2.0**: Historical tracking
   - Store audit results in SQLite
   - Trend visualization
   - Compare audits over time

3. **v3.0**: Full web UI
   - No CLI required for non-technical users
   - Schedule recurring audits
   - Email reports

4. **Enterprise Features**:
   - Batch audits (multiple URLs)
   - Custom branding (white-label reports)
   - API endpoints
   - Plugin system for custom checks

## 14. Open Questions & Decisions Needed

### 14.1 Resolved

1. **Primary implementation approach**: Python CLI (not browser extension)
2. **Output formats**: PDF, HTML, JSON, Markdown
3. **Distribution**: PyPI package
4. **Testing**: Mock/fixture tests (pytest)
5. **Concurrency**: Sequential only (no parallelism)
6. **Logging**: Minimal by default (errors only)
7. **Telemetry**: None (privacy-focused)

### 14.2 Pending

1. **Package name availability**: Check if `seo-audit` is available on PyPI
2. **Lighthouse integration method**: CLI subprocess vs. Python library (recommend: subprocess for reliability)
3. **React + TypeScript for HTML reports**: User mentioned React for frontend but HTML reports are template-based. **Clarification**: React unnecessary for static HTML reports; Jinja2 sufficient. React only if building interactive web UI (out of scope for v1.0).
4. **Chromium bundling**: Should we bundle Chromium (via Playwright) or require separate install? **Recommendation**: Separate install (`playwright install chromium`) to reduce package size.

## 15. Appendices

### 15.1 Glossary

- **BFS**: Breadth-First Search
- **CLS**: Cumulative Layout Shift
- **CWV**: Core Web Vitals
- **FID**: First Input Delay
- **INP**: Interaction to Next Paint
- **JSON-LD**: JSON for Linking Data (structured data format)
- **LCP**: Largest Contentful Paint
- **SEO**: Search Engine Optimization
- **TTFB**: Time to First Byte
- **WCAG**: Web Content Accessibility Guidelines

### 15.2 References

1. **Google Search Central**: https://developers.google.com/search
2. **Web.dev**: https://web.dev (Core Web Vitals, performance)
3. **Schema.org**: https://schema.org (structured data specs)
4. **Lighthouse**: https://github.com/GoogleChrome/lighthouse
5. **Playwright**: https://playwright.dev
6. **WeasyPrint**: https://weasyprint.org

### 15.3 PRD Traceability

This Technical Specification implements all requirements from **prd-final.md v3.0**:

| PRD Section | Tech Spec Section | Status |
|-------------|-------------------|--------|
| FR-1: URL Input | 3.1 CLI Interface | ✓ Covered |
| FR-2: Crawling | 3.3 Crawler Engine | ✓ Covered |
| FR-3: Performance | 3.4.2 Performance Analyzer | ✓ Covered |
| FR-4: Crawlability | 3.4.3 Crawlability Analyzer | ✓ Covered |
| FR-5: On-Page | 3.4.4 On-Page Analyzer | ✓ Covered |
| FR-6: Structured Data | 3.4.5 Structured Data Analyzer | ✓ Covered |
| FR-7: Severity | 3.4.6, 3.4.7 Filtering & Severity | ✓ Covered |
| FR-8: PDF Reports | 3.5 Reporter Engine | ✓ Covered |
| FR-9: CLI | 3.1 CLI Interface | ✓ Covered |
| FR-10: Error Handling | 9. Error Handling | ✓ Covered |
| NFR-1: Performance | 8. Performance | ✓ Covered |
| NFR-2: Reliability | 9. Error Handling | ✓ Covered |
| NFR-3: Usability | 3.1 CLI | ✓ Covered |
| NFR-5: Compatibility | 2.1 Tech Stack, 11.4 Cross-Platform | ✓ Covered |
| IN-1, IN-2: Distribution | 11. Deployment | ✓ Covered (PyPI, not binaries) |

**Note**: PRD specifies "platform-specific binaries with bundled Chromium" (IN-1.1), but technical interview selected "PyPI package" distribution. This is reconcilable: PyPI package + post-install `playwright install chromium` achieves similar outcome with simpler distribution.

---

**End of Technical Specification v1.0**
