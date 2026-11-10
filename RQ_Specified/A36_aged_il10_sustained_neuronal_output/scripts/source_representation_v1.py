"""A36 exposed source qualification and finite-pool representation; no inference."""
import argparse
import csv
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import platform
import xml.etree.ElementTree as ET
import zipfile

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import openpyxl


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def write_tsv(path, rows):
    with path.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter='\t')
        w.writeheader()
        w.writerows(rows)


def raw_xlsx(path):
    ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    with zipfile.ZipFile(path) as z:
        strings = []
        if 'xl/sharedStrings.xml' in z.namelist():
            strings = [''.join(n.itertext()) for n in ET.fromstring(z.read('xl/sharedStrings.xml'))]
        sheets = []
        for k in range(1, 5):
            values = {}
            for c in ET.fromstring(z.read(f'xl/worksheets/sheet{k}.xml')).findall('.//s:c', ns):
                v = c.find('s:v', ns)
                if c.get('t') == 'inlineStr':
                    values[c.get('r')] = ''.join(c.find('s:is', ns).itertext())
                elif v is not None:
                    values[c.get('r')] = strings[int(v.text)] if c.get('t') == 's' else v.text
            sheets.append(values)
        return sheets


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args(); out = args.output
    raw = Path('raw_data/a36/source_v1')
    inputs = [raw / n for n in ['paper.xml', 'S1.xlsx', 'S3.xlsx', 'S4.xlsx', 'code_v1.zip', 'supplement.pdf', 'zenodo.json', 'ena.tsv', 'retrievals.json']]
    rec = Path('analysis/research/runs/nn26_rds_metadata_v2/recovery.tsv')
    rec2 = Path('analysis/research/runs/nn26_rds_metadata_review_v1/recovery.tsv')
    inputs += [rec, rec2]
    write_json(out / 'input_manifest.json', [dict(path=p.as_posix(), bytes=p.stat().st_size, sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in inputs])
    with rec.open() as f: rows = list(csv.DictReader(f, delimiter='\t'))
    with rec2.open() as f: repeat = list(csv.DictReader(f, delimiter='\t'))
    assert rows == repeat
    indexed = {(r['condition'], r['celltype']): r for r in rows}
    assert len(indexed) == len(rows) == 96
    conditions = ['Young', 'Control', 'WT5', 'Mut5']
    lineage = ['Astrocytes_qNSCs', 'aNSCs_NPCs', 'Neuroblasts']
    checks = 0
    for cond in sorted({r['condition'] for r in rows}):
        selected = [r for r in rows if r['condition'] == cond]
        total = sum(int(r['cells']) for r in selected)
        assert all(int(r['condition_total']) == total for r in selected)
        for r in selected:
            assert math.isclose(float(r['fraction_of_recovered_condition']), int(r['cells']) / total, abs_tol=1e-14)
            checks += 1
    assert sum(int(r['cells']) for r in rows) == 51176
    result = []
    for cond in conditions:
        denom = sum(int(indexed[(cond, t)]['cells']) for t in lineage)
        for t in sorted({r['celltype'] for r in rows}):
            r = indexed[(cond, t)]; n = int(r['cells']); total = int(r['condition_total'])
            result.append(dict(condition=cond, celltype=t, cells=n, all_recovered=total, fraction_all=n/total,
                               lineage_denominator=denom if t in lineage else '', fraction_lineage=n/denom if t in lineage else ''))
    write_tsv(out / 'representation.tsv', result)
    lookup = {(r['condition'], r['celltype']): r for r in result}
    contrasts = []
    for left, right in [('Mut5', 'WT5'), ('Mut5', 'Control'), ('WT5', 'Control'), ('Young', 'Control')]:
        for t in sorted({r['celltype'] for r in rows}):
            a,b = lookup[(left,t)],lookup[(right,t)]
            difference = a['fraction_all'] - b['fraction_all']
            exact = Fraction(a['cells'], a['all_recovered']) - Fraction(b['cells'], b['all_recovered'])
            assert abs(difference - float(exact)) < 1e-14; checks += 1
            ld = ''
            if t in lineage:
                ld = a['fraction_lineage']-b['fraction_lineage']
                exact2=Fraction(a['cells'],a['lineage_denominator'])-Fraction(b['cells'],b['lineage_denominator'])
                assert abs(ld-float(exact2)) < 1e-14; checks += 1
            contrasts.append(dict(contrast=left+'-'+right, celltype=t, left_cells=a['cells'], right_cells=b['cells'],
                                  difference_fraction_all=difference, difference_fraction_lineage=ld))
    write_tsv(out / 'representation_contrasts.tsv', contrasts)
    workbook = openpyxl.load_workbook(raw/'S3.xlsx', read_only=True, data_only=True)
    xml_sheets = raw_xlsx(raw/'S3.xlsx'); extracted = []; labels = {}; source_checks=0
    for si,sheet in enumerate(list(workbook)[1:],1):
        labels[sheet.title] = set()
        for ri, row in enumerate(sheet.values,1):
            if ri == 1 or not row[0]: continue
            labels[sheet.title].add(row[2])
            for ci,value in enumerate(row[:10],1):
                coordinate = openpyxl.utils.get_column_letter(ci)+str(ri)
                independent=xml_sheets[si].get(coordinate)
                if value is None: assert independent is None
                elif isinstance(value,(int,float)): assert math.isclose(float(independent),value,rel_tol=1e-14,abs_tol=1e-14)
                else: assert str(value)==independent
                source_checks += 1
            extracted.append(dict(sheet=sheet.title,row=ri,GO_ID=row[0],description=row[1],comparison=row[2],
                                  set_size=row[3],enrichment_score=row[4],NES=row[5],pvalue=row[6],p_adjust=row[7],qvalue=row[8],rank=row[9]))
    write_tsv(out/'S3_source_rows.tsv',extracted)
    overlap=dict(comparisons={k:sorted(v) for k,v in labels.items()},
                 direct_D25K_WT_table=False,
                 published_residual_IFN_locators=['astrocytes_qNSCs!A104:J105'],
                 S6='A/B: cell-type age clocks; C-E: whole-niche PCA; F: DG IBA1-associated STAT1 after behavior, not birthdated survival.',
                 source_annotation_limit='Methods explicitly cannot separate astrocytes/qNSCs or aNSCs/NPCs.',
                 added_scope='Broad-bin representation/within-bin RNA decomposition; not a purified-state or new IFN mechanism claim.')
    write_json(out/'source_overlap.json',overlap)
    s1=openpyxl.load_workbook(raw/'S1.xlsx',read_only=True,data_only=True)
    marker_sheet=s1['IL-10_concentration_Exp1']; marker_rows=[]
    wanted={'Gfap','Slc1a3','Sox2','Egfr','Ascl1','Mki67','Top2a','Dcx','Dlx2','Rbfox3','Sox10','Mbp'}
    headers=next(marker_sheet.values)
    for ri,row in enumerate(marker_sheet.values,1):
        if ri>1 and any(str(v) in wanted for v in row):
            marker_rows.append(dict(row=ri,values=list(row)))
    write_json(out/'annotation_source.json',dict(sheet=marker_sheet.title,headers=list(headers),declared_marker_rows=marker_rows,
               rule='Original deposited labels only. Marker values cannot define new states or independent validation.'))
    write_json(out/'feasibility.json',dict(later_output='Not estimable from inspected one-week source snapshots; no eligible later transient D25K/WT/vehicle birthdating cohort located in bounded search.',
               exact_missing=['exposure cessation and later time','later birthdated survival/maturation measurements','eligible biological-unit/comparator linkage'],
               age_modification='Matched young treatment arms absent; young vehicle is reference only.',
               fine_identity='Purified NSC-state claim held; original combined-bin description eligible.',
               other_aliases='WT50/Mut50 expression held; no suffix-based dose assignment.',
               injury='No lesion or repair endpoint measured.',population_inference='No independent mouse replication recoverable from condition pools.'))
    fig,axes=plt.subplots(1,2,figsize=(12,4.8))
    colors=['#809eaa','#b3bd84','#cf987a']
    for ax,denominator,title in zip(axes,['fraction_all','fraction_lineage'],['Among all recovered cells','Among three lineage-associated bins']):
        for j,t in enumerate(lineage):
            ax.bar([i+(j-1)*.24 for i in range(4)],[100*lookup[(c,t)][denominator] for c in conditions],width=.23,label=t,color=colors[j])
        ax.set_xticks(range(4),conditions);ax.set_ylabel('Recovered-cell fraction (%)');ax.set_title(title)
        ax.spines[['right','top']].set_visible(False)
    axes[0].legend(fontsize=8)
    fig.suptitle('A36: observed condition pools; capture fractions are not tissue abundance',fontsize=12)
    fig.text(.5,.01,'Young is age reference only. No cell-resampled uncertainty or inferred mouse replication.',ha='center',fontsize=9)
    fig.tight_layout(rect=(0,.035,1,.96));fig.savefig(out/'representation.png',dpi=180);plt.close(fig)
    write_json(out/'independent_verification.json',dict(status='passed',same_source_not_replication=True,recovery_rows=96,
               recovery_and_fraction_checks=checks,S3_OOXML_scalar_checks=source_checks,retained_total_cells=51176,
               verification='Separate receipt table equality, integer totals, Fraction arithmetic, direct ZIP/OOXML versus openpyxl reading.'))
    write_json(out/'software_versions.json',dict(python=platform.python_version(),openpyxl=openpyxl.__version__,matplotlib=matplotlib.__version__))
    print(json.dumps(dict(status='complete',fraction_checks=checks,S3_source_checks=source_checks)))


if __name__ == '__main__':
    main()
