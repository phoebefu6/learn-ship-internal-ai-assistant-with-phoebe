# Official course map - learn-ship-internal-ai-assistant-with-phoebe

"Ship It: Internal AI Assistant". Ship bucket, two tracks: Leader a1-a6 (no code) and Builder
b1-b8 (bench at b8). Skeleton approved by Phoebe 2026-10-17. Internal build document: never link it
from an audience page. Every fact a page prints must be in this file with its tier, or be a bench
number listed under "Canon".

Evidence tiers:
- **READ AT SOURCE** - read in the primary document on 2026-10-17 (quotes and page locations in
  `materials/sources-notes.md`).
- **REPORTED** - only a secondary source was read; say "reported" on the page.
- **CONSTRUCTED** - invented for Tidewell Freight; say "constructed" on the page.
- **MEASURED (bench)** - printed by `assets/assist-live.js`, matched by `materials/assist_reference.py`.

## The running case: Tidewell Freight (CONSTRUCTED)

A constructed 1,200-person freight forwarder headquartered in Singapore. Its policy and ops
helpdesk assistant answers staff questions from HR, IT and finance policy documents, cites the
clause it used, and opens a ticket when it cannot answer. Labelled constructed on every page.
No real company, no real incident, no vendor or model named as a recommendation (name tool
classes: "a hosted model API", "a document store with access control", "a ticketing system").

Constructed facts pages may use (all from `materials/build_assist_data.py`):
- 1,200 staff; 2,400 assistant questions a month (assumption for cost); helpdesk ticket cost
  12 minutes at SGD 45 an hour = SGD 9 a ticket (assumption).
- Policy store: 49 clause versions across 16 documents (6 HR, 5 IT, 5 finance), 42 current and
  7 superseded versions still in the store. Access groups: all staff, managers (managers + HR),
  HR only, finance only, IT only. Every clause has a stable key, version, effective date,
  superseded flag, owner and access group.
- The seven superseded versions: HR-LV-1 v2 (18 days "holiday entitlement"), HR-LV-2 v2 ("carry
  forward" 10 days to 30 June), HR-WFH-1 v1 (3 "remote work days"), IT-ACC-1 v3 (change every 90
  days), FIN-EXP-1 v4 (claims within 60 days), FIN-EXP-2 v4 ("per diem" SGD 50), FIN-TRV-1 v2
  (business class over 8 hours).
- Golden set: 54 questions. 42 answerable by the asker, 6 restricted (a clause answers it but the
  asker may not read it), 6 with no policy at all. 7 of the answerable ones are worded in the old
  policy's vocabulary. Risk tiers: 21 high, 19 medium, 14 low. Askers: 46 staff, 5 managers,
  1 HR, 1 finance, 1 IT.
- Ticket log: 600 tickets in one quarter (seeded). See canon below.

## Per-session coverage

### Leader track (no code)
| File | Title | Owns | Sources |
|---|---|---|---|
| a1-what-staff-actually-ask.html | What staff actually ask | Scoping from the ticket log: policy lookups vs actions vs no-policy; three resolution types; the scope sentence | Ticket log canon (constructed); NIST AI 600-1 confabulation (read at source) for why "no-policy" questions are the dangerous ones |
| a2-buy-build-or-wait.html | Buy, build or wait | Buy/build/wait for THIS assistant: the parts you cannot buy (the corpus, the permissions, the owners) | Links `learn-ship-playbook` 02 verdict and 04 data gate; Lewis et al. 2020 definition (read at source) |
| a3-who-may-see-what.html | Who may see what | Permission-aware retrieval as a leader decision; filter before generation, never after | OWASP LLM02, LLM08 (read at source); bench leaks 18 -> 0 |
| a4-when-it-does-not-know.html | What it says when it doesn't know | Abstain-and-hand-off design; the hand-off is a product, not an error | NIST AI 600-1 confabulation; OWASP LLM09 overreliance (read at source); bench r3 vs r4 |
| a5-what-it-costs-to-run.html | What it costs to run | Run cost: model tokens are small, hand-off tickets dominate; price as a range, labelled assumption | Bench cost canon (assumption) |
| a6-launch-then-keep-it-true.html | Launch, then keep it true | The go/no-go decision stitched together; document owners, versioning, staleness after launch; productivity claims taught as disagreement | NIST AI RMF 1.0 functions; IMDA GenAI framework incident reporting (read at source); Brynjolfsson et al. vs Humlum and Vestergaard (read at source) |

