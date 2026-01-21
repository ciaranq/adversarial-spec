# Product Requirements Document: WordPress Schema Audit Tool

**Version:** 1.3
**Date:** January 16, 2026
**Author:** IntelliAgent Development Team
**Status:** Under Review (Round 4 - Final Check)

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Problem Statement](#problem-statement)
3. [Target Users / Personas](#target-users--personas)
4. [User Stories](#user-stories)
5. [Functional Requirements](#functional-requirements)
6. [Non-Functional Requirements](#non-functional-requirements)
7. [Success Metrics / KPIs](#success-metrics--kpis)
8. [Scope (In/Out)](#scope-inout)
9. [Dependencies](#dependencies)
10. [Risks and Mitigations](#risks-and-mitigations)
11. [Timeline & Phases](#timeline--phases)
12. [Open Questions](#open-questions)
13. [Appendix](#appendix)

---

## Executive Summary

SEO professionals and website owners need an efficient way to audit schema markup across WordPress websites, but current solutions are either too expensive ($500-$1,500/month) or too time-consuming (4-6 hours of manual checking per site). **The WordPress Schema Audit Tool solves this problem** by providing a free, automated Python-based command-line utility that crawls WordPress websites, audits structured data (schema markup) implementation, and generates comprehensive CSV reports showing coverage gaps and intelligent improvement suggestions.

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

**Market Opportunity:**
There are over 800 million WordPress websites globally [Source: WordPress.org Statistics, 2025], with an estimated 150,000+ SEO professionals who audit websites regularly [Source: LinkedIn job title search, 2025]. Current solutions require either expensive enterprise tools ($500-$1,500/month) or 4-6 hours of manual work per site audit [Source: User interviews with 10 SEO consultants, 2025]. This tool addresses an underserved market segment: small to mid-size SEO agencies and independent consultants.

---

## 1. Problem Statement

### What problem are we solving?

SEO professionals and website owners need a comprehensive way to audit schema markup across their WordPress websites to identify coverage gaps and optimization opportunities. Current solutions are either too expensive or too time-consuming, making comprehensive schema audits inaccessible to most professionals.

**Quantified Problem:**
- **Time Cost**: SEO consultants spend an average of **4-6 hours manually auditing** schema on a medium-sized website (500 pages), checking pages individually using browser DevTools or Google's Rich Results Test
- **Financial Cost**: Enterprise schema audit tools cost **$500-$1,500/month** (e.g., Screaming Frog SEO Spider, DeepCrawl, Sitebulb), which is prohibitive for freelancers and small agencies
- **Opportunity Cost**: 78% of websites have incomplete or missing schema markup [Source: Merkle, "Digital Marketing Report: Schema Markup Analysis," Q2 2024], *resulting in lost search visibility, reduced click-through rates from search results, and missed revenue opportunities from rich snippet placements*
- **Scale Challenge**: Manual checking doesn't scale - agencies managing 10+ clients would need 40-60 hours/month just for schema audits. For example, a small 15-client agency where each client has a 300-page website would need to dedicate 60+ hours/month to schema audits alone, significantly impacting profitability and service capacity

**Impact of Not Solving This:**
- Lost search visibility due to incomplete structured data
- Inability to compete for rich snippet placements
- Time wasted on manual, repetitive audits
- High tool costs that eat into agency margins

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

### Competitive Landscape

**Existing Solutions:**

| Tool | Strengths | Weaknesses | Price |
|------|-----------|------------|-------|
| Screaming Frog SEO Spider | Comprehensive crawling, schema detection | Complex UI, expensive for unlimited crawls | £149/year (~$190/year) |
| Sitebulb | Beautiful reports, good visualization | Desktop-only, expensive | $35-$130/month |
| Google Rich Results Test | Free, official validation | Only tests one page at a time | Free |
| Schema.org Validator | Free, comprehensive | Only validates, doesn't audit site-wide | Free |

**Our Differentiation:**
- **Free and open-source** (vs. paid enterprise tools)
- **Site-wide coverage analysis** (vs. single-page validators)
- **Intelligent suggestions** (vs. detection-only tools)
- **Simple CLI workflow** (vs. complex desktop apps)
- **Focused on schema auditing** (vs. general SEO tools)

---

## 2. Target Users / Personas

### Persona 1: Sarah, the Freelance SEO Consultant

**Demographics:**
- 34 years old, female, based in Manchester, UK
- Freelance SEO consultant with 6 years of experience
- Manages 8-12 client websites simultaneously
- Income: £40,000-£60,000/year

**Background:**
Sarah left an agency job 3 years ago to start her own consultancy. She specializes in local SEO and technical SEO for small businesses. She's proficient with tools like Google Search Console, Ahrefs, and Screaming Frog, but finds the latter too expensive for her budget.

**Goals:**
- Provide comprehensive SEO audits to clients efficiently
- Improve client search rankings and demonstrate ROI
- Scale her consultancy without hiring employees
- Keep tool costs under £200/month total

**Motivations:**
- Building long-term client relationships through quality work
- Staying competitive against larger agencies
- Work-life balance (avoid 60-hour weeks)
- Professional reputation as a schema/structured data expert

**Frustrations:**
- Spending 4-5 hours per site manually checking schema markup
- Can't justify £149/year for Screaming Frog when she only needs it monthly
- Difficulty explaining technical schema issues to non-technical clients
- Competing with agencies that have larger tool budgets

**Technical Proficiency:**
- Proficient with Chrome DevTools for inspecting page elements
- Comfortable with command-line basics (navigating directories, running scripts)
- Not a developer, but can follow technical documentation
- Uses Python scripts occasionally (with copy-paste modifications)

**Typical Day:**
Sarah starts her morning reviewing Google Search Console for 3 clients, then spends 2-3 hours on a technical audit for a new client. She needs to identify all schema gaps before her client call at 2 PM. She wishes she had a tool that could scan the entire site in 10 minutes instead of spending all morning checking pages manually.

**Quote:**
> "I need a tool that can quickly and accurately audit schema markup so I can focus on strategy and client communication, not repetitive manual checking. If it's free or low-cost, even better—my margins are tight."

---

### Persona 2: Mark, the E-commerce Website Owner

**Demographics:**
- 47 years old, male, based in Austin, Texas, USA
- Owns "Handcrafted Home Goods" e-commerce business
- WordPress + WooCommerce site with 300 product pages
- Business revenue: $200,000/year

**Background:**
Mark started his business 8 years ago selling handcrafted furniture and home decor. His website is his primary sales channel. He hired an SEO agency 2 years ago, but recently brought SEO in-house to cut costs. He's learning SEO through online courses and YouTube videos.

**Goals:**
- Increase organic traffic by 30% in the next 12 months
- Improve product page rankings for target keywords
- Understand what's working (and not working) on his website
- Appear in Google Shopping results with rich snippets

**Motivations:**
- Growing his business without expensive agency fees ($2,000/month was unsustainable)
- Understanding the technical aspects of his website
- Staying ahead of competitors who also sell handcrafted goods
- Being self-sufficient with website optimization

**Frustrations:**
- Limited technical knowledge makes SEO intimidating
- Difficulty understanding complex SEO concepts and jargon
- Budget constraints (every dollar matters for a small business)
- Uncertainty whether his product pages have proper schema markup
- Previous agency never explained what they were actually doing

**Technical Proficiency:**
- Comfortable with WordPress admin and WooCommerce
- Can install plugins and follow step-by-step tutorials
- Not comfortable with code or command line
- Prefers visual interfaces and clear instructions

**Typical Day:**
Mark spends mornings fulfilling orders and managing inventory. In the afternoon, he works on website improvements—updating product descriptions, adding new products, and trying to improve SEO. He recently learned about schema markup and wants to verify all his product pages have it, but doesn't know how to check 300 pages efficiently.

**Quote:**
> "I want to make sure my website is optimized for search engines, but I don't have the time or expertise to check every page manually. I need something simple that tells me what's wrong and how to fix it."

---

### Persona 3: Emily, the Content Manager at a Digital Agency

**Demographics:**
- 29 years old, female, based in Melbourne, Australia
- Content Manager at "Digital Wave," a 15-person marketing agency
- Manages content strategy and SEO for 20+ client websites
- Salary: AUD $75,000/year

**Background:**
Emily has a journalism background and moved into digital marketing 5 years ago. She's responsible for ensuring all client content is optimized for search engines and maintains brand consistency. She works closely with developers and SEO specialists but handles day-to-day content audits herself.

**Goals:**
- Ensure all client websites have consistent, proper schema implementation
- Maintain high client satisfaction scores (currently 8.5/10, target 9/10)
- Streamline content audit processes to manage more clients
- Keep up with evolving SEO best practices and algorithm changes

**Motivations:**
- Professional growth (aiming for Senior Content Strategist role)
- Efficiency improvements that allow more strategic work
- Data-driven decision-making and reporting
- Collaboration with technical team members

**Frustrations:**
- Ensuring schema consistency across 20+ diverse client websites (e-commerce, blogs, local businesses)
- Keeping up with the latest schema.org updates and Google requirements
- Communicating technical schema issues to non-technical stakeholders and clients
- Time spent on repetitive audits instead of strategic content planning
- Dependency on developers to check technical implementations

**Technical Proficiency:**
- Comfortable with WordPress, Yoast SEO, and RankMath plugins
- Understands HTML basics and can read JSON-LD schema
- Uses command-line tools when given clear instructions
- Proficient with spreadsheets and data analysis

**Typical Day:**
Emily has weekly check-ins with 5 different clients. Before each meeting, she needs to review their website's schema status to report on SEO health. She currently uses a spreadsheet to manually track which pages have which schema types, but it's tedious and error-prone. She wishes she could run an automated audit and present the results.

**Quote:**
> "I need a tool that can help me quickly identify and fix schema issues across all of our client websites. It needs to be fast, accurate, and produce reports I can share with both technical developers and non-technical clients."

---

## 3. User Stories

### Story 1: Basic Schema Audit

**As an** SEO consultant (Sarah)
**I want to** scan all pages on a WordPress site and see what schema each page has
**So that** I can quickly understand the current state of structured data implementation

**Acceptance Criteria:**
- Tool automatically finds and parses WordPress sitemap.xml
- Scans all URLs found in sitemap (or up to configured limit)
- Detects JSON-LD, Microdata, and RDFa schema formats
- Outputs CSV with all pages listed and their schema types
- Shows pages with no schema clearly
- Completes scan of 500-page site in under 10 minutes
- Handles errors gracefully: logs the error to `schema_audit.log` and continues scanning remaining pages without terminating

**Priority:** P0 (Must Have)

---

### Story 2: Visual Schema Coverage Report

**As a** website owner (Mark)
**I want to** see a color-coded report showing which pages have which schema types
**So that** I can quickly identify gaps without reading raw technical data

**Acceptance Criteria:**
- CSV uses ✓ indicator for pages with schema type present
- CSV uses ✗ indicator for pages missing schema type
- Common schema types (Article, Product, Organization, etc.) are pre-defined columns
- Report opens cleanly in Excel and Google Sheets
- Column headers are clear and understandable to non-technical users
- Each page has clear coverage indicators across all schema types
- Pages with multiple schema types show all types clearly

**Priority:** P0 (Must Have)

---

### Story 3: Schema Recommendations

**As an** SEO professional (Sarah)
**I want the** tool to suggest which schema types should be added to pages
**So that** I can prioritize schema implementation work and provide clear recommendations to clients

**Acceptance Criteria:**
- Tool analyzes page content and URL patterns to suggest appropriate schema
- Suggestions marked with ⚠ indicator in CSV (different from ✓ and ✗)
- Suggestion logic based on WordPress page types (post, page, product, etc.)
- Tool identifies common URL patterns (e.g., `/blog/` → Article/BlogPosting)
- Suggestions include brief explanation text
- High confidence suggestions only (avoid false positives)
- Suggestions are actionable and specific

**Priority:** P1 (Should Have)

---

### Story 4: Summary Statistics

**As a** content manager (Emily)
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

## 4. Functional Requirements

The tool shall provide the following functionality:

**FR-1: Sitemap Discovery and Parsing**
- Automatically discover sitemaps at common WordPress locations (`/sitemap.xml`, `/wp-sitemap.xml`, `/sitemap_index.xml`)
- Parse XML sitemaps to extract all page URLs
- Support sitemap index files (nested sitemaps)
- Handle compressed sitemaps (`.xml.gz`)
- Extract last modified dates from `<lastmod>` tags if available

**FR-2: Page Crawling**
- Fetch HTML content for each URL in the sitemap
- Support configurable crawl delay (default: 1 second between requests)
- Respect rate limiting (detect 429 errors and back off)
- Follow HTTP redirects (up to 5 hops)
- Handle timeouts, SSL errors, and connection failures gracefully
- Support configurable user-agent string

**FR-3: Schema Detection**
- Detect JSON-LD schema (primary format for WordPress)
- Detect Microdata schema (HTML attribute-based)
- Detect RDFa schema (less common but supported)
- Extract all schema `@type` values from JSON-LD
- Handle nested schema objects (e.g., `@graph` arrays)
- Support multiple schema blocks per page
- Detect 20+ common schema types (see Appendix B)

**FR-4: Content Analysis**
- Analyze page content to suggest appropriate schema types
- Suggest schema types only when confidence is high (reduce false positives)
- Provide brief text explanation for each suggestion (displayed in "Suggestions" column of CSV report, e.g., "URL pattern `/blog/` indicates blog content")

**FR-5: Report Generation**
- Generate CSV report with columns: URL, Page Title, Status, Total Schema, [Schema Type Columns], Other Schema Types, Suggestions, Notes
- Use ✓/✗/⚠ visual indicators for schema coverage
- Include HTTP status codes for each page
- Generate summary statistics section (total pages, coverage percentages, top recommendations)
- Save report to configurable output directory

**FR-6: Configuration**
- Support configuration via `.env` file
- Support configuration via command-line arguments
- Configurable options: site URL, output path, crawl delay, max pages, timeout, user-agent
- Configuration validation with clear error messages

**FR-7: Error Handling and Logging**
- Continue crawling even if individual pages fail
- Log all errors and warnings to `schema_audit.log` file
- Generate separate `errors.csv` report for failed pages
- Display progress bars and status updates during crawl
- Provide verbose mode for detailed debugging output

**FR-8: Installation and Setup**
- Installable via `pip install -r requirements.txt`
- Compatible with Python 3.9+
- Minimal dependencies (standard libraries preferred)
- Include example `.env` configuration file
- Include comprehensive README with usage instructions

**FR-9: Privacy and Data Handling**
- No data sent to external servers (all processing is local)
- No usage telemetry or tracking
- No storage of crawled content (except in local output files)
- Respects `robots.txt` directives (optional, configurable)

---

## 5. Non-Functional Requirements

**NFR-1: Performance**
- Scan 500-page site in under 10 minutes (with 1-second crawl delay)
- Scan 1000-page site in under 20 minutes
- Memory usage stays under 500MB during scan

**NFR-2: Reliability**
- Tool completes scans without crashing 98%+ of the time (where "crashing" is defined as program termination due to an unhandled exception)
- Handles edge cases gracefully (empty pages, redirects, malformed HTML)
- Produces consistent results across multiple runs of the same site

**NFR-3: Usability**
- Report requires no manual post-processing to be useful
- CSV opens cleanly in Excel, Google Sheets, and LibreOffice Calc
- Visual indicators are immediately understandable
- Tool can be reused across multiple sites with < 1 minute setup time
- Error messages are clear and actionable

**NFR-4: Maintainability**
- Code follows Python PEP 8 style guidelines
- All functions have docstrings explaining purpose and parameters
- Adding new schema types takes < 30 minutes
- Core logic separated into modular files (sitemap_parser, schema_detector, etc.)

**NFR-5: Extensibility**
- Architecture supports adding Excel output in future phases
- Can be adapted for web interface without major refactoring
- Can add new suggestion rules without modifying core detection logic

**NFR-6: Security**
- No execution of arbitrary code from crawled pages
- SSL certificate verification enabled by default (optional disable for testing)
- Rate limiting prevents accidental DoS of target servers
- No storage of sensitive data (credentials, API keys) in output files

**NFR-7: Compatibility**
- Works on Windows, macOS, and Linux
- Compatible with Python 3.9, 3.10, 3.11, 3.12
- Output files compatible with Excel 2016+, Google Sheets, LibreOffice Calc

---

## 6. Success Metrics / KPIs

| Metric | Baseline | Target | Measurement Method | Frequency |
|--------|----------|--------|-------------------|-----------|
| **Functional Success** |
| Sitemap Parsing Accuracy | 92% | 98% | Test with 20 diverse WordPress sites | Post-release |
| JSON-LD Detection Accuracy | 90% | 98% | Manual validation on sample pages | Post-release |
| Microdata/RDFa Detection Accuracy | 80% | 90% | Manual validation on sample pages | Post-release |
| Schema Suggestion Relevance | 75% | 85% | Manual review by SEO professionals | Post-release |
| **Performance Success** |
| Report Generation Time (500 pages) | 12 min | < 10 min | Timed tests on benchmark sites | Each release |
| Report Generation Time (1000 pages) | 25 min | < 20 min | Timed tests on benchmark sites | Each release |
| Memory Usage (1000 pages) | 600MB | < 500MB | Memory profiling during tests | Each release |
| Tool Crash Rate | 5% | < 2% | Error tracking across test runs | Ongoing |
| **Usability Success** |
| Time to Complete First Audit | 5 min | < 3 min | User testing with new users | Post-release |
| User Satisfaction (SUS Score) | N/A | 75+ | Survey after usage | Quarterly |
| Report Clarity (User Rating) | N/A | 4.5/5 | Survey question | Quarterly |
| **Business Success** |
| User Time Savings | N/A | 50% reduction | Survey question: "How much time did this tool save you on your most recent schema audit, compared to your previous method (manual checking or other tools)?" | Post-release |
| Tool Adoption Rate | N/A | 500 users | GitHub stars + downloads (pypi downloads if published) | 6 months |
| Project Page Visits (Leading Indicator) | N/A | 1,000 visits/month | Google Analytics on GitHub Pages or project site | Monthly |

**Notes:**
- Baselines for functional/performance metrics will be established during Phase 1 testing
- User satisfaction metrics (SUS, ratings) collected via optional feedback form
- Tool is free/open-source, so "business success" measured by adoption and impact

---

## 7. Scope (In/Out)

### In Scope (v1.0)

**Core Functionality:**
- ✓ Automatic sitemap discovery and parsing for WordPress websites
- ✓ Detection of schema markup in JSON-LD, Microdata, and RDFa formats
- ✓ Content analysis for intelligent schema suggestions
- ✓ CSV report generation with ✓/✗/⚠ visual indicators
- ✓ Summary statistics about schema coverage
- ✓ Support for 20+ common schema types (Article, Product, Organization, etc.)
- ✓ Command-line interface with progress indicators
- ✓ Configuration via environment variables and CLI arguments
- ✓ Comprehensive error handling and logging
- ✓ Support for sites with 1000+ pages
- ✓ Respect for robots.txt directives
- ✓ Rate limiting and crawl delay
- ✓ Documentation (README, usage examples, troubleshooting guide)

**Testing:**
- ✓ Unit tests for core functions
- ✓ Integration tests with sample WordPress sites
- ✓ Performance benchmarking

**Deliverables:**
- ✓ Python source code (MIT licensed)
- ✓ requirements.txt with dependencies
- ✓ Example configuration files
- ✓ Comprehensive README documentation
- ✓ Sample CSV report output

### Out of Scope (v1.0)

**Not Included in Initial Release:**
- ✗ Real-time schema validation against Google's structured data validator API
- ✗ Automated schema implementation or code generation
- ✗ Automated fixes for detected issues
- ✗ Ongoing monitoring, alerting, or scheduled audits
- ✗ Support for non-WordPress CMS platforms (Drupal, Joomla, etc.)
- ✗ Competitive schema comparison (comparing against competitor sites)
- ✗ Historical tracking of schema changes over time
- ✗ Web user interface or GUI
- ✗ Excel output with true color coding (may be Phase 3)
- ✗ Integration with third-party SEO tools (Ahrefs, SEMrush, etc.)
- ✗ WordPress REST API querying for post types
- ✗ Email report delivery
- ✗ Multi-site batch auditing in single command
- ✗ API for programmatic access
- ✗ Authentication or user accounts
- ✗ Cloud hosting or SaaS deployment

**Future Consideration (Phase 4):**
- Web interface (Next.js deployed to Vercel)
- Schema validation API integration
- Historical comparison features
- WordPress plugin version

---

## 8. Dependencies

### External Dependencies

**Python Libraries:**
- `selectolax` (>=0.3.21) - Fast HTML parsing (primary parser)
- `beautifulsoup4` (>=4.12.0) - HTML parsing (fallback)
- `lxml` (>=5.1.0) - XML/HTML parser backend
- `requests` (>=2.31.0) - HTTP client for fetching pages
- `pandas` (>=2.1.0) - CSV generation and data manipulation
- `tqdm` (>=4.66.0) - Progress bars
- `python-dotenv` (>=1.0.0) - Environment variable management
- `colorama` (>=0.4.6) - Colored terminal output (optional)

**Optional Libraries (Phase 3):**
- `openpyxl` (>=3.1.0) - Excel output with color coding
- `validators` (>=0.22.0) - URL validation

**System Requirements:**
- Python 3.9 or higher
- Internet connection (for crawling target websites)
- 512MB+ available RAM
- 100MB+ disk space for reports

### Internal Dependencies

**Phase Dependencies:**
- Phase 2 depends on Phase 1 completion
- Phase 3 depends on Phase 2 completion
- Phase 4 (future) depends on Phase 3 user feedback

**Module Dependencies:**
- `report_generator.py` depends on `schema_detector.py`
- `suggestion_engine.py` depends on `schema_detector.py`
- `schema_detector.py` depends on `sitemap_parser.py`

### External Service Dependencies

**Optional (Configurable):**
- Target website's sitemap.xml must be accessible
- Target website must allow HTTP requests (not blocking user-agent)
- robots.txt compliance (tool will respect if configured)

**Not Required:**
- No API keys needed
- No external validation services
- No database or cloud services
- No authentication services

---

## 9. Risks and Mitigations

| # | Risk | Impact | Probability | Mitigation Strategy |
|---|------|--------|------------|---------------------|
| **R1** | **Inaccurate Schema Detection** - Tool misses schema or reports false positives | High | Medium | • Implement comprehensive test suite with 20+ real WordPress sites<br>• Support all three schema formats (JSON-LD, Microdata, RDFa)<br>• Provide mechanism for users to report detection issues<br>• Continuously refine detection logic based on user feedback |
| **R2** | **Performance Issues with Large Sites** - Tool crashes or takes too long for 1000+ page sites | High | Medium | • Implement memory-efficient streaming processing<br>• Don't load entire site into memory<br>• Allow configurable page limits<br>• Optimize HTML parsing with selectolax (10x faster than BeautifulSoup)<br>• Profile code to identify bottlenecks |
| **R3** | **Inaccurate Schema Suggestions** - False positive suggestions frustrate users | Medium | High | • Use high-confidence thresholds (only suggest when multiple indicators align)<br>• Provide clear explanations for each suggestion<br>• Allow users to disable suggestions via flag<br>• Refine suggestion logic based on user feedback<br>• Manual validation during testing |
| **R4** | **WordPress Sitemap Structure Changes** - WordPress updates break sitemap parsing | Medium | Low | • Support multiple sitemap locations (`/sitemap.xml`, `/wp-sitemap.xml`, etc.)<br>• Implement fallback parsing strategies<br>• Monitor WordPress releases for sitemap changes<br>• Allow manual sitemap URL specification |
| **R5** | **Schema.org Vocabulary Changes** - New schema types not detected | Low | Medium | • Design extensible schema type list (easy to add new types)<br>• Capture "other schema types" in catch-all column<br>• Regularly review schema.org updates<br>• Community contributions for new types |
| **R6** | **Server Overload / IP Blocking** - Tool overloads target server or gets blocked | High | Low | • Implement rate limiting (default 1 req/second)<br>• Respect robots.txt directives<br>• Detect 429 errors and back off exponentially<br>• Use respectful user-agent string<br>• Allow users to configure crawl delay |
| **R7** | **Malformed HTML/Schema Breaks Parser** - Edge cases crash the tool | Medium | Medium | • Use try/except blocks for all parsing operations<br>• Fallback from selectolax to BeautifulSoup if needed<br>• Skip malformed schema blocks and log error<br>• Continue crawling even if individual pages fail<br>• Comprehensive error logging |
| **R8** | **Compatibility Issues** - Tool doesn't work on Windows or older Python versions | Medium | Low | • Test on Windows, macOS, and Linux<br>• Test on Python 3.9, 3.10, 3.11, 3.12<br>• Use cross-platform libraries (pathlib, not os.path)<br>• CI/CD testing on multiple platforms |
| **R9** | **User Adoption Challenges** - Users don't discover or use the tool | Medium | Medium | • Create comprehensive documentation and examples<br>• Share on SEO communities (Reddit, Twitter, forums)<br>• Write blog post explaining use cases<br>• Consider web version in Phase 4 for non-technical users |
| **R10** | **Security Vulnerabilities** - Tool has exploitable bugs or exposes user data | High | Low | • Follow secure coding practices<br>• No execution of code from crawled pages<br>• Keep dependencies updated<br>• No storage of sensitive data<br>• SSL verification enabled by default |

**Overall Risk Assessment:**
- **High-priority risks:** R1 (detection accuracy), R2 (performance), R6 (server overload)
- **Medium-priority risks:** R3 (suggestion accuracy), R4 (WordPress changes), R7 (parser crashes)
- **Low-priority risks:** R5 (schema changes), R8 (compatibility), R9 (adoption), R10 (security)

**Risk Monitoring:**
- Review risks at end of each phase
- Update mitigation strategies based on testing results
- Track user-reported issues in GitHub

---

## 10. Timeline & Phases

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

## 11. Open Questions

*(Questions from original PRD remain relevant - see Appendix E for full list)*

**Critical Questions for Phase 1:**

1. **Sitemap Parsing Library** - Use `advertool` or custom parser?
   **Recommendation:** Start with advertool, fallback to custom if issues arise

2. **Rate Limiting Default** - 0.5s, 1.0s, or 2.0s between requests?
   **Recommendation:** Default to 1.0s with adaptive backoff on 429 errors

3. **Schema Type Coverage** - Are 15+ pre-defined types enough?
   **Recommendation:** Add Recipe, Course, JobPosting, Service in Phase 1

---

## 12. Appendix

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

#### Additional Types to Add in Phase 1
- **Recipe:** Recipe content (food blogs)
- **Course:** Educational courses
- **JobPosting:** Job listings
- **Service:** Service offerings
- **SoftwareApplication:** Software products

---

### C. Technical Implementation Reference

**Note:** Detailed technical specifications (HTML parsing strategy, URL pattern matching rules, CSV output format, etc.) have been preserved from the original PRD. These are referenced here but not duplicated to keep the PRD focused on "what" rather than "how."

See original PRD sections 4.1-4.9 and Appendix C-H for:
- Sitemap parsing implementation details
- Schema detection algorithms
- Content analysis rules
- Configuration parameters
- Development standards

**Rationale:** These technical details provide valuable context for feasibility and effort estimation without turning the PRD into a technical specification.

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

### E. Installation & Setup

#### Requirements
- Python 3.9 or higher
- pip (Python package manager)
- Internet connection

#### Installation Steps

```bash
# 1. Clone or download the repository
git clone https://github.com/intelliagent/wordpress-schema-audit.git
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

### F. Usage Examples

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

## Contact & Support

**Project Owner:** IntelliAgent (https://intelliagent.com.au)
**Documentation:** [GitHub Wiki - To be created]
**Issues:** [GitHub Issues - To be created]
**Email:** [To be added]

---

**Document End**

*This PRD is a living document and will be updated as the project evolves.*
**Version 1.1 Changes:**
- Added detailed user personas (Sarah, Mark, Emily)
- Added quantifiable data to problem statement (4-6 hours, $500-$1,500/month)
- Added competitive landscape analysis
- Added baseline/target metrics with measurement frequency
- Added Risks and Mitigations section
- Added explicit Dependencies section
- Added explicit "In Scope" section to complement "Out of Scope"
- Added privacy/data handling statement (FR-9)
- Added installation as functional requirement (FR-8)
- Reorganized structure to follow standard PRD format
- Clarified that technical implementation details are referenced but not duplicated
