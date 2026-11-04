"""Rebuild source-only A5 annotation artifacts; verify existing bytes by default.
No expression or contribution table is read. --write-missing writes absent files only.
"""
from pathlib import Path
import argparse, collections, csv, hashlib, io, json


def build(base):
    load = lambda name: json.loads((base / name).read_text(encoding="utf-8"))
    selected = load("A5_SELECTED_ANNOTATIONS_V2.json")
    annotations = load("A5_GO_ANNOTATIONS_V2.json")["results"]
    roots = {r["id"]: r["name"] for r in load("A5_GO_ROLE_ROOTS_V2.json")["results"]}
    terms = {r["id"]: r for name in ("A5_GO_ANCESTRY_V2.json", "A5_GO_ANCESTRY_ADDITIONS_V2.json") for r in load(name)["results"]}
    entries = {r["primaryAccession"]: r for r in selected["entries"]}
    owner = {}
    for gene in selected["genes"]:
        for accession in gene["accessions"].split(";"):
            assert accession not in owner
            owner[accession] = gene["original_gene"]
    experimental = set("EXP IDA IPI IMP IGI IEP HTP HDA HMP HGI HEP".split())
    phylogenetic = set("IBA IBD IKR IRD".split())
    computational = set("ISS ISO ISA ISM IGC RCA".split())
    by_gene = collections.defaultdict(list)
    evidence_rows = []
    for item in annotations:
        accession = item["geneProductId"].split(":", 1)[1]
        gene = owner[accession]
        term = terms[item["goId"]]
        qualifier, code = item["qualifier"], item["goEvidence"]
        negated = "NOT" in qualifier.split("|")
        positive = not negated and code != "ND" and not term.get("isObsolete", False)
        family = "experimental" if code in experimental else "phylogenetic" if code in phylogenetic else "sequence_or_computational" if code in computational else "electronic" if code == "IEA" else "author_statement" if code in {"TAS", "NAS"} else "curator_inference" if code == "IC" else "no_data" if code == "ND" else "other"
        related = sorted(set(roots) & ({item["goId"]} | set(term.get("ancestors", []))))
        relation = "upstream_or_within_association" if "acts_upstream" in qualifier else "contribution" if "contributes_to" in qualifier else "annotated_activity_or_involvement" if qualifier in {"enables", "involved_in"} else "location_or_complex_context"
        row = {"original_gene": gene, "accession": accession, "entry_status": entries[accession]["entryType"], "annotation_id": item["id"], "GO_ID": item["goId"], "GO_name": term["name"], "GO_aspect": item["goAspect"], "qualifier": qualifier, "GO_evidence": code, "ECO_code": item["evidenceCode"], "evidence_family": family, "reference": item["reference"], "assigned_by": item["assignedBy"], "annotation_date": item["date"], "taxon_id": item["taxonId"], "relation_scope": relation, "negated": str(negated).lower(), "positive_annotation_eligible": str(positive).lower(), "draft_role_roots": ";".join(related), "draft_role_names": ";".join(roots[r] for r in related), "with_from": json.dumps(item.get("withFrom"), ensure_ascii=False, separators=(",", ":")), "extensions": json.dumps(item.get("extensions"), ensure_ascii=False, separators=(",", ":"))}
        evidence_rows.append(row)
        by_gene[gene].append(row)
    def role_ids(rows):
        return sorted({role for row in rows for role in row["draft_role_roots"].split(";") if role})
    member_rows = []
    for gene in selected["genes"]:
        rows = by_gene[gene["original_gene"]]
        positive = [r for r in rows if r["positive_annotation_eligible"] == "true"]
        all_roles = role_ids(positive)
        direct = role_ids([r for r in positive if r["relation_scope"] == "annotated_activity_or_involvement"])
        upstream = role_ids([r for r in positive if r["relation_scope"] == "upstream_or_within_association"])
        functions = []
        for accession in gene["accessions"].split(";"):
            for comment in entries[accession].get("comments", []):
                if comment.get("commentType") == "FUNCTION":
                    for text in comment.get("texts", []):
                        functions.append({"accession": accession, "text": text.get("value", ""), "evidences": text.get("evidences", [])})
        member_rows.append({**gene, "GO_annotation_records": len(rows), "negated_records": sum(r["negated"] == "true" for r in rows), "ND_records": sum(r["GO_evidence"] == "ND" for r in rows), "draft_positive_role_roots": ";".join(all_roles), "draft_positive_role_names": ";".join(roots[r] for r in all_roles), "experimental_role_roots": ";".join(role_ids([r for r in positive if r["evidence_family"] == "experimental"])), "activity_or_involvement_roots": ";".join(direct), "upstream_only_roots": ";".join(sorted(set(upstream) - set(direct))), "classification_limit": "No positive annotation in these 14 draft categories" if not all_roles else "Annotation associations only; categories overlap; source effects not used", "UniProt_function_text_and_evidence": json.dumps(functions, ensure_ascii=False, separators=(",", ":"))})
    old_path = base.parents[1] / "2026-11-03-full-priority-screening/prerequisites/A5_ROLE_TABLE_V1.tsv"
    with old_path.open(encoding="utf-8", newline="") as stream:
        old = {r["gene"]: r for r in csv.DictReader(stream, delimiter="\t")}
    assert set(old) == {r["original_gene"] for r in member_rows}
    crosswalk = []
    for member in member_rows:
        gene = member["original_gene"]
        original = old[gene]
        relevant = [{k: r[k] for k in ("GO_ID", "qualifier", "GO_evidence", "ECO_code", "reference", "relation_scope", "negated")} for r in by_gene[gene] if "GO:0010468" in r["draft_role_roots"].split(";")]
        crosswalk.append({"original_gene": gene, "in_99": original["in_99"], "in_57": original["in_57"], "in_53": original["in_53"], "v1_roles": original["roles"], "v1_annotation_summary": original["annotation_summary"], "v1_source_url": original["source_url"], "v1_role_overlap_note": original["role_overlap_note"], "v2_GO_association_roots": member["draft_positive_role_roots"], "v2_GO_association_names": member["draft_positive_role_names"], "GO_gene_expression_relation_evidence": json.dumps(relevant, ensure_ascii=False, separators=(",", ":")), "interpretation": "Original source-nominated roles and GO ancestry associations are different definitions; neither replaces the other"})
    assert len(member_rows) == len(crosswalk) == 99
    assert len(evidence_rows) == len({r["annotation_id"] for r in evidence_rows}) == 4344
    assert all(r["positive_annotation_eligible"] == "false" for r in evidence_rows if r["negated"] == "true" or r["GO_evidence"] == "ND")
    outputs = {}
    for name, rows in [("A5_GO_EVIDENCE_ROWS_V2.tsv", evidence_rows), ("A5_MEMBER_ANNOTATION_V2.tsv", member_rows), ("A5_ROLE_SCOPE_CROSSWALK_V2.tsv", crosswalk)]:
        stream = io.StringIO(newline="")
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
        outputs[name] = stream.getvalue().encode()
    return outputs, old_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-missing", action="store_true")
    args = parser.parse_args()
    base = Path(__file__).resolve().parent
    outputs, old_path = build(base)
    for name, content in outputs.items():
        target = base / name
        if target.exists():
            if target.read_bytes() != content:
                raise SystemExit("Existing bytes differ; preserve them and investigate: " + name)
        elif args.write_missing:
            target.write_bytes(content)
        else:
            raise SystemExit("Missing output: " + name)
    print("Verified 99 original members, 4,344 annotation IDs and original-role crosswalk; existing bytes preserved.")


if __name__ == "__main__":
    main()
