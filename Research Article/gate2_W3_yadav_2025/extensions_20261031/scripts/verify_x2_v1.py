"""Independent OOXML parsing and Decimal arithmetic for X2 source reconstruction."""
import csv, json, math, zipfile
from decimal import Decimal, localcontext
from pathlib import Path
import xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[4]
EXT=ROOT/'Research Article/gate2_W3_yadav_2025/extensions_20261031'
def read(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def close(a,b):assert math.isclose(float(a),float(b),rel_tol=1e-11,abs_tol=1e-14),(a,b)
def workbook(path):
    ns={'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    with zipfile.ZipFile(path) as z:
        shared=[''.join(e.itertext()) for e in E.fromstring(z.read('xl/sharedStrings.xml'))]
        links={r.get('Id'):r.get('Target') for r in E.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        result={}
        for sh in E.fromstring(z.read('xl/workbook.xml')).findall('s:sheets/s:sheet',ns):
            target=links[sh.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')]
            xml=E.fromstring(z.read(target.lstrip('/') if target.startswith('/') else 'xl/'+target))
            for c in xml.findall('.//s:c',ns):
                val=c.findtext('s:v',namespaces=ns)
                if val is None:continue
                if c.get('t')=='s':val=shared[int(val)]
                result[(sh.get('name'),c.get('r'))]=(c.get('t','n'),val)
    return result
def verify(out):
    spec=json.loads((EXT/'config/x2_spec_v1.json').read_text())
    source=workbook(ROOT/spec['source_workbook'])
    cells=read(ROOT/'analysis/research/runs/Yd1_extension_x0_v1/panel_cells.csv')
    for row in cells:
        actual=source.get((row['sheet'],row['cell']))
        if row['role']=='blank':assert actual is None
        else:assert actual==(row['source_type'],row['source_value'])
    obs=read(out/'observations.csv');groups=read(out/'group_summaries.csv');contrasts=read(out/'contrasts.csv')
    expected={};allcoords=set();nchecks=0
    with localcontext() as ctx:
        ctx.prec=45
        for panel in spec['panels']:
            for g in panel['groups']:
                values=[Decimal(source[(panel['sheet'],c)][1]) for c in g['cells']]
                allcoords.update((panel['sheet'],c) for c in g['cells'])
                mean=sum(values)/len(values)
                sd=(sum((v-mean)**2 for v in values)/(len(values)-1)).sqrt()
                expected[(panel['id'],g['id'])]=dict(n=len(values),mean=mean,sd=sd,min=min(values),max=max(values))
        assert len(obs)==len(allcoords) and {(r['sheet'],r['cell']) for r in obs}==allcoords
        for row in obs:
            close(row['value'],Decimal(source[(row['sheet'],row['cell'])][1]))
        for row in groups:
            e=expected[(row['panel'],row['group'])]
            for key,val in e.items():close(row[key],val);nchecks+=1
        for r in contrasts:
            delta=expected[(r['panel'],r['target'])]['mean']-expected[(r['panel'],r['reference'])]['mean']
            close(r['mean_difference'],delta)
    assert len(groups)==sum(len(p['groups']) for p in spec['panels'])
    assert len(contrasts)==sum(len(p['contrasts']) for p in spec['panels'])
    return dict(method='Direct workbook OOXML values/blank map plus 45-digit Decimal group means/sample SD/ranges/differences; main script uses frozen CSV and NumPy',panel_cells_checked=len(cells),observations_checked=len(obs),groups_checked=len(groups),summary_value_checks=nchecks,contrasts_checked=len(contrasts),passed=True,replication=False)
if __name__=='__main__':
    import sys
    print(json.dumps(verify(Path(sys.argv[1])),indent=2))
