# Notion Candidate Audit

Audit date: 2026-07-15. Source: Notion database `Links Proyectos Encontrados` (`36de283a-e1ef-80a1-afbf-f21331e9af0e`).

## Coverage and method

- Queried the sole data source directly, without relying on the initial Notion view or semantic search ranking.
- Reviewed all 31 non-archived rows and all 31 associated Notion pages; the archived partition contained 0 rows.
- Found 30 external links: 27 GitHub repositories, NVIDIA Build, Sesame, and an Osiris deployment. One row was empty.
- The page bodies contain only the default Background/Analysis/Recommendations/Implementation headings. Decisions therefore rely on row properties and the linked resources.
- GitHub candidates were checked through the connected GitHub integration, including repository resolution and README content. No candidate source was copied wholesale.

Decision meanings: **integrate** = part of the base; **adapt partially** = a narrow idea or component is retained; **reference** = useful for a project-specific choice; **discard** = outside the universal bootstrap.

## Inventory

| # | Candidate | What it offers / reusable component | Compatibility, maintenance, and risk | Decision |
|---:|---|---|---|---|
| 1 | [LLM Scraper](https://github.com/mishushakov/llm-scraper) | Typed LLM-assisted extraction with Playwright. | Adds Node, browser, model-provider, and schema dependencies for a domain-specific workflow. | **Reference** for scraping projects; not a base dependency. |
| 2 | [Karpathy guidelines](https://github.com/multica-ai/andrej-karpathy-skills) | Assumption surfacing, simplicity, surgical diffs, and verifiable goals. | Already adapted locally with attribution; duplicating the upstream plugin would create two authorities. Low maintenance in its compact local form. | **Integrate** the existing adapted skill. |
| 3 | [Google MCP catalog](https://github.com/google/mcp) | Official catalog and deployment guidance for Google MCP servers. | MCP needs are project-specific and may require cloud credentials or services. Enabling all would expand permissions and maintenance. | **Reference** when a target project uses Google services. |
| 4 | [CodeGraph](https://github.com/colbymchenry/codegraph) | Local semantic code graph and agent integrations. | Duplicates the selected graph engine. Maintaining two graph stores, commands, docs, and MCP registrations would add friction. | **Discard** in favor of `codebase-memory-mcp`; remove stale references. |
| 5 | [Microsoft Webwright](https://github.com/microsoft/webwright) | Re-runnable browser automation scripts for coding agents. | Useful but requires Python/Playwright and browser assets; browser automation is not universal. | **Reference** for web-automation projects. |
| 6 | [Agents Towards Production](https://github.com/NirDiamant/agents-towards-production) | Broad production-agent tutorials covering security, evaluation, deployment, and observability. | A large educational collection, not a bootstrap component; copying patterns without a concrete architecture would create speculative scaffolding. | **Reference** only. |
| 7 | [LLMs from Scratch](https://github.com/rasbt/LLMs-from-scratch) | Educational implementation and training of GPT-style models. | Requires ML dependencies and serves training/education, not project initialization. | **Discard** from the base. |
| 8 | [NVIDIA Build models](https://build.nvidia.com/models) | Hosted model discovery and inference endpoints. | Provider-specific, credentialed, and unnecessary for Codex initialization. | **Discard** from the base. |
| 9 | [Claude Code Game Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) | Large hierarchy of game-development agents and skills. | Domain-specific and high maintenance (dozens of agents/skills); conflicts with the small universal setup. | **Reference** for game projects only. |
| 10 | [Voicebox](https://github.com/jamiepine/voicebox) | Local voice cloning, speech, dictation, and agent voice I/O. | Large application and model stack, unrelated to bootstrap duties. | **Discard** from the base. |
| 11 | [pdf-inspector](https://github.com/firecrawl/pdf-inspector) | Fast PDF classification, extraction, and Markdown conversion. | Valuable only when document ingestion is in scope and introduces a binary/library dependency. | **Reference** for document projects. |
| 12 | [Awesome DESIGN.md](https://github.com/VoltAgent/awesome-design-md) | Curated design-system documents for consistent agent-generated UI. | Design language is application-specific; bundling a default would bias unrelated projects and require upstream curation. | **Reference** for frontend projects. |
| 13 | [Caveman](https://github.com/JuliusBrussee/caveman) | Aggressively compressed agent responses. | Existing pragmatic verbosity and Ponytail cover concision without degrading normal prose; an additional style skill is duplicative. | **Reference**, not included as a Codex default. |
| 14 | [autoskills](https://github.com/midudev/autoskills) | Detects technology and downloads matching audited skills with hashes. | Adds Node execution, a remote registry, supply-chain updates, and dynamic project mutation. The bootstrap already owns an explicit minimal skill set. | **Reference**; do not auto-run. |
| 15 | [Sesame](https://app.sesame.com/welcome) | Conversational voice AI service. | External service and unrelated to reusable coding-project setup. | **Discard**. |
| 16 | Empty Notion row (`372e283a-e1ef-805b-a1a3-db736f0e640e`) | No title, URL, category, or substantive content. | Nothing implementable or assessable. | **Discard**. |
| 17 | [Terax](https://github.com/crynta/terax-ai) | AI-native terminal workspace with editor, Git, preview, and local models. | Replaces the user interface rather than improving generated repositories; substantial independent application stack. | **Reference** as an optional workstation. |
| 18 | [Odysseus](https://github.com/odysseus-dev/odysseus) | Local AI-related application; linked repository resolved after an owner rename. | No universal bootstrap component was established; application-level dependency and maintenance are disproportionate. | **Discard** from the base. |
| 19 | [Osiris live](https://osirisai.live/) | Deployed global intelligence dashboard. | External application with no reusable initialization component. | **Discard**. |
| 20 | [Osiris source](https://github.com/simplifaisoul/osiris) | Next.js/WebGL OSINT dashboard. | Domain-specific application, data-source and operational risks, and no overlap with Codex setup. | **Discard**. |
| 21 | [Open Notebook](https://github.com/lfnovo/open-notebook) | Local, multi-model research and knowledge workspace. | Full application with model and storage dependencies; not a base-project concern. | **Reference** for research/RAG projects. |
| 22 | [NVIDIA SkillSpector](https://github.com/NVIDIA/SkillSpector) | Security scanning for agent skills and prompt-injection patterns. | Strong security value, but adds Python tooling and a changing analyzer to a dependency-free bootstrap. Manual source review and explicit skill selection remain the base policy. | **Reference**; consider as an opt-in pre-install check. |
| 23 | [Web Quality Skills](https://github.com/addyosmani/web-quality-skills) | Lighthouse, Core Web Vitals, accessibility, SEO, and quality skills. | High value for web projects, but irrelevant to non-web targets and creates many skills to maintain. | **Reference** for detected web projects; do not bundle universally. |
| 24 | [Ponytail](https://github.com/DietrichGebert/ponytail) | YAGNI ladder and shortest-working-diff discipline. | Already included as an opt-in local skill with attribution. Some overlap with Karpathy is acceptable because activation is explicit. | **Integrate** existing narrow adaptation. |
| 25 | [Headroom](https://github.com/headroomlabs-ai/headroom) | Token/context reduction tooling for agents. | Adds an intermediary runtime and operational complexity; benefits depend on workload and duplicate graph/context optimization. | **Reference**, not a base dependency. |
| 26 | [GEO/SEO Claude](https://github.com/zubair-trabzada/geo-seo-claude) | Skills and workflow for AI-search and traditional SEO optimization. | Marketing/web-domain specific and includes claims requiring ongoing verification. | **Reference** for relevant web projects. |
| 27 | [vLLM](https://github.com/vllm-project/vllm) | High-throughput local/distributed LLM serving. | Heavy hardware, Python, driver, and model dependencies; unnecessary for hosted Codex defaults. | **Discard** from the base. |
| 28 | [no-mistakes](https://github.com/kunchenguid/no-mistakes) | Worktree-based AI review/test/docs/CI gate before push and PR creation. | Useful but replaces the normal Git workflow, installs a proxy remote, and depends on configured agents. Existing validation/PR templates cover the lightweight baseline. | **Reference** as an opt-in release gate. |
| 29 | [codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp) | Local code knowledge graph, symbol search, call tracing, impact analysis, and multi-agent MCP support. | Direct fit, MIT-licensed, no API key, single binary. Binary installation remains explicit; generated config and fallback instructions are maintained locally. | **Integrate** and complete its migration throughout the repo. |
| 30 | [AI Job Search](https://github.com/MadsLorentzen/ai-job-search) | Structured job-search, CV, cover-letter, and interview workflow. | Personal/domain-specific, with Bun, Python, LaTeX, and optional PDF dependencies. | **Discard** from the universal base. |
| 31 | [LiteRT.js](https://github.com/google-ai-edge/LiteRT/tree/main/litert/js) | Browser/on-device ML inference via WebGPU/WASM. | Application-specific runtime with build/model constraints; unrelated to Codex bootstrap behavior. | **Reference** for client-side ML projects. |

## Selected changes

1. Keep the compact Karpathy and Ponytail adaptations already present; do not install duplicate upstream plugins.
2. Complete the replacement of CodeGraph with `codebase-memory-mcp` in configuration, launchers, generated assets, commands, and agent instructions.
3. Make `.mcp.json` updates additive and backup-safe.
4. Use the supported model identifier `gpt-5.6-sol`, medium reasoning, medium response verbosity, and full trusted-repository autonomy.
5. Keep specialist candidates discoverable in this inventory instead of expanding the universal dependency or skill surface.

## Maintenance and security conclusion

The resulting base remains dependency-free at runtime except for the explicitly installed `codebase-memory-mcp` binary. It does not download skills dynamically, enable provider-specific MCP servers, embed credentials, or copy third-party project code. Attributions for adapted skills remain in their skill files and reference notes.