### Builder track
| File | Title | Owns | Sources |
|---|---|---|---|
| b1-the-corpus-is-the-product.html | The corpus is the product | The clause schema: key, version, effective date, superseded flag, owner, access group; why metadata is the build | Constructed store; Lewis et al. 2020 (index can be updated without retraining, read at source) |
| b2-chunk-index-retrieve.html | Chunk, index, retrieve | Clause-level chunks, BM25 by hand (k1, b, IDF), top-k; depth links to learn-rag | Robertson and Zaragoza 2009 (read at source) |
| b3-golden-questions.html | Golden questions from the ticket log | Drawing the golden set from tickets; answerable / restricted / no-policy; asker group; risk tier | Ticket log + golden set (constructed); method depth links to learn-ai-evals b2 |
| b4-grounded-answers.html | Grounded answers with citations | Answer only from retrieved clauses; the citation check (in the retrieved set AND current) | OWASP LLM09; NIST AI 600-1 information integrity (read at source) |
| b5-permissions-inside-retrieval.html | Permissions inside retrieval | The permission filter as code, before ranking; the leak count | OWASP LLM08 "permission-aware vector and embedding stores" (read at source); depth links to learn-data-access-control |
| b6-open-the-ticket.html | One tool: open the ticket | The single tool call: abstain threshold, the ticket payload (question, asker group, top clauses, why) | Bench r4; multi-step agents link to learn-ai-agents |
| b7-versions-and-superseded.html | Versions and superseded policies | The version register vs the index flag; staleness; the break button mechanism | Bench break canon; Lewis et al. index hot-swap (read at source) |
| b8-the-go-no-go-bench.html | The go/no-go bench | The full ladder, the anti-lever, the break button, the decision | All canon below |

## Seams (link with absolute URLs, never reteach; say out loud which side we take)

- `learn-rag` owns chunking strategies, embeddings, vector databases, reranking:
  https://phoebefu6.github.io/learn-rag-with-phoebe/courses/b2-chunking.html ,
  b5-metadata-hybrid.html (BM25 plus dense), b6-reranking.html, b7-grounding-citations.html.
  We take: one lexical retriever (BM25) because it is inspectable by hand.
- `learn-ai-evals` owns metric design, golden-set method, LLM-as-judge:
  https://phoebefu6.github.io/learn-ai-evals-with-phoebe/courses/b2-golden-set.html , b3-retrieval-metrics.html.
  We take: the golden set drawn from THIS assistant's tickets; hit rate and MRR only.
- `learn-agent-launch` owns the launch-gate method and risk tiers in depth:
  https://phoebefu6.github.io/learn-agent-launch-with-phoebe/courses/a5-risk-tiers-and-the-gate.html , b9-the-launch-gate.html.
  The heading "launch gate" is TAKEN; ours is "the go/no-go bench" / "go/no-go".
- `learn-ai-agents` owns multi-step agents: https://phoebefu6.github.io/learn-ai-agents-with-phoebe/ . We use ONE tool call.
- `learn-ai-observability` owns tracing and monitoring: https://phoebefu6.github.io/learn-ai-observability-with-phoebe/
- `learn-ai-red-team` owns adversarial testing (prompt injection in depth): https://phoebefu6.github.io/learn-ai-red-team-with-phoebe/courses/b3-prompt-injection.html
- `learn-data-access-control` owns access models: https://phoebefu6.github.io/learn-data-access-control-with-phoebe/courses/a1-who-can-see-what.html , b3-row-level-security.html
- `learn-gdpr` / `learn-pdpa-dnc` own the law: https://phoebefu6.github.io/learn-gdpr-with-phoebe/ , https://phoebefu6.github.io/learn-pdpa-dnc-with-phoebe/
- `learn-ship-playbook` owns the use-case verdict and data gate (a2 links to it):
  https://phoebefu6.github.io/learn-ship-playbook-with-phoebe/courses/02-the-four-way-verdict.html , 04-the-data-gate.html

## Verified facts (cite exactly as written here)

