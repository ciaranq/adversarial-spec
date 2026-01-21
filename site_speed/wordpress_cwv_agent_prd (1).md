# Adversarial Specification
# WordPress Core Web Vitals Analyzer

**Version:** 1.0  
**Type:** Python CLI Script  
**Estimated Build Time:** 4-8 hours

---

## Overview

A Python script that analyzes WordPress sites for Core Web Vitals issues using PageSpeed Insights API, detects WordPress-specific problems, and generates actionable optimization reports.

**What it does:**
1. Takes WordPress URL as input
2. Calls PageSpeed Insights API
3. Parses results for WordPress-specific issues
4. Generates prioritized recommendations
5. Outputs markdown report

**What it does NOT do (v1):**
- Modify live sites
- Run real-time monitoring
- Process multiple sites in batch
- Test changes before implementation (future)
- Require authentication to WordPress sites

---

## Critical Failure Modes

### 1. API Failures

**Failure:** PageSpeed Insights API rate limiting
- **Impact:** Script hangs or crashes
- **Mitigation:** 
  - Implement exponential backoff (1s, 2s, 4s, 8s)
  - Max 3 retries before graceful failure
  - Clear error message: "API rate limit reached. Wait 60 seconds and retry."
  - Log API response codes

**Failure:** API returns 500/502/503 errors
- **Impact:** Script crashes with unclear error
- **Mitigation:**
  - Catch HTTP exceptions explicitly
  - Return user-friendly error: "PageSpeed Insights unavailable. Try again later."
  - Don't expose raw API error messages

**Failure:** API response structure changes
- **Impact:** Script fails to parse data, crashes
- **Mitigation:**
  - Validate JSON schema before parsing
  - Use `response.get('key', default)` instead of `response['key']`
  - Fail gracefully with partial data: "Warning: Some metrics unavailable"

### 2. Input Validation Failures

**Failure:** User provides non-WordPress site
- **Impact:** Analysis runs but recommendations are irrelevant
- **Mitigation:**
  - Check for WordPress signatures in HTML (wp-content, wp-includes)
  - Warn user: "Warning: Site does not appear to be WordPress. Results may not apply."
  - Continue analysis but flag in report

**Failure:** User provides invalid URL
- **Examples:**
  - Missing protocol: `example.com` instead of `https://example.com`
  - Local URLs: `localhost:3000`
  - Invalid domains: `http://not-a-real-site`
- **Mitigation:**
  - Validate URL format with regex
  - Auto-prepend `https://` if missing
  - Test URL accessibility before API call
  - Error: "Cannot access URL. Check that site is publicly accessible."

**Failure:** User provides URL with authentication
- **Impact:** PageSpeed cannot access, returns error
- **Mitigation:**
  - Detect 401/403 responses
  - Error: "Site requires authentication. Analyze a publicly accessible page."
  - Document limitation in README

**Failure:** Redirect chains or infinite redirects
- **Impact:** API timeout or unexpected results
- **Mitigation:**
  - Set max redirects in requests (5)
  - Timeout after 30 seconds
  - Report final URL analyzed: "Analyzed: https://final-url.com (redirected)"

### 3. WordPress Detection Failures

**Failure:** WordPress site uses custom directory structure
- **Impact:** False negative on WordPress detection
- **Mitigation:**
  - Multiple detection methods:
    1. Check for `wp-content` in HTML
    2. Look for `generator` meta tag
    3. Check common WP script handles
    4. Test `/wp-json/` endpoint
  - Require 2/4 positive for confidence

**Failure:** Heavily cached or CDN-optimized WordPress site
- **Impact:** Cannot detect plugins or theme from HTML
- **Mitigation:**
  - Document limitation: "Plugin detection requires unoptimized HTML"
  - Focus on observable issues (images, scripts, fonts)
  - Don't fail if detection incomplete

**Failure:** Headless WordPress or decoupled frontend
- **Impact:** WordPress detected but front-end is React/Next.js
- **Mitigation:**
  - Detect frontend framework from scripts
  - Warning: "Headless WordPress detected. Some recommendations may not apply."
  - Provide generic optimization advice

### 4. Data Parsing Failures

**Failure:** Lighthouse audit has unexpected structure
- **Impact:** KeyError crashes script
- **Mitigation:**
  - Safe dictionary access everywhere
  - Default values for all metrics
  - Log warnings for missing data
  - Continue with available data

