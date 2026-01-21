# Technical Specification: Technical SEO Audit System

## Overview / Context

This document provides the technical architecture and implementation guidance for the Technical SEO Audit System, a CLI tool that automates technical SEO audits for websites. The system analyzes websites across four categories (Core Web Vitals & Performance, Crawlability & Indexability, On-Page SEO, Structured Data) and generates client-ready PDF reports.

**Based on**: Product Requirements Document v3.0 (2026-01-12)

**Primary Requirements**:
- Audit completion time < 10 minutes for typical sites (< 100 pages)
- Support macOS, Linux, Windows with bundled Chromium
- Generate single-page PDF reports with 0-100 health score
- CLI-first interface with JSON output option
- No persistent data storage beyond generated reports

**Success Criteria**:
- 95% audit completion rate on accessible websites
- < 5% false positive rate on critical issues
- < 2GB memory footprint during execution
- Cross-platform binary distribution via package managers

## Goals and Non-Goals

### Goals

**G-1**: Build a robust, standalone CLI tool requiring no external dependencies beyond OS libraries
**G-2**: Achieve consistent audit results across all supported platforms (macOS, Linux, Windows)
**G-3**: Minimize false positives through intelligent filtering and context-aware severity assignment
**G-4**: Support future extensibility (web UI, historical tracking) through loosely-coupled architecture
**G-5**: Provide clear observability through structured logging, correlation IDs, and optional telemetry

### Non-Goals

**NG-1**: Real-time monitoring or continuous audit scheduling (users script via cron/Task Scheduler)
**NG-2**: Persistent database for audit history (v1.0 generates reports only; pure in-memory execution)
**NG-3**: Multi-user authentication or access control (single-user CLI tool; file-system permissions provide minimal security)
**NG-4**: Distributed crawling across multiple machines (single-machine execution)
**NG-5**: Custom UI frameworks or web rendering (PDF generation only in v1.0)

**Security Note on NG-3**: While authentication is a non-goal, the tool acknowledges potential unauthorized access in shared environments (e.g., multi-user servers). Mitigation: (1) Document that reports may contain sensitive site data; (2) Users should restrict file permissions on output directory; (3) Consider adding `--encrypt` flag in v1.1 for password-protected PDFs.

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLI Interface                         │
│  (Argument Parsing, Validation, Progress Display)           │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ (correlationId: UUID)
                         │
┌────────────────────────▼────────────────────────────────────┐
│                    Orchestrator                              │
│  (Audit Lifecycle, Error Handling, Timeout Management)      │
└─┬───────┬────────┬───────────┬──────────┬──────────┬───────┘
  │       │        │           │          │          │
  ▼       ▼        ▼           ▼          ▼          ▼
┌───┐   ┌───┐   ┌─────┐    ┌─────┐   ┌──────┐   ┌──────┐
│ C │   │ P │   │ I&C │    │ O-P │   │ S&S  │   │ FPF  │
│ r │   │ e │   │     │    │     │   │      │   │      │
│ a │   │ r │   │     │    │     │   │      │   │      │
│ w │   │ f │   │     │    │     │   │      │   │      │
│ l │   │ o │   │     │    │     │   │      │   │      │
│ e │   │ r │   │     │    │     │   │      │   │      │
│ r │   │ m │   │     │    │     │   │      │   │      │
└─┬─┘   └─┬─┘   └──┬──┘    └──┬──┘   └───┬──┘   └───┬──┘
  │       │        │          │          │          │
  │       └────────┴──────────┴──────────┴──────────┘
  │                         │
  ▼                         ▼
┌─────────────┐      ┌──────────────────┐
│  Headless   │      │  Analysis Engine │
│  Browser    │      │  (Severity,      │
│  (Chromium) │      │   Prioritization)│
└─────────────┘      └─────────┬────────┘
                               │
                     ┌─────────▼─────────┐
                     │  Report Generator │
                     │  (PDF/JSON)       │
                     └───────────────────┘

Legend:
- Crawler: Web crawling and page discovery
- Perf: Performance & Core Web Vitals analysis
- I&C: Indexability & Crawlability checks
- O-P: On-Page SEO analysis
- S&S: Structured Data & Schema validation
- FPF: False Positive Filter

