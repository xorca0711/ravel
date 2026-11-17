"""Artificial joins/associations/coupling; never reads real biological outcomes."""
import csv
import gzip
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

from s5m_math_v1 import average_ranks, moments
from s5m_integrate_v1 import ANCHORS, GSMS, tsv, save


def test():
    assert np.array_equal(average_ranks([0, 1, 1, 2]), [1, 2.5, 2.5, 4])
    assert moments([1, 2, 3], [3, 5, 7])['coefficient'] == 1
    assert abs(moments([1, 2, 3], [3, 5, 7], [.5, .5, 1])['coefficient']-1) < 1e-14
    assert moments([1, 1, 1], [3, 5, 7], [1/3, 1/3, 1/3])['reason'] == 'constant_x'
    assert moments([1], [2])['coefficient'] is None
    assert moments(average_ranks([0, 0, 1]), average_ranks([1, 1, 0]))['coefficient'] == -1
    assert abs(moments([0, 0, 1, 2], [0, 3, 2, 4])['coefficient']-moments([0, 0, 1, 2], [0, 3, 2, 4], [.5, .5, 1, 1])['coefficient']) > .01
    try: moments([1, float('nan')], [2, 3])
    except ValueError: pass
    else: raise AssertionError('nonfinite accepted')
    assert average_ranks([0, 1, 2])[0] != average_ranks([0, 0, 2])[0]
    root = Path(__file__).resolve().parents[3]; parent = root/'raw_data'
    with tempfile.TemporaryDirectory(prefix='s5m_synthetic_', dir=parent) as temporary:
        fixture=Path(temporary);assert fixture.resolve().parent == parent.resolve()
        source=fixture/'sources';source.mkdir();output=fixture/'outputs';output.mkdir()
        genes=ANCHORS+[('Dup','artificial_dup'),('Noncode','artificial_noncode'),('NoRNA','artificial_no_rna'),
                       ('Low','artificial_low'),('Zero','artificial_zero'),('Ygene','artificial_y'),('Unknown','artificial_unknown'),('MissingValue','artificial_missing')]
        lines=[];maps=[];windows={}
        for i,(name,gene) in enumerate(genes):
            if name=='Unknown':continue
            chrom='chrY' if name=='Ygene' else 'chr1';kind='lincRNA' if name=='Noncode' else 'protein_coding'
            start=5000 if name=='Dup' else 5000+i*10000
            lines.append(f'{chrom}\tARTIFICIAL\tgene\t{start+1}\t{start+501}\t.\t+\t.\tgene_id "{gene}"; gene_name "{name}"; gene_type "{kind}";\n')
            if chrom=='chrY' or kind!='protein_coding':continue
            for flank in [1000,2000]:
                key=f'{flank}:{chrom}:{start-flank}-{start+flank}';anchor=f'{chrom}:{start}'
                maps.append(dict(gene_id=gene,gene_name=name,gene_type=kind,strand='+',tss=start,window_id=key,anchor_id=anchor,flank=flank))
                windows[key]=dict(window_id=key,anchor_id=anchor,flank=flank,chrom=chrom,start=start-flank,end=start+flank,clipped=False)
        with gzip.open(source/'gencode.vM9.annotation.gtf.gz','wt') as f:f.writelines(lines)
        tsv(source/'gene_window_map.tsv.gz',pd.DataFrame(maps));effects=[]
        for flank in [1000,2000]:
            subset=sorted([w for w in windows.values() if w['flank']==flank],key=lambda w:w['start']);n=len(subset)
            means=np.array([[((i*5+j*3+(flank//1000))%11)+1 for i in range(n)] for j in range(8)],float)
            zero_index=next(i for i,w in enumerate(subset) if w['anchor_id']==f'chr1:{5000+9*10000}')
            means[:,zero_index]=0
            means[2:4,1]=0;means[4:6,1:3]=0
            ranks=np.array([100*(average_ranks(v)-1)/(n-1) for v in means])
            for i,w in enumerate(subset):
                row=dict(w)
                for j,gsm in enumerate(GSMS):
                    row[gsm+'__mean']=means[j,i];row[gsm+'__zero_bases']=2*flank if means[j,i]==0 else 0;row[gsm+'__percentile']=ranks[j,i]
                for phase,offset in [('D6',0),('D30',4)]:
                    c,h=ranks[offset:offset+2,i],ranks[offset+2:offset+4,i];pairs=[float(y-x) for y in h for x in c]
                    row[phase+'_delta']=float(h.mean()-c.mean())
                    for label,value in zip(['h1_c1','h1_c2','h2_c1','h2_c2'],pairs):row[phase+'_'+label]=value
                    row.update({phase+'_range_min':min(pairs),phase+'_range_max':max(pairs),phase+'_range_width':max(pairs)-min(pairs),phase+'_range_touches_zero':min(pairs)<=0<=max(pairs)})
                effects.append(row)
        tsv(source/'window_effects.tsv.gz',pd.DataFrame(effects))
        s2rows=[];s4rows=[];s4brows=[]
        for i,(name,gene) in enumerate(genes):
            qualified=name not in ['Low','Il18'];kind='lincRNA' if name=='Noncode' else 'protein_coding'
            s2=dict(gene_id=gene,gene_name=name,gene_type=kind,eligible_both=qualified,D6_qualified_cpm=qualified,D30_qualified_cpm=True,
                    D6_zero_libraries=i%3,D30_all_zero=False,D6_regularization_sensitive=i%5==0,original_note='preserve this unused field')
            s4=dict(gene_id=gene,gene_name=name,all_three_qualified=True,B0_qualified_cpm=True,W6_qualified_cpm=True,W12_qualified_cpm=True,
                    B0_control_zero=i%4==0,W6_adjustment_low_mean=i%5==0)
            s4b=dict(gene_id=gene,gene_name=name,all_three_qualified=True,c2_h2_reference_any_zero=i%4==1,c1_h1_reference_low_mor=i%5==1)
            b=(i%4-1)*.5;post6=(i*3%7-2)/3;post12=(i*5%9-3)/4
            for norm in ['mor','total']:
                transform=lambda v:v if norm=='mor' else .8*v+.1*(i%2)
                s2['D6_log2_effect_'+norm]=transform((i*7%11-5)/3)
                s2['D30_log2_effect_'+norm]=transform((i*2%6-2)/5)
                baseline=transform(b);s4['B0_log2_effect_'+norm]=baseline
                for phase,post in [('W6',post6),('W12',post12)]:
                    s4[phase+'_log2_effect_'+norm]=transform(post);s4[phase+'_adjusted_'+norm]=transform(post)-baseline
                for ref,alt in [('c2_h2',b+.3*(i%3-1)),('c1_h1',b-.25*(i%4-1))]:
                    s4b['B0_'+ref+'_'+norm]=transform(alt)
                    s4b['W6_'+ref+'_'+norm]=transform(post6)-transform(alt)
                    s4b['W12_'+ref+'_'+norm]=transform(post12)-transform(alt)
            if name=='MissingValue':s2['D30_log2_effect_mor']='NA'
            if name!='NoRNA':s2rows.append(s2)
            s4rows.append(s4);s4brows.append(s4b)
        for name,data in [('gene_effects.tsv',s2rows),('gene_effects.tsv.gz',s4rows),('reference_effects.tsv.gz',s4brows)]:tsv(source/name,pd.DataFrame(data))
        contract={'analysis_id':'synthetic.s5m','inputs':[{'path':p.relative_to(root).as_posix()} for p in source.iterdir()]}
        cp=fixture/'contract.json';save(cp,contract)
        command=[sys.executable,str(Path(__file__).with_name('s5m_integrate_v1.py')),'--contract',str(cp),'--output',str(output)]
        run=subprocess.run(command,capture_output=True,text=True);assert run.returncode==0,run.stdout+run.stderr
        verification=json.loads((output/'verification.json').read_text());summary=json.loads((output/'universe_summary.json').read_text())
        assert summary['gene_records']==13 and summary['universes']['primary']['genes']==6 and summary['universes']['all_mapped']['genes']==8
        with gzip.open(output/'gene_join.tsv.gz','rt') as f:missing=next(r for r in csv.DictReader(f,delimiter='\t') if r['gene_id']=='artificial_missing')
        assert missing['all_mapped_eligibility_reason']=='nonfinite_required_rna' and missing['s2__D30_log2_effect_mor']=='NA'
        with gzip.open(output/'gene_atac.tsv.gz','rt') as f:zero=[r for r in csv.DictReader(f,delimiter='\t') if r['gene_id']=='artificial_zero']
        assert all(r['D6_all_zero_means']=='True' and float(r['atac__D6_delta'])!=0 for r in zero)
        verifier=[sys.executable,str(Path(__file__).with_name('s5m_verify_v1.py')),'--contract',str(cp),'--run-dir',str(output)]
        path=output/'association_results.tsv';original=path.read_bytes();frame=pd.read_csv(path,sep='\t');frame.loc[0,'coefficient']+=.05;tsv(path,frame)
        bad=subprocess.run(verifier,capture_output=True,text=True);assert bad.returncode!=0 and 'association:coefficient' in bad.stderr;path.write_bytes(original)
        path=output/'gene_join.tsv.gz';original=path.read_bytes();frame=pd.read_csv(path,sep='\t',dtype=str,keep_default_na=False);frame.loc[0,'s2__original_note']='tampered';tsv(path,frame)
        bad=subprocess.run(verifier,capture_output=True,text=True);assert bad.returncode!=0 and 'source field' in bad.stderr;path.write_bytes(original)
        print(json.dumps(dict(status='passed',artificial_genes=13,primary_genes=6,all_mapped_genes=8,independent_checks=verification['checks'],
                              maximum_scaled_error=verification['maximum_scaled_error'],associations=verification['associations'],covariance_identities=verification['covariance_identities'],
                              altered_coefficient_and_source_join_rejected=True,real_biological_inputs_read=False)))


if __name__=='__main__':test()
