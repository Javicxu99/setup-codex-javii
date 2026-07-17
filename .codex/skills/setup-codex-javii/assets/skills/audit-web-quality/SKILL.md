---
name: audit-web-quality
description: Audit and improve web projects across accessibility, Core Web Vitals, performance, security hygiene, compatibility, and SEO. Use when Codex builds or reviews a website, frontend, landing page, web application, HTML/CSS/JavaScript UI, or is asked for Lighthouse, WCAG, performance, SEO, or web-quality improvements.
---

# Audit web quality

Work from evidence and make the smallest verified improvements that fit the project's stack.

## Procedure

1. Identify the affected pages, supported browsers, rendering model, deployment constraints, and existing quality tooling.
2. Establish a baseline with tools already present in the project. Prefer its tests, build, linter, Lighthouse, axe, browser traces, or framework diagnostics. Do not install or call external services without need.
3. Review in this order:
   - **Accessibility:** semantic structure, keyboard operation, visible focus, accessible names, form errors, contrast, reflow, motion, and WCAG 2.2 AA risks.
   - **Core Web Vitals:** LCP, INP, and CLS. Separate field data from lab estimates and identify the actual element or interaction causing the metric.
   - **Performance:** request waterfall, render blockers, image sizing and formats, fonts, JavaScript cost, caching, third-party code, and unnecessary client rendering.
   - **Security and compatibility:** HTTPS, mixed content, dependency findings, CSP and security headers where applicable, unsafe DOM sinks, deprecated APIs, and browser support.
   - **SEO:** crawlability, index directives, titles, descriptions, canonical URLs, headings, internal links, sitemap, structured data, and mobile behavior.
4. Rank findings by user impact, confidence, severity, and effort. Do not present a generic checklist as evidence of a defect.
5. Implement only requested or clearly in-scope fixes. Preserve the framework's conventions and avoid speculative rewrites.
6. Re-run the relevant measurements and report before/after evidence. Label anything not measured as an inference or pending verification.

## Guardrails

- Treat automated scores as signals, not proof. Manually verify keyboard, focus, semantics, and important user flows.
- Do not claim field Core Web Vitals from a local Lighthouse run.
- Do not weaken security, accessibility, or content semantics to improve a score.
- Do not add structured data that the visible page does not support.
- Keep third-party scripts, analytics, and new dependencies opt-in and justified.

## Result

Return a prioritized table or concise list containing: finding, evidence, affected surface, severity, proposed or applied fix, and validation result.

This workflow is a compact adaptation of the MIT-licensed ideas in [addyosmani/web-quality-skills](https://github.com/addyosmani/web-quality-skills), consolidated to avoid six overlapping default skills.
