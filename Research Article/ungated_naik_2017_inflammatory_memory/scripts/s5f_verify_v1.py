"""Independent ZIP/XML source extraction and Decimal arithmetic verification."""
import argparse
from collections import defaultdict
import csv
from decimal import Decimal, getcontext
import json
from pathlib import Path
import posixpath
import xml.etree.ElementTree as ET
import zipfile

getcontext().prec=50
NS={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
REL='{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'


def xml_cells(mapping,paths):
    wanted=defaultdict(set)
    for e in mapping['endpoints']:
        key=e['workbook'],e['sheet']
        wanted[key].update(x['cell'] for x in e['header_guards'])
        for g in e['groups']:
            wanted[key].add(g['label_cell'])
            wanted[key].update(g['cells'] if e['kind']=='records' else [g[k] for k in ['mean_cell','se_cell','n_cell']])
    out={}
    for book,path in paths.items():
        with zipfile.ZipFile(path) as archive:
            shared=[]
            if 'xl/sharedStrings.xml' in archive.namelist():
                shared=[''.join(x.text or '' for x in si.iter('{'+NS['m']+'}t')) for si in ET.fromstring(archive.read('xl/sharedStrings.xml'))]
            rels={x.attrib['Id']:x.attrib['Target'] for x in ET.fromstring(archive.read('xl/_rels/workbook.xml.rels'))}
            sheets={x.attrib['name']:rels[x.attrib[REL]] for x in ET.fromstring(archive.read('xl/workbook.xml')).findall('m:sheets/m:sheet',NS)}
            for (b,name),addresses in wanted.items():
                if b!=book:continue
                target=sheets[name];part=target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/'+target)
                for x in ET.fromstring(archive.read(part)).findall('m:sheetData/m:row/m:c',NS):
                    address=x.attrib['r']
                    if address not in addresses:continue
                    assert x.find('m:f',NS) is None,'Formula in requested XML source cell'
                    t=x.attrib.get('t','n');v=x.find('m:v',NS)
                    if t=='inlineStr':value=''.join(y.text or '' for y in x.findall('m:is//m:t',NS))
                    elif v is None or v.text is None:value=None
                    elif t=='s':value=shared[int(v.text)]
                    elif t=='str':value=v.text
                    elif t=='n':value=Decimal(v.text)
                    else:raise AssertionError('Unsupported source cell type: '+t)
                    out[b,name,address]=value
                for address in addresses:out.setdefault((b,name,address),None)
    return out


def csv_rows(path):
    with path.open(encoding='utf-8',newline='') as handle:return list(csv.DictReader(handle,delimiter='\t'))


def mean(values):return sum(values,Decimal(0))/len(values)
def median(values):
    v=sorted(values);n=len(v)
    return v[n//2] if n%2 else (v[n//2-1]+v[n//2])/2


def verify(mapping,paths,run_dir,analysis_id=None):
    cache=xml_cells(mapping,paths);roles=defaultdict(set);checks=0;maximum=Decimal(0)
    def equal(actual,expected,label):
        nonlocal checks,maximum
        checks+=1
        if expected is None:assert actual=='NA',(label,actual,expected)
        elif isinstance(expected,Decimal):
            a=Decimal(actual);assert a.is_finite()
            error=abs(a-expected)/max(Decimal(1),abs(a),abs(expected));maximum=max(maximum,error)
            assert error<=Decimal('1e-10'),(label,actual,str(expected))
        else:assert actual==str(expected),(label,actual,expected)
    def compare(name,expected):
        actual=csv_rows(run_dir/(name+'.tsv'));assert len(actual)==len(expected),(name,len(actual),len(expected))
        for i,(a,e) in enumerate(zip(actual,expected)):
            assert a.keys()==e.keys(),('table schema',name)
            for k,v in e.items():equal(a[k],v,name+':'+str(i)+':'+k)
    def cell(e,address,role):
        key=e['workbook'],e['sheet'],address;roles[key].add(role)
        return cache[key]
    groups=[];observations=[];vectors={};by_group={};endpoints={e['id']:e for e in mapping['endpoints']}
    assert len(endpoints)==len(mapping['endpoints'])
    for e in mapping['endpoints']:
        for h in e['header_guards']:
            actual=cell(e,h['cell'],'header');expected=h['value']
            if not isinstance(expected,str):expected=Decimal(str(expected))
            assert actual==expected,('XML header guard',e['id'],h['cell'])
            checks+=1
        for g in e['groups']:
            assert cell(e,g['label_cell'],'group_label')==g['source_label'];checks+=1
            common=dict(endpoint=e['id'],group=g['id'],label=g['label'],source_label=g['source_label'],kind=e['kind'],unit=e['unit'],time=e['time'],
                        normalization_reference=g['normalization_reference'],caption_n=e['caption_n'],caption_n_relation=e['caption_n_relation'])
            if e['kind']=='records':
                pairs=[]
                for address in g['cells']:
                    value=cell(e,address,'observation')
                    if value is not None:
                        assert isinstance(value,Decimal) and value.is_finite();pairs.append((address,value))
                    observations.append(dict(endpoint=e['id'],group=g['id'],workbook=e['workbook'],sheet=e['sheet'],cell=address,value=value,missing=value is None,
                        record_kind='normalization_reference' if g['normalization_reference'] else 'source_observation'))
                values=[v for c,v in pairs];n=len(values);assert n==g['expected_n'] and n>0
                if g['normalization_reference']:assert values==[Decimal(1)]*n
                average=mean(values)
                sd=(sum((v-average)**2 for v in values)/(n-1)).sqrt() if n>1 and not g['normalization_reference'] else None
                stats=dict(source_n=n,source_n_meaning='source_records',mean=average,median=median(values),source_min=min(values),source_max=max(values),sample_sd=sd,
                           reported_se=None,dispersion_scope='normalization_reference_no_empirical_variance' if g['normalization_reference'] else ('finite_source_values' if n>1 else 'singleton_no_sd'),
                           source_cells=';'.join(g['cells']),se_source_label='NA')
                vectors[e['id'],g['id']]=pairs
            else:
                assert e['kind']=='reported_summary'
                average=cell(e,g['mean_cell'],'reported_mean');se=cell(e,g['se_cell'],'reported_se');n=cell(e,g['n_cell'],'reported_n')
                assert all(isinstance(x,Decimal) and x.is_finite() for x in [average,se,n])
                assert n==int(n)==g['expected_n'] and n>0 and se>=0
                stats=dict(source_n=int(n),source_n_meaning='reported_fitted_rate_N',mean=average,median=None,source_min=None,source_max=None,sample_sd=None,
                           reported_se=se,dispersion_scope='reported_SE_only',source_cells=';'.join([g['mean_cell'],g['se_cell'],g['n_cell']]),se_source_label=g['se_source_label'])
            if e['caption_n_relation']=='context_only':status='not_comparable_daily_records'
            elif e['caption_n_relation']=='at_least':status='meets_caption_minimum' if stats['source_n']>=e['caption_n'] else 'source_caption_N_discrepancy'
            else:
                assert e['caption_n_relation']=='equal'
                status='matches_caption_number' if stats['source_n']==e['caption_n'] else 'source_caption_N_discrepancy'
            record={**common,**stats,'caption_n_comparison':status};groups.append(record);by_group[e['id'],g['id']]=record
    compare('groups',groups);compare('observations',observations)
    contrasts=[];deletions=[]
    for spec in mapping['contrasts']:
        eid=spec['endpoint'];e=endpoints[eid];coeff=spec['coefficients'];assert sum(coeff.values())==0
        averages={g:by_group[eid,g]['mean'] for g in coeff}
        full=sum(Decimal(c)*averages[g] for g,c in coeff.items());deleted=[]
        if spec['leave_one_source_record_out']:
            assert e['kind']=='records' and not spec['delete_normalization_references']
            for g,c in coeff.items():
                if by_group[eid,g]['normalization_reference']:continue
                data=vectors[eid,g]
                if len(data)==1:continue
                for j,(address,value) in enumerate(data):
                    remainder=[v for i,(a,v) in enumerate(data) if i!=j]
                    # Update a single component by its independently computed mean change.
                    estimate=full+Decimal(c)*(mean(remainder)-averages[g]);deleted.append(estimate)
                    deletions.append(dict(contrast=spec['id'],endpoint=eid,removed_group=g,removed_cell=address,removed_value=value,remaining_group_n=len(remainder),
                                          mean_contrast=estimate,change_from_full=estimate-full,scope='source_record_deletion_not_CI'))
        med=sum(Decimal(c)*by_group[eid,g]['median'] for g,c in coeff.items()) if e['kind']=='records' else None
        contrasts.append(dict(contrast=spec['id'],endpoint=eid,label=spec['label'],kind=e['kind'],unit=e['unit'],coefficients=json.dumps(coeff,sort_keys=True,separators=(',',':')),
            mean_contrast=full,median_contrast=med,source_ns=json.dumps({g:by_group[eid,g]['source_n'] for g in coeff},sort_keys=True,separators=(',',':')),
            deletion_count=len(deleted),deletion_min=min(deleted) if deleted else None,deletion_max=max(deleted) if deleted else None,
            deletion_scope='source_record_deletion_not_CI' if deleted else ('summary_only_no_individual_records' if e['kind']=='reported_summary' else 'no_eligible_nonreference_deletion')))
    compare('contrasts',contrasts);compare('deletion_diagnostics',deletions)
    source=[]
    for key in sorted(roles,key=lambda k:(int(k[0]),k[1],k[2])):
        value=cache[key];kind='blank' if value is None else ('number' if isinstance(value,Decimal) else 'text')
        source.append(dict(workbook=key[0],sheet=key[1],cell=key[2],kind=kind,value=value,roles='|'.join(sorted(roles[key]))))
    compare('source_cells',source)
    expected=dict(endpoint_count=len(endpoints),group_count=len(groups),contrast_count=len(contrasts),source_cell_count=len(source),observation_slots=len(observations),
        nonmissing_source_records=sum(x['value'] is not None for x in observations),missing_source_slots=sum(x['value'] is None for x in observations),deletion_rows=len(deletions),
        normalized_reference_groups=[{'endpoint':x['endpoint'],'group':x['group']} for x in groups if x['normalization_reference']],
        caption_n_discrepancies=[{'endpoint':x['endpoint'],'group':x['group'],'source_n':x['source_n'],'caption_n':x['caption_n']} for x in groups if x['caption_n_comparison']=='source_caption_N_discrepancy'],
        independent_biological_replication=False,population_inference=False,source_fits_rerun=False)
    if analysis_id is not None:expected.update(analysis_id=analysis_id,source_files=mapping['source_files'])
    actual=json.loads((run_dir/'metadata.json').read_text());assert actual==expected,'Metadata differs';checks+=1
    return dict(status='passed',checks=checks,maximum_scaled_error=float(maximum),source_reader='stdlib ZIP/XML',arithmetic='50-digit Decimal',
        endpoints=len(endpoints),groups=len(groups),contrasts=len(contrasts),source_cells=len(source),deletion_rows=len(deletions),independent_biological_replication=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--contract',type=Path,required=True);parser.add_argument('--run-dir',type=Path,required=True)
    args=parser.parse_args();root=Path(__file__).resolve().parents[3];contract=json.loads(args.contract.read_text(encoding='utf-8-sig'))
    mapping=json.loads(next(root/x['path'] for x in contract['inputs'] if x['path'].endswith('/S5F_SOURCE_MAP_V1.json')).read_text(encoding='utf-8'))
    pdf=(root/mapping['caption_source']['path']).read_text(encoding='utf-8').splitlines()
    for axis in mapping['pdf_axis_guards']:assert pdf[axis['line']-1]==axis['value'] and 'day–1' in axis['value']
    result=verify(mapping,{k:root/v['path'] for k,v in mapping['source_files'].items()},args.run_dir,contract['analysis_id'])
    result['pdf_axis_guards_checked']=len(mapping['pdf_axis_guards']);result['analysis_id']=contract['analysis_id']
    (args.run_dir/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result),flush=True)
