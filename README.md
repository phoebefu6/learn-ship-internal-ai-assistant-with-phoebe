<!-- learn-with-phoebe hub banner -->
> ### 📚 Part of [**Learn with Phoebe**](https://phoebefu6.github.io/learn-with-phoebe/)
> The shelf of 170 free, hands-on courses on AI, data, and the craft around them. **[Browse every course ↗](https://phoebefu6.github.io/learn-with-phoebe/)**
<!-- /learn-with-phoebe hub banner -->

# Ship It: Internal AI Assistant

Fourteen 45-minute sessions on shipping one internal AI assistant end to end: a policy and ops
helpdesk that answers staff from HR, IT and finance policy, cites the clause it used, and opens a
ticket when it cannot answer. By Phoebe Fu.

- **Leader track (6, no code):** what staff actually ask, buy build or wait, who may see what, what
  it says when it does not know, what it costs to run, and launching then keeping it true.
- **Builder track (8, Python and the browser):** the clause store, chunk index retrieve, golden
  questions from the ticket log, grounded answers with citations, permissions inside retrieval, one
  tool that opens the ticket, versions and superseded policies, and the go/no-go bench.

The bench (builder session 8) runs in the browser: BM25 over 49 constructed policy clause
versions, the permission and current-version filters, abstain-and-hand-off, and a go/no-go board
scored against 54 golden questions. `materials/assist_reference.py` is an independent Python
reference; `materials/compare-ladder.py` checks it against the browser engine by value.

Tidewell Freight is constructed. Its policies, tickets, golden questions, satisfaction signal and
answer text are invented and labelled so on every page. Token counts and prices are assumptions;
the go/no-go thresholds are Tidewell's policy choice, not a standard.
