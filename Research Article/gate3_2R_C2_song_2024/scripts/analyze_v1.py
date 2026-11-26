"""Descriptive recovery of Song source observations and GEO library contrasts."""
import argparse
import csv
import gzip
import hashlib
import json
import math
import re
import statistics as st
import tarfile
from pathlib import Path

import openpyxl

ROOT = Path("raw_data/song_v1")
PANELS = {
    "S1": {3: "1A 1B 1C", 4: "2D 2E 2F 2G 2H 2I 2J 2K 2L",
           7: "1B 1C 1D 1E", 10: "4B 4D 4F 4H"},
    "S2": {11: "5A 5B 5C 5D", 12: "6C 6D 6E 6F 6G", 13: "7A 7B 7C 7D"},
    "S4": {3: "1D 1E 1F 1I", 5: "3F 3G 3H", 12: "6A 6B", 16: "10D 10E"},
    "S5": {5: "3A 3B 3C 3D 3E", 6: "4B 4D 4E 4G 4H 4I 4J 4K 4M 4N 4O",
           15: "9C 9D 9E 9F 9G 9H"},
}
LABEL = re.compile(r"(WT|KO|Ctrl|78c)[ _]*(Ctrl|MCUKD)?[ _]*\d+", re.I)


def write_table(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def panel_data(stage, output):
    observations, summaries = [], []
    for book, requested in PANELS[stage].items():
        sheet = openpyxl.load_workbook(ROOT / f"m{book}.xlsx", data_only=True).active
        headers = {}
        for row in range(1, sheet.max_row + 1):
            label = str(sheet.cell(row, 1).value)
            match = re.fullmatch(r"(?:Extended Data Figure|Fig)\s*(\d+)\s*([A-Z])\s*", label)
            if match:
                headers["".join(match.groups())] = row
        for panel in requested.split():
            header = headers[panel]
            end = min((row for row in headers.values() if row > header), default=sheet.max_row + 1)
            columns = [2]
            second = str(sheet.cell(header + 1, 3).value).strip()
            if second == "8 wks":
                columns = [5]
            elif "myeloid" in second:
                columns = [2, 3]
            elif second.lower().replace(".", "") == "au":
                columns = [3]
            figure = ("Fig " if book <= 6 else "ED ") + panel
            for col in columns:
                endpoint = str(sheet.cell(header + 1, col).value).strip()
                if col == 3 and second.lower().replace(".", "") == "au":
                    endpoint = str(sheet.cell(header + 1, 2).value).strip() + " (control-normalized AU)"
                groups = {}
                for row in range(header + 2, end):
                    label = str(sheet.cell(row, 1).value).strip()
                    match = LABEL.fullmatch(label)
                    if not match:
                        continue
                    group = "_".join(part for part in match.groups() if part)
                    cell = sheet.cell(row, col)
                    value = cell.value
                    if value is not None:
                        assert isinstance(value, (int, float)) and math.isfinite(value), cell.coordinate
                        groups.setdefault(group, []).append(value)
                    observations.append(dict(panel=figure, endpoint=endpoint, workbook=f"m{book}.xlsx",
                                             cell=cell.coordinate, label=label, group=group, value=value))
                contrasts = [("KO_Ctrl", "WT_Ctrl"), ("KO_MCUKD", "WT_MCUKD")] if book == 13 else [
                    ("78c", "Ctrl") if book == 6 else ("KO", "WT")]
                for case, control in contrasts:
                    a, b = groups[case], groups[control]
                    delta = st.mean(a) - st.mean(b)
                    assert math.isclose(delta, math.fsum(a) / len(a) - math.fsum(b) / len(b), abs_tol=1e-9)
                    summaries.append(dict(panel=figure, endpoint=endpoint, contrast=f"{case} - {control}",
                                          n_case=len(a), n_control=len(b), mean_case=st.mean(a),
                                          mean_control=st.mean(b), difference=delta,
                                          loo_min=min([st.mean(a[:i]+a[i+1:])-st.mean(b) for i in range(len(a))]
                                                      + [st.mean(a)-st.mean(b[:i]+b[i+1:]) for i in range(len(b))]),
                                          loo_max=max([st.mean(a[:i]+a[i+1:])-st.mean(b) for i in range(len(a))]
                                                      + [st.mean(a)-st.mean(b[:i]+b[i+1:]) for i in range(len(b))])))
                if book == 13:
                    a, b = summaries[-2:]
                    summaries.append(dict(panel=figure, endpoint=endpoint, contrast="MCUKD minus Ctrl genotype contrast",
                                          n_case="", n_control="", mean_case=b["difference"], mean_control=a["difference"],
                                          difference=b["difference"]-a["difference"],
                                          loo_min=min(b["loo_min"]-a["difference"], b["difference"]-a["loo_max"]),
                                          loo_max=max(b["loo_max"]-a["difference"], b["difference"]-a["loo_min"])))
    write_table(output / "observations.csv", observations)
    write_table(output / "contrasts.csv", summaries)
    if stage == "S1":
        activation_plot(output, observations)


def activation_plot(output, observations):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(14, 7), layout="constrained")
    outer = fig.add_gridspec(1, 2, width_ratios=(1, 2.6))
    for slot, panels, grid in [(0, ["1A", "1B", "1C"], (3, 1)), (1, list("DEFGHIJKL"), (3, 3))]:
        area = fig.add_subfigure(outer[slot])
        area.suptitle(["Cell behavior", "Metabolic measurements"][slot])
        for ax, panel in zip(area.subplots(*grid).flat, panels):
            name = "Fig " + ("2" if slot else "") + panel
            subset = [r for r in observations if r["panel"] == name]
            for i, (group, color) in enumerate([("WT", "#256388"), ("KO", "#a54037")]):
                values = [r["value"] for r in subset if r["group"] == group and r["value"] is not None]
                ax.scatter([i + (k - (len(values)-1)/2)*0.042 for k in range(len(values))], values, color=color, s=19)
                ax.hlines(st.mean(values), i-.2, i+.2, color="black")
            ax.set_xticks([0, 1], ["WT", "Cd38 KO"])
            ax.set_title(name + " · " + subset[0]["endpoint"].replace(" (control-normalized AU)", ""), fontsize=9)
            if slot:
                ax.set_ylabel("Normalized AU")
    fig.savefig(output / "activation.png", dpi=160)


