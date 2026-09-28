"""Run the committed exposed-data corrected C1 comparison; preserve original Stage1."""
from __future__ import annotations
import argparse, csv, gzip, hashlib, json, os, subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pandas as pd
import scipy
from scipy import io, linalg, sparse
from scipy.spatial.distance import cdist
from threadpoolctl import threadpool_limits
from c1_invariants import remaining_columns, quartiles, eligibility, effects
BASE=Path(__file__).resolve().parents[1]; ROOT=BASE.parents[2]
PAPER=ROOT/'Research Article/gate2_C2_england_2025'
KS=[5,10,20]
EP=['priming_associated','AT2_identity','AT1_identity','Itga2','cycling','shared_gate_cycle_stress_disjoint','lesion_gate_cycle_stress_disjoint']
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(8<<20),b''): h.update(block)
    return h.hexdigest()
def array_sha(a): return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()
def read_json(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def old_stage_hashes():
    a16=BASE.parent
    files=list((a16/'tables/stage1').glob('*'))+[a16/'config/a16_question_contract.json',a16/'scripts/01_stage1_c3_c4.py',a16/'scripts/02_stage1_c1_c2_c5.py',a16/'reports/STAGE1_RESULTS.md',a16/'reports/STAGE1_ERRATUM.md']
    return {str(p.relative_to(ROOT)).replace('\\','/'):sha(p) for p in files if p.is_file()}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--spec-commit',required=True); args=ap.parse_args()
    output=BASE/'tables/corrected_c1'
    if output.exists(): raise SystemExit('Refuse overwrite of existing corrected_c1 output; inspect partial run before any replay')
    paths=[BASE/'config/corrected_c1_specification.json',BASE/'config/excluded_genes.tsv',BASE/'config/exclusion_provenance.json']
    for p in paths:
        frozen=subprocess.check_output(['git','show',args.spec_commit+':'+p.relative_to(ROOT).as_posix()],cwd=ROOT)
        assert hashlib.sha256(frozen).hexdigest()==sha(p),f'Uncommitted or changed configuration: {p.name}'
    spec=read_json(paths[0]); prov=read_json(paths[2]); ready=read_json(BASE/'tables/readiness.json')
    assert ready['status']=='ready_for_specification_review' and ready['original_cells_table_verified']
    cfg_path=PAPER/'config/continuation_contract.json'; assert sha(cfg_path)==prov['source_contract_sha256']
    cfg=read_json(cfg_path); modules=cfg['modules']
    excluded=set(pd.read_csv(paths[1],sep='\t').gene); assert len(excluded)==prov['n_excluded']==660
    assert sha(paths[1])==prov['exclusion_sha256']
    inputs={}
    for r in ready['inputs']:
        if r['role'] in ['raw_count_provenance','original_cells_table_inclusion_and_gates']:
            p=Path(r['path']); assert sha(p)==r['expected_sha256'],f'Input changed: {p}'
            inputs[str(p)]={'sha256':sha(p),'bytes':p.stat().st_size}
    cellpath=next(Path(r['path']) for r in ready['inputs'] if r['role']=='original_cells_table_inclusion_and_gates')
    col=lambda ep:'raw_'+ep if ep in modules else 'raw_'+ep+'_log1p'
    use=['gsm','barcode','primary_include','gate_transition','total_umis','n_genes','Cd177_umi']+[col(ep) for ep in EP]
    cells=pd.read_csv(cellpath,usecols=use,dtype={'gsm':str,'barcode':str})
    assert cells[['gsm','barcode']].duplicated().sum()==0
    old=old_stage_hashes(); output.mkdir()
    record={'status':'started','started_utc':datetime.now(timezone.utc).isoformat(),'specification_commit':args.spec_commit,'specification_sha256':sha(paths[0]),'exclusion_sha256':sha(paths[1]),'script_sha256':sha(Path(__file__)),'helper_sha256':sha(BASE/'scripts/c1_invariants.py'),'inputs':inputs,'original_stage1_hashes':old,'versions':{'numpy':np.__version__,'scipy':scipy.__version__,'pandas':pd.__version__},'libraries':{},'biological_units_available':0,'formal_inference':False}
    (output/'started.json').write_text(json.dumps(record,indent=2)+'\n')
    metrics=[]; quality=[]; pc_quality=[]; feature_rows=[]; matched_edges=[]; parity=[]; cell_scores=[]
    for gsm in spec['libraries']:
        d=cells[(cells.gsm==gsm)&cells.primary_include&cells.gate_transition].sort_values('barcode').reset_index(drop=True)
        assert d.primary_include.all() and d.gate_transition.all()
        files={}
        for r in ready['inputs']:
            if r['role']=='raw_count_provenance' and gsm in r['path']:
                files[Path(r['path']).name.split('_')[-1]]=Path(r['path'])
        fpath=files['features.tsv.gz']; bpath=files['barcodes.tsv.gz']; mpath=files['matrix.mtx.gz']
        features=pd.read_csv(fpath,sep='\t',header=None,dtype=str,keep_default_na=False)
        symbols=features.iloc[:,1].to_numpy(str); barcodes=pd.read_csv(bpath,sep='\t',header=None,dtype=str).iloc[:,0]
        assert barcodes.is_unique
        indices=pd.Index(barcodes).get_indexer(d.barcode); assert (indices>=0).all()
        with gzip.open(mpath,'rb') as handle, threadpool_limits(limits=1): raw=io.mmread(handle).tocsr().T.tocsr()
        assert raw.shape==(len(barcodes),len(symbols))
        assert np.all(raw.data>=0) and np.all(raw.data==np.floor(raw.data))
        X=raw[indices].tocsr(); del raw
        total=np.asarray(X.sum(axis=1)).ravel(); ng=np.asarray((X>0).sum(axis=1)).ravel()
        assert np.array_equal(total,d.total_umis.to_numpy()) and np.array_equal(ng,d.n_genes.to_numpy()),gsm+' count/depth parity'
        named={g:np.asarray(X[:,np.flatnonzero(symbols==g)].sum(axis=1)).ravel() for g in set(sum([modules[ep] if ep in modules else [ep] for ep in EP],[])+cfg['gates']['transition']+['Cd177']) if np.any(symbols==g)}
        assert 'Cd177' in named and 'Itga2' in named
        assert np.array_equal(named['Cd177'],d.Cd177_umi.to_numpy())
        assert np.all(sum(named[g]>0 for g in cfg['gates']['transition'])>=cfg['gate_min_detected'])
        positive=named['Cd177']>=1
        outcome={}
        for ep in EP:
            genes=modules[ep] if ep in modules else [ep]; present=[g for g in genes if g in named]
            assert len(present)/len(genes)>=cfg['coverage_floor']
            y=np.mean([np.log1p(named[g]/total*1e4) for g in present],axis=0)
            error=float(np.max(np.abs(y-d[col(ep)].to_numpy()))) if len(d) else 0
            assert error<=1e-8,f'{gsm} {ep} score parity error {error}'
            outcome[ep]=y
            parity.append({'library':gsm,'endpoint':ep,'frozen_genes':len(genes),'present_genes':len(present),'max_abs_score_error':error,'fixed_cells':len(d),'n_positive':int(positive.sum()),'n_negative':int((~positive).sum()),'totals_and_gate_parity':True})
        pd.DataFrame(parity).to_csv(output/'instrument_parity.csv',index=False)
        print(json.dumps({'milestone':'raw_count_fixed_population_and_score_parity_passed','library':gsm,'cells':len(d),'n_positive':int(positive.sum()),'n_negative':int((~positive).sum()),'max_endpoint_abs_error':max(r['max_abs_score_error'] for r in parity if r['library']==gsm)}),flush=True)
        # The excluded genes are removed before both normalization and depth-stratum construction.
        keep=np.asarray(remaining_columns(symbols,excluded),dtype=int)
        assert not set(symbols[keep])&excluded and all(not s.lower().startswith('mt-') for s in symbols[keep])
        Z=X[:,keep].astype(float); remaining=np.asarray(Z.sum(axis=1)).ravel(); assert np.all(remaining>0)
        strata=np.asarray(quartiles(remaining.tolist(),d.barcode.tolist()))
        Z=sparse.diags(1e4/remaining)@Z; Z=Z.tocsr(); Z.data=np.log1p(Z.data)
        detected=np.asarray((Z>0).sum(axis=0)).ravel(); mean=np.asarray(Z.mean(axis=0)).ravel(); variance=np.maximum(0,np.asarray(Z.power(2).mean(axis=0)).ravel()-mean**2)
        eligible=np.flatnonzero((detected>=3)&(variance>0))
        selected=sorted(eligible,key=lambda j:(-variance[j],symbols[keep[j]],int(keep[j])))[:2000]
        matrix=Z[:,selected].toarray(); matrix-=matrix.mean(axis=0)
        with threadpool_limits(limits=1): u,s,vt=linalg.svd(matrix,full_matrices=False,lapack_driver='gesdd')
        rank=int(np.sum(s>max(matrix.shape)*np.finfo(float).eps*s[0])); npc=min(20,len(d)-1,len(selected)-1,rank)
        assert npc>=5,'Fewer than five usable PCs'
        coords=u[:,:npc]*s[:npc]; loadings=vt[:npc]
        for j in range(npc):
            sign=1 if loadings[j,np.argmax(np.abs(loadings[j]))]>=0 else -1
            coords[:,j]*=sign; loadings[j]*=sign
        coord=pd.DataFrame(coords,columns=[f'PC{j+1}' for j in range(npc)])
        coord.insert(0,'barcode',d.barcode); coord.insert(0,'library',gsm); coord['depth_quartile']=strata; coord['remaining_gene_umis']=remaining.astype(int)
        coord.to_csv(output/f'{gsm}_coordinates.csv',index=False)
        for rank,j in enumerate(selected,1): feature_rows.append({'library':gsm,'variance_rank':rank,'original_feature_index':int(keep[j]),'gene':symbols[keep[j]],'population_variance':float(variance[j]),'detected_cells':int(detected[j])})
        for i,b in enumerate(d.barcode):
            cell_scores.append({'library':gsm,'barcode':b,'positive':bool(positive[i]),'Cd177_umi':int(named['Cd177'][i]),'total_umis':int(total[i]),'remaining_gene_umis':int(remaining[i]),'depth_quartile':int(strata[i]),**{ep:float(y[i]) for ep,y in outcome.items()}})
        lr={'cells':len(d),'n_positive':int(positive.sum()),'n_negative':int((~positive).sum()),'n_excluded':len(excluded),'features':len(selected),'pcs':npc,'coordinate_array_sha256':array_sha(coords),'loading_array_sha256':array_sha(loadings),'fixed_barcode_sha256':hashlib.sha256('\n'.join(d.barcode).encode()).hexdigest(),'strata':[]}
        for q in range(4): lr['strata'].append({'quartile':q,'positive':int(np.sum(positive&(strata==q))),'negative':int(np.sum(~positive&(strata==q)))})
        pos_index=np.flatnonzero(positive); neg_index=np.flatnonzero(~positive)
        pc_sd=coords.std(axis=0,ddof=1)
        for k in KS:
            status=eligibility(positive.tolist(),strata.tolist(),k)
            matches=[]; distances=[]
            if status=='assessed':
                for i in pos_index:
                    candidates=np.flatnonzero((~positive)&(strata==strata[i]))
                    # d is barcode-sorted; stable sorting resolves exact distance ties by barcode.
                    dist=cdist(coords[i:i+1],coords[candidates],metric='euclidean')[0]
                    order=np.argsort(dist,kind='stable')[:k]
                    matches.append(candidates[order]); distances.extend(dist[order])
                matches=np.asarray(matches,dtype=int)
                status=eligibility(positive.tolist(),strata.tolist(),k,matches.ravel().tolist())
            if status!='assessed':
                quality.append({'library':gsm,'k':k,'status':status,'fixed_positives':len(pos_index),'fixed_negative_pool':len(neg_index)})
                continue
            assert matches.shape==(len(pos_index),k) and not positive[matches].any()
            assert np.all(strata[matches]==strata[pos_index,None])
            weight=Counter(matches.ravel().tolist()); w=np.array(list(weight.values()),dtype=float)/(len(pos_index)*k)
            ess=float(1/np.sum(w*w))
            qrow={'library':gsm,'k':k,'status':'assessed','fixed_positives':len(pos_index),'matched_positives':len(pos_index),'fixed_negative_pool':len(neg_index),'unique_matched_negatives':len(weight),'negative_weight_ESS':ess,'max_negative_reuse':max(weight.values()),'max_negative_weight':float(w.max()),'distance_mean':float(np.mean(distances)),'distance_median':float(np.median(distances)),'distance_p95':float(np.quantile(distances,.95)),'distance_max':float(np.max(distances)),'PC_standardized_imbalance_abs_max_before':float(np.max(abs((coords[pos_index].mean(0)-coords[neg_index].mean(0))/pc_sd))),'PC_standardized_imbalance_abs_max_after':float(np.max(abs((coords[pos_index].mean(0)-coords[matches].mean(axis=(0,1)))/pc_sd)))}
            quality.append(qrow)
            for i,controls in zip(pos_index,matches):
                for rank,j in enumerate(controls,1): matched_edges.append({'library':gsm,'k':k,'positive_barcode':d.barcode.iloc[i],'negative_barcode':d.barcode.iloc[j],'depth_quartile':int(strata[i]),'neighbor_rank':rank,'distance':float(np.linalg.norm(coords[i]-coords[j])),'negative_reuse_count':weight[j]})
            for j in range(npc): pc_quality.append({'library':gsm,'k':k,'PC':j+1,'fixed_population_sd':float(pc_sd[j]),'standardized_difference_before':float((coords[pos_index,j].mean()-coords[neg_index,j].mean())/pc_sd[j]),'standardized_difference_after':float((coords[pos_index,j].mean()-coords[matches,j].mean())/pc_sd[j])})
            for ep,y in outcome.items():
                e=effects(y[pos_index].tolist(),y[neg_index].tolist(),y[matches].mean(axis=1).tolist(),y.tolist())
                metrics.append({'library':gsm,'k':k,'endpoint':ep,'status':'assessed','n_positive':len(pos_index),'n_negative_pool':len(neg_index),'n_negative_matched_unique':len(weight),**e})
        record['libraries'][gsm]=lr
    for name,rows in [('effects.csv',metrics),('matching_quality.csv',quality),('PC_balance.csv',pc_quality),('latent_features.csv',feature_rows),('matched_edges.csv',matched_edges),('cell_outcomes.csv',cell_scores)]: pd.DataFrame(rows).to_csv(output/name,index=False)
    assert old_stage_hashes()==old,'Original Stage1 bytes changed'
    record.update(status='corrected_C1_exploratory_complete',completed_utc=datetime.now(timezone.utc).isoformat(),original_stage1_unchanged=True,interpretation='Separate-library exposed-data descriptions; excluded genes prevent direct reuse but correlated features may encode outcomes/overadjust biology; matching support, detection selection and ambient uncertainty remain.',output_sha256={p.name:sha(p) for p in output.iterdir() if p.is_file()})
    (output/'run_record.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({'status':record['status'],'effect_rows':len(metrics),'assessed_library_k':sum(r['status']=='assessed' for r in quality),'primary_k10':[r for r in metrics if r['k']==10 and r['endpoint']=='priming_associated']}),flush=True)
if __name__=='__main__': main()
