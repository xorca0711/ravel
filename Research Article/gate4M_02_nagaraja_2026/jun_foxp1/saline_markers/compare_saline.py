"""Frozen eight-CpG analysis for execution after Step 1 review."""
from fractions import Fraction
import csv
import gzip
from pathlib import Path
import sys


RUNS = Path("analysis/research/runs")
SPEC = RUNS / "ng26_saline_specimens_v1"
GEOMETRY = RUNS / "ng26_jf_external_qualification_v1/array_dyads.tsv"
MATRIX = Path("raw_data/nagaraja_jf_external/matrix.gz")
STUDIES = ("GSE283386", "GSE316762")


def read(path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write(path, rows):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys(), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def mean_pp(values):
    return 100 * sum(values, start=Fraction()) / len(values)


def sign(v):
    return "increase" if v > 0 else "decrease" if v < 0 else "tie"


def joint(array, native, stable):
    if array == native == "tie":
        return "both tied"
    if array == "tie" or native == "tie":
        return "external tied" if array == "tie" else "Nagaraja tied"
    if array != native:
        return "opposite directions"
    return f"joint {array}, " + ("stable" if stable else "omission-sensitive")


def number(v):
    return format(float(v), ".15g")


def main(out):
    people = read(SPEC / "specimens.tsv")
    native = read(SPEC / "nagaraja_same_strand.tsv")
    probes = {r["probe"]: r for r in read(GEOMETRY)}
    assert len(probes)==8 and len({r["locus"] for r in probes.values()})==5
    sids = {s["gsm"]: s for s in people}
    assert len(sids)==len(people)==12
    values = {(r["probe"],r["gsm"]):r["source_fraction"] for r in native}
    assert len(values)==len(native)==48
    columns = {s["chip_position"]:s["gsm"] for s in people if s["study"]==STUDIES[0]}
    assert len(columns)==6
    with gzip.open(MATRIX,"rt",encoding="utf-8",newline="") as f:
        reader=csv.reader(f)
        header=next(reader)
        assert all(header.count(pos)==1 for pos in columns)
        selected=[(header.index(pos), gsm) for pos,gsm in columns.items()]
        for row in reader:
            probe=row[0]
            if probe in probes:
                for idx,gsm in selected:
                    assert (probe,gsm) not in values
                    values[probe,gsm]=row[idx]
    assert set(values)=={(probe,gsm) for probe in probes for gsm in sids}
    mice, arms, omitted, pairs = [], [], [], []
    for probe,g in sorted(probes.items()):
        key=dict(probe=probe,locus=g["locus"],flank=g["window"],chrom=g["chrom"],
                 plus_C_0=g["plus_C_0"],strand=g["interrogated_strand"],assayed_ref_0=g["interrogated_reference_base_0"])
        effects, robust = {}, {}
        for study in STUDIES:
            by_arm={"control":{}, "DSS":{}}
            for s in people:
                if s["study"]!=study:
                    continue
                raw=values[probe,s["gsm"]]
                v=Fraction(raw)
                assert 0<=v<=1
                by_arm[s["group"]][s["gsm"]]=v
                mice.append(dict(**key,study=study,gsm=s["gsm"],mouse=s["mouse"],arm=s["source_arm"],
                                 deposited_fraction=raw,methylation_percent=number(v*100)))
            controls, exposed=by_arm["control"],by_arm["DSS"]
            assert len(controls)==len(exposed)==3
            full=mean_pp(exposed.values())-mean_pp(controls.values())
            effects[study]=full
            influence=[]
            for arm,entries in by_arm.items():
                for gsm in entries:
                    choices={group:[v for id_,v in group_entries.items() if id_!=gsm]
                             for group,group_entries in by_arm.items()}
                    diff=mean_pp(choices["DSS"])-mean_pp(choices["control"])
                    influence.append(diff)
                    omitted.append(dict(**key,study=study,omitted_gsm=gsm,omitted_arm=arm,
                                        n_DSS=len(choices["DSS"]),n_control=len(choices["control"]),
                                        delta_pp=number(diff),delta_exact_rational_pp=str(diff),direction=sign(diff)))
            stable=full!=0 and all(sign(i)==sign(full) for i in influence)
            robust[study]=stable
            arms.append(dict(**key,study=study,n_control=len(controls),n_DSS=len(exposed),
                             control_mean_percent=number(mean_pp(controls.values())),
                             control_min_percent=number(100*min(controls.values())),control_max_percent=number(100*max(controls.values())),
                             DSS_mean_percent=number(mean_pp(exposed.values())),
                             DSS_min_percent=number(100*min(exposed.values())),DSS_max_percent=number(100*max(exposed.values())),
                             delta_pp=number(full),delta_exact_rational_pp=str(full),direction=sign(full),
                             omission_min_pp=number(min(influence)),omission_max_pp=number(max(influence)),
                             omissions_tied=sum(x==0 for x in influence),omissions_reversing=sum(x*full<0 for x in influence),
                             nonzero_sign_preserved=stable))
        a,b=[effects[k] for k in STUDIES]
        pairs.append(dict(**key,external_delta_pp=number(a),Nagaraja_delta_pp=number(b),
                          external_minus_Nagaraja_pp=number(a-b),difference_exact_rational_pp=str(a-b),
                          external_direction=sign(a),Nagaraja_direction=sign(b),
                          external_nonzero_sign_preserved=robust[STUDIES[0]],Nagaraja_nonzero_sign_preserved=robust[STUDIES[1]],
                          directional_screen=joint(sign(a),sign(b),all(robust.values()))))
    assert (len(mice),len(arms),len(omitted),len(pairs))==(96,16,96,8)
    for name,table in [("mouse_values.tsv",mice),("study_differences.tsv",arms),
                       ("mouse_omissions.tsv",omitted),("site_comparison.tsv",pairs)]:
        write(out/name,table)


if __name__=="__main__":
    main(Path(sys.argv[1]))
