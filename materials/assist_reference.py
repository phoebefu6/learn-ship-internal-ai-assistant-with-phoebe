#!/usr/bin/env python3
"""Independent Python reference for the go/no-go bench (assets/assist-live.js).

Written separately from the JavaScript, from the same written rules, so that agreement means
something. Reads materials/assist-data.json and prints the canon as JSON over the whole ladder:
four rungs, each also with the break button pressed, plus the ticket-log summary.

BM25 (Robertson and Zaragoza 2009, eq. 3.15 with the eq. 3.3 IDF), k1 = 1.2, b = 0.75:
    score(d, q) = sum over distinct query terms t of
        tf(t, d) / (k1 * ((1 - b) + b * dl / avdl) + tf(t, d)) * log((N - n_t + 0.5) / (n_t + 0.5))
Tidewell Freight and every row here are CONSTRUCTED.

Usage: python3 materials/assist_reference.py > /tmp/py.json
"""
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STOP = set(("a an the and or of to in on for is are be been by with at as it its this that from i my me we our you your "
            "do does did can could how what when where which who whom will would should shall may must much many get got "
            "if not no any into than then there their they them was were has have had about so am also just only").split())
TIERS = ("high", "medium", "low")


def tokenize(text):
    out = []
    for t in re.split(r"[^a-z0-9]+", text.lower()):
        if not t or t in STOP:
            continue
        if len(t) > 3 and t.endswith("s") and not t.endswith("ss"):
            t = t[:-1]
        out.append(t)
    return out


def nwords(text):
    return len(text.split())