def load_libraries():
    soft = gzip.decompress((ROOT / "soft").read_bytes()).decode()
    return {block.splitlines()[0]: block for block in soft.split("^SAMPLE = ")[1:]}


def rna(stage, output):
    samples, counts = [], {}
    soft = load_libraries()
    with tarfile.open(ROOT / "geo") as archive:
        for member in sorted(archive.getmembers(), key=lambda item: item.name):
            raw = archive.extractfile(member).read()
            gsm, suffix = member.name.split("_", 1)
            context, geno = re.fullmatch(r"(young_homeo|young_ex_vivo|old)_(WT|KO)[12]\.txt.gz", suffix).groups()
            assert f"genotype: {geno}" in soft[gsm]
            assert {"young_homeo": "freshly isolate", "young_ex_vivo": "cytokine stimulation",
                    "old": "freshly isolate"}[context] in soft[gsm]
            entries = [line.split("\t") for line in gzip.decompress(raw).decode().splitlines()]
            assert len({gene for gene, _ in entries}) == len(entries)
            values = {gene: int(count) for gene, count in entries if not gene.startswith("__")}
            assert min(values.values()) >= 0
            counts[gsm] = values
            samples.append(dict(gsm=gsm, group=context, genotype=geno,
                                age_geo="24 months" if context == "old" else "2 months",
                                age_figures="24 months" if context == "old" else "3 months",
                                stimulation="24 h cytokines" if context == "young_ex_vivo" else "fresh",
                                gate="Lin- c-Kit+ Sca-1+", sex="unresolved by sample",
                                donor_pool="unresolved", preparation="QuantSeq 3prime, mm10, HTSeq",
                                file=member.name, sha256=hashlib.sha256(raw).hexdigest(),
                                features=len(values), detected=sum(v > 0 for v in values.values()),
                                total=sum(values.values())))
    assert len(samples) == 12 and set(counts) == set(soft)
    universe = set.intersection(*(set(c) for c in counts.values()))
    assert all(len(universe) == len(c) for c in counts.values())
    write_table(output / "libraries.csv", samples)
    if stage == "S0":
        return
    gsms = list(counts)
    references = {}
    workbook = openpyxl.load_workbook(ROOT / "m2.xlsx", data_only=True, read_only=True)
    for sheet in workbook:
        references[sheet.title] = {r[0]: r[2] for r in sheet.values if isinstance(r[2], (float, int))}
    group_order = [(ctx, geno) for ctx in ("young_homeo", "young_ex_vivo", "old") for geno in ("WT", "KO")]
    indices = [[i for i, s in enumerate(samples) if (s["group"], s["genotype"]) == group] for group in group_order]
    assert all(len(ix) == 2 for ix in indices)
    results = []
    for gene in sorted(universe):
        if sum(counts[gsm][gene] >= 10 for gsm in gsms) < 2:
            continue
        vals = [math.log2(0.5 + counts[s["gsm"]][gene] * 1e6 / s["total"]) for s in samples]
        a, b, c, d, e, f = [[vals[i] for i in ix] for ix in indices]
        fresh, stimulated, old = st.mean(b)-st.mean(a), st.mean(d)-st.mean(c), st.mean(f)-st.mean(e)
        all_pair = [x-y for x in d for y in c]
        results.append(dict(gene=gene, young_stim_KO_WT=stimulated, young_fresh_KO_WT=fresh, old_fresh_KO_WT=old,
                            stim_minus_fresh=stimulated-fresh, old_minus_young_fresh=old-fresh,
                            stim_pair_min=min(all_pair), stim_pair_max=max(all_pair),
                            **dict(zip(gsms, vals)), **{k: v.get(gene) for k, v in references.items()}))
    write_table(output / "expression.csv", results)
    checks = {}
    for tab in references:
        checks[tab] = {}
        for contrast in ("young_stim_KO_WT", "young_fresh_KO_WT", "old_fresh_KO_WT"):
            selected = [r for r in results if r[tab] and r[contrast] and abs(r[tab]) >= 0.5]
            checks[tab][contrast] = [sum(r[tab]*r[contrast] > 0 for r in selected), len(selected)]
    panels = {"cytosolic_ribosomal_symbols": r"^Rp[sl]\d+[a-z]?$",
              "mitochondrially_encoded_symbols": r"^mt-",
              "cell_cycle_marker_adaptation": r"^(Mki67|Pcna|Mcm[2-7]|Top2a|Cdk1|Ccnb[12])$"}
    markers = {}
    for name, pattern in panels.items():
        selected = [r for r in results if re.search(pattern, r["gene"])]
        markers[name] = {"n": len(selected), **{contrast: st.median(r[contrast] for r in selected)
                        for contrast in ("young_stim_KO_WT", "young_fresh_KO_WT", "old_fresh_KO_WT",
                                         "old_minus_young_fresh", "stim_minus_fresh")} if selected else {"n": 0}
    (output / "rna_summary.json").write_text(json.dumps(dict(tested=len(results), sign_matches=checks,
                                                             adapted_panels=markers), indent=2)+"\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["S0", "S1", "S2", "S3", "S4", "S5"])
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if args.stage in ("S0", "S3"):
        rna(args.stage, args.output)
    else:
        panel_data(args.stage, args.output)


if __name__ == "__main__":
    main()