**Failure:** Missing CrUX field data (new/low-traffic sites)
- **Impact:** Script expects field data that doesn't exist
- **Mitigation:**
  - Check `field_data` presence before parsing
  - Report: "No real user data available (low traffic or new site)"
  - Rely on Lab data only

**Failure:** Scores are null or undefined
- **Impact:** Cannot calculate priorities or display results
- **Mitigation:**
  - Default scores to 0 if missing
  - Flag in report: "Some metrics unavailable"
  - Calculate priorities from available data

### 5. Recommendation Generation Failures

**Failure:** Generic recommendations not relevant to WordPress
- **Impact:** User gets unhelpful advice
- **Mitigation:**
  - WordPress-specific recommendation database
  - Map PSI opportunities to WP solutions
  - Always include plugin options for common issues

**Failure:** Outdated plugin recommendations
- **Impact:** User installs abandoned/incompatible plugins
- **Mitigation:**
  - Version recommendations with last-updated date
  - Include alternative plugins (2-3 options)
  - Link to WordPress plugin repository for version check

**Failure:** Conflicting recommendations
- **Example:** Recommend both WP Rocket and Autoptimize (conflict)
- **Mitigation:**
  - Mark mutually exclusive recommendations
  - Prioritize comprehensive solutions over piecemeal
  - Group by implementation approach (plugin vs code vs hosting)

### 6. Report Generation Failures

**Failure:** Report file write permission denied
- **Impact:** Script completes but no output saved
- **Mitigation:**
  - Check write permissions before analysis
  - Default to user home directory if current dir fails
  - Print report to stdout as fallback

**Failure:** Report too large or malformed markdown
- **Impact:** Report unreadable or crashes markdown viewers
- **Mitigation:**
  - Limit detailed sections (top 10 issues)
  - Validate markdown syntax
  - Include table of contents for navigation

**Failure:** Special characters in URL break filename
- **Impact:** Cannot create file with URL-based name
- **Mitigation:**
  - Sanitize URLs for filenames (remove special chars)
  - Use domain name only for file: `example-com-cwv-report.md`
  - Include full URL in report header

---

## Security Concerns

### 1. Malicious Input

**Attack:** User provides URL to malicious site that returns XSS payload
- **Risk:** If report rendered as HTML, could execute scripts
- **Mitigation:**
  - Escape all user input in reports
  - Use markdown only (no HTML rendering in v1)
  - Sanitize URLs before display

**Attack:** SSRF via URL manipulation to scan internal networks
- **Example:** `http://192.168.1.1/admin` or `http://localhost:5432`
- **Mitigation:**
  - Validate URLs against allowed schemes (https/http only)
  - Block private IP ranges (RFC1918)
  - Block localhost/127.0.0.1
  - Use PSI API (they handle SSRF protection)

**Attack:** Command injection via URL
- **Example:** URL with shell metacharacters: `example.com; rm -rf /`
- **Mitigation:**
  - Never use URL in shell commands
  - Pass URLs as strings to API only
  - No subprocess calls with user input

### 2. Data Privacy

**Risk:** Storing analyzed site data without consent
- **Mitigation:**
  - No persistent storage of site HTML/data
  - Only save generated reports locally
  - Document in README: "No data sent to third parties except PSI API"

**Risk:** Exposing sensitive info in reports
- **Examples:** API keys in scripts, internal IPs, private URLs
- **Mitigation:**
  - Sanitize all URLs (remove query params by default)
  - Don't log full API responses
  - Warn users before sharing reports publicly

### 3. Dependency Security

**Risk:** Malicious packages in dependencies
- **Mitigation:**
  - Pin all dependency versions in requirements.txt
  - Use well-known packages only (requests, beautifulsoup4, rich)
  - No subprocess execution of untrusted code
  - Regular dependency audits (`pip audit`)

**Risk:** Outdated dependencies with known vulnerabilities
- **Mitigation:**
  - Include versions in requirements.txt
  - Document update schedule (quarterly)
  - Provide update instructions in README

---

## Edge Cases & Boundary Conditions

### 1. Unusual Site Configurations

**Edge Case:** Site behind Cloudflare or aggressive CDN
- **Behavior:** PSI may see heavily cached/optimized version
- **Impact:** Scores don't reflect typical user experience
- **Handling:** Note in report if CDN detected, suggest testing origin server