class Bench:
    def __init__(self, data):
        self.D = data
        self.S = data["settings"]
        self.C = data["clauses"]
        self.docs, self.df, total = [], {}, 0
        for c in self.C:
            toks = tokenize(c["title"] + " " + c["text"])
            tf = {}
            for t in toks:
                tf[t] = tf.get(t, 0) + 1
            for t in tf:
                self.df[t] = self.df.get(t, 0) + 1
            self.docs.append((tf, len(toks)))
            total += len(toks)
        self.N = len(self.docs)
        self.avdl = total / self.N

    def readable(self, asker, c):
        return asker in self.S["access"][c["access"]]

    def idx_superseded(self, c, broken):
        if broken and c["doc"] == self.S["breakDoc"] and c["version"] == self.S["breakVersion"]:
            return False
        return c["superseded"]

    def score(self, qtoks, i):
        k1, b = self.S["bm25"]["k1"], self.S["bm25"]["b"]
        tf, dl = self.docs[i]
        s, seen = 0.0, set()
        for t in qtoks:
            if t in seen:
                continue
            seen.add(t)
            f = tf.get(t, 0)
            if not f:
                continue
            n = self.df.get(t, 0)
            s += f / (k1 * ((1 - b) + b * dl / self.avdl) + f) * math.log((self.N - n + 0.5) / (n + 0.5))
        return s

    def ask(self, g, rung, k, tau, broken, skip_perm=False):
        q = tokenize(g["q"])
        cands = []
        for i, c in enumerate(self.C):
            if rung["perm"] and not skip_perm and not self.readable(g["asker"], c):
                continue
            if rung["version"] and self.idx_superseded(c, broken):
                continue
            s = self.score(q, i)
            if s > 0:
                cands.append((s, i))
        cands.sort(key=lambda x: (-x[0], x[1]))
        top = cands[:k]
        gold = []
        for key in g["gold"]:
            cur = [c for c in self.C if c["key"] == key and not c["superseded"]]
            if cur and self.readable(g["asker"], cur[0]):
                gold.append(key)
        rank = 0
        for r, (s, i) in enumerate(top):
            if self.C[i]["key"] in gold and not self.C[i]["superseded"]:
                rank = r + 1
                break
        top_score = top[0][0] if top else 0.0
        answered = bool(top) and not (rung["abstain"] and top_score < tau)
        res = {"tier": g["tier"], "answerable": bool(gold), "rank": rank, "answered": answered,
               "leak": any(not self.readable(g["asker"], self.C[i]) for s, i in top),
               "thumb": g["thumbsAnswer"] if answered else g["thumbsHandoff"]}
        if answered:
            c = self.C[top[0][1]]
            key_ok, rd = c["key"] in gold, self.readable(g["asker"], c)
            res["staleTruth"] = c["superseded"]
            res["stalePipe"] = self.idx_superseded(c, broken)
            res["leakedAnswer"] = not rd
            res["correct"] = key_ok and rd and not c["superseded"]
            res["correctPipe"] = key_ok and rd and not res["stalePipe"]
            w = nwords(g["q"]) + sum(nwords(self.C[i]["text"]) for s, i in top)
            res["tokensIn"] = self.S["cost"]["systemTokens"] + math.ceil(w * self.S["cost"]["tokensPerWord"])
        return res

    def rung(self, rung, broken, skip_perm=False):
        k, tau = self.S["k"], self.S["abstainBelow"]
        rows = [self.ask(g, rung, k, tau, broken, skip_perm) for g in self.D["golden"]]
        n = len(rows)
        na = sum(r["answerable"] for r in rows)
        hits = sum(1 for r in rows if r["answerable"] and r["rank"])
        rr = 0.0
        for r in rows:
            if r["answerable"] and r["rank"]:
                rr += 1 / r["rank"]
        ans = [r for r in rows if r["answered"]]
        ho = [r for r in rows if not r["answered"]]
        tier_n = {t: sum(1 for r in rows if r["tier"] == t) for t in TIERS}
        wrong = {t: sum(1 for r in ans if r["tier"] == t and not r["correct"]) / tier_n[t] for t in TIERS}
        wrong_p = {t: sum(1 for r in ans if r["tier"] == t and not r["correctPipe"]) / tier_n[t] for t in TIERS}
        m = {
            "hitRate": hits / na, "mrr": rr / na,
            "leaks": sum(r["leak"] for r in rows), "leakedAnswers": sum(r["leakedAnswer"] for r in ans),
            "answered": len(ans), "correct": sum(r["correct"] for r in ans),
            "coverage": sum(r["correct"] for r in ans) / na,
            "staleTruth": sum(r["staleTruth"] for r in ans), "stalePipe": sum(r["stalePipe"] for r in ans),
            "handoffs": len(ho), "handoffRight": sum(1 for r in ho if not r["answerable"]),
            "missed": sum(1 for r in ho if r["answerable"]),
            "wrongRate": wrong, "wrongRatePipe": wrong_p,
            "thumbsRate": sum(r["thumb"] for r in rows) / n,
        }
        m["handoffRightRate"] = m["handoffRight"] / (n - na)
        cov_p = sum(r["correctPipe"] for r in ans) / na
        m["go"] = self.gate(m, m["stalePipe"], wrong_p, cov_p)
        m["goTruth"] = self.gate(m, m["staleTruth"], wrong, m["coverage"])
        m["thumbsGo"] = m["thumbsRate"] >= self.S["thumbsGate"]
        C = self.S["cost"]
        tin = sum(r["tokensIn"] for r in ans)
        tout = C["outputTokens"] * len(ans)
        lo = (tin * C["inPerM"][0] + tout * C["outPerM"][0]) / 1e6
        hi = (tin * C["inPerM"][1] + tout * C["outPerM"][1]) / 1e6
        per_lo = lo / len(ans) if ans else 0
        per_hi = hi / len(ans) if ans else 0
        q = C["questionsPerMonth"]
        a_sh, h_sh = len(ans) / n, len(ho) / n
        m["perAnswerUsd"] = [per_lo, per_hi]
        m["avgTokensIn"] = tin / len(ans) if ans else 0
        m["monthModelSgd"] = [q * a_sh * per_lo * C["usdToSgd"], q * a_sh * per_hi * C["usdToSgd"]]
        m["monthTicketsSgd"] = q * h_sh * (C["ticketMinutes"] / 60 * C["ticketSgdPerHour"])
        m["monthAllTicketsSgd"] = q * (C["ticketMinutes"] / 60 * C["ticketSgdPerHour"])
        return m

    def gate(self, m, stale, wrong, cov):
        G = self.S["gate"]
        return (m["leaks"] <= G["maxLeaks"] and stale <= G["maxStale"]
                and all(wrong[t] <= G["maxWrongRate"][t] for t in TIERS)
                and cov >= G["minCoverage"] and m["handoffRightRate"] >= G["minHandoffRight"])

    def tickets(self):
        T, tk = self.D["topics"], self.D["tickets"]
        by_team, by_res, by_topic, minutes, total = {}, {}, {}, {}, 0
        for t in tk:
            tp = T[t[0]]
            by_team[tp[1]] = by_team.get(tp[1], 0) + 1
            by_res[tp[2]] = by_res.get(tp[2], 0) + 1
            by_topic[tp[0]] = by_topic.get(tp[0], 0) + 1
            minutes[tp[2]] = minutes.get(tp[2], 0) + t[2]
            total += t[2]
        gold_topics = {g["topic"] for g in self.D["golden"] if g["kind"] == "answerable"}
        covered = sum(1 for t in tk if T[t[0]][2] == "policy" and T[t[0]][0] in gold_topics)
        return {"n": len(tk), "byTeam": by_team, "byRes": by_res, "byTopic": by_topic, "minutes": minutes,
                "totalMinutes": total, "policyShare": by_res.get("policy", 0) / len(tk),
                "goldCoversPolicy": covered / (by_res.get("policy", 0) or 1)}

    def ladder(self):
        out = {"index": {"N": self.N, "avdl": self.avdl, "vocab": len(self.df)}, "rungs": {}, "broken": {}}
        for r in self.S["rungs"]:
            out["rungs"][r["id"]] = self.rung(r, False)
            out["broken"][r["id"]] = self.rung(r, True)
        out["tickets"] = self.tickets()
        return out


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "assist-data.json")
    data = json.load(open(path, encoding="utf-8"))
    print(json.dumps(Bench(data).ladder(), indent=1))