Storage: Pure in-memory (Map/Set for deduplication, arrays for page list)
```

### Component Interaction Flow

1. **CLI** validates input, generates correlation ID (UUID v4), initializes Orchestrator with config
2. **Orchestrator** instantiates Crawler, passes URL, config, and correlation ID
3. **Crawler** discovers pages (up to depth/limit), stores in memory (Map<URL, PageInfo>), returns page list
4. **Orchestrator** distributes pages to analysis modules via `Promise.all([perf.analyze(), indexability.analyze(), ...])`
5. **Analysis modules** return findings with metadata (affected pages, severity hints)
6. **False Positive Filter** reviews findings, applies exclusion rules
7. **Analysis Engine** assigns final severity, prioritizes top 15-20 issues
8. **Report Generator** renders PDF/JSON from structured findings (HTML escaped for XSS prevention)
9. **CLI** writes report to disk, displays summary, exits with code 0/1/2

**Correlation ID Flow**: UUID generated at CLI → passed to all components → included in every log entry as `correlationId` field → enables request tracing across entire audit lifecycle.

### Technology Stack

**Language**: **Node.js 18+ with TypeScript 5.0+**

**Rationale**:
- Playwright native integration (better than Python bindings)
- Superior cross-platform binary packaging (pkg, nexe)
- Strong async/await performance for I/O-heavy workload
- Mature PDF generation ecosystem (Puppeteer PDF)
- **Python is NOT an option for v1.0 to ensure team alignment and avoid tech stack fragmentation**

**Key Dependencies**:
- **Playwright 1.40+** (headless browser, Chromium bundling, page automation)
- **Lighthouse 11+** (Core Web Vitals measurement, runs via Playwright)
- **Cheerio 1.0+** (HTML parsing for static analysis)
- **Puppeteer 21+** (PDF generation from HTML)
- **Commander.js 11+** (CLI argument parsing)
- **Winston 3.11+** (structured JSON logging)
- **Ajv 8.12+** (JSON Schema validation for structured data)
- **robots-parser 3.0+** (robots.txt parsing)

**Build & Packaging**:
- **@vercel/ncc** (TypeScript compilation + dependency bundling)
- **pkg 5.8+** (Node.js binary compilation with bundled Chromium)
- **Docker** (alternative containerized distribution)

**TypeScript Configuration** (`tsconfig.json`):
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

## Error Handling

### Error Code Enumeration

All errors follow standardized code ranges:

```typescript
enum ErrorCode {
  // 1000-1999: User/Input Errors
  INVALID_URL = 1001,
  INVALID_ARGUMENTS = 1002,
  OUTPUT_PATH_NOT_WRITABLE = 1003,
  INVALID_CONFIG_FILE = 1004,

  // 2000-2999: Network Errors
  DNS_RESOLUTION_FAILED = 2001,
  CONNECTION_TIMEOUT = 2002,
  SSL_ERROR = 2003,
  HTTP_ERROR = 2004,
  RATE_LIMITED = 2005,

  // 3000-3999: Crawl Errors (partial success possible)
  ROBOTS_TXT_BLOCKS_CRAWL = 3001,
  MOST_PAGES_FAILED = 3002,
  SITEMAP_INACCESSIBLE = 3003,

  // 4000-4999: System Errors
  OUT_OF_MEMORY = 4001,
  DISK_FULL = 4002,
  CHROMIUM_LAUNCH_FAILED = 4003,
  TIMEOUT_EXCEEDED = 4004,

  // 5000-5999: Analysis Errors
  LIGHTHOUSE_FAILED = 5001,
  PDF_GENERATION_FAILED = 5002,
  INVALID_STRUCTURED_DATA = 5003,
}

interface ErrorResponse {
  code: ErrorCode;
  message: string;
  suggestion?: string;
  recoverable: boolean;
  retryAfter?: number; // milliseconds
  correlationId: string;
}
```

### Retry Strategy

```typescript
interface RetryConfig {
  maxAttempts: 3;
  baseDelay: 1000;  // milliseconds
  maxDelay: 8000;   // cap exponential backoff
  backoffMultiplier: 2;
}

async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  config: RetryConfig,
  correlationId: string
): Promise<T> {
  let lastError: Error;

  for (let attempt = 1; attempt <= config.maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;

      if (attempt < config.maxAttempts && isRetryable(error)) {
        const delay = Math.min(
          config.baseDelay * Math.pow(config.backoffMultiplier, attempt - 1),
          config.maxDelay
        );

        logger.warn('Retrying after error', {
          correlationId,
          attempt,
          error: error.message,
          retryAfter: delay,
        });

        await sleep(delay);
      }
    }
  }

  throw lastError;
}

function isRetryable(error: Error): boolean {
  return error instanceof NetworkError ||
         error instanceof TimeoutError ||
         error.code === ErrorCode.RATE_LIMITED;
}
```

## Data Models

### Structured Finding Types

```typescript
// Base finding interface
interface BaseFinding {
  id: string;  // UUID
  type: string;
  category: 'performance' | 'crawlability' | 'onpage' | 'structured-data';
  severity: 'critical' | 'high' | 'medium' | 'low';
  affectedPages: string[];
  affectedPercent: number;
  title: string;
  description: string;
  remediation: string;
  correlationId: string;
}

// Performance-specific findings
interface PerformanceFinding extends BaseFinding {
  category: 'performance';
  type: 'slow-lcp' | 'high-cls' | 'slow-fid' | 'slow-inp' | 'slow-ttfb' |
        'oversized-image' | 'oversized-script' | 'render-blocking' |
        'missing-lazy-loading' | 'suboptimal-image-format';
  details: {
    metrics?: {
      lcp?: number;
      cls?: number;
      fid?: number;
      inp?: number;
      ttfb?: number;
    };
    resources?: {
      url: string;
      size: number;
      type: 'image' | 'script' | 'stylesheet';
    }[];
  };
}

