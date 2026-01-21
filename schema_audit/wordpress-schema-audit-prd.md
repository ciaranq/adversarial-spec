# Product Requirements Document: WordPress Schema Audit Tool

**Version:** 1.0  
**Date:** January 15, 2026  
**Author:** IntelliAgent Development Team  
**Status:** Ready for Development

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Problem Statement](#problem-statement)
3. [Goals & Objectives](#goals--objectives)
4. [User Stories](#user-stories)
5. [Technical Requirements](#technical-requirements)
6. [Success Metrics](#success-metrics)
7. [Timeline & Phases](#timeline--phases)
8. [Open Questions](#open-questions)
9. [Appendix](#appendix)

---

## Executive Summary

The WordPress Schema Audit Tool is a Python-based command-line utility that automatically crawls WordPress websites to audit structured data (schema markup) implementation. It generates comprehensive CSV reports showing which schema types are present on each page, identifies gaps in coverage, and provides intelligent suggestions for schema improvements.

**Key Features:**
- Automatic sitemap discovery and parsing
- Multi-format schema detection (JSON-LD, Microdata, RDFa)
- Visual coverage reports with ✓/✗/⚠ indicators
- Intelligent schema suggestions based on content analysis
- Summary statistics and executive reporting
- Support for sites with 1000+ pages

**Target Users:**
- SEO consultants auditing client websites
- Website owners optimizing structured data
- Content managers ensuring schema consistency
- Digital marketing agencies

---

## 1. Problem Statement

### What problem are we solving?

SEO professionals and website owners need a comprehensive way to audit schema markup across their WordPress websites to identify coverage gaps and optimization opportunities. Current solutions require manual checking or expensive enterprise tools, making comprehensive schema audits time-consuming and inaccessible.

### Who experiences this problem?

**Primary Users:**
- SEO consultants who audit multiple client websites
- Digital marketing agencies managing client portfolios
- Website owners wanting to improve their structured data
- Content managers ensuring consistent schema implementation

**Secondary Users:**
- Developers implementing schema markup
- Technical SEO specialists
- E-commerce managers optimizing product schema

### Current pain points and limitations

1. **Manual Effort:** Checking schema on each page manually is extremely time-consuming
2. **No Visibility:** No easy way to see schema coverage across an entire site at a glance
3. **Pattern Recognition:** Difficult to identify patterns of missing schema across page types
4. **Prioritization:** Hard to prioritize which pages need schema additions first
5. **Validation:** Existing tools focus on validation but not coverage analysis
6. **Cost:** Enterprise tools are expensive for small agencies and individual consultants
7. **Reporting:** Creating client reports requires significant manual data compilation

---

## 2. Goals & Objectives

### Primary Goal

Create a Python-based tool that automatically audits all schema markup on a WordPress website and produces an actionable CSV report showing coverage, gaps, and intelligent recommendations.

### Secondary Goals

1. **Visual Clarity:** Provide visual indicators (✓/✗/⚠) for quick schema assessment without reading raw data
2. **Intelligence:** Suggest appropriate schema types for pages based on content and URL pattern analysis
3. **Executive Reporting:** Generate summary statistics suitable for client presentations
4. **Reusability:** Make the tool easily reusable for multiple website audits with minimal configuration
5. **Performance:** Scan medium-sized sites (500-1000 pages) in under 10 minutes
6. **Accuracy:** Detect 95%+ of schema markup on WordPress sites

### Non-Goals (Explicitly NOT in scope for v1.0)

1. **Real-time Validation:** Not validating schema against Google's structured data validator API (detection only)
2. **Automated Fixes:** Not implementing or fixing schema automatically (audit tool only)
3. **Ongoing Monitoring:** Not providing continuous monitoring or alerting (one-time audit)
4. **Non-WordPress Sites:** Not optimized for non-WordPress CMS platforms in v1.0
5. **Schema Generation:** Not creating schema markup code for users
6. **Competitive Analysis:** Not comparing schema against competitor sites (separate tool)
7. **Historical Tracking:** Not tracking schema changes over time in v1.0

---

## 3. User Stories

### Story 1: Basic Schema Audit

**As an** SEO consultant  
**I want to** scan all pages on a WordPress site and see what schema each page has  
**So that** I can quickly understand the current state of structured data implementation

**Acceptance Criteria:**
- Tool automatically finds and parses WordPress sitemap.xml
- Scans all URLs found in sitemap (or up to configured limit)
- Detects JSON-LD, Microdata, and RDFa schema formats
- Outputs CSV with all pages listed and their schema types
- Shows pages with no schema clearly
- Completes scan of 500-page site in under 10 minutes
- Handles errors gracefully (404s, timeouts) without crashing

**Priority:** P0 (Must Have)

---

### Story 2: Visual Schema Coverage Report

**As a** website owner  
**I want to** see a color-coded report showing which pages have which schema types  
**So that** I can quickly identify gaps without reading raw technical data

**Acceptance Criteria:**
- CSV uses ✓ indicator for pages with schema type present
- CSV uses ✗ indicator for pages missing schema type
- Common schema types (Article, Product, Organization, etc.) are pre-defined columns
- Report opens cleanly in Excel and Google Sheets
- Column headers are clear and understandable
- Each page has clear coverage indicators across all schema types
- Pages with multiple schema types show all types clearly

**Priority:** P0 (Must Have)

---

### Story 3: Schema Recommendations

**As an** SEO professional  
**I want the** tool to suggest which schema types should be added to pages  
**So that** I can prioritize schema implementation work and provide clear recommendations to clients

**Acceptance Criteria:**
- Tool analyzes page content and URL patterns to suggest appropriate schema
- Suggestions marked with ⚠ indicator in CSV (different from ✓ and ✗)
- Suggestion logic based on WordPress page types (post, page, product, etc.)
- Tool identifies common URL patterns:
  - `/blog/` → Article/BlogPosting
  - `/product/` → Product
  - `/about/` → Organization/Person
  - `/contact/` → LocalBusiness/Organization
  - `/faq/` → FAQPage
- Suggestions include brief explanation text
- High confidence suggestions only (avoid false positives)
- Suggestions are actionable and specific

**Priority:** P1 (Should Have)

---

### Story 4: Summary Statistics

**As a** project manager or agency owner  
**I want** summary statistics about schema coverage  
**So that** I can report on overall site health to stakeholders and demonstrate ROI

**Acceptance Criteria:**
- Summary section shows total pages scanned
- Shows count and percentage of pages with each schema type
- Shows most common schema types found on the site
- Shows count of pages with no schema at all
- Shows pages grouped by HTTP status code (200, 404, 500, etc.)
- Summary is easy to extract and include in presentations
- Statistics are accurate and match detailed page data
- Summary appears at top of report or in separate file

**Priority:** P1 (Should Have)

---

### Story 5: Handle Large Sites

**As an** enterprise SEO consultant  
**I want to** audit sites with 1000+ pages efficiently  
**So that** I can serve larger clients without performance issues

**Acceptance Criteria:**
- Tool handles sites with 1000+ pages without crashing
- Configurable page limit for testing (e.g., scan first 100 pages)
- Progress indicator shows crawl status (X of Y pages completed)
- Option to resume interrupted crawls (nice to have)
- Memory-efficient processing (doesn't load entire site into memory)
- Respects rate limiting to avoid overwhelming target server
- Configurable crawl delay between requests

**Priority:** P1 (Should Have)

---

### Story 6: Error Handling and Reporting

**As a** developer running the tool  
**I want** clear error messages and robust error handling  
**So that** I can troubleshoot issues and understand what went wrong

**Acceptance Criteria:**
- Failed page requests don't stop entire crawl
- Error log file captures all issues encountered
- CSV report includes HTTP status codes for each URL
- Unreachable pages clearly marked in output
- Timeout errors handled gracefully
- Malformed schema doesn't crash the parser
- Clear error messages for configuration issues
- Tool exits cleanly even with errors

**Priority:** P0 (Must Have)

---

## 4. Technical Requirements

### Architecture Overview

```
┌─────────────────┐
│   CLI Entry     │
│  (schema_audit) │
└────────┬────────┘
         │
         ├──────────────┬──────────────┬──────────────┬──────────────┐
         │              │              │              │              │
         ▼              ▼              ▼              ▼              ▼
┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐
│  Sitemap   │  │   Schema   │  │ Suggestion │  │   Report   │  │   Utils    │
│   Parser   │  │  Detector  │  │   Engine   │  │ Generator  │  │  (Helpers) │
└────────────┘  └────────────┘  └────────────┘  └────────────┘  └────────────┘
```

---

### Core Functionality

#### 4.1 Sitemap Discovery & Parsing

**Requirements:**
- Auto-detect sitemap at common WordPress locations:
  - `/sitemap.xml`
  - `/sitemap_index.xml`
  - `/wp-sitemap.xml`
  - `/sitemap-index.xml`
- Support for sitemap index files (multiple nested sitemaps)
- Parse all `<loc>` URLs from sitemap(s)
- Handle compressed sitemaps (`.xml.gz`)
- Extract last modified date from `<lastmod>` if available
- Follow sitemap index to child sitemaps automatically
- Handle both HTTP and HTTPS protocols
- Validate URLs before adding to crawl queue

**Error Handling:**
- Gracefully handle missing sitemaps (prompt user for URL list)
- Handle malformed XML in sitemaps
- Report sitemap parsing errors to user
- Continue with manual URL list if sitemap unavailable

**Libraries to Use:**
- `advertool.sitemap_to_df()` - if suitable for parsing
- `xml.etree.ElementTree` - as backup parser
- `requests` - for fetching sitemaps
- `gzip` - for compressed sitemaps

---

#### 4.2 Page Crawling & Schema Detection

**HTML Parsing:**
- Use `selectolax` as primary HTML parser (faster, more efficient)
- Fall back to `BeautifulSoup4` if selectolax fails for a page
- Parse HTML once per page (efficient memory usage)
- Extract all schema markup formats in single pass

**Schema Detection - JSON-LD (Primary Format):**
- Find all `<script type="application/ld+json">` tags
- Parse JSON content (handle malformed JSON gracefully)
- Extract `@type` values (can be string or array)
- Handle nested schema objects (e.g., `@graph` arrays)
- Support multiple JSON-LD blocks per page
- Extract organization/publisher info if present

**Schema Detection - Microdata:**
- Find elements with `itemscope` attribute
- Extract `itemtype` attribute values (schema.org URLs)
- Handle nested itemscope elements
- Support common microdata properties (itemprop)

**Schema Detection - RDFa (Less Common):**
- Find elements with `typeof` attribute
- Extract RDFa type declarations
- Support vocabulary declarations

**HTTP Request Configuration:**
- User-Agent: `Mozilla/5.0 (compatible; SchemaAudit/1.0; +https://intelliagent.com.au)`
- Timeout: 30 seconds per request
- Respect robots.txt (optional, configurable)
- Follow redirects (max 5 redirects)
- Handle SSL certificate errors gracefully

**Rate Limiting:**
- Configurable delay between requests (default: 1 second)
- Option to randomize delay (0.5-1.5 seconds)
- Detect 429 (Too Many Requests) and back off
- Option to crawl faster for localhost/staging sites

**Data Extracted Per Page:**
- URL (canonical if available)
- HTTP status code
- Page title (from `<title>` tag)
- Schema types found (list)
- Schema format(s) used (JSON-LD, Microdata, RDFa)
- Raw schema JSON (optional, for debugging)
- Crawl timestamp
- Response time (optional metric)

---

#### 4.3 Schema Type Detection

**Pre-defined Common Schema Types:**

The tool will check for these schema types as columns in the CSV:

**Content Types:**
- `Article` - General articles
- `BlogPosting` - Blog posts
- `NewsArticle` - News content
- `WebPage` - Generic web pages
- `VideoObject` - Video content
- `ImageObject` - Image content

**Business Types:**
- `Organization` - Company information
- `LocalBusiness` - Local businesses with location
- `Person` - Individual person profiles

**E-commerce Types:**
- `Product` - Product pages
- `Offer` - Pricing/availability info
- `Review` - Individual reviews
- `AggregateRating` - Rating summaries

**Interactive Types:**
- `FAQPage` - FAQ pages
- `HowTo` - How-to guides
- `QAPage` - Q&A pages

**Navigation Types:**
- `BreadcrumbList` - Breadcrumb navigation
- `WebSite` - Site-wide schema

**Event Types:**
- `Event` - Events and occurrences

**Support for Custom Schema Types:**
- Detect any schema.org type not in pre-defined list
- Add to "Other Schema Types" column
- Count custom types in summary statistics

---

#### 4.4 Content Analysis for Suggestions

**URL Pattern Analysis:**

Analyze URL structure to suggest appropriate schema:

```python
URL_PATTERNS = {
    r'/blog/': ['Article', 'BlogPosting'],
    r'/news/': ['NewsArticle', 'Article'],
    r'/product/': ['Product'],
    r'/products/': ['Product'],
    r'/shop/': ['Product'],
    r'/about': ['Organization', 'Person'],
    r'/about-us': ['Organization'],
    r'/contact': ['LocalBusiness', 'Organization'],
    r'/faq': ['FAQPage'],
    r'/how-to': ['HowTo'],
    r'/guide/': ['HowTo', 'Article'],
    r'/events?/': ['Event'],
    r'/locations?/': ['LocalBusiness'],
    r'/team/': ['Person'],
    r'/author/': ['Person'],
    r'/video/': ['VideoObject'],
}
```

**Page Content Analysis:**

Check page title and H1 headings for clues:
- "How to..." → HowTo schema
- "FAQ" or "Frequently Asked" → FAQPage
- Product indicators (price, "buy", "add to cart") → Product
- Event indicators (date, time, location) → Event

**WordPress Page Type Detection:**

Check HTML for WordPress-specific indicators:
- Body classes: `single-post`, `page`, `archive`, `product`
- Meta tags: `article:published_time` (Article)
- Meta tags: `product:price:amount` (Product)
- Yoast SEO graph (extract intended schema type)

**Suggestion Confidence Levels:**

- **High Confidence (show ⚠):** Multiple indicators match (URL + content + WP class)
- **Medium Confidence (show ⚠):** Single strong indicator matches
- **Low Confidence (don't suggest):** Weak or conflicting indicators

**Suggestion Logic Rules:**

1. Only suggest if page has NO existing schema of that type
2. Don't suggest generic WebPage (too broad)
3. Prefer specific types over generic (BlogPosting > Article)
4. Don't over-suggest (max 2 suggestions per page)
5. Provide brief explanation for each suggestion

---

### 4.5 Output Generation

#### CSV Structure

**Primary Columns (Left to Right):**

```csv
URL, Page Title, Status, Total Schema, Article, BlogPosting, NewsArticle, WebPage, Organization, LocalBusiness, Person, Product, FAQPage, HowTo, VideoObject, BreadcrumbList, Review, Event, Other Schema Types, Suggestions, Notes
```

**Column Details:**

1. **URL** - Full page URL
2. **Page Title** - Extracted from `<title>` tag
3. **Status** - HTTP status code (200, 404, 500, etc.)
4. **Total Schema** - Count of schema types on page
5. **[Schema Type Columns]** - One column per common schema type
   - `✓` if present
   - `✗` if not present
   - `⚠` if suggested but not present
   - (blank) for N/A
6. **Other Schema Types** - Comma-separated list of non-standard types found
7. **Suggestions** - Text explanation of suggestions (if any)
8. **Notes** - Errors, warnings, special cases

**Visual Indicators:**
- ✓ (green checkmark concept) - Schema present
- ✗ (red X concept) - Schema not present  
- ⚠ (amber warning concept) - Schema suggested
- (blank) - Not applicable

**Note:** CSV files don't support actual colors. The indicators are text symbols that convey the color concept. If Excel output is added in Phase 3, actual cell colors can be implemented.

---

#### Summary Statistics Section

**Place at top of CSV or in separate `summary.csv` file.**

**Metrics to Include:**

```
=== SCHEMA AUDIT SUMMARY ===
Site URL: https://example.com
Scan Date: 2026-01-15 14:30:00
Total Pages Scanned: 487
Pages with Schema: 312 (64.1%)
Pages without Schema: 175 (35.9%)

=== SCHEMA TYPE COVERAGE ===
Schema Type          | Count | Percentage
---------------------|-------|------------
Article              | 245   | 50.3%
BreadcrumbList       | 487   | 100.0%
Organization         | 487   | 100.0%
BlogPosting          | 198   | 40.7%
ImageObject          | 156   | 32.0%
Product              | 45    | 9.2%
FAQPage              | 12    | 2.5%
...

=== PAGES BY STATUS CODE ===
Status Code | Count
------------|------
200         | 450
301         | 25
404         | 10
500         | 2

=== TOP RECOMMENDATIONS ===
- 123 blog posts missing Article/BlogPosting schema
- 45 product pages missing Product schema
- 23 pages could benefit from FAQPage schema
- 8 contact/location pages missing LocalBusiness schema

=== ERRORS & WARNINGS ===
- 12 pages timed out during scan
- 5 pages had malformed schema JSON
- 2 pages returned 500 errors
```

---

### 4.6 Technology Stack

#### Required Python Libraries

```txt
# Core Dependencies
selectolax>=0.3.21          # Fast HTML parsing (primary)
beautifulsoup4>=4.12.0      # HTML parsing (backup)
lxml>=5.1.0                 # XML/HTML parser backend
requests>=2.31.0            # HTTP client
advertools>=0.14.0          # Sitemap parsing (evaluate usefulness)

# Data Processing
pandas>=2.1.0               # CSV generation and data manipulation

# Configuration & Environment
python-dotenv>=1.0.0        # Environment variable management

# Progress & Logging
tqdm>=4.66.0                # Progress bars
colorama>=0.4.6             # Colored terminal output

# Optional (Phase 3)
openpyxl>=3.1.0             # Excel output with color coding
validators>=0.22.0          # URL validation
```

#### Python Version
- **Minimum:** Python 3.9
- **Recommended:** Python 3.11+
- **Note:** Use type hints for Python 3.9+ compatibility

---

### 4.7 Configuration

#### Environment Variables (.env)

```bash
# Required Configuration
SITE_URL=https://example.com

# Optional Configuration
CRAWL_DELAY=1.0                    # Seconds between requests
MAX_PAGES=1000                     # Max pages to scan (0 = unlimited)
TIMEOUT=30                         # Request timeout in seconds
USER_AGENT="SchemaAudit/1.0"       # Custom user agent

# Output Configuration
OUTPUT_DIR=./reports               # Where to save reports
OUTPUT_FORMAT=csv                  # csv or excel
INCLUDE_RAW_SCHEMA=false          # Include raw JSON in output

# Advanced Configuration
RESPECT_ROBOTS=true               # Respect robots.txt
FOLLOW_REDIRECTS=true             # Follow HTTP redirects
MAX_REDIRECTS=5                   # Max redirect hops
VERIFY_SSL=true                   # Verify SSL certificates
ENABLE_SUGGESTIONS=true           # Enable schema suggestions
```

#### Command Line Arguments

```bash
python schema_audit.py \
  --url https://example.com \
  --output report.csv \
  --delay 1.0 \
  --max-pages 500 \
  --format csv \
  --verbose
```

**Argument Definitions:**
- `--url, -u`: Target website URL (required)
- `--output, -o`: Output file path (default: `schema_audit_[timestamp].csv`)
- `--delay, -d`: Crawl delay in seconds (default: 1.0)
- `--max-pages, -m`: Max pages to scan (default: 0 = unlimited)
- `--format, -f`: Output format: csv or excel (default: csv)
- `--verbose, -v`: Verbose logging output
- `--no-suggestions`: Disable schema suggestions
- `--summary-only`: Generate only summary statistics

---

### 4.8 Error Handling

**HTTP Request Errors:**
- **Timeout:** Log error, mark page as "timeout", continue crawling
- **404 Not Found:** Log, mark status as 404, continue
- **500 Server Error:** Log, mark status as 500, continue
- **SSL Certificate Error:** Log warning, optionally skip verification
- **Connection Error:** Log error, retry once, then skip
- **429 Too Many Requests:** Back off exponentially, wait 60 seconds

**Parsing Errors:**
- **Malformed HTML:** Try selectolax, fallback to BeautifulSoup, log if both fail
- **Malformed JSON-LD:** Log error, skip that schema block, continue with page
- **Invalid URLs in Sitemap:** Log warning, skip invalid URL
- **Empty Response:** Log error, mark page as failed

**File System Errors:**
- **Cannot Write Output:** Fail gracefully with clear error message
- **Cannot Create Directory:** Attempt to create, fail if impossible
- **Disk Space:** Check before writing large reports

**Logging Strategy:**
- **Console Output:** Progress bars, summary statistics, critical errors
- **Log File (`schema_audit.log`):** All errors, warnings, debug info
- **Error Report (`errors.csv`):** All failed pages with reasons

**Graceful Degradation:**
- Continue crawling even if individual pages fail
- Report what WAS scanned successfully
- Provide partial results if scan interrupted
- Don't crash on unexpected schema types

---

### 4.9 Performance Considerations

**Efficiency Targets:**
- Scan 500-page site in under 10 minutes (1 sec delay = 500 seconds ~8 min)
- Scan 1000-page site in under 20 minutes
- Memory usage stays under 500MB for 1000-page scan

**Optimization Strategies:**

1. **Use selectolax for parsing** (10x faster than BeautifulSoup)
2. **Stream results to CSV** (don't hold all data in memory)
3. **Minimal regex usage** (prefer string methods)
4. **Efficient JSON parsing** (use built-in `json` library)
5. **Connection pooling** (reuse HTTP connections)
6. **Lazy evaluation** (process pages as they're fetched)

**Configurable Rate Limiting:**
- Default: 1 request per second (respectful)
- Aggressive: 0.5 seconds (for own sites)
- Conservative: 2 seconds (for sensitive sites)
- Adaptive: Detect 429 errors and slow down

**Progress Feedback:**
- Progress bar showing pages scanned
- ETA calculation based on current speed
- Pages per second metric
- Option for quiet mode (no progress bars)

---

## 5. Success Metrics

### Functional Success Criteria

**Accuracy:**
- ✓ Successfully parses 95%+ of URLs in WordPress sitemaps
- ✓ Accurately detects schema in JSON-LD format (most common WordPress format)
- ✓ Detects Microdata and RDFa with 85%+ accuracy
- ✓ Schema suggestions have 80%+ relevance (manually evaluated)

**Performance:**
- ✓ Generates readable CSV report in < 10 minutes for 500-page site
- ✓ Memory usage stays under 500MB for 1000-page scan
- ✓ Tool handles sites with 1000+ pages without crashing
- ✓ Error rate < 5% for accessible pages (200 status)

**Usability:**
- ✓ Report requires no manual post-processing to be useful
- ✓ CSV opens cleanly in Excel and Google Sheets
- ✓ Visual indicators are immediately understandable
- ✓ Tool can be reused across multiple sites with < 1 minute setup

---

### User Success Criteria

**Time Savings:**
- Users can identify schema gaps in < 2 minutes of reviewing report
- Users save 2+ hours vs. manual schema checking
- Report generation is faster than writing manual audit notes

**Decision Support:**
- Report provides clear next steps for schema implementation
- Suggestions are actionable and specific
- Summary statistics support executive presentations

**Quality:**
- Users trust the accuracy of the tool's detection
- Users understand what each indicator means without documentation
- Users can explain results to non-technical stakeholders

---

### Technical Success Criteria

**Reliability:**
- Tool completes scans without crashing 95%+ of the time
- Handles edge cases gracefully (empty pages, redirects, errors)
- Produces consistent results across multiple runs

**Maintainability:**
- Code is well-documented and follows Python best practices
- Adding new schema types takes < 30 minutes
- Updating detection logic is straightforward

**Extensibility:**
- Architecture supports adding Excel output in Phase 3
- Can be adapted for web interface in Phase 4
- Can add new suggestion rules without refactoring

---

## 6. Timeline & Phases

### Phase 1: Core Functionality (MVP)
**Estimated Effort:** 4-6 hours  
**Status:** Ready for Development

**Deliverables:**
- ✓ Sitemap discovery and parsing (`sitemap_parser.py`)
- ✓ Basic page crawling with rate limiting
- ✓ JSON-LD schema detection (primary format)
- ✓ CSV output with ✓/✗ indicators
- ✓ Pre-defined common schema types (15+ types)
- ✓ Basic error handling (timeouts, 404s)
- ✓ Progress bars for user feedback
- ✓ Command-line interface
- ✓ Configuration via .env and CLI args

**Milestone:** Working script that audits a WordPress site and outputs basic CSV report

**Testing Checklist:**
- [ ] Test with small site (< 50 pages)
- [ ] Test with medium site (500 pages)
- [ ] Test with site using JSON-LD schema
- [ ] Test with site using no schema
- [ ] Test error handling (timeout a few requests)
- [ ] Verify CSV opens in Excel without issues

---

### Phase 2: Enhanced Detection & Suggestions
**Estimated Effort:** 3-4 hours  
**Dependencies:** Phase 1 complete and tested

**Deliverables:**
- ✓ Microdata schema detection
- ✓ RDFa schema detection (if time permits)
- ✓ Content analysis engine (`suggestion_engine.py`)
- ✓ URL pattern matching for suggestions
- ✓ Page content analysis (title, headings)
- ✓ WordPress page type detection
- ✓ ⚠ indicators for suggestions in CSV
- ✓ Suggestions explanation column

**Milestone:** Enhanced script with intelligent suggestion engine

**Testing Checklist:**
- [ ] Test suggestion accuracy on known site (manual validation)
- [ ] Test with sites using Microdata
- [ ] Verify suggestions don't create false positives
- [ ] Test suggestion logic with edge cases

---

### Phase 3: Reporting & Polish
**Estimated Effort:** 2-3 hours  
**Dependencies:** Phase 2 complete and tested

**Deliverables:**
- ✓ Summary statistics section in CSV
- ✓ Alternative Excel output with true color coding (optional)
- ✓ Enhanced logging system
- ✓ Comprehensive error reporting
- ✓ README.md documentation
- ✓ Usage examples and screenshots
- ✓ Schema types documentation
- ✓ Troubleshooting guide

**Milestone:** Production-ready tool with comprehensive documentation

**Testing Checklist:**
- [ ] Test with 5+ real WordPress sites
- [ ] Verify documentation is complete and accurate
- [ ] Test installation on clean Python environment
- [ ] Gather user feedback from initial test users

---

### Phase 4: Future Enhancements (Post-MVP)
**Estimated Effort:** TBD  
**Status:** Planning / Future Consideration

**Potential Features:**
- ✓ Web interface with Next.js (deploy to Vercel)
- ✓ Schema validation against Google's requirements
- ✓ Historical tracking (compare audits over time)
- ✓ Competitor schema comparison tool
- ✓ WordPress plugin integration
- ✓ Email report delivery
- ✓ Scheduled/automated audits
- ✓ Multi-site batch auditing
- ✓ API for integration with other tools

**Considerations for Web Version:**
- Vercel serverless function timeout limits (10 seconds hobby, 5 min pro)
- May need queue system for long-running crawls
- Consider background job processing
- User authentication for saved reports
- Rate limiting for public tool

**Decision Point:** Evaluate after Phase 3 based on user feedback and demand

---

## 7. Open Questions

### Technical Decisions

#### Question 1: Sitemap Parsing Library
**Question:** Should we use `advertool` for sitemap parsing or build a custom parser?

**Options:**
- **Option A:** Use `advertool.sitemap_to_df()` - battle-tested, handles edge cases
- **Option B:** Custom parser with `xml.etree` - more control, fewer dependencies

**Recommendation:** Start with `advertool`, fallback to custom parser if it doesn't meet needs

**Decision Needed By:** Phase 1 start

---

#### Question 2: Schema Suggestion Confidence
**Question:** How aggressive should we be with schema suggestions?

**Options:**
- **Option A:** Conservative - only high-confidence suggestions (fewer false positives)
- **Option B:** Aggressive - show medium-confidence suggestions (more helpful but noisier)
- **Option C:** Configurable - let user choose confidence level

**Recommendation:** Option A for v1.0, add Option C in Phase 2 if time permits

**Decision Needed By:** Phase 2 start

---

#### Question 3: WordPress REST API Usage
**Question:** Should we check WordPress REST API for post types to improve suggestions?

**Considerations:**
- **Pro:** More accurate post type detection
- **Pro:** Can get taxonomy information
- **Con:** Additional HTTP requests (slower)
- **Con:** REST API may be disabled on some sites
- **Con:** Adds complexity

**Recommendation:** Not for v1.0 - rely on HTML analysis. Consider for Phase 4.

**Decision Needed By:** Phase 2 (if time permits)

---

#### Question 4: Output Format Priority
**Question:** Should we prioritize Excel output with true color coding in Phase 3?

**Considerations:**
- **Pro:** More visual, better for client presentations
- **Pro:** Easier to sort/filter with colors
- **Con:** Requires `openpyxl` dependency
- **Con:** Larger file sizes
- **Con:** Not all users have Excel

**Recommendation:** Make Excel optional. CSV is universal and should remain primary format.

**Decision Needed By:** Phase 3 start

---

### Product Decisions

#### Question 5: Validation vs. Detection
**Question:** Should v1.0 include schema validation or just detection?

**Considerations:**
- Detection = "This page has Article schema"
- Validation = "This Article schema is missing required 'datePublished' field"

**Recommendation:** Detection only for v1.0. Validation requires Google API integration (Phase 4).

**Decision Needed By:** Phase 1 start

---

#### Question 6: Competitor Comparison
**Question:** Should competitor comparison be part of this tool or separate?

**Considerations:**
- **Same Tool:** Convenient, but adds complexity
- **Separate Tool:** Cleaner separation of concerns
- **Integration:** Could share schema detection code

**Recommendation:** Separate tool. Keep this focused on single-site audits.

**Decision Needed By:** Post-Phase 3

---

#### Question 7: Web UI Development
**Question:** Should we build CLI-only initially or web UI in parallel?

**Considerations:**
- CLI is faster to build and test
- Web UI more accessible to non-technical users
- Web UI has deployment complexity (Vercel timeouts)
- Can build web UI after CLI is proven

**Recommendation:** CLI for Phase 1-3. Web UI in Phase 4 after validating with users.

**Decision Needed By:** Phase 1 start

---

#### Question 8: WordPress Agent Integration
**Question:** Can WordPress agent help with post type detection? Worth the complexity?

**Considerations:**
- Unclear what WordPress agent capabilities are
- May require additional authentication/setup
- Could improve suggestion accuracy
- Adds dependency and complexity

**Recommendation:** Research WordPress agent capabilities. Not for v1.0 unless trivially easy.

**Decision Needed By:** Phase 2 (research phase)

---

### Scope Questions

#### Question 9: Schema Type Coverage
**Question:** Are the 15+ pre-defined schema types comprehensive enough?

**Current List:**
- Article, BlogPosting, NewsArticle, WebPage
- Organization, LocalBusiness, Person
- Product, Review, AggregateRating
- FAQPage, HowTo, QAPage
- BreadcrumbList, WebSite
- Event, VideoObject, ImageObject

**Missing Common Types:**
- Recipe (food blogs)
- Course (education)
- JobPosting (careers pages)
- Service (service businesses)
- SoftwareApplication (software products)

**Recommendation:** Add Recipe, Course, JobPosting, Service in Phase 1. Easy to add more.

**Decision Needed By:** Phase 1 start

---

#### Question 10: Rate Limiting Strategy
**Question:** What's the right default crawl delay balance?

**Options:**
- **0.5 seconds:** Fast but potentially aggressive
- **1.0 seconds:** Good balance (recommended)
- **2.0 seconds:** Very respectful but slow for large sites
- **Adaptive:** Start fast, slow down if 429 errors

**Recommendation:** Default to 1.0 seconds with adaptive backoff for 429 errors.

**Decision Needed By:** Phase 1 start

---

## 8. Appendix

### A. File Structure

```
wordpress-schema-audit/
│
├── src/
│   ├── __init__.py
│   ├── sitemap_parser.py       # Sitemap discovery and URL extraction
│   ├── schema_detector.py      # HTML parsing and schema extraction
│   ├── suggestion_engine.py    # Content analysis and recommendations
│   ├── report_generator.py     # CSV/Excel output generation
│   └── utils.py                # Helper functions and constants
│
├── tests/
│   ├── __init__.py
│   ├── test_sitemap_parser.py
│   ├── test_schema_detector.py
│   ├── test_suggestion_engine.py
│   └── test_report_generator.py
│
├── docs/
│   ├── SCHEMA_TYPES.md         # Documentation of supported schema types
│   ├── USAGE.md                # Usage examples and tutorials
│   └── TROUBLESHOOTING.md      # Common issues and solutions
│
├── examples/
│   ├── example_report.csv      # Sample output
│   └── example_config.env      # Example configuration
│
├── reports/                    # Default output directory (git ignored)
│
├── schema_audit.py             # Main CLI entry point
├── requirements.txt            # Python dependencies
├── .env.example                # Example environment variables
├── .gitignore                  # Git ignore rules
├── README.md                   # Main documentation
└── LICENSE                     # License file (MIT recommended)
```

---

### B. Schema Type Definitions

#### Core Content Types
- **Article:** General article content
- **BlogPosting:** Blog posts (more specific than Article)
- **NewsArticle:** News articles (more specific than Article)
- **WebPage:** Generic web pages

#### Business Types
- **Organization:** Company or organization information
- **LocalBusiness:** Local business with physical location
- **Person:** Individual person profiles

#### E-commerce Types
- **Product:** Products for sale
- **Offer:** Pricing and availability information
- **Review:** Individual reviews
- **AggregateRating:** Aggregate rating information

#### Interactive Content
- **FAQPage:** Frequently asked questions pages
- **HowTo:** Step-by-step guides
- **QAPage:** Question and answer pages

#### Media Types
- **VideoObject:** Video content
- **ImageObject:** Image content

#### Navigation
- **BreadcrumbList:** Breadcrumb navigation
- **WebSite:** Site-wide information

#### Events
- **Event:** Events, concerts, conferences, etc.

#### Additional Types (Consider Adding)
- **Recipe:** Recipe content
- **Course:** Educational courses
- **JobPosting:** Job listings
- **Service:** Service offerings

---

### C. URL Pattern Matching Rules

```python
SCHEMA_SUGGESTIONS = {
    # Blog and Article Pages
    r'/blog/': {
        'schema': ['Article', 'BlogPosting'],
        'confidence': 'high',
        'reason': 'URL indicates blog content'
    },
    r'/\d{4}/\d{2}/': {  # Date-based URLs like /2024/01/
        'schema': ['BlogPosting', 'Article'],
        'confidence': 'high',
        'reason': 'Date-based URL structure typical of blog posts'
    },
    r'/news/': {
        'schema': ['NewsArticle', 'Article'],
        'confidence': 'high',
        'reason': 'URL indicates news content'
    },
    
    # E-commerce Pages
    r'/product/': {
        'schema': ['Product'],
        'confidence': 'high',
        'reason': 'URL indicates product page'
    },
    r'/shop/': {
        'schema': ['Product'],
        'confidence': 'medium',
        'reason': 'Shop section may contain products'
    },
    
    # Business Information Pages
    r'/about': {
        'schema': ['Organization', 'Person'],
        'confidence': 'medium',
        'reason': 'About pages typically describe organization or people'
    },
    r'/contact': {
        'schema': ['LocalBusiness', 'Organization'],
        'confidence': 'medium',
        'reason': 'Contact pages often benefit from business schema'
    },
    r'/location': {
        'schema': ['LocalBusiness'],
        'confidence': 'high',
        'reason': 'Location pages should have business schema'
    },
    
    # Interactive Content
    r'/faq': {
        'schema': ['FAQPage'],
        'confidence': 'high',
        'reason': 'FAQ pages should use FAQPage schema'
    },
    r'/how-to': {
        'schema': ['HowTo'],
        'confidence': 'high',
        'reason': 'How-to guides should use HowTo schema'
    },
    
    # People Pages
    r'/team/': {
        'schema': ['Person'],
        'confidence': 'medium',
        'reason': 'Team member pages should use Person schema'
    },
    r'/author/': {
        'schema': ['Person'],
        'confidence': 'high',
        'reason': 'Author pages should use Person schema'
    },
    
    # Event Pages
    r'/event': {
        'schema': ['Event'],
        'confidence': 'high',
        'reason': 'Event pages should use Event schema'
    },
    
    # Media Pages
    r'/video': {
        'schema': ['VideoObject'],
        'confidence': 'high',
        'reason': 'Video content should use VideoObject schema'
    },
    r'/gallery': {
        'schema': ['ImageObject'],
        'confidence': 'medium',
        'reason': 'Image galleries can benefit from ImageObject schema'
    },
}
```

---

### D. CSV Output Example

```csv
URL,Page Title,Status,Total Schema,Article,BlogPosting,WebPage,Organization,Product,FAQPage,BreadcrumbList,Other Schema,Suggestions,Notes
https://example.com/,Example Site Home,200,3,✗,✗,✓,✓,✗,✗,✓,,✗,
https://example.com/blog/post-1,My First Blog Post,200,2,✗,✓,✗,✗,✗,✗,✓,,✗,
https://example.com/about,About Us,200,2,✗,✗,✓,✓,✗,✗,✓,,✗,
https://example.com/blog/post-2,Second Post,200,1,✗,✗,✗,✗,✗,✗,✓,,⚠ BlogPosting,"URL pattern suggests blog post"
https://example.com/products/widget,Amazing Widget,200,3,✗,✗,✗,✗,✓,✗,✓,"Review, AggregateRating",✗,
https://example.com/faq,FAQ,200,1,✗,✗,✓,✗,✗,✗,✓,,⚠ FAQPage,"Page contains Q&A content"
https://example.com/contact,Contact Us,200,2,✗,✗,✓,✓,✗,✗,✓,,⚠ LocalBusiness,"Contact page could use LocalBusiness schema"
```

---

### E. Summary Statistics Example

```csv
=== SCHEMA AUDIT SUMMARY ===
Site URL,https://example.com
Scan Date,2026-01-15 14:30:00
Total Pages Scanned,487
Pages with Schema,312 (64.1%)
Pages without Schema,175 (35.9%)
Scan Duration,8m 32s
Average Response Time,1.2s

=== SCHEMA TYPE COVERAGE ===
Schema Type,Count,Percentage
BreadcrumbList,487,100.0%
Organization,487,100.0%
Article,245,50.3%
BlogPosting,198,40.7%
WebPage,178,36.5%
ImageObject,156,32.0%
Product,45,9.2%
FAQPage,12,2.5%
HowTo,8,1.6%
LocalBusiness,5,1.0%
VideoObject,3,0.6%

=== PAGES BY STATUS CODE ===
Status Code,Count,Percentage
200,450,92.4%
301,25,5.1%
404,10,2.1%
500,2,0.4%

=== TOP RECOMMENDATIONS ===
Recommendation,Affected Pages
Blog posts missing Article/BlogPosting schema,123
Product pages missing Product schema,45
Pages could benefit from FAQPage schema,23
Contact/location pages missing LocalBusiness schema,8

=== ERRORS & WARNINGS ===
Issue,Count
Pages timed out during scan,12
Pages with malformed schema JSON,5
Pages returned 500 errors,2
```

---

### F. Installation & Setup

#### Requirements
- Python 3.9 or higher
- pip (Python package manager)
- Internet connection

#### Installation Steps

```bash
# 1. Clone or download the repository
git clone https://github.com/yourusername/wordpress-schema-audit.git
cd wordpress-schema-audit

# 2. Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment (optional)
cp .env.example .env
# Edit .env with your preferred settings

# 5. Run the tool
python schema_audit.py --url https://example.com --output report.csv
```

---

### G. Usage Examples

#### Basic Usage
```bash
# Audit a WordPress site with default settings
python schema_audit.py --url https://example.com
```

#### Custom Output Location
```bash
# Save report to specific location
python schema_audit.py --url https://example.com --output ./reports/example_audit.csv
```

#### Limit Number of Pages
```bash
# Scan only first 100 pages (useful for testing)
python schema_audit.py --url https://example.com --max-pages 100
```

#### Faster Crawling (Own Site)
```bash
# Reduce crawl delay for faster scanning
python schema_audit.py --url https://example.com --delay 0.5
```

#### Verbose Output
```bash
# Show detailed logging during scan
python schema_audit.py --url https://example.com --verbose
```

#### Disable Suggestions
```bash
# Scan without generating schema suggestions
python schema_audit.py --url https://example.com --no-suggestions
```

---

### H. Development Standards

#### Python Code Style
- Follow PEP 8 style guide
- Use Black for code formatting
- Use snake_case for functions and variables
- Use PascalCase for classes
- Maximum line length: 100 characters
- Use type hints where beneficial

#### File Headers
```python
"""
Description: [Brief description of the file's purpose]
Version: 1.0
Author: IntelliAgent Development Team
"""
```

#### Docstring Format
```python
def function_name(param1: str, param2: int) -> bool:
    """
    Brief description of function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: Description of when this is raised
    """
    pass
```

#### Error Handling
- Use try/except blocks for external calls (HTTP, file I/O)
- Log errors don't silently fail
- Provide helpful error messages
- Continue processing when possible (don't crash on single failures)

---

### I. Testing Checklist

#### Phase 1 Testing
- [ ] Test with small WordPress site (< 50 pages)
- [ ] Test with medium WordPress site (500 pages)
- [ ] Test with large WordPress site (1000+ pages)
- [ ] Test with site using JSON-LD schema
- [ ] Test with site using no schema
- [ ] Test with site using Yoast SEO plugin
- [ ] Test with site using RankMath plugin
- [ ] Test error handling (simulate timeouts)
- [ ] Verify CSV opens in Excel without issues
- [ ] Verify CSV opens in Google Sheets without issues
- [ ] Test with non-WordPress site (should handle gracefully)

#### Phase 2 Testing
- [ ] Test Microdata detection on sites using it
- [ ] Test suggestion accuracy (manual validation on known sites)
- [ ] Test URL pattern matching with diverse URLs
- [ ] Test with sites using custom post types
- [ ] Verify suggestions don't create false positives
- [ ] Test with multilingual sites

#### Phase 3 Testing
- [ ] Test with 5+ diverse real WordPress sites
- [ ] Verify summary statistics are accurate
- [ ] Test Excel output (if implemented)
- [ ] Test documentation completeness
- [ ] Test installation on clean Python environment
- [ ] Gather user feedback from initial test users

---

### J. Future Enhancement Ideas

#### Short-term (Phase 4)
- Excel output with actual color coding
- Schema validation against Google requirements
- Historical tracking (compare audits over time)
- Batch auditing (multiple sites)
- API for integration

#### Medium-term
- Web interface with Next.js
- User authentication and saved reports
- Email report delivery
- Scheduled audits
- WordPress plugin integration

#### Long-term
- Competitor comparison tool
- Schema implementation code generator
- AI-powered schema suggestions
- Integration with Google Search Console
- Automated schema testing

---

### K. Glossary

**Schema Markup:** Structured data added to HTML that helps search engines understand page content

**JSON-LD:** JavaScript Object Notation for Linked Data - most common schema format in WordPress

**Microdata:** HTML attribute-based schema markup format

**RDFa:** Resource Description Framework in Attributes - another schema markup format

**Sitemap:** XML file listing all pages on a website for search engines

**WordPress:** Popular content management system (CMS)

**CSV:** Comma-Separated Values - spreadsheet file format

**User-Agent:** String identifying the client making HTTP requests

**Rate Limiting:** Controlling the frequency of requests to avoid overloading servers

**Structured Data:** Organized format of data that search engines can easily read

---

## Contact & Support

**Project Owner:** IntelliAgent (https://intelliagent.com.au)  
**Documentation:** [To be added]  
**Issues:** [To be added]  
**Email:** [To be added]

---

**Document End**

*This PRD is a living document and will be updated as the project evolves. Last updated: January 15, 2026*
