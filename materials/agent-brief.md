# Agent brief - shared by every fan-out page of learn-ship-internal-ai-assistant-with-phoebe

Filled from `course-builder/references/agent-brief.template.md` on 2026-10-17. Internal build
document: never link it from an audience page.

You are writing ONE static HTML session page. No servers, no npm. **If your target file already
exists on disk, do not write it; report that and stop.** Write the file, return its path and one
line of coverage. No HTML in your reply.

REPO = `/Users/phoebe.fu/Documents/claude_work/github_repo/learn-ship-internal-ai-assistant-with-phoebe`

## Read first, in this order

1. The template page for YOUR track. Copy its structure, classes, SVG grammar and quiz markup
   EXACTLY, including how many options each question has (FOUR, A to D):
   - Leader: `REPO/courses/a1-what-staff-actually-ask.html`
   - Builder: `REPO/courses/b1-the-corpus-is-the-product.html`
2. The source map: every verified fact with its tier, per-session coverage, the seams, the
   constructed Tidewell facts and the bench canon. Use ONLY its numbers; never invent a statistic;
   if a fact is missing, teach the uncertainty. `REPO/materials/official-course-map.md`
3. The stylesheet `:root` block (first 35 lines only): `REPO/assets/style.css`
4. For bench numbers and the bench's own words: `REPO/courses/b8-the-go-no-go-bench.html`. Quote
   only numbers that page, the map's canon or the widget prints. To check a number yourself:
   `node REPO/materials/run_ladder_node.js` prints the whole canon as JSON.

## Page skeleton (keep every component)

toolbar (crumb EXACTLY "learn-ship-internal-ai-assistant-with-phoebe / Leader session N of 6" or
"... / Builder session N of 8", the repo name linked to ../index.html, #toggle-all, #zoom-toggle)
· masthead (eyebrow "Ship It: Internal AI Assistant · Leader session N of 6" (or Builder ... of 8),
h1 with one `<span class="accent">`, .sub, .chip-row with the level chip (🟢 Foundational /
🟡 Core / 🟠 Advanced as given in your outline) then two .chip.audience then .chip.time "45 min",
.agenda a1-a4 with flex weights) · main.wrap · section#intro (Part 0: kicker, .lede, .legend pills
exactly as the template, .callout.win "★ What you walk out with tonight.") · 3 Parts, each
`section.section#part-N` with section-kicker (klabel "Part N · covers ...", h2 EXACTLY as your
outline gives it, `.tag.concept "N min live"`), a `.lede`, ONE figure, `details.card` accordions
(summary: `.mode.live` or `.mode.self`, title, `.mini`, `.caret ▶`), at least one
`.callout.example` with `span.ex-pill` "Real world" on the page · section#demo-1 Build-along
(kicker `.tag.demo "★ 20 min · everyone builds"` for Leader, `"★ 22 min · everyone builds"` for
Builder, .lede, ONE figure, `.steps > .step`, each with a `<p>` and, where there is code or a
template, a `.prompt-box.good` with a `span.label` BELOW the p; one `.prompt-box.bad` after the
steps) · section#exercise Homework (ol, 4 items) · section#quiz (the line "Clear all three and
Leader session N gets stamped in your passport." then 3 x `.quiz-q data-answer="0-based"`,
`p.qtext` numbered "1 · ...", FOUR `button.qopt` "A · ..." to "D · ...", `p.qwhy`; one
`p.quiz-score` after the last; vary the correct letter) · section#official, h2 EXACTLY "What this
session teaches, and where it came from", `.covered > .covered-row` (pill solid ✓ / light ◐ + name
+ note), then the `.mono` line EXACTLY "Every fact on this page, and its verification tier, is
recorded in the course's source map." · section.cheat#cheatsheet (h3 "Leader session N cheat sheet
<span>· pin this</span>" or "Builder session N cheat sheet ...", .grid-2 of six .cheat-item) ·
`.callout.next` with `.nx-pill` "Next session" · footer.pagefoot inside main, as in the template ·
`<script src="../assets/app.js?v=1"></script>`.

