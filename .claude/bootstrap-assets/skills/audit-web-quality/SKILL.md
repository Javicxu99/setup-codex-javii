---
name: audit-web-quality
description: Audit and improve web projects across accessibility, Core Web Vitals, performance, security hygiene, compatibility, and SEO. Use when building or reviewing a website, frontend, landing page, web application, HTML/CSS/JavaScript UI, or when asked for Lighthouse, WCAG, performance, SEO, or web-quality improvements.
---

# Audit web quality

Work from evidence and make the smallest verified improvements that fit the project's stack.

1. Identify the affected pages, supported browsers, rendering model, deployment constraints, and existing quality tooling.
2. Establish a baseline with tools already present. Do not install or call external services without need.
3. Review accessibility and WCAG 2.2 AA risks; LCP, INP, and CLS; loading and runtime performance; web security and compatibility; then technical SEO.
4. Rank findings by user impact, confidence, severity, and effort. A generic checklist is not evidence of a defect.
5. Implement only requested or clearly in-scope fixes, preserving framework conventions.
6. Re-run relevant measurements and distinguish verified results, lab estimates, field data, and inferences.

Never weaken security, accessibility, or semantics to improve a score. Manually verify keyboard, focus, semantics, and important flows. Do not add unsupported structured data or unjustified third-party dependencies.

Return each finding with evidence, affected surface, severity, fix, and validation result.

Compact adaptation of the MIT-licensed [addyosmani/web-quality-skills](https://github.com/addyosmani/web-quality-skills).
