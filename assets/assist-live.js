/* assist-live.js - the go/no-go bench for learn-ship-internal-ai-assistant-with-phoebe
 *
 * Tidewell Freight is CONSTRUCTED. Its policy clauses, golden questions, ticket log and the
 * pre-written answers are invented (see assist-data.js, built by materials/build_assist_data.py).
 *
 * COMPUTED LIVE, every click:
 *   BM25 retrieval over every clause in the store (Robertson and Zaragoza 2009, eq. 3.15 with the
 *   eq. 3.3 IDF): score = sum over distinct query terms of
 *     tf / (k1 * ((1 - b) + b * dl / avdl) + tf) * log((N - n + 0.5) / (n + 0.5))
 *   with k1 = 1.2, b = 0.75. Tokens: lower case, split on anything not a letter or digit, a short
 *   stopword list, a trailing "s" dropped from words longer than 3 letters (not "ss"). No stemming.
 *   Then, per rung: the permission filter (the asker's group must be allowed to read the clause),
 *   the current-version filter (the index's superseded flag), top-k, and abstain-and-hand-off when
 *   the top score is under the threshold. Scores: top-k hit rate and MRR against the golden set,
 *   leaks, stale citations, confident wrong answers by risk tier, right hand-offs, cost per answer.
 * PRE-WRITTEN (a browser cannot run a language model): the answer text for each clause.
 * ASSUMPTION: token counts (words x 1.3) and the price ranges per million tokens.
 * TIDEWELL'S POLICY CHOICE, not a standard: the go/no-go thresholds by risk tier.
 *
 * materials/assist_reference.py is an independent Python reference; materials/compare-ladder.py
 * checks that it and this file print the same canon over the whole ladder.
 */