Head: the template's social meta block with this page's own title/description/url (og:image
stays assets/og-cover.png); `<title>Leader session N · Title - learn ship internal ai assistant
with phoebe</title>` (Builder: "Builder session N · Title - ..."); `<link rel="stylesheet"
href="../assets/style.css?v=2">`. Nothing else external.

First `details.card` in the FIRST Part is `open`; no other. Sentence case headings. Warm
practitioner voice, concrete, never dry. Inside prompt-boxes escape `&` `<` `>`. 450 to 650 lines
is guidance about depth, never a target: never collapse whitespace, dissolve a list into a
paragraph, or drop a component to fit.

## Hard rules (a violation is rework)

- NEVER an em dash or en dash, anywhere (prose, code, aria-labels, comments). Hyphen only.
- No meta text: never "this course", "in this course", "the course teaches", "banned here". State
  the professional norm directly with its reason. The two exact estate phrases above are the only
  self-references; "session 5" cross-references are fine.
- Attribution "by Phoebe Fu". Never "built with" a tool.
- Every number comes from the map or the bench, or is labelled constructed. For constructed data
  print "your numbers will differ", never invented outputs as if run. If you print code output on a
  Builder page, RUN THE CODE in a scratch directory
  (`/private/tmp/claude-504/-Users-phoebe-fu-claude-works/f280eff0-d1fd-4038-a2fb-3b5356ff5206/scratchpad/ship-assistant/agents/<your page>/`,
  never the repo) and paste exactly what it printed. Code is plain Python 3 standard library.
- Contested or missing evidence: teach the disagreement; never resolve what the literature has not.
  Productivity uplift, deflection rates and hallucination rates are CONTESTED: use only the map's
  read-at-source numbers (Brynjolfsson, Li and Raymond NBER 14% / 34% / 5,179 agents; QJE 15% /
  5,172; Humlum and Vestergaard 3% time savings, effects above 1% ruled out), never mix the NBER
  34% with the QJE citation, and never quote any deflection or hallucination rate.
- Citations in the exact form of the map's appendix; anything marked reported is "reported".
- NEVER "lottery" or "lotteries"; say the mechanism. Default to the English word; any Chinese term
  carries its English in brackets.
- **Tidewell Freight is CONSTRUCTED**: say so on the page (masthead .sub and wherever its numbers
  appear). No real company, no real incident, no real employer.
- **No vendor, product or model names as recommendations.** Name tool CLASSES: "a hosted model
  API", "a document store with access control", "a ticketing system", "an enterprise search
  product". The only model names allowed are the map's neutral description of the 2020 RAG paper.
  No price list: prices are the bench's ASSUMPTION range only.
- Titles, widget ids and class names must not collide with siblings: never use the heading
  "launch gate" or "The launch gate" (learn-agent-launch owns it; ours is "go/no-go"); avoid the
  h1s "Who can see what" and "Unity Catalog: who may see what"; never use any `tw-` class or the id
  `tw-bench` (the bench owns them). Use only classes that exist in the template pages and
  style.css; invent none.
- **Seams: link, never re-teach** (absolute URLs in the map): chunking, embeddings, vector
  databases and reranking belong to learn-rag; metric design, golden-set method and LLM-as-judge to
  learn-ai-evals; launch-gate method and risk tiers in depth to learn-agent-launch; multi-step
  agents to learn-ai-agents (we use ONE tool call); tracing and monitoring to
  learn-ai-observability; adversarial testing and prompt injection in depth to learn-ai-red-team;
  access models to learn-data-access-control; the law to learn-gdpr and learn-pdpa-dnc; the
  use-case verdict and data gate to learn-ship-playbook. Say which side this page takes, in one
  line, then link.

## Figure grammar (hand-drawn, every figure)

Palette, ONLY these hexes (no invented greys): `#0E8086` (accent, hachure line) `#0A5A60` (deep,
for .V values and dark fills with white text) `#4FA9AD` (mid) `#AEDCDE` (soft) `#E8F6F6`
(accent-50 fill) `#13292C` (ink) `#4D6466` (muted) `#C5DADB` (faint) `#E2EEEE` (hairline)
`#F4B63F` (saffron contrast: the ONE thing the figure is about; ALWAYS ink text on it, never white)
`#6B4A00` (saffron ink, .B text on white or pale fills) `#FEF5E0` (saffron tint) `#F8FCFC` (paper)
`#5F7375` · `#FFFFFF` · universal reds `#991B1B` `#FEF2F2` `#FCA5A5` only for a wrong-way, failing
or closed panel.

