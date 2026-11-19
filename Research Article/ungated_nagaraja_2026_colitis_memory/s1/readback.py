"""Read the published Fig. 1 measurements on their original assay scales."""
import csv
import math
import re
import sys
from collections import Counter
from io import BytesIO
from pathlib import Path
from statistics import mean, median
from zipfile import ZipFile

import openpyxl

from plot_readback import draw_figure

CACHE = Path("raw_data/nagaraja_s0")
# The source workbook gives protocol days. Withdrawal references come from Fig. 1a.
TIME = {
    "Control": (0, None, None, 3),
    "Acute injury": (10, 1, 8, 2),
    "Chronic injury": (49, 3, 42, 2),
    "Early recovery": (63, 3, 42, 3),
    "50d recovery": (92, 3, 42, 3),
    "79d recovery": (121, 3, 42, 2),
    "102d recovery": (144, 3, 42, 4),
}
STAGES = {"Acute injury":"Colitis_acute", "Chronic injury":"Colitis_chronic",
          "Recovered":"Colitis_recovered"}
STATES = ["stem_prog", "AE_inter", "AE_diff"]


def write(out, name, records):
    with (out/name).open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(records[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in records:
            writer.writerow({k: "NA" if v is None else v for k,v in row.items()})


def sheet_rows(sheet):
    rows = iter(sheet.values)
    fields = next(rows)
    for row in rows:
        if any(x is not None for x in row):
            yield {k: v for k,v in zip(fields,row) if k is not None}


def protein(out):
    book = openpyxl.load_workbook(CACHE/"moesm7.xlsx",read_only=True,data_only=True)
    mice = []
    for row in sheet_rows(book["Fig. 1k,l"]):
        label = row["sample"]
        match = re.fullmatch(r"(.+) replicate (\d+)",label)
        stage, replicate = match.groups()
        protocol_day, cycle, withdrawal, _ = TIME[stage]
        k, n = row["Fos+CD44+"], row["CD44+"]
        assert row["protocol_day"] == protocol_day and isinstance(k,int) and isinstance(n,int)
        assert n > 0 and 0 <= k <= n and abs(k/n-row["Fraction Fos+"]) < 1e-12
        mice.append(dict(stage=stage,mouse_label=label,replicate=int(replicate),protocol_day=protocol_day,
                         withdrawal_cycle=cycle,withdrawal_reference_day=withdrawal,
                         days_after_referenced_withdrawal=protocol_day-withdrawal if withdrawal else None,
                         FOS_CD44_double_positive=k,CD44_positive=n,percent_double_positive=100*k/n))
    book.close()
    assert len({r["mouse_label"] for r in mice})==len(mice)
    mice.sort(key=lambda r:(list(TIME).index(r["stage"]),r["replicate"]))
    write(out,"fos_mice.tsv",mice)
    stages, by_stage = [], {}
    for stage,(day,_,_,n) in TIME.items():
        values = [r["percent_double_positive"] for r in mice if r["stage"] == stage]
        assert len(values) == n
        by_stage[stage] = values
        stages.append(dict(stage=stage,protocol_day=day,n_mice=n,mean_mouse_percent=mean(values),
                           minimum_mouse_percent=min(values),maximum_mouse_percent=max(values)))
    write(out,"fos_stages.tsv",stages)
    recovered, control = by_stage["Early recovery"], by_stage["Control"]
    omitted = [mean(recovered[:i]+recovered[i+1:])-mean(control) for i in range(len(recovered))]
    omitted += [mean(recovered)-mean(control[:i]+control[i+1:]) for i in range(len(control))]
    contrast = dict(control_mice=len(control),early_recovery_mice=len(recovered),control_mean_pct=mean(control),
                    early_recovery_mean_pct=mean(recovered),recovered_minus_control_pp=mean(recovered)-mean(control),
                    min_omit_one_mouse_pp=min(omitted),max_omit_one_mouse_pp=max(omitted))
    write(out,"fos_primary.tsv",[contrast])
    return mice,contrast


def workbook(archive, number):
    name, = [s for s in archive.namelist() if f"SupplementalTable{number}_" in s]
    return openpyxl.load_workbook(BytesIO(archive.read(name)),read_only=True,data_only=True)


def number(value):
    if value in (None, "NA", "NaN"):
        return None
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"Unexpected nonfinite value {value}")
    return result


def motifs(out, archive):
    book = workbook(archive,3)
    result = []
    for row in sheet_rows(book.active):
        if row["bag_leader"] == "Fos":
            result.append(dict(stage=row["sample"],epithelial_state=row["cell_type"],family_leader="Fos",
                               delta=number(row["delta"]),author_p=number(row["pval"]),
                               author_BH_p=number(row["padj"])))
    book.close()
    assert Counter((r["stage"],r["epithelial_state"]) for r in result) == Counter(
        (stage,state) for stage in STAGES.values() for state in STATES)
    assert all(r["delta"] is not None and 0<=r["author_p"]<=1 and 0<=r["author_BH_p"]<=1 for r in result)
    write(out,"fos_motif_by_state.tsv",result)
    return result


def rna_call(lfc, adjusted):
    if adjusted is None:
        return "adjusted_p_unavailable"
    if lfc is None:
        return "fold_change_unavailable"
    if adjusted >= 0.05 or lfc == 0:
        return "threshold_not_met"
    return "up" if lfc > 0 else "down"


def rna(out, archive):
    book = workbook(archive,1)
    results, markers = {}, []
    for sheet,stage in STAGES.items():
        genes = {}
        for r in sheet_rows(book[sheet]):
            gene = r["gene"]
            assert isinstance(gene,str) and gene and gene not in genes and r["timepoint"]==stage
            lfc, p, q = [number(r[key]) for key in ["log2FoldChange","pvalue","padj"]]
            assert (p is None or 0<=p<=1) and (q is None or 0<=q<=1)
            genes[gene] = (lfc,p,q,rna_call(lfc,q))
        results[stage] = genes
        for gene in ("Lgr5","Mki67"):
            lfc,p,q,call = genes.get(gene,(None,None,None,"absent_from_sheet"))
            markers.append(dict(stage=stage,gene=gene,log2FC=lfc,author_p=p,author_padj=q,call=call))
    book.close()
    acute, chronic, _ = STAGES.values()
    injury_sets = [{g for g,v in results[s].items() if v[3]=="up"} for s in (acute,chronic)]
    union = sorted(set.union(*injury_sets))
    assert union
    details,summary = [],[]
    for stage, genes in results.items():
        calls = Counter(v[3] for v in genes.values())
        restricted = Counter()
        fold_changes = []
        for gene in union:
            lfc,p,q,call = genes.get(gene,(None,None,None,"absent_from_sheet"))
            restricted[call] += 1
            if lfc is not None:
                fold_changes.append(lfc)
            details.append(dict(stage=stage,gene=gene,up_in_acute=gene in injury_sets[0],
                                up_in_chronic=gene in injury_sets[1],log2FC=lfc,author_p=p,author_padj=q,call=call))
        summary.append(dict(stage=stage,sheet_genes=len(genes),sheet_finite_padj=sum(v[2] is not None for v in genes.values()),
                            sheet_up=calls["up"],sheet_down=calls["down"],injury_union=len(union),
                            union_present=len(union)-restricted["absent_from_sheet"],
                            union_up=restricted["up"],union_down=restricted["down"],
                            union_threshold_not_met=restricted["threshold_not_met"],
                            union_unavailable_padj=restricted["adjusted_p_unavailable"],
                            union_unavailable_lfc=restricted["fold_change_unavailable"],
                            union_absent=restricted["absent_from_sheet"],
                            union_n_finite_lfc=len(fold_changes),
                            union_median_log2FC=median(fold_changes) if fold_changes else None))
    write(out,"rna_stages.tsv",summary)
    write(out,"rna_injury_union.tsv",details)
    write(out,"rna_fig1f_markers.tsv",markers)
    return summary


if __name__=="__main__":
    destination=Path(sys.argv[1])
    mice,primary=protein(destination)
    with ZipFile(CACHE/"moesm5.zip") as supplements:
        motif_rows=motifs(destination,supplements)
        gene_rows=rna(destination,supplements)
    draw_figure(destination,mice,primary,motif_rows,gene_rows)
