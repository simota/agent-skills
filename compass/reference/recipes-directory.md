# Recipes Directory

Catalog of every global skill and available project-local extension's Subcommand (Recipe) list. Default Recipe marked with ★.

Project-local entries are sourced from `.claude/skills/`; availability and fallback rules live in `_common/PROJECT_LOCAL_SKILLS.md`.

Canonical protocol: `_common/RECIPES.md`. Per-skill detail lives in each `SKILL.md` `## Recipes` table.

Invocation: `/<skill> <subcommand> [args]`. Without a matching first token, the default Recipe is activated (backward compatible).

Regenerate with: `python3 _common/scripts/generate-recipes-directory.py`

---

- **architect**: create★ / improve / compress / audit-verbosity / evolve
- **artisan**: component★ / state / form / fetch / rsc / a11y / i18n / perf
- **atelier**: pipeline★ / extract / persist / assets
- **atlas**: analyze★ / deps / godclass / adr / rfc / cycle / coupling / boundary / multi / c4-model / deps / adr / boundary / c4-model / coupling / multi
- **attest**: verify★ / bdd / trace / report / gherkin / property / oracle
- **beacon**: slo★ / tracing / alerts / dashboard / capacity / log / golden / toil
- **bolt**: frontend★ / backend / render / async / cache / bundle / network / memory
- **breach**: scenario★ / threat-model / purple / ai-red / phishing / supply / social
- **builder**: fix★ / crud / api / ddd / harden / port / integrate / patch / pair / image / image-edit / image-prompt / image-batch / image-style / image-postprocess / image-cinematic / image-provenance / image-policy / grammar / cli
- **canon**: owasp★ / wcag / openapi / iso / gap / nist / pci / gdpr / regulatory / soc2 / hipaa / iso27001 / policy / audit / vendor / tos / privacy / tokushoho / legal-gap / dpa / eula / cookie / appstore / claims
- **canvas**: flow★ / sequence / er / journey / class / c4 / architecture / gantt
- **cast**: generate★ / registry / evolve / fuse / distribute / speak / retire / archetype / segment / bias-audit
- **chain**: intake★ / audit / mcp / scan / recover / malware-scan / campaign-scan / lockfile / eradicate / rotate / harden / propagation
- **chisel**: spec★ / scan / role / audit / brief
- **cloak**: pii★ / flow / consent / dpia / gdpr / ccpa / appi / pseudonymize / mobile
- **compass**: recommend★ / catalog / onboard / recipes / init / refresh
- **compete**: matrix★ / swot / positioning / llm-visibility / battle / winloss / moat / brand / multi
- **crypt**: algorithm★ / key / e2ee / tls / signature / password / kms / pqc / mobile
- **cue**: script★ / storyboard / narration / explainer / shorts / captions / localize / demo / scenario / record / onboard / aspects / vision / quality / geo / voiceover / thumbnail
- **darwin**: health★ / fitness / evolve / sunset
- **echo**: walkthrough★ / confusion / emotion / persona / heuristic / sus / aloud / multi / council / demand
- **experiment**: ab★ / cuped / switchback / analyze / guardrail / ff / srm / sequential / bayesian
- **field**: interview★ / usability / analysis / persona / journey / survey / diary / cards / multi
- **flow**: hover★ / loading / transition / gesture / spring / scroll / parallax
- **flux**: reframe★ / shift / cross / challenge / scamper / analogy / inversion / multi / ideate
- **forge**: ui★ / api / fullstack / landing / mobile / dashboard / ai
- **frame**: extract★ / code-connect / rules / inspect / variants / tokens / breakpoint
- **funnel**: build★ / cta / conversion / responsive / form / copy / trust / premium / build / conversion / form / trust
- **gateway**: design★ / openapi / versioning / breaking / rest / graphql / webhook / auth / rate-limit / deprecation / rest / graphql / breaking / auth / webhook
- **gauge**: audit★ / fix / research / checklist / staleness
- **gear**: deps★ / ci / docker / logs / health / alert / secret / k8s / gha
- **grove**: audit★ / design / docs / migrate / monorepo / tests / scripts / llm / audit / docs / monorepo
- **growth**: seo★ / smo / cro / geo / keyword / audit / vitals / retention
- **guardian**: pr★ / commit / naming / strategy / reshape / audit / split / health / ship
- **hone**: audit★ / codex / agy / claude / diff / hook / hook-debug / env / automate
- **ink**: icon★ / illustration / system / sprite / animate / theme / a11y / optimize / pictogram / logo
- **judge**: pr★ / security / perf / style / quick / intent / lean / pair
- **launch**: plan★ / changelog / notes / rollback / flag / hotfix / canary / mobile / weekly / monthly / client-report / retro / dora / okr / pr-flow
- **ledger**: estimate★ / rightsizing / anomaly / ri-sp / gpu-cost / tagging / finops-framework / unit-economics / greenops
- **lens**: map★ / ask / discover / trace / responsibility / dependency / hotspot / evolution
- **lore**: curate★ / decay / propagate / extract
- **magi**: decide★ / tradeoff / arbitrate / strategic / sixhat / devil / delphi / advisor / multi / simulate
- **matrix**: combine★ / cover / plan / prioritize / pairwise / equiv-class / risk-cover / qa-scenario
- **mend**: runbook★ / diagnose / rollback / verify / scale / circuit / canary
- **muse**: tokens★ / apply / theme / typography / spacing / motion / elevation / radius
- **native**: swiftui★ / compose / liquidglass / expressive / offline / push / deeplink / bg / passkey / privacy / rollout / store / cli / visualloop / macos / macdist
- **nexus**: bug / feature / deliver / security / refactor / optimize / kaizen / anneal / restyle / converge / quell / whet / burnish / apex / charter / enact / layer / goal / gedanken / delve / cartograph / chronicle / verity / abide / spec / essential / killer / trim / acceptance / summit / podium / newsroom / eureka / wish / runway / hallmark / rebrand / crucible / silhouette / lattice / assay / chorus / migrate / transmute / clone / fuse / graft / package / pack
- **omen**: premortem★ / rpn / ap / mode / faulttree / bowtie / hazop / multi
- **oracle**: prompt★ / rag / safety / mlops / agent / cost / embed / review / tooling
- **orbit**: plan / generate★ / contract / audit / recover / ralph
- **palette**: usability★ / cognitive / feedback / a11y / keyboard / mobile / forms / error / empty / loading / usability / forms / error / mobile / cognitive / usability
- **pdm**: status★ / features / gaps / roadmap / wbs / ask
- **pixel**: reproduce★ / verify / gap / audit / responsive / dark / animation
- **polyglot**: extract★ / intl / keys / rtl / pluralize / locale / translate / mobile
- **port**: blueprint★ / survey / parity / map / roadmap / risk / regulatory / xplat
- **probe**: zap★ / burp / nuclei / pentest / api / mobile / recon
- **prose**: microcopy★ / errors / onboarding / a11y / tone / empty-state / notification / status
- **prune**: audit★ / merge / sunset / pack-impact
- **pulse**: kpi★ / funnel / cohort / event / dashboard / northstar / retention / activation
- **quill**: docstring★ / readme / types / comments / adr / migrate / tutorial
- **radar**: edge★ / flaky / coverage / regression / ci / unit / integration / mutation / fixtures
- **rally**: parallel★ / teams / codex-subagents / coordinate / engine-paradigm
- **rank**: ice★ / rice / wsjf / moscow / kano / cod / value-effort / pokerplan
- **ripple**: impact★ / vertical / horizontal / naming / blast-radius / rollback-plan / canary-scope
- **saga**: story★ / scenario / narrative / customer / hero-journey / bab / pyramid / onboarding / audit / micro / multi / story / narrative / hero-journey / pyramid / audit / multi
- **scaffold**: terraform★ / cloudformation / pulumi / compose / env / k8s / helm / cdk
- **schema**: design★ / migration / er / normalize / index / rollback / tenant / partition / audit-log / event-sourcing / soft-delete
- **scout**: bug★ / regression / prod / multi / cascade / perf / memory / flake / 5whys / fishbone / timeline / video
- **scribe**: prd★ / srs / hld / lld / testspec / adr / runbook / api-doc / unified / convert
- **seek**: fulltext★ / vector / hybrid / index / rag / rerank / suggest / authz / eval / fulltext / hybrid / eval / suggest
- **sentinel**: scan★ / secrets / injection / deps / headers / authn / authz / aisec / mobile / multi
- **sherpa**: epic★ / story / replan / review / atomic / walking-skeleton / vertical-slice
- **shift**: plan★ / codemod / strangler / verify / framework / lang / deprecate / detect / modernize / radar
- **siege**: load★ / contract / chaos / mutation / fuzz / property / smoke / concurrency
- **sigil**: generate★ / analyze / convention / migrate / blueprint / blueprint
- **spark**: propose★ / plan / brainstorm / refine / opportunity / kill / retro / multi
- **stage**: marp★ / reveal / slidev / conference / timing / narrative / visual / rehearsal
- **stream**: etl★ / elt / stream / dbt / cdc / reverse / quality
- **sweep**: dead★ / orphan / unused / tidy / imports / comments / types / dead / tidy / comments
- **tome**: learn★ / diff / onboard / record / worked / kata / quickstart / article / note / zenn / qiita / devto / article-series / headline / repurpose / interview
- **trace**: replay★ / persona / story / archaeology / rageclick / funnel / heatmap
- **trail**: regression★ / bisect / blame / history / flame / delta / revert / static-rules
- **triage**: respond★ / impact / recover / postmortem / first-response / escalation / comms
- **tuner**: explain★ / slow / index / plan / cache / connection / vacuum / explain / index / connection
- **vector**: collect★ / form / screenshot / network / stealth / mobile / parallel / crawl
- **vigil**: sigma★ / yara / coverage / hunt / snort / playbook / ioc / sigma / coverage / snort / ioc
- **vision**: direction★ / redesign / trend / system / brand / moodboard / audit / multi / pair
- **vitrine**: story★ / catalog / vrt / csf3 / interaction / mdx / cosmos / a11y / chromatic / coverage
- **voice**: nps★ / review / sentiment / classify / insight / kano / thematic / csat
- **void**: prune★ / cut / question / simplify
- **voyager**: playwright★ / page-object / auth / a11y / visual / api / mobile / component / ios
- **weave**: design★ / saga / approval / detect / retry / timeout / compensation / design / approval / retry / compensation / schedule
- **zen**: refactor★ / naming / extract / constants / dead / simplify / split / guard / naming / constants / simplify

---

**Total**: 93 skills with Recipes (90 global + 3 project-local).

Auto-generated from SKILL.md `## Recipes` tables by `_common/scripts/generate-recipes-directory.py`. Do not edit by hand.