- `<figure class="zoomable">` > `<svg viewBox="0 0 880 H" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="the data, not the
  shape">` > `<defs>` + `<style>` + content, then `<figcaption>🔍 Click to zoom - takeaway</figcaption>`.
  Grow H, never W.
- Prefix unique per figure, used for every class and id: `<page><letter>`, e.g. `a2a`, `a2b`,
  `b3c` (so ids `a2aSk`, `a2aHc`, `a2aAr`; classes `.a2aH`, `.a2aL`...). Never reuse a prefix.
- `<defs>` holds three things with the figure prefix P: a wobble filter `id="PSk"`
  (`feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" seed="<int>"` +
  `feDisplacementMap scale="2.4" xChannelSelector="R" yChannelSelector="G"`, `x="-3%" y="-3%"
  width="106%" height="106%"`), a hachure pattern `id="PHc"` (7x7 userSpaceOnUse, rotate(-38), one
  `#0E8086` line, opacity .5), an open arrowhead `id="PAr"` (path `M1 1 L9 5 L1 9`, fill none, ink
  stroke 1.6). ALL shapes sit inside ONE `<g filter="url(#PSk)" fill="none" stroke="#13292C"
  stroke-width="2" stroke-linecap="round" stroke-linejoin="round">`; rects carry a tiny rotation
  (-4 to 4 degrees for hand-placed items, under 1 for panels). Fills: white, `#E8F6F6`, the
  hachure for "the pile" or "the data", and saffron ONLY for the one thing the figure is about.
  One doodle anchor per figure, simple strokes, never a mascot. Text classes: `.PH` 800 12px ink
  heading · `.PL` 600 12px ink label · `.PS` 400 11px muted · `.PB` 800 11px `#6B4A00` · `.PV` 800
  16-20px `#0A5A60` value · `.PW` 800 12px white ONLY on a `#0A5A60` or `#0E8086` fill (NEVER on
  saffron, the hachure or a pale fill: it paints invisible or fails contrast) · `.PA` 700 11px
  `#0A5A60` axis caption · `.PN` 400 12px muted note · `.PR` 800 11px `#991B1B` for failing or
  closed. On a saffron fill use .PL/.PH (ink), never .PS muted. Hand-stacked items must not overlap
  as painted rects (the gate flags a pile).
- ALL `<text>` OUTSIDE the filtered group, Inter sans stack, never below 10.5px.
- Fit: max chars ≈ (box width - 20) / 7 at 12px, 6.4px/char at 11px; full-width note under 110
  chars; 40px between neighbouring point labels; bottom note 22px below the last row, H clears it
  by 8px. Arrows and curves must not run through labels. When in doubt, shorten.
- Floor: one figure per Part plus one in the build-along (4 figures). Draw the MECHANISM (a
  question travelling through filters, a clause being scored, a ticket being opened, a version
  flag being read, money per answer vs per ticket), never a metaphor literally, never decoration.

## Voice and honesty

Every Part gets a `.callout.example` "Real world" story from the map's read-at-source facts (NIST
AI 600-1 confabulation, OWASP LLM02/LLM08/LLM09/LLM01, Lewis et al. index hot-swap, IMDA's nine
dimensions and incident reporting, the two field studies) or a constructed Tidewell case that SAYS
"constructed" in the text. Honest limits: answers on the bench are pre-written; tokens and prices
are assumptions; thresholds are Tidewell's policy choice; the thumbs signal is constructed.

## Cross-links (absolute URLs)

- RAG: https://phoebefu6.github.io/learn-rag-with-phoebe/ ; chunking courses/b2-chunking.html ;
  hybrid courses/b5-metadata-hybrid.html ; reranking courses/b6-reranking.html ; grounding
  courses/b7-grounding-citations.html