// Crawlability-specific findings
interface CrawlabilityFinding extends BaseFinding {
  category: 'crawlability';
  type: 'no-sitemap' | 'noindex-directive' | 'noindex-http-header' |
        'canonical-conflict' | 'redirect-chain' | 'redirect-loop' |
        'broken-link' | 'orphaned-page' | 'robots-txt-blocks';
  details: {
    redirectChain?: string[];
    canonicalUrl?: string;
    conflictingPages?: string[];
    brokenLinks?: { page: string; target: string; statusCode: number }[];
  };
}

// On-page-specific findings
interface OnPageFinding extends BaseFinding {
  category: 'onpage';
  type: 'missing-title' | 'duplicate-title' | 'long-title' | 'short-title' |
        'missing-meta-description' | 'duplicate-meta-description' |
        'long-meta-description' | 'heading-hierarchy' | 'multiple-h1' |
        'missing-h1' | 'missing-alt-text' | 'mixed-content' |
        'thin-content' | 'missing-https';
  details: {
    title?: string;
    titleLength?: number;
    metaDescription?: string;
    metaDescriptionLength?: number;
    headingIssues?: { page: string; issue: string }[];
    contentWordCount?: number;
    mixedContentResources?: string[];
  };
}

// Structured data-specific findings
interface StructuredDataFinding extends BaseFinding {
  category: 'structured-data';
  type: 'missing-schema' | 'invalid-schema-syntax' | 'schema-error' |
        'missing-required-property' | 'invalid-property-value';
  details: {
    schemaType?: string;
    errors?: { property: string; message: string }[];
    expectedSchemaTypes?: string[];  // e.g., ['Product'] for product pages
  };
}

// Union type for all findings
type Finding = PerformanceFinding | CrawlabilityFinding | OnPageFinding | StructuredDataFinding;
```

### Page Information

```typescript
interface PageInfo {
  url: string;
  statusCode: number;
  redirectChain: string[];
  depth: number;
  html: string;  // Cleared after analysis to reduce memory
  headers: Record<string, string>;
  resources: Resource[];
  errors: CrawlError[];
  metadata: {
    title?: string;
    metaDescription?: string;
    canonical?: string;
    contentLength: number;
    robotsNoindex: boolean;  // From meta tag
    robotsNoindexHeader: boolean;  // From X-Robots-Tag HTTP header
  };
}

interface Resource {
  url: string;
  type: 'image' | 'script' | 'stylesheet' | 'font' | 'other';
  size: number;
  cached: boolean;
  blocking: boolean;
}

interface CrawlError {
  url: string;
  type: 'dns' | 'timeout' | 'ssl' | 'http' | 'parse';
  message: string;
  code?: ErrorCode;
}
```

### Configuration

**Default Config** (`.seoauditrc` example):
```json
{
  "crawl": {
    "maxDepth": 3,
    "maxPages": 100,
    "requestDelay": 500,
    "timeout": 900,
    "userAgent": "TechnicalSEOAuditBot/1.0 (+https://github.com/yourorg/seo-audit)",
    "respectRobots": true
  },
  "performance": {
    "measurements": 3,
    "outlierThreshold": 2.0
  },
  "analysis": {
    "maxFindings": 20,
    "applyFalsePositiveFilter": true
  },
  "report": {
    "format": "pdf",
    "outputPath": "./audit-report.pdf"
  },
  "integrations": {
    "pageSpeedInsights": {
      "enabled": false,
      "apiKey": ""
    }
  },
  "telemetry": {
    "enabled": false
  }
}
```

## Component Design

### 1. CLI Interface (`src/cli/index.ts`)

**API Contract**:
- **Input**: Command-line arguments (process.argv)
- **Output**: Exit code (0 = success, 1 = error, 2 = partial success)
- **Side Effects**: Writes PDF/JSON to disk, logs to stdout/stderr

```typescript
interface CLIConfig {
  url: string;
  depth: number;          // 1-5
  pages: number;          // 1-500
  output: string;         // file path
  format: 'pdf' | 'json';
  timeout: number;        // seconds
  verbose: boolean;
  ignoreRobots: boolean;
  noHeadless: boolean;
  config?: string;        // path to .seoauditrc
}

class CLI {
  async run(argv: string[]): Promise<number> {
    const correlationId = uuidv4();
    const config = this.parseCLI(argv);

    try {
      const result = await orchestrator.runAudit(config, correlationId);
      this.displaySummary(result);
      return 0;
    } catch (error) {
      this.handleError(error, correlationId);
      return error.recoverable ? 2 : 1;
    }
  }

