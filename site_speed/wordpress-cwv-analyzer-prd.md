# Product Requirements Document: WordPress Core Web Vitals Analyzer

**Version:** 2.0
**Document Type:** PRD (Product Requirements Document)
**Date:** 2026-01-13
**Status:** Draft - Pending Adversarial Review

---

## Executive Summary

The WordPress Core Web Vitals (CWV) Analyzer is a Python CLI tool that bridges the gap between generic performance analysis and WordPress-specific, actionable optimization recommendations. While Google's PageSpeed Insights tells users "optimize images," our tool tells them "install ShortPixel plugin" or "add this code to functions.php."

**The Problem:** WordPress site owners struggle to translate PageSpeed Insights data into concrete actions within the WordPress ecosystem.

**The Solution:** A free, open-source CLI tool that analyzes WordPress sites, detects configuration issues, and provides prioritized, implementation-ready recommendations with multiple approaches (plugins, code snippets, hosting changes).

**Success Criteria:** Users report measurable CWV score improvements after implementing recommendations.

**Target v1 Launch:** 4-8 hours development time, focused on core analysis and recommendation engine.

---

## Problem Statement / Opportunity

### The Problem

1. **Generic analysis tools lack WordPress context**
   - PageSpeed Insights identifies issues but doesn't understand WordPress architecture
   - Recommendations like "reduce unused JavaScript" don't tell users which plugin is causing it
   - No guidance on WordPress-specific solutions (plugins, theme settings, hosting configs)

2. **WordPress users have varying technical levels**
   - Site owners don't know how to implement PSI recommendations
   - Developers waste time translating generic advice to WordPress fixes
   - Agencies need efficient tools to audit multiple client sites

3. **Existing premium tools are expensive**
   - WP Rocket, NitroPack, and similar tools charge monthly subscriptions
   - Many users need analysis, not automatic optimization
   - No free, community-driven alternative exists

### The Opportunity

- **28+ million active WordPress websites** (43% of the web)
- **Core Web Vitals became ranking factor** in 2021, sustained SEO importance
- **Growing demand for performance optimization** as sites become more complex
- **Open-source community** eager for free, quality tools

### Evidence of Need

- PageSpeed Insights has no WordPress-specific features despite WP market dominance
- Popular Reddit threads and forums ask "what PSI recommendations mean for WordPress"
- Agencies manually create WordPress optimization guides for clients (inefficient)

---

## Target Users / Personas

### Persona 1: "Alex the Agency Owner"

**Background:**
- Runs digital marketing agency with 20-30 WordPress client sites
- Understands WordPress ecosystem but isn't a developer
- Needs to audit sites and delegate implementation to team

**Goals:**
- Quickly assess client site performance
- Generate reports to share with clients and developers
- Prioritize optimization work by impact

**Pain Points:**
- Manually analyzing PSI results for each client site takes hours
- Generic recommendations require additional research to make WordPress-specific
- Clients ask "what do we do about this?" and expect actionable answers

**How this tool helps:**
- CLI enables batch analysis (future: script multiple sites)
- Reports are client-ready with clear priorities
- Recommendations include specific plugins and implementation options

---

### Persona 2: "Sam the Site Owner"

**Background:**
- Runs small business WordPress site (ecommerce, blog, services)
- Non-technical, uses plugins for everything
- DIY approach to save money

**Goals:**
- Fix Core Web Vitals warnings in Google Search Console
- Improve site speed without hiring a developer
- Understand what to do in plain English

**Pain Points:**
- PageSpeed Insights is full of technical jargon
- Doesn't know which WordPress plugins solve which problems
- Afraid of breaking site with wrong configuration

**How this tool helps:**
- Reports include plugin recommendations (no coding required)
- Multiple options presented with pros/cons
- Warnings about conflicting plugins prevent mistakes

---

### Persona 3: "Jordan the WordPress Developer"

**Background:**
- Freelance WordPress developer or agency technical lead
- Comfortable with PHP, WordPress internals, and server configs
- Needs efficient workflow to optimize client sites

**Goals:**
- Identify root causes of performance issues quickly
- Implement fixes properly the first time
- Document optimizations for clients