- AI evals: https://phoebefu6.github.io/learn-ai-evals-with-phoebe/ ; golden set
  courses/b2-golden-set.html ; retrieval metrics courses/b3-retrieval-metrics.html ; LLM-as-judge
  courses/b5-llm-as-judge.html
- Agent launch: https://phoebefu6.github.io/learn-agent-launch-with-phoebe/ ; risk tiers
  courses/a5-risk-tiers-and-the-gate.html ; after launch courses/a6-after-launch.html
- AI agents: https://phoebefu6.github.io/learn-ai-agents-with-phoebe/
- AI observability: https://phoebefu6.github.io/learn-ai-observability-with-phoebe/ ; what AI
  costs you courses/a4-what-ai-costs-you.html
- AI red team: https://phoebefu6.github.io/learn-ai-red-team-with-phoebe/ ; prompt injection
  courses/b3-prompt-injection.html
- Data access control: https://phoebefu6.github.io/learn-data-access-control-with-phoebe/ ;
  courses/a1-who-can-see-what.html ; courses/b3-row-level-security.html
- GDPR: https://phoebefu6.github.io/learn-gdpr-with-phoebe/ ; PDPA:
  https://phoebefu6.github.io/learn-pdpa-dnc-with-phoebe/
- Ship playbook: https://phoebefu6.github.io/learn-ship-playbook-with-phoebe/ ; verdict
  courses/02-the-four-way-verdict.html ; data gate courses/04-the-data-gate.html
- Hub: https://phoebefu6.github.io/learn-with-phoebe/

## Footer chains and session titles

Footer left: "Leader session N of 6 · learn-ship-internal-ai-assistant-with-phoebe · by Phoebe Fu &nbsp;·&nbsp; 📚 <a href="https://phoebefu6.github.io/learn-with-phoebe/">Learn with Phoebe ↗</a>" (Builder: "Builder session N of 8 ...").
Footer right: `<a href="PREV.html">← Prev: Title</a> &nbsp;·&nbsp; <a href="NEXT.html">Next: Title →</a>`.

Leader chain (exact titles, one accent span in the h1):
a1-what-staff-actually-ask.html "What staff actually ask" ·
a2-buy-build-or-wait.html "Buy, build or wait" ·
a3-who-may-see-what.html "Who may see what" ·
a4-when-it-does-not-know.html "What it says when it doesn't know" ·
a5-what-it-costs-to-run.html "What it costs to run" ·
a6-launch-then-keep-it-true.html "Launch, then keep it true" (last Leader page: right side
"← Prev: ..." and "Next track: Builder session 1 →" linking b1-the-corpus-is-the-product.html).

Builder chain:
b1-the-corpus-is-the-product.html "The corpus is the product" ·
b2-chunk-index-retrieve.html "Chunk, index, retrieve" ·
b3-golden-questions.html "Golden questions from the ticket log" ·
b4-grounded-answers.html "Grounded answers with citations" ·
b5-permissions-inside-retrieval.html "Permissions inside retrieval" ·
b6-open-the-ticket.html "One tool: open the ticket" ·
b7-versions-and-superseded.html "Versions and superseded policies" ·
b8-the-go-no-go-bench.html "The go/no-go bench".

## One-line outlines (the main thread expands each into the fan-out prompt)

Part h2s below are the knowledge-map concepts on the landing page; keep their meaning.
- **a2 Buy, build or wait** (🟡 Core): Part 1 "What you cannot buy" (the corpus, owners, access
  groups and ticket integration stay yours whatever you buy; figure: bought product vs your
  three layers) · Part 2 "Build what is yours" (buy/build/wait by layer, tool classes only; links
  the playbook's four-way verdict and data gate) · Part 3 "When to wait" (no owners, no access
  metadata, more than half the asked topics unwritten: wait and fix the corpus first) ·
  Build-along: a one-page buy/build/wait sheet for Tidewell's layers.
- **a3 Who may see what** (🟡 Core): Part 1 "Leaks, counted" (18 questions leak on rung 1, 7
  answered from the forbidden clause; OWASP LLM02) · Part 2 "Filter before ranking" (filter
  inside retrieval vs redact the answer; OWASP LLM08 permission-aware stores) · Part 3 "Who sets
  access" (owner-set per clause, never folder-inherited; links data access control) · Build-along:
  an access matrix for five askers and nine restricted clauses.