  private parseCLI(argv: string[]): CLIConfig {
    const program = new Command();
    program
      .argument('<url>', 'Website URL to audit')
      .option('--depth <number>', 'Crawl depth', '3')
      .option('--pages <number>', 'Max pages', '100')
      .option('--output <path>', 'Output path', './audit-report.pdf')
      .option('--format <format>', 'Output format (pdf|json)', 'pdf')
      .option('--timeout <seconds>', 'Timeout', '900')
      .option('-v, --verbose', 'Verbose logging')
      .option('--ignore-robots', 'Ignore robots.txt')
      .option('--no-headless', 'Disable headless mode')
      .option('--config <path>', 'Config file path');

    program.parse(argv);
    // Validate and return config...
  }
}
```

### 2. Orchestrator (`src/core/orchestrator.ts`)

**API Contract**:
```typescript
// Request
interface AuditConfig {
  url: string;
  depth: number;
  maxPages: number;
  timeout: number;
  ignoreRobots: boolean;
  headless: boolean;
}

// Response
interface AuditResult {
  url: string;
  timestamp: Date;
  duration: number;  // seconds
  pages: PageInfo[];
  findings: Finding[];
  healthScore: number;
  metadata: {
    totalPages: number;
    crawledPages: number;
    errors: number;
    version: string;
    correlationId: string;
  };
}

// Errors
class OrchestrationError extends Error {
  constructor(
    public code: ErrorCode,
    message: string,
    public correlationId: string
  ) {
    super(message);
  }
}
```

**Concurrency Model**:
```typescript
class Orchestrator {
  async runAudit(config: AuditConfig, correlationId: string): Promise<AuditResult> {
    const startTime = Date.now();

    // Phase 1: Crawl (Sequential with rate limiting)
    const pages = await this.crawler.crawl(config, correlationId);

    // Phase 2: Analysis (Parallel via Promise.all)
    const [perfFindings, crawlFindings, onPageFindings, schemaFindings] =
      await Promise.all([
        this.perfAnalyzer.analyze(pages, correlationId),
        this.crawlAnalyzer.analyze(pages, correlationId),
        this.onPageAnalyzer.analyze(pages, correlationId),
        this.schemaAnalyzer.analyze(pages, correlationId),
      ]);

    const allFindings = [
      ...perfFindings,
      ...crawlFindings,
      ...onPageFindings,
      ...schemaFindings,
    ];

    // Phase 3: False Positive Filter
    const filteredFindings = this.fpFilter.filter(allFindings, {
      pages,
      correlationId,
    });

    // Phase 4: Analysis Engine (severity assignment, prioritization)
    const analyzed = this.analysisEngine.analyze(filteredFindings, pages.length);

    // Phase 5: Report Generation
    await this.reportGen.generate({
      url: config.url,
      timestamp: new Date(),
      duration: (Date.now() - startTime) / 1000,
      pages,
      findings: analyzed.prioritizedFindings,
      healthScore: analyzed.healthScore,
      metadata: {
        totalPages: pages.length,
        crawledPages: pages.filter(p => p.statusCode === 200).length,
        errors: pages.filter(p => p.errors.length > 0).length,
        version: VERSION,
        correlationId,
      },
    }, config);

    return result;
  }
}
```

### 3. Crawler (`src/crawler/crawler.ts`)

**X-Robots-Tag HTTP Header Support**:
```typescript
async function fetchPage(url: string, correlationId: string): Promise<PageInfo> {
  const response = await retryWithBackoff(
    () => axios.get(url, {
      headers: { 'User-Agent': config.userAgent },
      timeout: 30000,
      maxRedirects: 5,
    }),
    RETRY_CONFIG,
    correlationId
  );

  // Check X-Robots-Tag HTTP header
  const xRobotsTag = response.headers['x-robots-tag'] || '';
  const robotsNoindexHeader = xRobotsTag.toLowerCase().includes('noindex');

  // Also check meta robots tag in HTML
  const $ = cheerio.load(response.data);
  const metaRobots = $('meta[name="robots"]').attr('content') || '';
  const robotsNoindex = metaRobots.toLowerCase().includes('noindex');

  return {
    url: response.request.res.responseUrl,  // Final URL after redirects
    statusCode: response.status,
    redirectChain: extractRedirectChain(response),
    depth: 0,  // Set by crawler
    html: response.data,
    headers: response.headers,
    resources: [],  // Populated later
    errors: [],
    metadata: {
      title: $('title').text(),
      metaDescription: $('meta[name="description"]').attr('content'),
      canonical: $('link[rel="canonical"]').attr('href'),
      contentLength: response.data.length,
      robotsNoindex,
      robotsNoindexHeader,
    },
  };
}
```

### 4. Performance Analyzer (`src/analyzers/performance.ts`)

**Lighthouse Integration via Playwright**:
```typescript
import { chromium } from 'playwright';
import lighthouse from 'lighthouse';