**Pain Points:**
- PSI shows symptoms, not root causes (which plugin is the problem?)
- Testing different optimizations manually is time-consuming
- Needs production-ready code snippets, not just concepts

**How this tool helps:**
- Detects problematic themes/plugins from HTML analysis
- Provides tested, safe code snippets for direct implementation
- Historical tracking shows impact of changes over time

---

## User Stories / Use Cases

### Epic 1: Site Analysis

**As Alex (Agency Owner),**
I want to run the tool against a client's WordPress site URL,
So that I can get a comprehensive performance report without manual PSI analysis.

**Acceptance Criteria:**
- Tool accepts any valid WordPress URL
- Analysis completes in < 3 minutes for typical site
- Report generated in multiple formats (MD, JSON, HTML, PDF)

---

**As Sam (Site Owner),**
I want the tool to tell me if my site is even WordPress before analyzing,
So that I don't get irrelevant recommendations.

**Acceptance Criteria:**
- Tool detects WordPress using multiple signals (wp-content, generator tag, /wp-json/, common scripts)
- Warns user if site doesn't appear to be WordPress
- Continues analysis with warning flag in report

---

**As Jordan (Developer),**
I want to see both mobile and desktop analysis when it matters,
So that I can optimize for both user bases appropriately.

**Acceptance Criteria:**
- Tool intelligently determines whether to run mobile-only or both strategies based on CrUX traffic data
- Default to mobile-first (Google's priority)
- CLI flag available to override: `--strategy mobile|desktop|both`

---

### Epic 2: WordPress-Specific Recommendations

**As Sam (Site Owner),**
I want plugin recommendations instead of code changes,
So that I can fix issues without hiring a developer.

**Acceptance Criteria:**
- Every recommendation includes at least one plugin option
- Plugins are currently maintained (last updated within 6 months)
- Alternatives provided (2-3 plugin options per issue)

---

**As Jordan (Developer),**
I want production-ready code snippets for functions.php modifications,
So that I can implement fixes confidently without debugging.

**Acceptance Criteria:**
- Code snippets include error handling and safety checks
- Comments explain what the code does
- Tested on WordPress 6.2+ before inclusion
- Clear instructions on where to add code

---

**As Alex (Agency Owner),**
I want recommendations prioritized by implementation ease (quick wins first),
So that I can show clients fast results and build momentum.

**Acceptance Criteria:**
- Recommendations ranked: plugin installs > settings changes > code modifications > infrastructure changes
- Each recommendation shows estimated implementation time (5 min, 30 min, 2 hours)
- "Quick Wins" section highlights easiest high-impact fixes

---

**As Jordan (Developer),**
I want the tool to detect and warn about conflicting plugins,
So that I can avoid making performance worse by stacking incompatible solutions.

**Acceptance Criteria:**
- Tool detects common conflicts (WP Rocket + Autoptimize, multiple caching plugins)
- Report warns about conflicts and recommends which plugin to keep
- Explains why the conflict occurs

---

### Epic 3: Report Generation and Exports

**As Sam (Site Owner),**
I want a simple, readable report that explains what's wrong,
So that I can understand my site's issues without technical background.

**Acceptance Criteria:**
- Report limited to top 10 issues (avoid overwhelm)
- Each issue explained in plain English
- Visual indicators (🔴 Critical, 🟡 Medium, 🟢 Quick Win)

---

**As Alex (Agency Owner),**
I want to export reports in multiple formats,
So that I can share with clients (PDF), developers (JSON), and track in version control (MD).

**Acceptance Criteria:**
- Markdown: readable, version-controllable, default format
- JSON: structured data for integrations and automation
- HTML: standalone browser-viewable with charts
- PDF: professional reports for client delivery
- CSV: quick data export for spreadsheets

---

**As Jordan (Developer),**
I want historical tracking of analysis runs,
So that I can measure the impact of my optimizations over time.

**Acceptance Criteria:**
- Analysis results stored locally in `~/.cwv-analyzer/<domain>/`
- JSON files include timestamp and all metrics
- Simple CLI command to compare two analysis runs: `python main.py compare <run1> <run2>`

---

### Epic 4: Error Handling and Edge Cases

**As any user,**
I want clear error messages when something goes wrong,
So that I know how to fix the problem or try again.

**Acceptance Criteria:**
- API rate limiting: "API rate limit reached. Wait 60 seconds and retry."
- Invalid URL: "Cannot access URL. Check that site is publicly accessible."
- Authentication required: "Site requires authentication. Analyze a publicly accessible page."
- PSI API down: "PageSpeed Insights unavailable. Try again later."

---

**As Sam (Site Owner),**
I want the tool to work even without a PageSpeed Insights API key,
So that I can try it without setup friction.

**Acceptance Criteria:**
- Tool works out-of-box with no API key (400 requests/100 seconds limit)
- Clear instructions in README on how to add API key for heavier usage
- When approaching rate limit, tool suggests getting API key

---

**As Jordan (Developer),**
I want the tool to handle sites behind CDNs gracefully,
So that I understand whether I'm seeing origin server or cached performance.

**Acceptance Criteria:**
- Tool detects CDN usage (Cloudflare, Fastly, CloudFront, etc.)
- Report includes warning: "CDN detected. Results reflect cached performance, not origin server."
- No attempt to bypass CDN (PSI analyzes real user experience)

---

## Functional Requirements

### FR-1: Input Validation and URL Handling

**Priority:** Must Have

- Accept WordPress site URL as command-line argument
- Validate URL format (auto-prepend https:// if missing)
- Test URL accessibility before calling PSI API
- Block private IP ranges (192.168.x.x, 10.x.x.x, 127.0.0.1)
- Block localhost and internal URLs (SSRF protection)
- Handle redirects (up to 5 redirects, 30s timeout)
- Report final analyzed URL in output

**Error Cases:**
- Invalid URL format: clear error with example
- Inaccessible URL: "Cannot connect to site"
- Authentication required (401/403): "Site requires public access"

---

### FR-2: WordPress Detection

**Priority:** Must Have

- Detect WordPress using multiple signals (require 2 of 4):
  1. Check for `wp-content` in HTML
  2. Look for `generator` meta tag
  3. Check common WP script handles (jquery.js?ver=)
  4. Test `/wp-json/` endpoint
- Detect WordPress version if available
- Detect theme from HTML (best effort)
- Detect plugins from script/style handles
- Detect page builders (Elementor, Divi, Beaver Builder)
- Detect CDN usage (Cloudflare, etc.)

**Warning Cases:**
- Site doesn't appear to be WordPress: proceed with warning
- Heavily cached site (plugin detection incomplete): note limitation
- Headless WordPress (React/Next.js frontend): adjust recommendations

---

### FR-3: PageSpeed Insights API Integration

**Priority:** Must Have

- Call PSI API for specified URL
- Optional API key (works without, recommended for heavy usage)
- Exponential backoff retry on failure (1s, 2s, 4s, 8s, max 3 retries)
- Handle rate limiting gracefully
- Handle API errors (500/502/503)
- Validate JSON response schema before parsing
- Parse Lab data (Lighthouse metrics)
- Parse Field data (CrUX metrics) when available
- Intelligent strategy selection:
  - Check CrUX traffic data to determine mobile vs desktop priority
  - Default to mobile (Google mobile-first indexing)
  - Option to override via `--strategy` flag

**Error Cases:**
- Rate limit: "Wait 60 seconds and retry"
- API unavailable: "Try again later"
- Malformed response: "Partial data available"

---

### FR-4: Core Web Vitals Analysis

**Priority:** Must Have

- Extract and parse Core Web Vitals:
  - **LCP (Largest Contentful Paint)**: target < 2.5s
  - **INP (Interaction to Next Paint)**: target < 200ms
  - **CLS (Cumulative Layout Shift)**: target < 0.1
- Calculate scores (0-100 scale)
- Categorize metrics: Good (green) / Needs Improvement (yellow) / Poor (red)
- Extract opportunities from Lighthouse audit:
  - Unused JavaScript
  - Unused CSS
  - Image optimization
  - Render-blocking resources
  - Font loading
  - Third-party impact
- Extract diagnostics (additional context)
- Parse potential savings (time in seconds)

**Data Handling:**
- Safe dictionary access (use `.get()` with defaults)
- Handle missing Field data (low-traffic sites)
- Handle null/undefined scores
- Highlight discrepancies between Lab and Field data

---

### FR-5: WordPress-Specific Recommendation Engine

**Priority:** Must Have

- Map PSI opportunities to WordPress solutions
- Maintain recommendation database (`config/recommendations.json`)
- For each issue, provide:
  - **Problem description** in plain English
  - **Impact estimate** (seconds saved, priority score)
  - **Multiple implementation options:**
    - Plugin recommendations (2-3 options with pros/cons)
    - Code snippets (production-ready with safety checks)
    - Hosting/server configuration changes
  - **Estimated implementation time** (5 min, 30 min, 2 hours)
  - **Difficulty level** (Easy, Moderate, Advanced)
  - **Links** to documentation, plugin pages, tutorials

**Prioritization Algorithm:**
- **Primary:** Implementation ease (plugin > settings > code > infrastructure)
- **Secondary:** Impact on CWV scores
- **Grouping:**
  - Critical Issues (high impact, immediate attention)
  - Quick Wins (low effort, visible results)
  - Medium Priority (important but more effort)
  - Low Priority (minor improvements)

**WordPress-Specific Intelligence:**
- Detect problematic themes/plugins and suggest alternatives
- Provide page builder-specific warnings (Elementor, Divi)
- Detect conflicting plugins (multiple caching, optimization plugins)
- Recommend which plugin to keep when conflicts detected
- Adjust recommendations based on detected WordPress version

---

### FR-6: Conflict Detection

**Priority:** Should Have

- Detect common plugin conflicts:
  - Multiple caching plugins (WP Rocket, W3 Total Cache, WP Super Cache)
  - Multiple optimization plugins (Autoptimize, WP Rocket, Perfmatters)
  - Image optimization overlaps
- Warn user about detected conflicts prominently
- Recommend which plugin to keep based on:
  - Current issues detected
  - Plugin capabilities and reputation
  - Ease of configuration
- Explain why the conflict occurs

---

### FR-7: Report Generation

**Priority:** Must Have

**Markdown Report (Default):**
```markdown
# Core Web Vitals Report: example.com
Generated: 2026-01-13 14:30:00
Strategy: Mobile (intelligent detection)

## Summary
- Performance Score: 75/100
- LCP: 2.8s 🟡 Needs Improvement
- INP: 150ms 🟢 Good
- CLS: 0.15 🟡 Needs Improvement

## WordPress Detection
- Platform: WordPress 6.4.2
- Theme: Astra Pro
- Page Builder: Elementor (detected)
- Detected Plugins: WooCommerce, Yoast SEO, Contact Form 7
- CDN: Cloudflare (results reflect cached performance)

## ⚠️ Conflicts Detected
- Multiple optimization plugins detected: Autoptimize + WP Rocket
- RECOMMENDATION: Keep WP Rocket (more comprehensive), disable Autoptimize

## 🔴 Critical Issues (High Impact)

### 1. Unoptimized Images [LCP Impact: -2.5s]
**Problem:** Large images loading without compression or modern formats.

**Solutions:**
📦 **Plugin Options (Easy - 5 min):**
- ShortPixel Image Optimizer (Recommended)
  - Pros: Automatic conversion to WebP, lazy loading, good free tier
  - Cons: Requires API key, monthly limits on free plan
- EWWW Image Optimizer
  - Pros: No external API, unlimited images
  - Cons: Slower processing, server resource intensive

💻 **Code Option (Moderate - 30 min):**
```php
// Add to functions.php
add_filter( 'wp_get_attachment_image_attributes', 'add_lazy_loading', 10, 2 );
function add_lazy_loading( $attr, $attachment ) {
    if ( ! isset( $attr['loading'] ) ) {
        $attr['loading'] = 'lazy';
    }
    return $attr;
}
```

🔗 **Resources:**
- [ShortPixel Plugin](https://wordpress.org/plugins/shortpixel-image-optimiser/)
- [WordPress Image Optimization Guide](https://wordpress.org/support/article/optimization/)

---

## 🟢 Quick Wins (Easy Fixes)

### 2. Missing Browser Caching [Savings: 0.5s]
...

## 📊 Detailed Metrics
[Lab Data vs Field Data comparison if both available]
...

## 📈 Next Steps
1. Install ShortPixel and optimize images (biggest impact)
2. Resolve Autoptimize/WP Rocket conflict
3. Enable browser caching via hosting control panel
...
```

**JSON Export:**
- Structured data for programmatic access
- All metrics, recommendations, timestamps
- Machine-readable for integrations

**HTML Report:**
- Standalone browser-viewable file
- Charts for visual score representation
- Professional formatting for client delivery
- Embedded CSS (no external dependencies)

**PDF Report:**
- Formatted version of markdown for professional sharing
- Client-ready appearance

**CSV Export:**
- Quick tabular data export
- Recommendations with priority, impact, effort columns

---

### FR-8: Data Persistence and History

**Priority:** Should Have

- Store analysis results in `~/.cwv-analyzer/<domain>/`
- JSON files named by timestamp: `2026-01-13-143000.json`
- Include full metrics, recommendations, detected config
- CLI command to list historical runs: `python main.py history example.com`
- CLI command to compare runs: `python main.py compare <domain> <run1> <run2>`
- Comparison shows:
  - Score changes (delta)
  - New issues appeared / resolved
  - Recommendations still relevant

---

### FR-9: CLI Interface

**Priority:** Must Have

```bash
# Basic usage (default: markdown output, mobile strategy, intelligent detection)
python main.py https://example.com

# Specify output format
python main.py https://example.com --format markdown
python main.py https://example.com --format json
python main.py https://example.com --format html
python main.py https://example.com --format pdf
python main.py https://example.com --format all  # generates all formats

# Specify strategy
python main.py https://example.com --strategy mobile
python main.py https://example.com --strategy desktop
python main.py https://example.com --strategy both

# Custom output location
python main.py https://example.com --output ~/Desktop/report.md

# Use API key (optional, better rate limits)
python main.py https://example.com --api-key YOUR_KEY
# Or set environment variable: PAGESPEED_API_KEY

# Historical comparison
python main.py history example.com
python main.py compare example.com run1 run2

# Help
python main.py --help
```

---

## Non-Functional Requirements

### NFR-1: Performance

- Analysis completes in < 3 minutes for typical WordPress site
- API calls timeout after 60 seconds
- Retry logic with exponential backoff
- Graceful handling of slow sites (report partial data)

### NFR-2: Reliability

- Handle all error cases gracefully (no crashes)
- Validate all external inputs (URLs, API responses)
- Safe dictionary access throughout codebase
- Fail gracefully with partial data when possible

### NFR-3: Security

- Block SSRF attacks (private IPs, localhost)
- Escape all user input in reports
- No shell command execution with user input
- No persistent storage of site HTML/data (only generated reports)
- Pin dependency versions in requirements.txt
- Sanitize URLs before display

### NFR-4: Usability

- Clear, actionable error messages
- Progress indicators during analysis
- Rich terminal output (colors, formatting via `rich` library)
- Reports readable by non-technical users
- Links to documentation and resources

### NFR-5: Maintainability

- Modular code structure (separate API, analysis, reporting)
- Type hints for key functions
- Docstrings for all public functions
- Comprehensive test coverage (unit + integration)
- Recommendation database externalized (JSON config)
- Quarterly manual review of recommendation database

### NFR-6: Compatibility

- Python 3.10+
- Cross-platform (macOS, Linux, Windows)
- WordPress 6.2+ (last 3 major versions)
- Works with and without PSI API key

---

## Success Metrics / KPIs

### Primary Success Metric (User Outcome)

**Users report measurable CWV score improvements**
- Target: 70% of users who implement recommendations see score increase
- Measurement: Post-implementation surveys, GitHub issue reports, community feedback
- Validation: Track "success stories" shared in issues/discussions

### Secondary Metrics (Adoption)

1. **GitHub Stars:** Indicator of community interest
   - Target: 100+ stars in first 3 months

2. **Weekly Active Users:** Downloads and usage
   - Target: 50+ users running analyses weekly after 3 months

3. **Recommendation Effectiveness:** Quality feedback
   - Track which recommendations users report as most helpful
   - Iterate database based on user feedback

4. **Community Contributions:** PRs for recommendation database
   - Target: 5+ community-contributed recommendations accepted by month 6

### Quality Metrics (Tool Reliability)

1. **Error Rate:** Percentage of analyses that fail
   - Target: < 5% failure rate

2. **WordPress Detection Accuracy:** False positives/negatives
   - Target: > 95% accurate WordPress detection

3. **Report Quality:** User satisfaction with report clarity
   - Target: 80%+ satisfaction based on feedback

---

## Scope

### In Scope (v1 - Must Have)

✅ URL input with validation
✅ PageSpeed Insights API integration
✅ WordPress detection (version, theme, plugins)
✅ Core Web Vitals analysis (LCP, INP, CLS)
✅ WordPress-specific recommendation engine
✅ Plugin conflict detection
✅ Multiple implementation options per issue (plugin, code, hosting)
✅ Production-ready code snippets with safety checks
✅ Prioritization by implementation ease
✅ Multiple export formats (MD, JSON, HTML, PDF, CSV)
✅ Local historical storage (JSON files)
✅ Intelligent mobile/desktop strategy selection
✅ CDN detection and warnings
✅ Error handling and graceful failures
✅ Rich CLI output with progress indicators

### In Scope (v1 - Should Have)

⭐ Historical comparison between runs
⭐ Page builder detection and warnings
⭐ Field data (CrUX) analysis when available
⭐ Estimated implementation time per recommendation

### Nice to Have (v1 - Could Defer)

💎 Configurable output verbosity (--verbose, --quiet flags)
💎 Recommendation filtering by category (--focus images, --focus caching)
💎 Export to task management format (GitHub Issues, Trello, etc.)

### Out of Scope (v1 - Future Versions)

❌ Automated fix implementation (one-click apply)
❌ Continuous monitoring and scheduled audits
❌ Batch processing multiple sites from CSV
❌ Web GUI or dashboard
❌ WordPress plugin version (run from WP admin)
❌ Before/after testing simulation (Puppeteer integration)
❌ Real-time analysis while editing site
❌ Team collaboration features
❌ Cloud storage or sync
❌ Commercial hosting/SaaS version

---

## Dependencies

### External Dependencies

1. **PageSpeed Insights API**
   - Free tier: 400 requests/100 seconds
   - With API key: 25,000 requests/day
   - Risk: API changes or deprecation
   - Mitigation: Version API calls, monitor Google updates, fallback to local Lighthouse

2. **WordPress Plugin Repository**
   - Source of plugin recommendations
   - Risk: Plugins become outdated or abandoned
   - Mitigation: Quarterly manual review of recommendations, include multiple alternatives

### Technical Dependencies

```
Python 3.10+
requests==2.31.0          # HTTP library for API calls
beautifulsoup4==4.12.2    # HTML parsing for WordPress detection
rich==13.7.0              # Terminal formatting and progress bars
python-dotenv==1.0.0      # Environment variable management
markdown==3.5.1           # Markdown to HTML conversion
pdfkit==1.0.0             # PDF generation
```

### System Dependencies

- `wkhtmltopdf` for PDF generation (optional, graceful fallback if missing)

---

## Risks and Mitigations

### Risk 1: Recommendations Don't Improve Scores (CRITICAL)

**Impact:** Tool loses credibility, users abandon it
**Likelihood:** High (biggest user concern from interview)
**Mitigation:**
- **Pre-launch validation:** Test recommendations on 10-20 real WordPress sites, measure actual improvements
- **Community feedback loop:** Encourage users to report results (positive and negative)
- **Recommendation database versioning:** Track which recommendations work, iterate quarterly
- **Include case study links:** Each recommendation links to evidence of effectiveness
- **Set realistic expectations:** Disclaimers that results depend on proper implementation

---

### Risk 2: PageSpeed Insights API Changes

**Impact:** Tool breaks, needs urgent maintenance
**Likelihood:** Medium (Google changes APIs occasionally)
**Mitigation:**
- Version API calls with explicit API version
- Validate JSON schema before parsing (graceful handling of schema changes)
- Monitor Google's API changelog
- Community alerts (GitHub issues) for breakage
- Fallback: Local Lighthouse execution (future enhancement)

---

### Risk 3: Recommendation Database Becomes Outdated

**Impact:** Tool recommends abandoned plugins, outdated code
**Likelihood:** High without maintenance
**Mitigation:**
- **Quarterly manual reviews:** Maintainers check plugin status, update recommendations
- **Plugin version warnings:** Include "Last verified: 2026-01" in database
- **Multiple alternatives:** Provide 2-3 plugin options so if one dies, others remain
- **Community contributions:** Accept PRs for recommendation updates
- **Automated monitoring (future):** Script to check WordPress.org for plugin update dates

---

### Risk 4: Tool Doesn't Differentiate from Existing Solutions

**Impact:** Low adoption, limited value proposition
**Likelihood:** Low (WordPress-specific focus is unique)
**Mitigation:**
- **Clear positioning:** Emphasize WordPress-specific intelligence in all marketing
- **Quality over features:** Focus on recommendation accuracy over feature bloat
- **Community engagement:** Build in open, involve WordPress community in development
- **Documentation:** Case studies showing real improvements

---

### Risk 5: Code Snippets Break Sites

**Impact:** Users implement code, site crashes, tool blamed
**Likelihood:** Medium (WordPress environments vary)
**Mitigation:**
- **Production-ready code only:** All snippets tested on WordPress 6.2+
- **Safety checks in code:** Error handling, capability checks, validation
- **Clear instructions:** "Add to child theme functions.php" (not parent theme)
- **Backup warnings:** Always recommend site backup before code changes
- **Disclaimers:** "Test in staging environment first" in documentation
- **Community validation:** Other developers review snippets via GitHub PRs

---

### Risk 6: Security Vulnerability in Tool

**Impact:** Tool used for attacks (SSRF, XSS, etc.)
**Likelihood:** Low (following security best practices)
**Mitigation:**
- Block private IPs and localhost (SSRF protection)
- Escape all user input in reports
- No shell command execution with user input
- Pin dependency versions
- Regular security audits (`pip audit`)
- Responsible disclosure policy in README

---

## Timeline / Milestones

**Note:** Time estimates are for development only, not project timeline commitments.

### Phase 1: Core Functionality (4-6 hours)

- Project setup, structure, dependencies
- API client module (PSI integration, retries, error handling)
- WordPress detection module
- Core Web Vitals parsing
- Basic recommendation engine
- Markdown report generation
- CLI interface

**Deliverable:** MVP that analyzes a WordPress site and generates markdown report

---

### Phase 2: Recommendation Database (2-3 hours)

- Create `recommendations.json` structure
- Populate with initial WordPress solutions (images, caching, scripts, CSS, fonts)
- Add plugin recommendations with pros/cons
- Add code snippets with safety checks
- Implement prioritization algorithm

**Deliverable:** WordPress-specific recommendations functional

---

### Phase 3: Advanced Features (2-3 hours)

- Multiple export formats (JSON, HTML, PDF, CSV)
- Local historical storage
- Comparison between runs
- Conflict detection
- Page builder detection
- CDN detection
- Intelligent strategy selection

**Deliverable:** Full-featured v1 ready for testing

---

### Phase 4: Testing & Validation (3-5 hours)

- Unit tests for core modules
- Integration tests with real PSI API
- Manual testing on 10+ WordPress sites
- Recommendation validation (implement and measure results)
- Documentation (README, usage examples, troubleshooting)

**Deliverable:** Tested, documented v1 ready for release

---

### Total Estimated Time: 11-17 hours

*Original estimate: 4-8 hours*
*Updated estimate: ~15 hours for fully-featured, validated v1*

**Note:** Estimates assume experienced Python developer familiar with WordPress. Recommendation validation testing (implementing fixes and measuring results) is the largest variable.

---

## Documentation Requirements

### README.md

- Quick start guide (install and run)
- Requirements (Python 3.10+, optional wkhtmltopdf)
- Installation instructions (`pip install -r requirements.txt`)
- Usage examples (basic, with flags, all formats)
- PageSpeed Insights API key setup (optional)
- Troubleshooting common errors
- Limitations and known issues
- Contributing guidelines
- License (open source)

### Code Documentation

- Docstrings for all public functions (Google or NumPy style)
- Type hints for function signatures
- Module-level descriptions
- Inline comments for complex logic
- README in each module folder explaining purpose

### User Guide (in reports or separate doc)

- How to interpret Core Web Vitals scores
- What each recommendation means in WordPress context
- When to use plugin vs code vs hosting solutions
- Prioritization logic explanation
- When to hire a developer vs DIY
- Backup and testing best practices

---

## Approval Checklist

Before starting development:

- [x] Interview completed, requirements clarified
- [ ] Adversarial specification review (pending)
- [ ] All user stories clear and testable
- [ ] Success criteria measurable and agreed upon
- [ ] Risks identified and mitigations planned
- [ ] Security requirements understood
- [ ] Timeline realistic (adjusted to 15 hours)
- [ ] Scope locked (no additions without explicit approval)
- [ ] Validation plan defined (10+ site testing)

**Next Steps:**
1. Run this PRD through adversarial debate with multiple LLMs
2. Incorporate feedback and finalize
3. Generate companion Technical Specification
4. Begin development with approved spec

---

## Appendix A: Recommendation Database Structure

```json
{
  "recommendations": [
    {
      "id": "optimize-images",
      "psi_opportunity": "uses-optimized-images",
      "cwv_impact": ["LCP"],
      "priority": "critical",
      "title": "Optimize and Compress Images",
      "problem": "Large images loading without compression or modern formats (WebP, AVIF)",
      "impact_estimate": "2-4 seconds saved on LCP",
      "solutions": [
        {
          "type": "plugin",
          "difficulty": "easy",
          "time": "5 min",
          "name": "ShortPixel Image Optimizer",
          "url": "https://wordpress.org/plugins/shortpixel-image-optimiser/",
          "pros": ["Automatic WebP conversion", "Lazy loading included", "Good free tier"],
          "cons": ["Requires API key", "Monthly limits on free plan"],
          "instructions": "Install plugin, enter API key, run bulk optimization"
        },
        {
          "type": "code",
          "difficulty": "moderate",
          "time": "30 min",
          "description": "Add lazy loading to images via functions.php",
          "snippet": "// Add to child theme functions.php\nadd_filter( 'wp_get_attachment_image_attributes', 'add_lazy_loading', 10, 2 );\nfunction add_lazy_loading( $attr, $attachment ) {\n    if ( ! isset( $attr['loading'] ) ) {\n        $attr['loading'] = 'lazy';\n    }\n    return $attr;\n}",
          "instructions": "Add to child theme functions.php, test that images still load"
        }
      ],
      "resources": [
        "https://wordpress.org/support/article/optimization/",
        "https://web.dev/optimize-lcp/"
      ],
      "last_verified": "2026-01"
    }
  ]
}
```

---

## Appendix B: User Flow Diagram

```
User Input: URL
    ↓
Validate URL
    ↓
Test Accessibility
    ↓
Detect WordPress (4 signals) ──→ [Warning if not WP, continue]
    ↓
Intelligent Strategy Detection (check CrUX traffic)
    ↓
Call PageSpeed Insights API
    ↓
[Retry on failure] ──→ [Max 3 retries] ──→ [Graceful error if all fail]
    ↓
Parse Response (Lab + Field data)
    ↓
Analyze Core Web Vitals (LCP, INP, CLS)
    ↓
Extract Opportunities & Diagnostics
    ↓
Map to WordPress Recommendations (recommendations.json)
    ↓
Detect Conflicts (multiple caching/optimization plugins)
    ↓
Prioritize by Implementation Ease
    ↓
Generate Report(s) ──→ Markdown, JSON, HTML, PDF, CSV
    ↓
Store History (~/.cwv-analyzer/<domain>/)
    ↓
Display Report & Summary
```

---

**End of PRD**