(function (root) {
  "use strict";

  var STOP = ("a an the and or of to in on for is are be been by with at as it its this that from i my me we our you your " +
    "do does did can could how what when where which who whom will would should shall may must much many get got " +
    "if not no any into than then there their they them was were has have had about so am also just only").split(" ");
  var STOPSET = {};
  STOP.forEach(function (w) { STOPSET[w] = 1; });

  function tokenize(text) {
    var raw = String(text).toLowerCase().split(/[^a-z0-9]+/);
    var out = [];
    for (var i = 0; i < raw.length; i++) {
      var t = raw[i];
      if (!t || STOPSET[t]) continue;
      if (t.length > 3 && t.charAt(t.length - 1) === "s" && t.charAt(t.length - 2) !== "s") t = t.slice(0, -1);
      out.push(t);
    }
    return out;
  }

  function words(text) { return String(text).split(/\s+/).filter(function (w) { return w.length > 0; }).length; }

  /* ---------- the index: every clause, every version ---------- */
  function buildIndex(D) {
    var docs = [], df = {}, total = 0;
    D.clauses.forEach(function (c) {
      var toks = tokenize(c.title + " " + c.text), tf = {};
      toks.forEach(function (t) { tf[t] = (tf[t] || 0) + 1; });
      Object.keys(tf).forEach(function (t) { df[t] = (df[t] || 0) + 1; });
      docs.push({ tf: tf, dl: toks.length });
      total += toks.length;
    });
    return { docs: docs, df: df, N: docs.length, avdl: total / docs.length };
  }

  function idf(ix, t) {
    var n = ix.df[t] || 0;
    return Math.log((ix.N - n + 0.5) / (n + 0.5));
  }

  function bm25(ix, qtoks, i, k1, b) {
    var d = ix.docs[i], s = 0, seen = {};
    for (var j = 0; j < qtoks.length; j++) {
      var t = qtoks[j];
      if (seen[t]) continue;
      seen[t] = 1;
      var tf = d.tf[t] || 0;
      if (!tf) continue;
      s += tf / (k1 * ((1 - b) + b * d.dl / ix.avdl) + tf) * idf(ix, t);
    }
    return s;
  }

  function canRead(D, asker, clause) { return D.settings.access[clause.access].indexOf(asker) >= 0; }

  /* The index's own superseded flag. The break button drops it for one document version, the way a
     re-imported PDF loses its metadata; the version register (clause.superseded) keeps the truth. */
  function indexSuperseded(D, c, broken) {
    if (broken && c.doc === D.settings.breakDoc && c.version === D.settings.breakVersion) return false;
    return c.superseded;
  }

  /* ---------- one question through one rung ---------- */
  function ask(D, ix, g, rung, opt) {
    var S = D.settings, k = opt.k, tau = opt.tau, broken = !!opt.broken;
    var q = tokenize(g.q), cands = [];
    for (var i = 0; i < D.clauses.length; i++) {
      var c = D.clauses[i];
      if (rung.perm && !opt.skipPermission && !canRead(D, g.asker, c)) continue;
      if (rung.version && indexSuperseded(D, c, broken)) continue;
      var s = bm25(ix, q, i, S.bm25.k1, S.bm25.b);
      if (s > 0) cands.push({ i: i, s: s });
    }
    cands.sort(function (x, y) { return y.s - x.s || x.i - y.i; });
    var top = cands.slice(0, k);
    var permittedGold = g.gold.filter(function (key) {
      var cur = D.clauses.filter(function (c) { return c.key === key && !c.superseded; })[0];
      return cur && canRead(D, g.asker, cur);
    });
    var answerable = permittedGold.length > 0;
    var rank = 0;
    for (var r = 0; r < top.length; r++) {
      var cr = D.clauses[top[r].i];
      if (permittedGold.indexOf(cr.key) >= 0 && !cr.superseded) { rank = r + 1; break; }
    }
    var leak = top.some(function (x) { return !canRead(D, g.asker, D.clauses[x.i]); });
    var topScore = top.length ? top[0].s : 0;
    var answered = top.length > 0 && !(rung.abstain && topScore < tau);
    var res = { id: g.id, tier: g.tier, kind: g.kind, answerable: answerable, top: top, topScore: topScore,
      rank: rank, leak: leak, answered: answered, cited: null };
    if (answered) {
      var cit = D.clauses[top[0].i];
      var keyOk = permittedGold.indexOf(cit.key) >= 0, readable = canRead(D, g.asker, cit);
      res.cited = top[0].i;
      res.staleTruth = cit.superseded;
      res.stalePipe = indexSuperseded(D, cit, broken);
      res.leakedAnswer = !readable;
      res.correct = keyOk && readable && !cit.superseded;
      res.correctPipe = keyOk && readable && !res.stalePipe;
    }
    res.thumb = answered ? g.thumbsAnswer : g.thumbsHandoff;
    if (answered) {
      var w = words(g.q);
      top.forEach(function (x) { w += words(D.clauses[x.i].text); });
      res.tokensIn = S.cost.systemTokens + Math.ceil(w * S.cost.tokensPerWord);
    }
    return res;
  }

  /* ---------- one rung over the whole golden set ---------- */
  function runRung(D, ix, rung, opt) {
    var S = D.settings, rows = D.golden.map(function (g) { return ask(D, ix, g, rung, opt); });
    var m = { n: rows.length, nAnswerable: 0, hits: 0, rrSum: 0, leaks: 0, leakedAnswers: 0, answered: 0,
      correct: 0, correctPipe: 0, staleTruth: 0, stalePipe: 0, handoffs: 0, handoffRight: 0, missed: 0,
      thumbsUp: 0, tierN: { high: 0, medium: 0, low: 0 }, tierWrong: { high: 0, medium: 0, low: 0 },
      tierWrongPipe: { high: 0, medium: 0, low: 0 }, tokensIn: 0 };
    rows.forEach(function (r) {
      m.tierN[r.tier] += 1;
      if (r.answerable) { m.nAnswerable += 1; if (r.rank) { m.hits += 1; m.rrSum += 1 / r.rank; } }
      if (r.leak) m.leaks += 1;
      if (r.thumb) m.thumbsUp += 1;
      if (r.answered) {
        m.answered += 1;
        m.tokensIn += r.tokensIn;
        if (r.leakedAnswer) m.leakedAnswers += 1;
        if (r.correct) m.correct += 1; else m.tierWrong[r.tier] += 1;
        if (r.correctPipe) m.correctPipe += 1; else m.tierWrongPipe[r.tier] += 1;
        if (r.staleTruth) m.staleTruth += 1;
        if (r.stalePipe) m.stalePipe += 1;
      } else {
        m.handoffs += 1;
        if (r.answerable) m.missed += 1; else m.handoffRight += 1;
      }
    });
    var nUn = m.n - m.nAnswerable;
    m.hitRate = m.hits / m.nAnswerable;
    m.mrr = m.rrSum / m.nAnswerable;
    m.coverage = m.correct / m.nAnswerable;
    m.coveragePipe = m.correctPipe / m.nAnswerable;
    m.handoffRightRate = m.handoffRight / nUn;
    m.thumbsRate = m.thumbsUp / m.n;
    m.wrongRate = {}; m.wrongRatePipe = {};
    ["high", "medium", "low"].forEach(function (t) {
      m.wrongRate[t] = m.tierWrong[t] / m.tierN[t];
      m.wrongRatePipe[t] = m.tierWrongPipe[t] / m.tierN[t];
    });
    m.cost = cost(D, m);
    return { rows: rows, m: m, verdict: verdict(D, m, false), verdictTruth: verdict(D, m, true),
      thumbs: m.thumbsRate >= S.thumbsGate };
  }

  /* Tidewell's go/no-go policy. pipeline = what the assistant's own checks can see (the index's
     version flags); truth = the version register. They differ only when the index metadata lies. */
  function verdict(D, m, truth) {
    var G = D.settings.gate, fails = [];
    if (m.leaks > G.maxLeaks) fails.push(m.leaks + (m.leaks === 1 ? " question" : " questions") + " retrieved a clause the asker may not read");
    var st = truth ? m.staleTruth : m.stalePipe;
    if (st > G.maxStale) fails.push(st + (st === 1 ? " answer cites" : " answers cite") + " a superseded version");
    ["high", "medium", "low"].forEach(function (t) {
      var w = truth ? m.wrongRate[t] : m.wrongRatePipe[t];
      if (w > G.maxWrongRate[t]) fails.push(t + "-risk confident wrong answers " + pct(w) + ", limit " + pct(G.maxWrongRate[t]));
    });
    var cov = truth ? m.coverage : m.coveragePipe;
    if (cov < G.minCoverage) fails.push("answers " + pct(cov) + " of answerable questions correctly, needs " + pct(G.minCoverage));
    if (m.handoffRightRate < G.minHandoffRight) fails.push("hands off " + pct(m.handoffRightRate) + " of questions it should not answer, needs " + pct(G.minHandoffRight));
    return { go: fails.length === 0, fails: fails };
  }

  /* ASSUMPTION: token counts and price ranges. Hand-offs skip generation but open a ticket. */
  function cost(D, m) {
    var C = D.settings.cost;
    var outT = C.outputTokens * m.answered;
    var lo = (m.tokensIn * C.inPerM[0] + outT * C.outPerM[0]) / 1e6;
    var hi = (m.tokensIn * C.inPerM[1] + outT * C.outPerM[1]) / 1e6;
    var perLo = m.answered ? lo / m.answered : 0, perHi = m.answered ? hi / m.answered : 0;
    var ansShare = m.answered / m.n, hoShare = m.handoffs / m.n;
    var ticket = C.ticketMinutes / 60 * C.ticketSgdPerHour;
    var q = C.questionsPerMonth;
    return { perAnswerUsd: [perLo, perHi], avgTokensIn: m.answered ? m.tokensIn / m.answered : 0,
      monthModelSgd: [q * ansShare * perLo * C.usdToSgd, q * ansShare * perHi * C.usdToSgd],
      monthTicketsSgd: q * hoShare * ticket, monthAllTicketsSgd: q * ticket, ticketSgd: ticket };
  }

  /* ---------- the ticket log ---------- */
  function ticketSummary(D) {
    var T = D.topics, n = D.tickets.length, byTeam = {}, byRes = {}, byTopic = {}, minutes = {}, total = 0;
    D.tickets.forEach(function (t) {
      var tp = T[t[0]];
      byTeam[tp[1]] = (byTeam[tp[1]] || 0) + 1;
      byRes[tp[2]] = (byRes[tp[2]] || 0) + 1;
      byTopic[tp[0]] = (byTopic[tp[0]] || 0) + 1;
      minutes[tp[2]] = (minutes[tp[2]] || 0) + t[2];
      total += t[2];
    });
    var goldTopics = {};
    D.golden.forEach(function (g) { if (g.kind === "answerable") goldTopics[g.topic] = 1; });
    var covered = 0;
    D.tickets.forEach(function (t) { var tp = T[t[0]]; if (tp[2] === "policy" && goldTopics[tp[0]]) covered += 1; });
    return { n: n, byTeam: byTeam, byRes: byRes, byTopic: byTopic, minutes: minutes, totalMinutes: total,
      policyShare: (byRes.policy || 0) / n, goldCoversPolicy: covered / (byRes.policy || 1) };
  }

  /* ---------- the whole ladder, for the canon ---------- */
  function ladder(D, opt) {
    opt = opt || {};
    var ix = buildIndex(D), S = D.settings, o = { k: opt.k || S.k, tau: opt.tau === undefined ? S.abstainBelow : opt.tau };
    var out = { index: { N: ix.N, avdl: ix.avdl, vocab: Object.keys(ix.df).length }, rungs: {}, broken: {} };
    S.rungs.forEach(function (r) {
      out.rungs[r.id] = summarise(runRung(D, ix, r, { k: o.k, tau: o.tau, broken: false, skipPermission: opt.skipPermission }));
      out.broken[r.id] = summarise(runRung(D, ix, r, { k: o.k, tau: o.tau, broken: true, skipPermission: opt.skipPermission }));
    });
    out.tickets = ticketSummary(D);
    return out;
  }
  function summarise(R) {
    var m = R.m;
    return { hitRate: m.hitRate, mrr: m.mrr, leaks: m.leaks, leakedAnswers: m.leakedAnswers, answered: m.answered,
      correct: m.correct, coverage: m.coverage, staleTruth: m.staleTruth, stalePipe: m.stalePipe,
      handoffs: m.handoffs, handoffRight: m.handoffRight, missed: m.missed, handoffRightRate: m.handoffRightRate,
      wrongRate: m.wrongRate, wrongRatePipe: m.wrongRatePipe, thumbsRate: m.thumbsRate,
      go: R.verdict.go, goTruth: R.verdictTruth.go, thumbsGo: R.thumbs,
      perAnswerUsd: m.cost.perAnswerUsd, avgTokensIn: m.cost.avgTokensIn, monthModelSgd: m.cost.monthModelSgd,
      monthTicketsSgd: m.cost.monthTicketsSgd, monthAllTicketsSgd: m.cost.monthAllTicketsSgd };
  }

  /* ---------- self-test: properties the bench must hold, and a planted fault it must catch ---------- */
  function properties(L) {
    return [
      ["the permission filter removes every leak", L.rungs.r1.leaks > 0 && L.rungs.r2.leaks === 0],
      ["the current-version filter removes every stale citation", L.rungs.r2.staleTruth > 0 && L.rungs.r3.staleTruth === 0],
      ["the full ladder ends in GO and the bare one in NO-GO", L.rungs.r4.go && !L.rungs.r1.go],
      ["the break button produces a GO the register contradicts", L.broken.r4.go && !L.broken.r4.goTruth],
      ["grading by thumbs-up passes the unsafe rung", L.rungs.r1.thumbsGo && !L.rungs.r1.go]
    ];
  }
  function selfTest(D) {
    var ok = properties(ladder(D)), held = ok.filter(function (p) { return p[1]; }).length;
    var planted = properties(ladder(D, { skipPermission: true }));
    var caught = !planted[0][1];
    return { held: held, total: ok.length, failed: ok.filter(function (p) { return !p[1]; }).map(function (p) { return p[0]; }),
      plantedCaught: caught, pass: held === ok.length && caught };
  }

  /* =================================================================== */
  /* UI                                                                   */
  /* =================================================================== */
  function esc(x) {
    return String(x).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; });
  }
  function pct(x) { return (x * 100).toFixed(1) + "%"; }
  function fmt(n) { return Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","); }
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html !== undefined) e.innerHTML = html; return e; }
  function kind(k) { return '<span class="tw-kind is-' + k + '">' + k + "</span>"; }
  function money(x, dp) { return "$" + x.toFixed(dp); }
  function sgd(x) { return "SGD " + fmt(x); }

  function accessMix(D) {
    var cur = D.clauses.filter(function (c) { return !c.superseded; }), n = {};
    cur.forEach(function (c) { n[c.access] = (n[c.access] || 0) + 1; });
    return (n.all || 0) + " are readable by all staff and " + (cur.length - (n.all || 0)) + " are restricted: " +
      (n.managers || 0) + " managers, " + (n.hr || 0) + " HR only, " + (n.finance || 0) + " finance only, " + (n.it || 0) + " IT only";
  }

  var D, IX, ui = {}, state = { rung: "r4", broken: false, thumbs: false, tau: null, k: null, qi: 0 };

  function metric(label, value, unit, k) {
    return '<div class="tw-metric"><span class="tw-mlabel">' + esc(label) + '</span><span class="tw-mvalue">' + value +
      '</span><span class="tw-munit">' + esc(unit) + "</span>" + kind(k) + "</div>";
  }

  function render() {
    var rung = D.settings.rungs.filter(function (r) { return r.id === state.rung; })[0];
    var R = runRung(D, IX, rung, { k: state.k, tau: state.tau, broken: state.broken });
    var m = R.m, c = m.cost;
    Object.keys(ui.rbtn).forEach(function (id) { ui.rbtn[id].classList.toggle("is-on", id === state.rung); });
    ui.thumbBtn.classList.toggle("is-on", state.thumbs);
    ui.breakBtn.classList.toggle("is-on", state.broken);
    ui.breakBtn.textContent = state.broken ? "Restore the version flag" : "Break it: index the superseded expenses policy as current";
    ui.tauOut.textContent = state.tau.toFixed(1);

    var v = R.verdict, vt = R.verdictTruth, html;
    if (state.thumbs) {
      var go = R.thumbs;
      html = '<div class="tw-verdict ' + (go && !vt.go ? "is-bad" : go ? "is-good" : "is-ok") + '"><strong>Graded by thumbs-up: ' + (go ? "GO" : "NO-GO") +
        "</strong> · " + pct(m.thumbsRate) + " of questions got a thumbs-up, the bar is " + pct(D.settings.thumbsGate) + "." +
        (go && !vt.go ? " This is a GO on an assistant the go/no-go policy rejects: " + esc(vt.fails.join("; ")) + ". Staff thumb up answers that sound sure, including stale and leaked ones, and thumb down hand-offs." :
          !go && vt.go ? " The thumbs grade fails the assistant the policy passes: hand-offs read as unhelpful, so the safest rung scores lowest." : "") + "</div>";
    } else if (v.go && !vt.go) {
      html = '<div class="tw-verdict is-bad"><strong>Go/no-go: GO, and it is false.</strong> Every check the pipeline can see passes. The version register says otherwise: ' +
        esc(vt.fails.join("; ")) + ". The index lost the superseded flag on " + esc(D.settings.breakDoc) + " " + esc(D.settings.breakVersion) +
        ", so the citation check, which reads that flag, waved the old clause through.</div>";
    } else if (v.go) {
      html = '<div class="tw-verdict is-good"><strong>Go/no-go: GO.</strong> No leaks, no stale citations, every risk tier under its limit, enough coverage and enough right hand-offs.</div>';
    } else {
      html = '<div class="tw-verdict is-bad"><strong>Go/no-go: NO-GO.</strong> ' + esc(v.fails.join("; ")) + ".</div>";
    }
    ui.verdict.innerHTML = html;

    ui.metrics.innerHTML =
      metric("Top-" + state.k + " hit rate", pct(m.hitRate), m.hits + " of " + m.nAnswerable + " answerable questions find a current gold clause", "measured") +
      metric("MRR", m.mrr.toFixed(3), "mean of 1 / rank of the first current gold clause", "measured") +
      metric("Leaks", String(m.leaks), "questions whose retrieved set holds a clause the asker may not read; " + m.leakedAnswers + " answered from it", "measured") +
      metric("Stale citations", String(m.staleTruth), "answers citing a superseded version (register)" + (state.broken ? "; the pipeline sees " + m.stalePipe : ""), "measured") +
      metric("Correct answers", pct(m.coverage), m.correct + " of " + m.nAnswerable + " answerable questions, cited clause right and current", "measured") +
      metric("Right hand-offs", pct(m.handoffRightRate), m.handoffRight + " of " + (m.n - m.nAnswerable) + " questions it should not answer", "measured") +
      metric("Confident wrong", pct(m.wrongRate.high) + " · " + pct(m.wrongRate.medium) + " · " + pct(m.wrongRate.low), "high · medium · low risk tier, share of each tier", "measured") +
      metric("Thumbs-up rate", pct(m.thumbsRate), "constructed satisfaction signal", "constructed") +
      metric("Model cost per answer", money(c.perAnswerUsd[0], 5) + " to " + money(c.perAnswerUsd[1], 4), "USD, " + fmt(c.avgTokensIn) + " input tokens on average", "assumption") +
      metric("A month, " + fmt(D.settings.cost.questionsPerMonth) + " questions", "SGD " + c.monthModelSgd[0].toFixed(2) + " to " + c.monthModelSgd[1].toFixed(2), "model cost, if the live mix matches the golden set; hand-off tickets add " + sgd(c.monthTicketsSgd) + "; all " + fmt(D.settings.cost.questionsPerMonth) + " as tickets would be " + sgd(c.monthAllTicketsSgd), "assumption");

    renderQuestion(R);
  }

  function renderQuestion(R) {
    var g = D.golden[state.qi], r = R.rows[state.qi];
    var html = '<p class="tw-q"><strong>' + esc(g.id) + "</strong> · asked by <strong>" + esc(g.asker) + "</strong> · " + esc(g.tier) + " risk · " + esc(g.kind) +
      "<br>" + esc(g.q) + "</p>";
    if (!r.top.length) html += '<p class="tw-none">Nothing in the readable, current store shares a word with the question.</p>';
    html += '<ol class="tw-hits">' + r.top.map(function (x, i) {
      var c = D.clauses[x.i], tags = [];
      if (!canRead(D, g.asker, c)) tags.push('<span class="tw-tag is-bad">' + esc(c.access) + " only</span>");
      if (c.superseded) tags.push('<span class="tw-tag is-bad">superseded ' + esc(c.retiredOn) + "</span>");
      if (g.gold.indexOf(c.key) >= 0 && !c.superseded) tags.push('<span class="tw-tag is-good">gold</span>');
      return '<li><span class="tw-hscore">' + x.s.toFixed(2) + '</span><span class="tw-hid">' + esc(c.id) + "</span> " + esc(c.title) + " " + tags.join(" ") + "</li>";
    }).join("") + "</ol>";
    if (r.answered) {
      var c = D.clauses[r.cited];
      html += '<div class="tw-answer"><span class="tw-alabel">Pre-written answer, constructed</span>' + esc(c.answer) +
        ' <span class="tw-cite">[' + esc(c.id) + "]</span></div>";
      html += '<p class="tw-check">' + (r.correct ? "✓ right clause, current version, readable by the asker" :
        r.leakedAnswer ? "✗ leaked: the asker may not read " + esc(c.id) :
          r.staleTruth ? "✗ stale: " + esc(c.id) + " was superseded on " + esc(c.retiredOn) + (r.stalePipe ? "" : ", and the index does not know") :
            "✗ confident and wrong: no clause answers this for this asker") + "</p>";
    } else {
      html += '<div class="tw-answer is-handoff"><span class="tw-alabel">Hand-off</span>Top score ' + r.topScore.toFixed(2) + " is under " + state.tau.toFixed(1) +
        ". The assistant says it cannot answer from policy and opens a ticket with the question attached.</div>" +
        '<p class="tw-check">' + (r.answerable ? "◐ safe but missed: a readable clause did answer this" : "✓ right: nothing this asker may read answers it") + "</p>";
    }
    ui.qbody.innerHTML = html;
  }

  function init() {
    var host = document.getElementById("tw-bench");
    if (!host || !root.ASSIST_DATA) return;
    D = root.ASSIST_DATA; IX = buildIndex(D);
    state.tau = D.settings.abstainBelow; state.k = D.settings.k;

    var T = ticketSummary(D);
    var p0 = el("div", "tw-panel");
    p0.appendChild(el("h4", null, "The ticket log · one quarter at Tidewell (constructed)"));
    p0.appendChild(el("p", "tw-intro", fmt(T.n) + " tickets: " + fmt(T.byTeam.HR) + " HR, " + fmt(T.byTeam.IT) + " IT, " + fmt(T.byTeam.Finance) + " finance. " +
      fmt(T.byRes.policy) + " (" + pct(T.policyShare) + ") were answered by pointing at a policy clause, " + fmt(T.byRes.action) + " needed a person to do something, " +
      fmt(T.byRes["no-policy"]) + " had no written answer anywhere. They took " + fmt(T.totalMinutes) + " minutes of helpdesk time: " + fmt(T.minutes.policy) + " on policy lookups, " +
      fmt(T.minutes.action) + " on actions, " + fmt(T.minutes["no-policy"]) + " on questions nobody had written down. Biggest topics: " +
      Object.keys(T.byTopic).sort(function (x, y) { return T.byTopic[y] - T.byTopic[x] || (x < y ? -1 : 1); }).slice(0, 6).map(function (k) { return k + " " + T.byTopic[k]; }).join(", ") +
      ". The golden set below covers the topics of " + pct(T.goldCoversPolicy) + " of the policy-answerable tickets."));
    host.appendChild(p0);

    var p1 = el("div", "tw-panel");
    p1.appendChild(el("h4", null, "The go/no-go bench · " + D.clauses.length + " clauses, " + D.golden.length + " golden questions"));
    p1.appendChild(el("p", "tw-intro", "Retrieval, filtering and every score are computed live in your browser over the constructed Tidewell store (" +
      D.clauses.filter(function (c) { return !c.superseded; }).length + " current clauses, " + D.clauses.filter(function (c) { return c.superseded; }).length +
      " superseded versions still in it; of the current ones " + accessMix(D) + "). The answers are pre-written, because a browser cannot run a language model: each clause carries one constructed answer, and the assistant gives the answer of the clause it ranks first."));
    var rr = el("div", "tw-row"); rr.appendChild(el("span", "tw-rlabel", "Rung"));
    ui.rbtn = {};
    D.settings.rungs.forEach(function (r) {
      var b = el("button", "tw-chip", esc(r.label)); b.type = "button";
      b.addEventListener("click", function () { state.rung = r.id; render(); });
      ui.rbtn[r.id] = b; rr.appendChild(b);
    });
    p1.appendChild(rr);
    var lr = el("div", "tw-row"); lr.appendChild(el("span", "tw-rlabel", "Grade"));
    ui.thumbBtn = el("button", "tw-chip is-anti", "Grade by thumbs-up instead"); ui.thumbBtn.type = "button";
    ui.thumbBtn.addEventListener("click", function () { state.thumbs = !state.thumbs; render(); });
    lr.appendChild(ui.thumbBtn);
    p1.appendChild(lr);
    var tr = el("div", "tw-row"); tr.appendChild(el("span", "tw-rlabel", "Abstain below"));
    var rng = el("input"); rng.type = "range"; rng.min = "0"; rng.max = "12"; rng.step = "0.5"; rng.value = String(state.tau); rng.className = "tw-range";
    rng.setAttribute("aria-label", "Abstain threshold on the top BM25 score");
    rng.addEventListener("input", function () { state.tau = parseFloat(rng.value); render(); });
    ui.tauOut = el("span", "tw-tau"); tr.appendChild(rng); tr.appendChild(ui.tauOut);
    tr.appendChild(el("span", "tw-knote", "used on rung 4 only · default " + D.settings.abstainBelow.toFixed(1)));
    p1.appendChild(tr);
    ui.breakBtn = el("button", "tw-break"); ui.breakBtn.type = "button";
    ui.breakBtn.addEventListener("click", function () { state.broken = !state.broken; render(); });
    p1.appendChild(ui.breakBtn);
    ui.verdict = el("div"); p1.appendChild(ui.verdict);
    ui.metrics = el("div", "tw-metrics"); p1.appendChild(ui.metrics);
    var st = selfTest(D);
    p1.appendChild(el("p", "tw-hint", "Self-test on load: " + st.held + " of " + st.total + " properties hold" + (st.failed.length ? " (failing: " + esc(st.failed.join("; ")) + ")" : "") +
      "; a planted fault (the permission filter switched off) " + (st.plantedCaught ? "was caught." : "was NOT caught, so do not trust this bench.") +
      " Index: " + IX.N + " clause versions, average length " + IX.avdl.toFixed(2) + " tokens, " + Object.keys(IX.df).length + " distinct terms. BM25 with k1 = " + D.settings.bm25.k1 + " and b = " + D.settings.bm25.b + ", top-" + D.settings.k + ". Go/no-go thresholds are Tidewell's own policy choice, not a standard. Token counts (words x " +
      D.settings.cost.tokensPerWord + ") and prices (USD " + D.settings.cost.inPerM[0].toFixed(2) + " to " + D.settings.cost.inPerM[1].toFixed(2) + " per million input tokens, " +
      D.settings.cost.outPerM[0].toFixed(2) + " to " + D.settings.cost.outPerM[1].toFixed(2) + " per million output) are assumptions, not a price list. A hand-off ticket is assumed at " +
      D.settings.cost.ticketMinutes + " minutes of helpdesk time at SGD " + D.settings.cost.ticketSgdPerHour + " an hour."));
    host.appendChild(p1);

    var p2 = el("div", "tw-panel");
    p2.appendChild(el("h4", null, "One question, all the way through"));
    var qr = el("div", "tw-row"); qr.appendChild(el("span", "tw-rlabel", "Question"));
    var sel = el("select", "tw-select"); sel.setAttribute("aria-label", "Pick a golden question");
    D.golden.forEach(function (g, i) { var o = el("option", null, esc(g.id + " · " + g.asker + " · " + g.q)); o.value = String(i); sel.appendChild(o); });
    sel.addEventListener("change", function () { state.qi = parseInt(sel.value, 10); render(); });
    qr.appendChild(sel); p2.appendChild(qr);
    ui.qbody = el("div", "tw-qbody"); p2.appendChild(ui.qbody);
    host.appendChild(p2);

    render();
    root.ASSIST_LIVE = {
      setRung: function (id) { state.rung = id; render(); },
      setBroken: function (b) { state.broken = !!b; render(); },
      setThumbs: function (b) { state.thumbs = !!b; render(); },
      setTau: function (t) { state.tau = t; rng.value = String(t); render(); },
      setQuestion: function (i) { state.qi = i; sel.value = String(i); render(); },
      current: function () {
        var rung = D.settings.rungs.filter(function (r) { return r.id === state.rung; })[0];
        return summarise(runRung(D, IX, rung, { k: state.k, tau: state.tau, broken: state.broken }));
      },
      selfTest: function () { return selfTest(D); }
    };
  }

  var api = { tokenize: tokenize, buildIndex: buildIndex, bm25: bm25, runRung: runRung, ladder: ladder,
    selfTest: selfTest, ticketSummary: ticketSummary, verdict: verdict };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  if (typeof document !== "undefined") {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
    else init();
  }
})(typeof window !== "undefined" ? window : this);
