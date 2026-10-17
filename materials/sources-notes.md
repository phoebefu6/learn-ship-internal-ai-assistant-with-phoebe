# Sources notes - ship an internal AI policy helpdesk assistant

Verified 2026-10-17. Quotes are short excerpts copied from the text extracted from the primary PDF/page. Page numbers are the printed page numbers unless marked "PDF p.".

---

## 1. Robertson & Zaragoza (2009) - The Probabilistic Relevance Framework: BM25 and Beyond

- Canonical: https://doi.org/10.1561/1500000019 (Foundations and Trends in IR, Vol. 3, No. 4 (2009) 333-389)
- Read from author copy: https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf (full 59-page text, journal pagination)
- Tier: READ AT SOURCE

Formulas as printed (rendered in plain text):
- Eq. 3.2, p.348, RSJ weight: w_i^RSJ = log [ (r_i + 0.5)(N - R - n_i + r_i + 0.5) ] / [ (n_i - r_i + 0.5)(R - r_i + 0.5) ]
- Why the 0.5: "a small pseudo-count of frequency 0.5. The resulting formula is the well-known Robertson/Sparck Jones weight" (p.348). Also: ratio of probabilities plus log "may yield (positive or negative) infinities as estimates" (p.348).
- Eq. 3.3, p.349, IDF form with no relevance info (set R = r_i = 0): w_i^IDF = log (N - n_i + 0.5) / (n_i + 0.5). Quote: "The resulting formula is a close approximation to classical idf" (p.349).
- Eq. 3.12, p.359, length normalisation: B := ( (1 - b) + b * dl/avdl ), 0 <= b <= 1. "setting b = 1 will perform full document-length normalisation, while b = 0 will switch normalisation off" (p.359-360).
- dl defined as sum of tf_i over the vocabulary; "avdl (average over collection)" (p.359).
- Eq. 3.15, p.360: w_i^BM25(tf) = tf / ( k1 * ((1 - b) + b * dl/avdl) + tf ) * w_i^RSJ. "This is the classic BM25 term-weighting and document-scoring function." Document score = sum of term weights over query terms (p.360).
- Parameter ranges, p.360-361: "values such as 0.5 < b < 0.8 and 1.2 < k1 < 2 are reasonably good in many circumstances."
- Caveat, p.361: "optimal values do depend on other factors (such as the type of documents or queries)."
- Also p.360: "the model provides no guidance on how these should be set."
- Variants, p.361: common variant adds a (k1 + 1) factor to the numerator - "does not affect the ranking produced". Some versions fix "b = 0.5 and k1 = 2" but "many experiments suggest a somewhat lower value of k1 and a somewhat higher value of b."
- Negative IDF: NOT discussed explicitly. The only related remark is the "(positive or negative) infinities" note on raw ratio estimates (p.348). The fact that log((N - n + 0.5)/(n + 0.5)) goes negative when a term appears in more than half the documents is true arithmetic but is not stated in this paper - teach it as our own derivation, not as a quote (Lucene's later BM25 adds 1 inside the log to avoid it; not verified here).

Safe to teach: BM25 = saturating tf (k1) x soft length normalisation (b, dl/avdl) x RSJ/IDF weight log((N - n + 0.5)/(n + 0.5)); typical 0.5 < b < 0.8 and 1.2 < k1 < 2, tune per collection.

---

## 2. Lewis et al. (2020) - Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (NeurIPS 2020)

- URL: https://arxiv.org/abs/2005.11401 (read PDF arXiv v4, 12 Apr 2021)
- Tier: READ AT SOURCE

Quotes:
- Definition (Abstract, p.1): "retrieval-augmented generation (RAG) - models which combine pre-trained parametric and non-parametric memory for language generation."
- Components (Abstract, p.1): "the parametric memory is a pre-trained seq2seq model and the non-parametric memory is a dense vector index of Wikipedia".
- Provenance / updating as open problems (Abstract, p.1): "providing provenance for their decisions and updating their world knowledge remain open research problems."
- Why hybrid helps (Sec. 1, p.1): "knowledge can be directly revised and expanded, and accessed knowledge can be inspected and interpreted."
- Retriever (Sec. 2.2, p.3): "The retrieval component p_eta(z|x) is based on DPR" - a bi-encoder, two BERT-base encoders, top-k by Maximum Inner Product Search.
- Generator (Sec. 2.3, p.3): "We use BART-large ... a pre-trained seq2seq transformer ... with 400M parameters." Input and retrieved passage are simply concatenated.
- Corpus (Sec. 3, p.4): December 2018 Wikipedia dump, "split into disjoint 100-word chunks, to make a total of 21M documents", FAISS index.
- Two variants (Abstract): RAG-Sequence (same passages for whole output) and RAG-Token (different passages per token).
- Updating knowledge (Sec. 4.5 "Index hot-swapping", p.7-8): "knowledge can be easily updated at test time." 2016 index on 2016 leaders: 70% correct; 2018 index on 2018 leaders: 68%; mismatched: 12% and 4% (82 world leaders).
- (p.8): "we can update RAG's world knowledge by simply replacing its non-parametric memory."
- Discussion (Sec. 6, p.9): the index "can be hot-swapped to update the model without requiring any retraining."

Safe to teach: RAG pairs a parametric generator (BART) with a non-parametric retrieved index (DPR over Wikipedia); its stated advantages are inspectable sources and knowledge updates by swapping the index, not retraining. Note the paper itself calls provenance an open problem - RAG makes it inspectable, it does not by itself guarantee correct citation.

---

## 3a. NIST AI RMF 1.0 (NIST AI 100-1, January 2023)

- URL: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf (DOI https://doi.org/10.6028/NIST.AI.100-1)
- Tier: READ AT SOURCE

Quotes:
- Four functions (Executive Summary, p.3): "These functions - GOVERN, MAP, MEASURE, and MANAGE - are broken down further into categories and subcategories."
- (p.3): "While GOVERN applies to all stages ... the MAP, MEASURE, and MANAGE functions can be applied in AI system-specific contexts".
- GOVERN (Sec. 5.1, p.22): "a cross-cutting function that is infused throughout AI risk management and enables the other functions".
- MAP (Sec. 5.2, p.24): "establishes the context to frame risks related to an AI system."
- MEASURE (Sec. 5.3, p.28): "employs quantitative, qualitative, or mixed-method tools ... to analyze, assess, benchmark, and monitor AI risk".
- MANAGE (Sec. 5.4, p.31): "entails allocating risk resources to mapped and measured risks"; risk treatment includes plans "to respond to, recover from, and communicate about incidents or events."
- Trustworthy characteristics (Sec. 3, p.12), exact section names (3.1-3.7): Valid and Reliable; Safe; Secure and Resilient; Accountable and Transparent; Explainable and Interpretable; Privacy-Enhanced; Fair - with Harmful Bias Managed.
- (p.12): "Characteristics of trustworthy AI systems include: valid and reliable, safe, secure and resilient, accountable and transparent, explainable and interpretable, privacy-enhanced, and fair with harmful bias managed."
- Fig. 4 caption (p.12): "Valid & Reliable is a necessary condition of trustworthiness"; Accountable & Transparent "relates to all other characteristics."

Safe to teach: 4 functions Govern (cross-cutting) / Map / Measure / Manage; 7 trustworthy characteristics with Valid and Reliable as the base.

## 3b. NIST AI 600-1 - Generative AI Profile (July 2024)

- URL: https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf (DOI https://doi.org/10.6028/NIST.AI.600-1)
- Tier: READ AT SOURCE

The 12 risks, exact names (Sec. 2, p.4-5):
1. CBRN Information or Capabilities
2. Confabulation
3. Dangerous, Violent, or Hateful Content
4. Data Privacy
5. Environmental Impacts
6. Harmful Bias or Homogenization
7. Human-AI Configuration
8. Information Integrity
9. Information Security
10. Intellectual Property
11. Obscene, Degrading, and/or Abusive Content
12. Value Chain and Component Integration

Quotes:
- Confabulation (list, p.4): "The production of confidently stated but erroneous or false content (known colloquially as 'hallucinations' or 'fabrications')".
- Confabulation (Sec. 2.2, p.6): "GAI systems generate and confidently present erroneous or false content in response to prompts."
- (p.6): also includes outputs "that diverge from the prompts or other input or that contradict previously generated statements".
- (p.6): "Confabulations are a natural result of the way generative models are designed".
- (p.6): risk arises "when users believe false content - often due to the confident nature of the response".
- Footnote 6 (p.4): "hallucination" and "fabrication" are said to "anthropomorphize GAI" - why NIST prefers "confabulation".
- Data Privacy (p.4): "Impacts due to leakage and unauthorized use, disclosure, or de-anonymization of" PII or sensitive data.
- Information Integrity (p.4): content "which may not distinguish fact from opinion or fiction or acknowledge uncertainties".
- Information Security (p.4-5): "Lowered barriers for offensive cyber capabilities"; also "increased attack surface" that may compromise confidentiality or integrity of training data, code, or model weights.
- Each risk is mapped "to relevant Trustworthy AI Characteristics identified in the AI RMF" (p.3).

Safe to teach: NIST names 12 GAI risks; for a policy helpdesk the four that bite are Confabulation (confident wrong answer), Data Privacy (leakage), Information Integrity (fact vs opinion, uncertainty) and Information Security (attack surface).

---

## 4. OWASP Top 10 for LLM Applications 2025

- URLs: https://genai.owasp.org/llm-top-10/ (list); entry pages https://genai.owasp.org/llmrisk/llm01-prompt-injection/ , https://genai.owasp.org/llmrisk/llm022025-sensitive-information-disclosure/ , https://genai.owasp.org/llmrisk/llm082025-vector-and-embedding-weaknesses/ , https://genai.owasp.org/llmrisk/llm092025-misinformation/
- Tier: READ AT SOURCE (live pages on genai.owasp.org, fetched 2026-10-17; quotes taken from page text via a fetch tool, so re-check punctuation before printing)

The 10 (exact ids and names):
- LLM01:2025 Prompt Injection
- LLM02:2025 Sensitive Information Disclosure
- LLM03:2025 Supply Chain
- LLM04:2025 Data and Model Poisoning
- LLM05:2025 Improper Output Handling
- LLM06:2025 Excessive Agency
- LLM07:2025 System Prompt Leakage
- LLM08:2025 Vector and Embedding Weaknesses
- LLM09:2025 Misinformation
- LLM10:2025 Unbounded Consumption

Quotes:
- LLM01 (Description): "A Prompt Injection Vulnerability occurs when user prompts alter the LLM's behavior or output in unintended ways."
- LLM01: "Indirect prompt injections occur when an LLM accepts input from external sources, such as websites or files."
- LLM01 on RAG: research shows RAG and fine-tuning "do not fully mitigate prompt injection vulnerabilities."
- LLM02 (Description): "Sensitive information can affect both the LLM and its application context."
- LLM02 (Prevention, Enforce Strict Access Controls): "Limit access to sensitive data based on the principle of least privilege."
- LLM08 (Description): "Weaknesses in how vectors and embeddings are generated, stored, or retrieved can be exploited".
- LLM08 (Risk: Unauthorized Access and Data Leakage): "Inadequate or misaligned access controls can lead to unauthorized access to embeddings containing sensitive information."
- LLM08 (Cross-Context Information Leaks): multi-tenant shared vector DB creates "a risk of context leakage between users or queries."
- LLM08 (Scenario #2): "A permission-aware vector database should be implemented to restrict access".
- LLM08 (Prevention): "Implement fine-grained access controls and permission-aware vector and embedding stores."
- LLM08 (Prevention): "strict logical and access partitioning of datasets in the vector database".
- LLM09 (Description): "Misinformation occurs when LLMs produce false or misleading information that appears credible."
- LLM09: "Overreliance occurs when users place excessive trust in LLM-generated content, failing to verify its accuracy."
- LLM09 (Prevention): "Use Retrieval-Augmented Generation to enhance the reliability of model outputs"; and "Implement human oversight and fact-checking processes, especially for critical or sensitive information."

Safe to teach: for a policy RAG bot, LLM01 (poisoned policy docs = indirect injection), LLM02 and LLM08 (retrieve only what the asker may see - OWASP's own words "permission-aware vector and embedding stores") and LLM09 (RAG plus human hand-off) are the core four.

---

## 6. Brynjolfsson, Li & Raymond - Generative AI at Work

- QJE: Quarterly Journal of Economics 140(2), 889-942, published online 2025-02-04, DOI https://doi.org/10.1093/qje/qjae044 (article page https://academic.oup.com/qje/article/140/2/889/7990658)
- NBER: https://www.nber.org/papers/w31161 (PDF read: "April 2023, revised November 2023")
- Tier: NBER w31161 READ AT SOURCE (full PDF). QJE abstract READ from the publisher-deposited abstract in Crossref metadata (api.crossref.org/works/10.1093/qje/qjae044); the OUP page itself did not render its text to the fetch tool, so the QJE body text was NOT read.

NBER w31161 (Nov 2023) quotes:
- Abstract (p.2 of PDF): "data from 5,179 customer support agents."
- Abstract: productivity "as measured by issues resolved per hour, by 14% on average, including a 34% improvement for novice and low-skilled workers but with minimal impact on experienced and highly skilled workers."
- Conclusion (Sec. 7, p.27): "our results do not capture the potential longer-term impacts of generative AI on skill demand, job design, wages, or customer demand."
- Conclusion (p.27-28): "the effects we find may not generalize across all firms and production processes"; setting has "a relatively stable product and a set of technical support questions."
- Conclusion (p.27): top performers "see relatively few improvements" and under the firm's relative-bonus pay "may even see a reduction in their pay."

QJE 2025 published abstract quotes (numbers differ from NBER - cite the version you use):
- "data from 5,172 customer-support agents."
- productivity "as measured by issues resolved per hour, by 15% on average, with substantial heterogeneity across workers."
- "Less experienced and lower-skilled workers improve both the speed and quality of their output, while the most experienced and highest-skilled workers see small gains in speed and small declines in quality."
- "the gains from AI adoption are largest for moderately rare problems".
- The QJE abstract gives no single percentage for novices; the 34% figure is the NBER Nov 2023 version only.

### 6b. Qualifier - Humlum & Vestergaard, "Large Language Models, Small Labor Market Effects" (NBER w33777)

- NBER page: https://www.nber.org/papers/w33777 - abstract READ AT SOURCE (2026-10-17). NOTE: the NBER page now carries a revised title, "Still Waters, Rapid Currents: Early Labor Market Transformation under Generative AI" (citation date 2025/05/12 in page metadata).
- Original-title version: BFI Working Paper 2025-56, May 9 2025, https://bfi.uchicago.edu/wp-content/uploads/2025/04/BFI_WP_2025-56-3.pdf - abstract READ AT SOURCE.

BFI WP 2025-56 (May 9 2025) abstract quotes:
- Sample: "11 exposed occupations (25,000 workers, 7,000 workplaces), linked to matched employer-employee data in Denmark."
- "we estimate precise zeros: AI chatbots have had no significant impact on earnings or recorded hours in any occupation, with confidence intervals ruling out effects larger than 1%."
- "Modest productivity gains (average time savings of 3%), combined with weak wage pass-through, help explain these limited labor market effects."

Current NBER w33777 abstract quotes (revised):
- "we estimate precise null effects on earnings and recorded hours at both the worker and workplace levels, ruling out effects larger than 2% two years after the launch of ChatGPT."
- "workers report productivity benefits" and "What moves is the structure of work" (task reorganisation, new AI-oversight tasks).
- Reported only (not read at source): an April 2025 draft said "average time savings of 2.8%" (per https://marginalrevolution.com/marginalrevolution/2025/04/large-language-models-small-labor-market-effects.html).

### 6c. Deflection rate for internal IT/HR helpdesk chatbots

- Searched 2026-10-17 for peer-reviewed or independent field evidence. Found NONE. Every hit was vendor marketing, vendor-hosted customer stories or unsourced statistics roundups (e.g. Oracle customer page https://www.oracle.com/customers/oracle-it/ reports 10% to 25% deflection - self-reported; roundups attribute 38.4% or 40-60% to ServiceNow/Gartner/HDI with no traceable study).
- Several vendor/blog pages themselves warn deflection overstates success (users time out or give up), e.g. https://blog.mavenoid.com/deflection-vs-resolution-why-chatbots-struggle-in-tech-support/amp/ (reported, not used as evidence).
- Verdict: no credible public deflection benchmark. Teach "deflection rate" as a contested, easily gamed metric; measure resolution plus "did the same person open a ticket within N days".

Safe to teach: in one contact-centre field study, AI help raised resolutions per hour 14% (NBER) / 15% (QJE), with big gains for novices and little or slightly negative for top performers; a large Danish study finds about 3% time savings and no measurable earnings or hours effect - so expect task-level gains, not proven bottom-line ones.

---

## 5. IMDA / AI Verify Foundation - Model AI Governance Framework for Generative AI (released 30 May 2024)

- Landing page: https://aiverifyfoundation.sg/resources/mgf-gen-ai/
- PDF read: https://aiverifyfoundation.sg/wp-content/uploads/2026/06/Model-AI-Governance-Framework-for-Generative-AI-19-June-2024.pdf (the file currently linked from the landing page is dated "19 June 2024" in its filename; the original May 2024 PDF URL now returns "Page not found"). Release date 30 May 2024 confirmed via IMDA factsheet (reported): https://imda.gov.sg/resources/press-releases-factsheets-and-speeches/factsheets/2024/gen-ai-and-digital-foss-ai-governance-playbook
- Tier: READ AT SOURCE (the 19 June 2024 file; assume content matches the 30 May release but flag the filename date if citing exact wording)

Nine dimensions, exact names (Contents p.2; Executive Summary p.3-4):
1. Accountability
2. Data
3. Trusted Development and Deployment
4. Incident Reporting
5. Testing and Assurance
6. Security
7. Content Provenance
8. Safety and Alignment Research & Development (R&D) (contents: "Safety and Alignment R&D")
9. AI for Public Good

Quotes:
- (p.3): "nine dimensions which the Framework proposes to be looked at in totality, to foster a trusted ecosystem."
- Incident Reporting (p.4): "no software we use today is completely foolproof. The same applies to AI."
- Incident Reporting (p.4): "Establishing structures and processes to enable incident monitoring and reporting is therefore key."
- Incident Reporting section (p.17): "Defining 'severe AI incidents' or setting the materiality threshold for formal reporting is therefore key."
- Vulnerability reporting (p.17): AI developers can allow "reporting channels for uncovered safety vulnerabilities"; product owners typically get "90 days, based on industry practice" to patch.
- Testing and Assurance (p.4): "third-party testing and assurance plays a complementary role."
- Evaluation (p.14): two approaches, benchmarking and red teaming; they "still fall far short in terms of providing a robust assessment of model performance and safety".
- Content Provenance (p.4): "Transparency about where and how content is generated enables end-users to determine how to consume online content in an informed manner."
- Content Provenance (p.4, p.23-24): governments look to "digital watermarking and cryptographic provenance"; "These technologies need to be used in the right context."
- RAG mention (Trusted Development and Deployment, p.13): "Techniques like Retrieval-Augmented Generation (RAG) and few-shot learning are also commonly used to reduce hallucinations and improve accuracy."
- Disclosure (p.4, p.13): "food label"-type transparency and disclosure.

Safe to teach: Singapore's GenAI framework has 9 dimensions; for an internal helpdesk the relevant ones are Accountability, Trusted Development and Deployment (it names RAG), Incident Reporting (set a severity threshold and a reporting channel), Testing and Assurance, Security and Content Provenance (show where an answer came from).