- **a4 What it says when it doesn't know** (🟠 Advanced): Part 1 "Confident and wrong" (rung 3:
  97.6% correct yet NO-GO; NIST confabulation, OWASP LLM09 overreliance) · Part 2 "The hand-off"
  (the hand-off as a product: what it says, what it opens) · Part 3 "Pick a threshold" (the 3.0
  line; G54 3.71 still answered, G07 2.77 missed; move it both ways) · Build-along: write
  Tidewell's hand-off message and its threshold decision note.
- **a5 What it costs to run** (🟠 Advanced): Part 1 "Tokens as a range" (465 input tokens per
  answer, USD 0.00011 to 0.0036 per answer, ASSUMPTION) · Part 2 "The ticket line" (SGD 0.25 to
  8.53 model cost a month vs SGD 6,000 hand-off tickets vs SGD 21,600 if all 2,400 were tickets) ·
  Part 3 "Cost per right answer" (the cheapest rung is the one you must not ship; links
  observability's AI cost session) · Build-along: a run-cost sheet with every input labelled.
- **a6 Launch, then keep it true** (🟠 Advanced): Part 1 "The go/no-go" (the board; thresholds as
  Tidewell's policy choice; NIST AI RMF Govern/Map/Measure/Manage) · Part 2 "Owners and versions"
  (stale answers after launch; the register; IMDA incident reporting threshold) · Part 3
  "Contested evidence" (Brynjolfsson et al. vs Humlum and Vestergaard as a disagreement; no
  deflection number) · Build-along: the one-page launch decision.
- **b2 Chunk, index, retrieve** (🟡 Core): Part 1 "One clause, one chunk" · Part 2 "BM25 by hand"
  (eq. 3.15 and 3.3, k1 1.2, b 0.75; compute three clauses for one question in plain Python, run
  it) · Part 3 "Top-3 retrieval" (hit rate 100.0%, MRR 0.913 to 0.988; lexical gaps; links RAG
  hybrid) · Build-along: a 40-line BM25 in Python over 6 constructed clauses.
- **b3 Golden questions from the ticket log** (🟡 Core): Part 1 "From the ticket log" (600
  tickets, topic coverage 100.0%) · Part 2 "Should not answer" (42 answerable, 6 restricted, 6
  no-policy; asker group on every question) · Part 3 "Risk tiers" (21 / 19 / 14; links AI evals
  golden set) · Build-along: draw 12 golden questions from 30 tickets.
- **b4 Grounded answers with citations** (🟠 Advanced): Part 1 "Answer from retrieved" · Part 2
  "The citation check" (in the retrieved set AND current) · Part 3 "A real citation that does not
  answer" (G49 dog question cites the disciplinary clause) · Build-along: a citation checker in
  Python.
- **b5 Permissions inside retrieval** (🟠 Advanced): Part 1 "The filter as code" · Part 2
  "Counting leaks" (18 to 0; G46 shows a filter changes what wins) · Part 3 "Filter after is too
  late" · Build-along: add the permission filter to the session 2 retriever and count leaks.
- **b6 One tool: open the ticket** (🟠 Advanced): Part 1 "Abstain threshold" · Part 2 "The ticket
  payload" (question, asker group, top clauses, scores, why) · Part 3 "One tool, not an agent"
  (links AI agents) · Build-along: the abstain rule plus a ticket JSON, run on four questions.
- **b7 Versions and superseded policies** (🟠 Advanced): Part 1 "Register vs index" · Part 2 "Old
  words, old answers" (rung 1 stale 6, rung 2 stale 7) · Part 3 "The nightly diff" (the break
  button's lost flag on FIN-EXP v4; links agent launch after-launch) · Build-along: a register vs
  index diff in Python.

## Before you return

Self-check your file: `grep -c '—\|–'` must be 0; `<details` count equals `</details>`;
`<section` equals `</section>`; `<figure` equals `</figure>`; `<text` equals `</text>`; no vendor
or model name; every hex inside figures is in the palette list; every number appears in the map or
on the bench page.