### BM25 - Robertson, S. and Zaragoza, H. (2009). "The Probabilistic Relevance Framework: BM25 and Beyond". Foundations and Trends in Information Retrieval 3(4), 333-389. READ AT SOURCE
- Term weight (eq. 3.15, p.360): tf / (k1 x ((1 - b) + b x dl/avdl) + tf) x w(RSJ); document score = sum over query terms.
- IDF form with no relevance information (eq. 3.3, p.349): log((N - n + 0.5) / (n + 0.5)), "a close approximation to classical idf".
- b = 1 is full length normalisation, b = 0 switches it off (p.359-360).
- "values such as 0.5 < b < 0.8 and 1.2 < k1 < 2 are reasonably good in many circumstances" (p.360-361); optimal values depend on the documents and queries; the model gives no guidance on setting them.
- The (k1 + 1) numerator factor in common variants "does not affect the ranking" (p.361). The bench uses eq. 3.15 without it.
- Our own arithmetic, NOT in the paper: the eq. 3.3 IDF goes negative for a term in more than half the documents (no term does in Tidewell's 49 clauses).

### RAG - Lewis, P. et al. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks". NeurIPS 2020, arXiv 2005.11401. READ AT SOURCE
- Definition: models "which combine pre-trained parametric and non-parametric memory for language generation".
- The paper calls "providing provenance for their decisions and updating their world knowledge" open research problems.
- Index hot-swap: knowledge "can be easily updated at test time" by replacing the non-parametric memory, without retraining (Sec. 4.5, 6).
- Neutral description only: a dense retriever over a Wikipedia index plus a seq2seq generator. Not a recommendation.

### NIST AI RMF 1.0 (NIST AI 100-1, January 2023). READ AT SOURCE
- Four functions: GOVERN (cross-cutting), MAP, MEASURE, MANAGE.
- Seven trustworthy characteristics: valid and reliable; safe; secure and resilient; accountable and transparent; explainable and interpretable; privacy-enhanced; fair with harmful bias managed.

### NIST AI 600-1 Generative AI Profile (July 2024). READ AT SOURCE
- Names 12 GAI risks, including Confabulation, Data Privacy, Information Integrity, Information Security.
- Confabulation: "The production of confidently stated but erroneous or false content"; NIST prefers the word because "hallucination" anthropomorphises.
- Risk arises "when users believe false content - often due to the confident nature of the response" (p.6).

### OWASP Top 10 for LLM Applications 2025 (genai.owasp.org). READ AT SOURCE (live pages; re-check punctuation before quoting)
- LLM01 Prompt Injection; LLM02 Sensitive Information Disclosure; LLM08 Vector and Embedding Weaknesses; LLM09 Misinformation (full list of ten in sources-notes).
- LLM08 prevention: "Implement fine-grained access controls and permission-aware vector and embedding stores."
- LLM02 prevention: limit access to sensitive data "based on the principle of least privilege".
- LLM09: overreliance is when users "place excessive trust in LLM-generated content"; prevention includes human oversight for critical information.
- LLM01: RAG and fine-tuning "do not fully mitigate prompt injection vulnerabilities" (a poisoned policy document is an indirect injection; depth in learn-ai-red-team).

### IMDA / AI Verify Foundation, Model AI Governance Framework for Generative AI (Singapore, released 30 May 2024). READ AT SOURCE (file dated 19 June 2024; release date reported via IMDA factsheet)
- Nine dimensions: Accountability; Data; Trusted Development and Deployment; Incident Reporting; Testing and Assurance; Security; Content Provenance; Safety and Alignment R&D; AI for Public Good.
- Names RAG among techniques "commonly used to reduce hallucinations and improve accuracy" (p.13).
- Incident reporting: "Defining 'severe AI incidents' or setting the materiality threshold for formal reporting is therefore key" (p.17).

### Field evidence on support assistants: TAUGHT AS DISAGREEMENT
- Brynjolfsson, E., Li, D. and Raymond, L. "Generative AI at Work". NBER Working Paper 31161 (revised Nov 2023), READ AT SOURCE: 5,179 customer support agents; issues resolved per hour up 14% on average, 34% for novice and low-skilled workers, minimal impact on experienced and highly skilled workers. Published in the Quarterly Journal of Economics 140(2), 2025: abstract READ (via publisher metadata) says 5,172 agents and 15% on average, with small declines in quality for the most experienced; QJE body not read. Cite the version you use; never mix 34% with the QJE citation.
- Humlum, A. and Vestergaard, E. "Large Language Models, Small Labor Market Effects", BFI Working Paper 2025-56 (May 2025), abstract READ AT SOURCE: 25,000 workers in 11 exposed occupations in Denmark; "precise zeros" on earnings and recorded hours, ruling out effects larger than 1%; average time savings of 3%. The NBER version (w33777, retitled "Still Waters, Rapid Currents") rules out effects larger than 2%.
- The disagreement: task-level speed gains in one contact centre vs no measurable earnings or hours effect across a labour market. Different outcomes, settings and horizons. Do not resolve it.
- Helpdesk "deflection rate": no credible public benchmark was found; only vendor-reported figures. Teach as contested and easily gamed (a user who gives up counts as deflected). Never quote a vendor number.

## Canon (MEASURED by the bench; python and node agree by value, 269 values, tolerance 1e-9)

Settings: BM25 k1 = 1.2, b = 0.75, top-3, abstain below a top score of 3.0. Index: N = 49 clause
versions, avdl = 21.76 tokens, vocabulary 445 terms. Gate (Tidewell's policy choice, not a
standard): 0 leaks; 0 stale citations; confident wrong answers at most 5% of high-risk, 10% of
medium-risk, 20% of low-risk questions; correct answers on at least 70% of answerable questions;
right hand-offs on at least 80% of questions it should not answer. Thumbs grade: GO if the
thumbs-up rate is at least 75%.

| Rung | Top-3 hit | MRR | Leaks | Stale | Correct (of 42) | Right hand-offs (of 12) | Wrong high / med / low | Thumbs-up | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| 1 No permission filter | 100.0% | 0.913 | 18 | 6 | 35 (83.3%) | 0 (0.0%) | 23.8% / 36.8% / 50.0% | 90.7% | NO-GO |
| 2 + permission filter | 100.0% | 0.913 | 0 | 7 | 35 (83.3%) | 0 (0.0%) | 23.8% / 36.8% / 50.0% | 90.7% | NO-GO |
| 3 + current-version filter | 100.0% | 0.988 | 0 | 0 | 41 (97.6%) | 1 (8.3%) | 4.8% / 31.6% / 35.7% | 90.7% | NO-GO |
| 4 + abstain and hand off | 100.0% | 0.988 | 0 | 0 | 38 (90.5%) | 11 (91.7%) | 0.0% / 0.0% / 7.1% | 81.5% | GO |

- Rung 1: 7 of the 18 leaking questions are answered FROM the clause the asker may not read (leaked answers 7).
- Rung 1 stale citations: G14, G36, G37, G38, G39, G41 (old password, holiday, carry forward, remote work and per diem versions).
- Rung 2 shows 7 stale citations, one more than rung 1: G46 (a staff member asks how long a performance improvement plan lasts); once the managers-only clause is filtered out, the superseded IT-ACC-1 v3 password clause is the best remaining match.
- Rung 4: 39 answered, 15 handed off (11 right, 4 safe misses: G07 pay day, G17 laptop refresh, G37 carry forward, G38 remote days). The one confident wrong answer is G54 (staff party, low risk, top score 3.71).
- Go/no-go reasons printed at rung 3: medium-risk 31.6% over 10.0%; low-risk 35.7% over 20.0%; hands off 8.3%, needs 80.0%.

**Anti-lever, grade by thumbs-up:** rung 1 thumbs-up 90.7% passes the 75% bar, so the thumbs grade
prints GO on the assistant the policy rejects (18 leaks, 6 stale citations). Thumbs fall as safety
rises: 90.7% on rungs 1-3, 81.5% on rung 4, because staff thumb down hand-offs.

**Break button, index the superseded expenses policy (FIN-EXP v4) as current:** rung 4 pipeline
verdict GO, register verdict NO-GO: 1 answer cites a superseded version (G41, per diem, SGD 50 from
v4 instead of the SGD 60 daily allowance in v5). The pipeline sees 0 stale citations. Correct 37 of
42 (88.1%), MRR 0.964. At rung 3 the break produces 2 register-stale citations (G38 and G41, both citing
FIN-EXP-2 v4) and the pipeline sees 0.

**Cost (ASSUMPTION; token count = words x 1.3, ceil; system 350 tokens; output 150 tokens; USD 0.10
to 3.00 per million input, 0.40 to 15.00 per million output; 1 USD = 1.35 SGD):** rung 4 average
465.1 input tokens per answer (widget prints "465"); model cost per answer USD 0.00011 to 0.0036 (widget prints
"$0.00011 to $0.0036"); a month of 2,400 questions SGD 0.25 to 8.53 in model cost; hand-off tickets
SGD 6,000; all 2,400 as tickets would be SGD 21,600. Rungs 1-2: SGD 0.34 to 11.78 model cost, 0
tickets. The model is the small line; the hand-off is the big one.

**Ticket log (constructed, seeded):** 600 tickets: 226 HR, 248 IT, 126 finance. 333 (55.5%)
answered by pointing at a policy clause, 223 needed a person to do something, 44 had no written
answer anywhere. 13,437 minutes in total: 3,707 on policy lookups, 9,064 on actions, 666 on
no-policy. Top topics: access 98, leave 95, expenses 75, devices 74, software 65, pay 51. The
golden set covers the topics of 100.0% of the policy-answerable tickets.

**Self-test (on load):** 5 of 5 properties hold; the planted fault (permission filter switched off)
is caught.

## Not covered (honest list)
- Embeddings, dense retrieval, hybrid search, reranking, chunking strategies: learn-rag.
- Metric design beyond hit rate and MRR; LLM-as-judge; answer-quality grading: learn-ai-evals.
- Tracing, monitoring, alerting in production: learn-ai-observability.
- Prompt injection and adversarial testing in depth: learn-ai-red-team.
- Multi-step agents and tool chains: learn-ai-agents.
- Law (PDPA, GDPR) and employment law: learn-pdpa-dnc, learn-gdpr. Tidewell's policies are not legal advice.
- Vendor or model selection, price lists: deliberately not covered.
- Real deflection or productivity numbers for internal helpdesk assistants: no credible public benchmark read.
- Generation itself: the bench's answers are pre-written; no language model runs in the browser.

## Titles, slugs, ids (grep-checked against the estate 2026-10-17)
- No estate h1 or title matches any of the 14 titles. Near miss: learn-databricks a3 "Unity Catalog: who may see what" (different, prefixed); learn-data-access-control a1 "Who can see what" (different wording). Keep ours.
- Bench host id `tw-bench`, class prefix `tw-` (free in the estate). Figure prefixes: page id + letter (a1a, b8c ...).
- "launch gate" is taken by learn-agent-launch: never use it as a heading.

## Citation appendix (use these exact forms)
- Robertson, S. and Zaragoza, H. (2009). The Probabilistic Relevance Framework: BM25 and Beyond. Foundations and Trends in Information Retrieval 3(4), 333-389. https://doi.org/10.1561/1500000019
- Lewis, P. et al. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. NeurIPS 2020. https://arxiv.org/abs/2005.11401
- NIST (2023). Artificial Intelligence Risk Management Framework (AI RMF 1.0), NIST AI 100-1. https://doi.org/10.6028/NIST.AI.100-1
- NIST (2024). Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile, NIST AI 600-1. https://doi.org/10.6028/NIST.AI.600-1
- OWASP (2025). OWASP Top 10 for LLM Applications 2025. https://genai.owasp.org/llm-top-10/
- IMDA and AI Verify Foundation (2024). Model AI Governance Framework for Generative AI. https://aiverifyfoundation.sg/resources/mgf-gen-ai/
- Brynjolfsson, E., Li, D. and Raymond, L. (2023). Generative AI at Work. NBER Working Paper 31161. https://www.nber.org/papers/w31161 (published QJE 140(2), 2025, https://doi.org/10.1093/qje/qjae044)
- Humlum, A. and Vestergaard, E. (2025). Large Language Models, Small Labor Market Effects. BFI Working Paper 2025-56. https://bfi.uchicago.edu/wp-content/uploads/2025/04/BFI_WP_2025-56-3.pdf (NBER w33777)

## Rebuild
```
python3 materials/build_assist_data.py      # data -> materials/assist-data.json + assets/assist-data.js
python3 materials/compare-ladder.py         # python vs node by value + planted fault; exit 0 = agree
```
