#!/usr/bin/env python3
"""Write window.MINDMAP_DATA into index.html with json.dumps (never an f-string).
Concept labels follow each page's Part headings (agent-brief.md lists the planned ones)."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE)
S = [
    ("What staff ask", "a1-what-staff-actually-ask", "#34D399", ["Three bins of tickets", "A ranking has a winner", "Minutes, not tickets"]),
    ("Buy, build or wait", "a2-buy-build-or-wait", "#FBBF24", ["What you cannot buy", "Build what is yours", "When to wait"]),
    ("Who may see what", "a3-who-may-see-what", "#FBBF24", ["Leaks, counted", "Filter before ranking", "Who sets access"]),
    ("When it doesn't know", "a4-when-it-does-not-know", "#FB923C", ["Confident and wrong", "The hand-off", "Pick a threshold"]),
    ("What it costs", "a5-what-it-costs-to-run", "#FB923C", ["Tokens as a range", "The ticket line", "Cost per right answer"]),
    ("Launch, keep it true", "a6-launch-then-keep-it-true", "#FB923C", ["The go/no-go", "Owners and versions", "Contested evidence"]),
    ("The corpus", "b1-the-corpus-is-the-product", "#34D399", ["A clause, not a document", "Old rules stay", "Access on the clause"]),
    ("Chunk, index, retrieve", "b2-chunk-index-retrieve", "#FBBF24", ["BM25 by hand", "Top-3 retrieval"]),
    ("Golden questions", "b3-golden-questions", "#FBBF24", ["From the ticket log", "Should not answer"]),
    ("Grounded answers", "b4-grounded-answers", "#FB923C", ["Answer from retrieved", "The citation check"]),
    ("Permissions inside", "b5-permissions-inside-retrieval", "#FB923C", ["The filter as code", "Counting leaks"]),
    ("Open the ticket", "b6-open-the-ticket", "#FB923C", ["Abstain threshold", "The ticket payload"]),
    ("Versions", "b7-versions-and-superseded", "#FB923C", ["Register vs index", "The nightly diff"]),
    ("The bench", "b8-the-go-no-go-bench", "#F87171", ["Four rungs", "Thumbs-up trap", "The break button"]),
]
data = {"title": "Internal AI\nAssistant", "centerColor": "#0A5A60", "sessions": [
    {"label": l, "href": "courses/%s.html" % f, "color": c,
     "concepts": [{"label": k, "href": "courses/%s.html" % f} for k in ks]} for l, f, c, ks in S]}
p = os.path.join(REPO, "index.html"); s = open(p, encoding="utf-8").read()
block = "window.MINDMAP_DATA = " + json.dumps(data, indent=2, ensure_ascii=True) + ";"
s2 = re.sub(r"(<script>\n)(?:/\*@@MINDMAP@@\*/|window\.MINDMAP_DATA = .*?;)(\n</script>)", lambda m: m.group(1) + block + m.group(2), s, count=1, flags=re.S)
assert s2 != s or block in s
open(p, "w", encoding="utf-8").write(s2)
print("mindmap:", len(S), "sessions,", sum(len(x[3]) for x in S), "concepts")