async function measureCoreWebVitals(
  url: string,
  correlationId: string
): Promise<PerformanceMetrics> {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  const measurements: number[][] = [];

  // Run 3 measurements
  for (let i = 0; i < 3; i++) {
    await page.goto(url, { waitUntil: 'networkidle' });

    // Use Lighthouse Node module directly
    const { lhr } = await lighthouse(url, {
      port: new URL(browser.wsEndpoint()).port,
      output: 'json',
      onlyCategories: ['performance'],
      logLevel: 'error',
    });

    measurements.push([
      lhr.audits['largest-contentful-paint'].numericValue,
      lhr.audits['cumulative-layout-shift'].numericValue,
      lhr.audits['max-potential-fid'].numericValue,
      lhr.audits['server-response-time'].numericValue,
    ]);
  }

  await browser.close();

  // Calculate median with outlier detection
  const [lcpValues, clsValues, fidValues, ttfbValues] = transpose(measurements);

  return {
    lcp: medianWithOutlierRemoval(lcpValues, 2.0),
    cls: medianWithOutlierRemoval(clsValues, 2.0),
    fid: medianWithOutlierRemoval(fidValues, 2.0),
    inp: 0,  // INP requires real user interaction
    ttfb: medianWithOutlierRemoval(ttfbValues, 2.0),
    measurements: {
      raw: measurements,
      median: calculateMedian(measurements),
      outliers: detectOutliers(measurements, 2.0),
    },
  };
}

function medianWithOutlierRemoval(values: number[], stdDevThreshold: number): number {
  const mean = values.reduce((a, b) => a + b) / values.length;
  const stdDev = Math.sqrt(
    values.map(v => Math.pow(v - mean, 2)).reduce((a, b) => a + b) / values.length
  );

  const filtered = values.filter(v =>
    Math.abs(v - mean) <= stdDevThreshold * stdDev
  );

  return filtered.length > 0
    ? filtered.sort((a, b) => a - b)[Math.floor(filtered.length / 2)]
    : mean;  // Fallback to mean if all outliers
}
```

### 5. Report Generator (`src/report/generator.ts`)

**XSS Prevention in PDF Generation**:
```typescript
import puppeteer from 'puppeteer';
import DOMPurify from 'isomorphic-dompurify';

async function generatePDF(data: ReportData, outputPath: string): Promise<void> {
  // Sanitize all user-provided content
  const sanitizedData = {
    ...data,
    url: DOMPurify.sanitize(data.url),
    findings: data.findings.map(f => ({
      ...f,
      title: DOMPurify.sanitize(f.title),
      description: DOMPurify.sanitize(f.description),
      remediation: DOMPurify.sanitize(f.remediation),
      affectedPages: f.affectedPages.map(p => DOMPurify.sanitize(p)),
    })),
  };

  const html = renderHTML(sanitizedData);

  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();

  await page.setContent(html, { waitUntil: 'networkidle0' });

  await page.pdf({
    path: outputPath,
    format: 'Letter',
    printBackground: true,
    margin: { top: '0.5in', right: '0.5in', bottom: '0.5in', left: '0.5in' },
  });

  await browser.close();
}

