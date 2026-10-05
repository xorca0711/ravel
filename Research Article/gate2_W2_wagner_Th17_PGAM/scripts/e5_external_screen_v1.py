#!/usr/bin/env python
"""Wp-E5: is there an independent Th17 dataset that could test the glucose result?

Wp-R1's strongest reproduced finding - the pro-regulatory arm falls at low
glucose, in 4 of 4 animal-paired comparisons - rests on two mice. The branch card
asks whether the direction generalises, and requires that the inclusion rule be
written before any candidate is opened. This entrypoint is that screen, and
nothing more: it searches GEO, scores candidates against the frozen rule using
deposited metadata only, and reports which pass. **No expression value is read
and no score is computed.** A screen returning nothing admissible is a result,
not a failure.

FROZEN INCLUSION RULE, all six required
  R1  CD4 T cells polarised toward Th17, or a Th17-containing CD4 population, in
      mouse or human.
  R2  An explicit nutrient or metabolic-environment contrast *within* the
      experiment - glucose concentration, glutamine, amino-acid or serum
      restriction, or a defined medium swap. A drug-only perturbation does not
      satisfy this: the Wp-R1 finding is about nutrient level, and an inhibitor
      contrast is a different comparison (that is Wp-R3's design).
  R3  Deposited expression values - a supplementary matrix or a SRA-linked
      processed file - not a figure or a summary table only.
  R4  At least two biological units per arm, where a unit is an animal, a donor
      or a verified independent culture. Technical replicates, lanes and
      repeated wells from one mixture do not count.
  R5  The nutrient contrast is crossed with, or held constant across, the Th17
      polarisation condition, so a glucose effect is not confounded with a
      change of differentiation cytokines.
  R6  Independent of this paper's own deposits: not GSE289733, GSE290297,
      GSE138266, and not an author-overlapping reanalysis of them.

A candidate failing any rule is recorded with the rule it failed. Rules R3 to R5
usually cannot be settled from a GEO summary alone; those candidates are
reported as `needs_record_inspection` rather than as passes, because a screen
that guesses is worse than one that defers.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
OWN_DEPOSITS = {"GSE289733", "GSE290297", "GSE138266"}

QUERIES = [
    '("Th17"[All Fields]) AND ("glucose"[All Fields]) AND "gse"[Filter]',
    '("Th17"[All Fields]) AND ("nutrient"[All Fields]) AND "gse"[Filter]',
    '("Th17"[All Fields]) AND ("glutamine"[All Fields]) AND "gse"[Filter]',
    '("T helper 17"[All Fields]) AND ("metabolic"[All Fields]) AND "gse"[Filter]',
    '("Th17"[All Fields]) AND ("amino acid"[All Fields]) AND "gse"[Filter]',
    '("CD4"[All Fields]) AND ("Th17"[All Fields]) AND ("restriction"[All Fields]) AND "gse"[Filter]',
]
NUTRIENT_TERMS = ["glucose", "nutrient", "glutamine", "amino acid", "serum starv",
                  "serum-free", "galactose", "2-deoxy", "medium", "media",
                  "starvation", "restriction", "fatty acid", "lipid", "hypoxia"]
TH17_TERMS = ["th17", "t helper 17", "il-17", "il17", "rorgt", "rorγt"]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "python-urllib"})
    with urllib.request.urlopen(req, timeout=60) as fh:
        return fh.read().decode("utf-8", "replace")


def esearch(term: str, email: str | None) -> list[str]:
    params = {"db": "gds", "term": term, "retmax": "60", "retmode": "json"}
    if email:
        params["email"] = email
    data = json.loads(fetch(f"{EUTILS}/esearch.fcgi?" + urllib.parse.urlencode(params)))
    return data.get("esearchresult", {}).get("idlist", [])


def esummary(uids: list[str], email: str | None) -> list[dict]:
    if not uids:
        return []
    params = {"db": "gds", "id": ",".join(uids), "retmode": "json"}
    if email:
        params["email"] = email
    data = json.loads(fetch(f"{EUTILS}/esummary.fcgi?" + urllib.parse.urlencode(params)))
    res = data.get("result", {})
    return [res[u] for u in res.get("uids", [])]


def screen(rec: dict) -> tuple[str, list[str], dict]:
    acc = rec.get("accession", "")
    text = " ".join(str(rec.get(k, "")) for k in ("title", "summary", "taxon", "gdstype")).lower()
    n_samples = int(rec.get("n_samples") or 0)
    failed = []
    if not any(t in text for t in TH17_TERMS):
        failed.append("R1_no_th17_evidence_in_record")
    nut = [t for t in NUTRIENT_TERMS if t in text]
    if not nut:
        failed.append("R2_no_nutrient_contrast_in_record")
    if acc in OWN_DEPOSITS:
        failed.append("R6_own_deposit")
    if n_samples < 4:
        failed.append("R4_fewer_than_four_samples")
    status = "failed" if failed else "needs_record_inspection"
    evidence = {"accession": acc, "title": rec.get("title", ""),
                "taxon": rec.get("taxon", ""), "gdstype": rec.get("gdstype", ""),
                "n_samples": n_samples, "pdat": rec.get("pdat", ""),
                "nutrient_terms_found": nut}
    return status, failed, evidence


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    ap.add_argument("--contact-email", default="")
    args = ap.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    email = args.contact_email or None

    rows, seen, query_log = [], {}, []
    for term in QUERIES:
        try:
            uids = esearch(term, email)
            time.sleep(0.4)
            recs = esummary(uids, email)
            time.sleep(0.4)
            query_log.append({"query": term, "n_uids": len(uids), "n_records": len(recs),
                              "status": "ok"})
        except Exception as exc:                       # noqa: BLE001 - network screen
            query_log.append({"query": term, "n_uids": 0, "n_records": 0,
                              "status": f"error: {type(exc).__name__}"})
            continue
        for rec in recs:
            acc = rec.get("accession", "")
            if not acc or acc in seen:
                continue
            seen[acc] = True
            status, failed, evidence = screen(rec)
            rows.append({**evidence, "screen_status": status,
                         "rules_failed": ";".join(failed), "found_by_query": term})

    import csv
    fields = ["accession", "title", "taxon", "gdstype", "n_samples", "pdat",
              "nutrient_terms_found", "screen_status", "rules_failed", "found_by_query"]
    with open(out / "candidates.csv", "w", newline="\n", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({**r, "nutrient_terms_found": ";".join(r["nutrient_terms_found"])})
    with open(out / "query_log.csv", "w", newline="\n", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["query", "n_uids", "n_records", "status"])
        w.writeheader()
        w.writerows(query_log)

    shortlist = [r for r in rows if r["screen_status"] == "needs_record_inspection"]
    results = {
        "schema": "wp_e5_external_screen/v1",
        "searched": "NCBI GEO DataSets (db=gds) via E-utilities",
        "queries": [q["query"] for q in QUERIES] if isinstance(QUERIES[0], dict) else QUERIES,
        "query_log": query_log,
        "n_unique_series_seen": len(rows),
        "n_failed_on_record": sum(1 for r in rows if r["screen_status"] == "failed"),
        "n_needing_record_inspection": len(shortlist),
        "shortlist": [{k: r[k] for k in ("accession", "title", "taxon", "n_samples",
                                         "nutrient_terms_found")} for r in shortlist],
        "frozen_inclusion_rule": {
            "R1": "CD4 T cells polarised toward Th17, or a Th17-containing CD4 population, mouse or human",
            "R2": "an explicit nutrient or metabolic-environment contrast within the experiment; a drug-only "
                  "perturbation does not satisfy this",
            "R3": "deposited expression values, not a figure or summary table only",
            "R4": "at least two biological units per arm, where a unit is an animal, a donor or a verified "
                  "independent culture",
            "R5": "the nutrient contrast crossed with or held constant across the Th17 polarisation condition",
            "R6": "independent of this paper's own deposits",
        },
        "screen_semantics": (
            "Only R1, R2, R6 and a weak form of R4 are decidable from a GEO summary record. Candidates surviving "
            "those are reported as needs_record_inspection, never as passes: R3, R5 and the biological-unit form of "
            "R4 require the sample records and the supplementary file list, which this screen does not open."),
        "interpretation_limit": (
            "A metadata screen over GEO DataSets summaries. It cannot establish that an admissible dataset exists - "
            "only that candidates do or do not survive the record-level rules - and a GEO summary that omits a "
            "nutrient contrast does not prove the experiment lacked one. Nothing here analyses expression, and no "
            "candidate may be used for the Wp-R1 comparison until its records are inspected and the result of that "
            "inspection is recorded under this contract's successor."),
    }
    (out / "results.json").write_text(json.dumps(results, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