**Edge Case:** Site with geo-restrictions
- **Behavior:** PSI cannot access from Google's servers
- **Impact:** API returns error or partial data
- **Handling:** Error message: "Site may be geo-restricted. PSI requires global accessibility."

**Edge Case:** Very slow sites (30+ seconds to load)
- **Behavior:** API timeout or very poor scores
- **Impact:** May not get complete metrics
- **Handling:** Set timeout to 60s, report what data is available

**Edge Case:** Mobile-only or desktop-only optimized sites
- **Behavior:** Scores vary drastically between strategies
- **Impact:** Recommendations may not apply to both
- **Handling:** 
  - Run both mobile and desktop analyses
  - Note strategy in recommendations
  - Default to mobile (Google's mobile-first indexing)

### 2. WordPress Variations

**Edge Case:** WordPress.com vs WordPress.org
- **Behavior:** WP.com has different plugin/theme restrictions
- **Impact:** Recommendations may not be applicable
- **Handling:** Detect WP.com (check for wp.com in HTML comments), adjust recommendations

**Edge Case:** Multisite WordPress installation
- **Behavior:** Different sites may share themes/plugins
- **Impact:** Generic analysis may miss site-specific issues
- **Handling:** Analyze each URL independently, note if multisite detected

**Edge Case:** WordPress with page builders (Elementor, Divi)
- **Behavior:** Page builders add significant overhead
- **Impact:** Need specific optimization strategies
- **Handling:** Detect page builder from HTML classes/scripts, add builder-specific recommendations

**Edge Case:** Completely headless WordPress (REST API only)
- **Behavior:** Frontend is separate (React, Next.js, etc.)
- **Impact:** WordPress plugin recommendations irrelevant
- **Handling:** Detect if analyzing frontend only, provide frontend-specific advice

### 3. Data Anomalies

**Edge Case:** Site with no CrUX data (new site, low traffic)
- **Behavior:** Field data unavailable
- **Impact:** Can only provide Lab data analysis
- **Handling:** Clear note in report: "Real user data unavailable (new/low-traffic site)"

**Edge Case:** Huge discrepancy between Lab and Field data
- **Example:** Lab score 95, Field score 40
- **Impact:** Unclear which to trust
- **Handling:** 
  - Highlight discrepancy prominently
  - Explain difference (Lab vs Real Users)
  - Prioritize Field data for recommendations

**Edge Case:** All scores are already excellent (>90)
- **Behavior:** No significant issues to report
- **Impact:** Report seems empty or unhelpful
- **Handling:** 
  - Congratulate user
  - Provide advanced optimization tips
  - Suggest monitoring setup

**Edge Case:** Lighthouse audit returns warnings/errors
- **Example:** "Page took too long to load", "Chrome crashed"
- **Impact:** Incomplete or no metrics
- **Handling:** 
  - Retry up to 2 times
  - Report partial data if available
  - Error: "Audit could not complete. Site may be too slow or unstable."

---

## Technical Specifications

### Required Python Dependencies
```
requests==2.31.0
beautifulsoup4==4.12.2
rich==13.7.0
python-dotenv==1.0.0
```

### Project Structure
```
wordpress-cwv-analyzer/
├── src/
│   ├── __init__.py
│   ├── api_client.py       # PSI API calls
│   ├── analyzer.py         # Parse & analyze results
│   ├── wordpress.py        # WP detection & recommendations
│   └── report.py           # Generate markdown reports
├── config/
│   └── recommendations.json  # WP-specific fix database
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── main.py                 # CLI entry point
```

### CLI Interface
```bash
# Basic usage
python main.py https://example.com

# With options
python main.py https://example.com --strategy mobile --output report.md

# Help
python main.py --help
```

### API Rate Limits
- **PageSpeed Insights**: 400 requests/100 seconds (no key), 25,000/day (with key)
- **Handling**: Exponential backoff, max 3 retries, clear error messages

### Output Format
```markdown
# Core Web Vitals Report: example.com
Generated: 2026-01-13 14:30:00

## Summary
- Performance Score: 75/100
- LCP: 2.8s (Needs Improvement)
- INP: 150ms (Good)
- CLS: 0.15 (Needs Improvement)

## WordPress Detection
- Platform: WordPress 6.4.2
- Theme: Astra Pro
- Detected Plugins: WooCommerce, Yoast SEO, Contact Form 7

## Critical Issues (High Priority)
1. [LCP] Large images not optimized (savings: 2.5s)
   - SOLUTION: Install ShortPixel or EWWW Image Optimizer
   - CODE: Add to functions.php... [snippet]

## Recommendations (Medium Priority)
...

## Quick Wins (Easy fixes)
...
```

---

## Testing Strategy

### Unit Tests Required
- URL validation logic
- WordPress detection (various HTML structures)
- API response parsing (with mock data)
- Recommendation prioritization algorithm
- Report generation

### Integration Tests Required
- Full workflow with real PSI API (rate limited)
- Multiple WordPress configurations
- Error handling paths
- File write operations

### Manual Testing Checklist
- [ ] Run against 5+ different WordPress sites
- [ ] Test with invalid URLs
- [ ] Test with non-WordPress sites
- [ ] Test with very slow sites (>30s load)
- [ ] Test with sites that have no CrUX data
- [ ] Test API rate limiting behavior
- [ ] Verify all recommendations are actionable
- [ ] Check report readability and formatting

---

## Success Criteria (v1)

### Must Have
- ✅ Accepts URL, validates input
- ✅ Calls PSI API successfully with retries
- ✅ Detects if site is WordPress
- ✅ Parses LCP, INP, CLS scores
- ✅ Generates at least 5 relevant recommendations
- ✅ Outputs readable markdown report
- ✅ Completes in < 3 minutes for typical site
- ✅ Handles errors gracefully (no crashes)

### Should Have
- ⭐ WordPress plugin detection
- ⭐ Recommendation prioritization by impact
- ⭐ Implementation effort estimates
- ⭐ Code snippets for common fixes
- ⭐ Field data (CrUX) when available

### Nice to Have
- 💎 Mobile + Desktop analysis
- 💎 Historical comparison (if run multiple times)
- 💎 HTML report export option
- 💎 Configurable output verbosity

### Out of Scope (v1)
- ❌ Automated fix implementation
- ❌ Continuous monitoring
- ❌ Batch processing multiple sites
- ❌ GUI/Dashboard
- ❌ WordPress plugin to run from admin
- ❌ Before/after testing simulation

---

## Known Limitations (Document These)

1. **Cannot analyze login-protected pages** - PSI requires public access
2. **WordPress detection may fail** on heavily customized sites - provide warnings
3. **Plugin detection is best-effort** - based on frontend HTML only
4. **Recommendations are generic** - may require developer interpretation
5. **No guarantee of score improvement** - actual results depend on implementation
6. **Rate limited to PSI API limits** - cannot analyze hundreds of sites quickly
7. **Cannot test changes** in v1 - must implement and re-test manually
8. **No ongoing monitoring** - single point-in-time analysis only

---

## Future Enhancements (Post v1)

### Phase 2: Testing Module
- Simulate common optimizations virtually
- Before/after comparison without touching live site
- Requires Puppeteer integration

### Phase 3: Batch Processing
- Analyze multiple URLs from CSV
- Compare across sites
- Generate comparative reports

### Phase 4: Dashboard
- Next.js web interface
- Historical tracking
- Team collaboration features
- Scheduled automatic audits

### Phase 5: WordPress Plugin
- Run analysis from WP admin
- One-click implementations of some fixes
- Visual diff of changes

---

## Documentation Requirements

### README.md Must Include
- Quick start (install, run, example)
- Requirements (Python 3.9+)
- Installation instructions
- Usage examples
- Troubleshooting common errors
- Limitations and known issues
- Contributing guidelines

### Code Documentation
- Docstrings for all functions
- Type hints where helpful
- Inline comments for complex logic
- Module-level descriptions

### User Documentation
- How to interpret scores
- What each recommendation means
- WordPress-specific advice
- When to hire a developer vs DIY

---

## Approval Checklist

Before starting development:
- [ ] Adversarial spec reviewed and approved
- [ ] Failure modes understood and mitigations planned
- [ ] Security concerns addressed
- [ ] Edge cases documented
- [ ] Success criteria agreed upon
- [ ] Timeline realistic (4-8 hours)
- [ ] No scope creep (stick to v1 features only)

**Once approved, this spec can be fed into adversarial-spec for PRD generation and validation.**