function renderHTML(data: ReportData): string {
  const grade = getGrade(data.healthScore);
  const gradeColor = getGradeColor(grade);

  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
      font-size: 11px;
      line-height: 1.4;
      color: #333;
      padding: 20px;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      padding-bottom: 15px;
      border-bottom: 2px solid #e0e0e0;
    }
    .header h1 {
      font-size: 18px;
      font-weight: 600;
      color: #1a1a1a;
    }
    .health-score {
      display: inline-block;
      padding: 8px 16px;
      border-radius: 6px;
      font-size: 16px;
      font-weight: 700;
      color: white;
      background-color: ${gradeColor};
    }
    .metadata {
      font-size: 10px;
      color: #666;
      margin-top: 8px;
    }
    .findings {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-top: 15px;
    }
    .finding {
      border: 1px solid #e0e0e0;
      border-left: 4px solid;
      padding: 10px;
      border-radius: 4px;
      background: #fafafa;
    }
    .finding.critical { border-left-color: #dc2626; }
    .finding.high { border-left-color: #ea580c; }
    .finding.medium { border-left-color: #eab308; }
    .finding.low { border-left-color: #9ca3af; }
    .finding-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
    }
    .finding-title {
      font-weight: 600;
      font-size: 11px;
      color: #1a1a1a;
    }
    .severity-badge {
      padding: 2px 8px;
      border-radius: 3px;
      font-size: 9px;
      font-weight: 600;
      text-transform: uppercase;
      color: white;
    }
    .severity-badge.critical { background: #dc2626; }
    .severity-badge.high { background: #ea580c; }
    .severity-badge.medium { background: #eab308; }
    .severity-badge.low { background: #9ca3af; }
    .finding-description {
      font-size: 10px;
      color: #4b5563;
      margin-bottom: 6px;
    }
    .finding-affected {
      font-size: 9px;
      color: #6b7280;
      margin-bottom: 6px;
    }
    .finding-remediation {
      font-size: 10px;
      color: #059669;
      font-weight: 500;
      background: #d1fae5;
      padding: 4px 6px;
      border-radius: 3px;
    }
    .footer {
      margin-top: 20px;
      padding-top: 10px;
      border-top: 1px solid #e0e0e0;
      text-align: center;
      font-size: 9px;
      color: #9ca3af;
    }
  </style>
</head>
<body>
  <div class="header">
    <div>
      <h1>Technical SEO Audit Report</h1>
      <div class="metadata">
        <div>URL: ${data.url}</div>
        <div>Date: ${data.timestamp.toLocaleDateString()} at ${data.timestamp.toLocaleTimeString()}</div>
        <div>Pages Audited: ${data.metadata.crawledPages} / ${data.metadata.totalPages}</div>
      </div>
    </div>
    <div class="health-score">
      ${data.healthScore} / 100<br>${grade}
    </div>
  </div>

  <div class="findings">
    ${renderFindings(data.findings)}
  </div>

  <div class="footer">
    Generated by Technical SEO Audit Tool v${data.metadata.version} | Correlation ID: ${data.metadata.correlationId}
  </div>
</body>
</html>
  `;
}

function renderFindings(findings: Finding[]): string {
  return findings.map(f => `
    <div class="finding ${f.severity}">
      <div class="finding-header">
        <div class="finding-title">${f.title}</div>
        <div class="severity-badge ${f.severity}">${f.severity}</div>
      </div>
      <div class="finding-description">${f.description}</div>
      <div class="finding-affected">
        Affects ${f.affectedPages.length} page${f.affectedPages.length !== 1 ? 's' : ''} (${f.affectedPercent.toFixed(1)}%)
      </div>
      <div class="finding-remediation">
        <strong>Fix:</strong> ${f.remediation}
      </div>
    </div>
  `).join('');
}

function getGrade(score: number): string {
  if (score >= 90) return 'Excellent';
  if (score >= 70) return 'Good';
  if (score >= 50) return 'Fair';
  return 'Poor';
}

function getGradeColor(grade: string): string {
  const colors = {
    'Excellent': '#10b981',
    'Good': '#84cc16',
    'Fair': '#f59e0b',
    'Poor': '#ef4444',
  };
  return colors[grade] || '#6b7280';
}
```

## Testing Strategy

### Unit Tests

**Coverage Target**: > 80% for core business logic (analysis modules, severity assignment, health score calculation, false positive filtering)

**Infrastructure code excluded from coverage**: CLI parsing, logging setup, binary packaging scripts

```typescript
// Example: Analysis Engine Tests
describe('AnalysisEngine', () => {
  let engine: AnalysisEngine;

  beforeEach(() => {
    engine = new AnalysisEngine();
  });

  describe('assignSeverity', () => {
    it('assigns Critical when > 90% pages have noindex', () => {
      const finding: Finding = {
        type: 'noindex-directive',
        affectedPages: Array(91).fill('http://example.com/page'),
        // ... other required fields
      };

      const severity = engine.assignSeverity(finding, 100);
      expect(severity).toBe('critical');
    });

    it('assigns High when 50-90% pages have noindex', () => {
      const finding: Finding = {
        type: 'noindex-directive',
        affectedPages: Array(70).fill('http://example.com/page'),
      };

      const severity = engine.assignSeverity(finding, 100);
      expect(severity).toBe('high');
    });
  });

  describe('calculateHealthScore', () => {
    it('returns 100 for zero findings', () => {
      expect(engine.calculateHealthScore([])).toBe(100);
    });

    it('returns 0 (clamped) for 7+ critical issues', () => {
      const findings = Array(7).fill({ severity: 'critical' });
      expect(engine.calculateHealthScore(findings)).toBe(100 - 7 * 15);  // -5, clamped to 0
    });

    it('clamps negative scores to 0', () => {
      const findings = Array(10).fill({ severity: 'critical' });
      expect(engine.calculateHealthScore(findings)).toBe(0);  // Would be -50, clamped
    });
  });
});
```

### Integration Tests

**Test Site Fixtures** (`tests/fixtures/`):
```
tests/fixtures/
├── perfect-seo/
│   └── index.html          # No issues, score = 100
├── broken-site/
│   ├── index.html          # Multiple critical issues
│   ├── noindex.html
│   └── broken-links.html
├── spa-site/
│   └── index.html          # React SPA requiring JS rendering
└── schema-validation/
    ├── valid-product.html
    └── invalid-product.html
```

**Automated Test Execution**:
```typescript
describe('End-to-End Audit', () => {
  it('generates perfect score for perfect-seo fixture', async () => {
    const server = await startTestServer('tests/fixtures/perfect-seo');
    const result = await runCLI([server.url, '--format', 'json']);

    expect(result.healthScore).toBe(100);
    expect(result.findings).toHaveLength(0);

    await server.close();
  });

  it('identifies critical issues in broken-site fixture', async () => {
    const server = await startTestServer('tests/fixtures/broken-site');
    const result = await runCLI([server.url, '--format', 'json']);

    expect(result.healthScore).toBeLessThan(50);
    expect(result.findings.some(f => f.severity === 'critical')).toBe(true);
    expect(result.findings.some(f => f.type === 'noindex-directive')).toBe(true);

    await server.close();
  });

  it('handles SPA rendering correctly', async () => {
    const server = await startTestServer('tests/fixtures/spa-site');
    const result = await runCLI([server.url, '--format', 'json']);

    // SPA should have JS-rendered content detected
    expect(result.pages[0].metadata.title).toBeTruthy();
    await server.close();
  });
});
```

### Performance Benchmarks

**Reference Hardware**: 2-core CPU, 8GB RAM, SSD

```typescript
describe('Performance Benchmarks', () => {
  it('completes 100-page site in < 10 minutes', async () => {
    const server = await startTestServer('tests/fixtures/large-site-100');
    const startTime = Date.now();

    await runCLI([server.url]);

    const duration = (Date.now() - startTime) / 1000;
    expect(duration).toBeLessThan(600);  // 10 minutes

    await server.close();
  });

  it('maintains < 2GB memory footprint', async () => {
    const server = await startTestServer('tests/fixtures/large-site-100');
    const { memoryUsage } = process;

    const before = memoryUsage().heapUsed;
    await runCLI([server.url]);
    const after = memoryUsage().heapUsed;

    const peakMemory = Math.max(before, after);
    expect(peakMemory).toBeLessThan(2 * 1024 * 1024 * 1024);  // 2GB

    await server.close();
  });

  it('handles 2 concurrent audits with < 20% degradation', async () => {
    const server1 = await startTestServer('tests/fixtures/medium-site-50');
    const server2 = await startTestServer('tests/fixtures/medium-site-50');

    // Measure single audit
    const singleStart = Date.now();
    await runCLI([server1.url]);
    const singleDuration = Date.now() - singleStart;

    // Measure concurrent audits
    const concurrentStart = Date.now();
    await Promise.all([
      runCLI([server1.url]),
      runCLI([server2.url]),
    ]);
    const concurrentDuration = (Date.now() - concurrentStart) / 2;  // Per audit

    const degradation = (concurrentDuration - singleDuration) / singleDuration;
    expect(degradation).toBeLessThan(0.2);  // < 20%

    await server1.close();
    await server2.close();
  });
});
```

### CI/CD Pipeline (GitHub Actions)

**`.github/workflows/test.yml`**:
```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node: [18, 20]

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node }}

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run unit tests
        run: npm run test:unit

      - name: Run integration tests
        run: npm run test:integration

      - name: Run performance benchmarks
        run: npm run test:perf
        if: matrix.os == 'ubuntu-latest' && matrix.node == '18'

      - name: Build binary
        run: npm run build

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        if: matrix.os == 'ubuntu-latest' && matrix.node == '18'
```

## Deployment & Distribution

### Binary Size Breakdown

**Target**: < 400MB total

- Chromium binary: ~280MB (bundled with Playwright)
- Node.js runtime: ~50MB (pkg-embedded)
- Application code + dependencies: ~40MB
- Assets (PDF templates, schemas): ~5MB
- **Total**: ~375MB ✓

### Package Distribution

**Homebrew Formula** (`Formula/seo-audit.rb`):
```ruby
class SeoAudit < Formula
  desc "Technical SEO audit tool"
  homepage "https://github.com/yourorg/seo-audit"
  url "https://github.com/yourorg/seo-audit/releases/download/v1.0.0/seo-audit-macos-x64.tar.gz"
  sha256 "..."
  version "1.0.0"

  def install
    bin.install "seo-audit"
  end

  test do
    system "#{bin}/seo-audit", "--version"
  end
end
```

**Docker Distribution**:
```dockerfile
FROM node:18-alpine

# Install Chromium dependencies
RUN apk add --no-cache \
  chromium \
  nss \
  freetype \
  harfbuzz \
  ttf-freefont

# Set Chromium path for Playwright
ENV PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 \
  PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium-browser

WORKDIR /app
COPY package*.json ./
RUN npm ci --production

COPY dist ./dist

ENTRYPOINT ["node", "dist/cli.js"]
```

### Configuration Management Across Environments

**Priority Order** (highest to lowest):
1. CLI flags (e.g., `--depth 5`)
2. Environment variables (e.g., `SEO_AUDIT_DEPTH=5`)
3. Config file in current directory (`./.seoauditrc`)
4. Config file in home directory (`~/.seoauditrc`)
5. Default values (hardcoded in code)

```typescript
function loadConfig(): Config {
  const defaults = DEFAULT_CONFIG;
  const homeConfig = loadConfigFile(path.join(os.homedir(), '.seoauditrc'));
  const localConfig = loadConfigFile('./.seoauditrc');
  const envConfig = loadFromEnv();
  const cliConfig = parseCommandLineArgs();

  return merge(defaults, homeConfig, localConfig, envConfig, cliConfig);
}

function loadFromEnv(): Partial<Config> {
  return {
    crawl: {
      maxDepth: process.env.SEO_AUDIT_DEPTH ? parseInt(process.env.SEO_AUDIT_DEPTH) : undefined,
      maxPages: process.env.SEO_AUDIT_PAGES ? parseInt(process.env.SEO_AUDIT_PAGES) : undefined,
    },
    telemetry: {
      enabled: process.env.SEO_AUDIT_TELEMETRY === 'true',
    },
  };
}
```

## Observability

### Structured Logging with Correlation IDs

```typescript
import winston from 'winston';

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'audit.log', level: 'debug' }),
  ],
});

// Usage throughout codebase
logger.info('Audit started', {
  correlationId: 'uuid-here',
  url: 'https://example.com',
  config: { depth: 3, pages: 100 },
});

logger.warn('Page failed to load', {
  correlationId: 'uuid-here',
  url: 'https://example.com/broken',
  error: 'DNS resolution failed',
  code: ErrorCode.DNS_RESOLUTION_FAILED,
});

logger.info('Audit completed', {
  correlationId: 'uuid-here',
  duration: 487,
  findings: 12,
  healthScore: 78,
});
```

**Log Output Example**:
```json
{
  "timestamp": "2026-01-12T15:30:45.123Z",
  "level": "info",
  "message": "Audit completed",
  "correlationId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "duration": 487,
  "findings": 12,
  "healthScore": 78
}
```

**Correlation ID Tracing**: Use `grep` or log aggregation tools (Splunk, ELK) to trace single audit:
```bash
cat audit.log | grep "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
```

## Security Considerations

### Input Validation

```typescript
function validateURL(input: string): URL {
  try {
    const url = new URL(input);

    // Only allow HTTP(S)
    if (!['http:', 'https:'].includes(url.protocol)) {
      throw new ValidationError(
        ErrorCode.INVALID_URL,
        `Invalid protocol: ${url.protocol}. Only http and https are supported.`
      );
    }

    // Reject private IPs (unless --allow-local flag)
    if (isPrivateIP(url.hostname) && !config.allowLocal) {
      throw new ValidationError(
        ErrorCode.INVALID_URL,
        `Private IP addresses are not allowed: ${url.hostname}. Use --allow-local to override.`
      );
    }

    // Reject other dangerous protocols
    const dangerous = ['file:', 'javascript:', 'data:', 'vbscript:'];
    if (dangerous.some(p => input.toLowerCase().startsWith(p))) {
      throw new ValidationError(
        ErrorCode.INVALID_URL,
        `Dangerous protocol detected: ${input}`
      );
    }

    return url;
  } catch (error) {
    throw new ValidationError(
      ErrorCode.INVALID_URL,
      `Invalid URL: ${error.message}`
    );
  }
}

function isPrivateIP(hostname: string): boolean {
  const ip = require('ip');
  try {
    return ip.isPrivate(hostname) || hostname === 'localhost';
  } catch {
    return false;  // If not an IP, allow (will be resolved via DNS)
  }
}
```

### Output Path Validation

```typescript
function validateOutputPath(input: string): string {
  const resolved = path.resolve(input);

  // Reject path traversal
  if (resolved.includes('..')) {
    throw new ValidationError(
      ErrorCode.OUTPUT_PATH_NOT_WRITABLE,
      'Path traversal detected in output path'
    );
  }

  // Check write permissions
  try {
    const dir = path.dirname(resolved);
    fs.accessSync(dir, fs.constants.W_OK);
    return resolved;
  } catch {
    throw new ValidationError(
      ErrorCode.OUTPUT_PATH_NOT_WRITABLE,
      `Output directory is not writable: ${path.dirname(resolved)}`
    );
  }
}
```

## Open Questions / Future Considerations

### V1.0 Open Questions

**Q1**: Should we support IPv6 URLs?
**A**: Yes, no additional work needed (Node.js handles natively)

**Q2**: How to handle internationalized domain names (IDN)?
**A**: Use Punycode encoding (Node.js `url` module handles automatically)

**Q3**: Should correlation IDs be user-provided or always generated?
**A**: Always generated (prevents ID collisions, ensures uniqueness)

### V1.1 Considerations

- Web-based report viewer (HTML/CSS/JS static page for JSON upload)
- Automated update notifications (check GitHub releases API)
- `--encrypt` flag for password-protected PDFs (using pdf-lib)
- User-defined false positive rules in config file

### V2.0+ Ideas

- Full web UI with audit history dashboard
- Batch audit support (CSV upload of URLs)
- Scheduled audits with cron-like syntax
- Historical trend visualization (requires database)
- REST API mode for programmatic access
- White-label PDF reports with custom branding

---

**Document Version**: 2.0
**Last Updated**: 2026-01-12
**Authors**: Engineering Team, with adversarial review by Gemini 2.0 Flash and Claude Sonnet 4.5
**Status**: Draft - Round 2 Review Pending
**Related Documents**: PRD v3.0
**Changelog**:
- v1.0: Initial draft
- v2.0: Incorporated Round 1 feedback (Gemini + Claude): Removed Python option (committed to Node.js/TypeScript), added structured Finding types, added comprehensive error code enumeration, added API contracts with error codes, added X-Robots-Tag HTTP header support, added correlation ID support throughout, clarified pure in-memory storage, specified Promises.all() concurrency model, added .seoauditrc config example, added PDF HTML template with XSS prevention, showed Lighthouse-via-Playwright integration, added test automation strategy, added deployment config management
