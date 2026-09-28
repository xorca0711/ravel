"""Deterministic A17 raw-source accounting; never fits or simulates a model.

Run through analysis/scripts/run_with_environment.py with scipy/numpy installed.
Outputs are exclusively created and completed-output overwrite is refused before
reading the archive. Source and reference directories are read-only.
"""
from __future__ import annotations
import argparse, ast, csv, hashlib, io, json, operator, sys, zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[3]
EXPECTED_ARCHIVE='404697263ca941b1b74dee9feb4c4680ff3077d9e20bb7105482d17f14e96a70'
EXPECTED_SIM='78f7157b8a01d1a8a785c479d33ad1c2c03eb902452f577e10f9e7e006008065'
OUTPUTS=['input_manifest.json','mouse_channel_manifest.csv','batch1_count_crosscheck.csv',
         'table_s1_reconciliation.csv','discrepancy_ledger.json','primary_cohort_manifest.csv',
         'primary_clone_size_frequencies.csv','mutant_parameter_trace.json','REPORT.md','run_record.json']


def sha_bytes(b):return hashlib.sha256(b).hexdigest()
def sha(path):return sha_bytes(path.read_bytes())
def json_text(value):return json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n'
def csv_text(rows):
    out=io.StringIO(newline='');w=csv.DictWriter(out,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows);return out.getvalue()
def read_csv(path):
    with path.open(encoding='utf-8-sig',newline='') as stream:return list(csv.DictReader(stream))

# Only arithmetic in the selected source assignments is interpreted, not MATLAB.
def arithmetic(expr,env):
    ops={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv}
    def visit(node):
        if isinstance(node,ast.Constant) and isinstance(node.value,(int,float)):return node.value
        if isinstance(node,ast.Name):return env[node.id]
        if isinstance(node,ast.BinOp) and type(node.op) in ops:return ops[type(node.op)](visit(node.left),visit(node.right))
        if isinstance(node,ast.UnaryOp) and isinstance(node.op,ast.USub):return -visit(node.operand)
        raise ValueError('Unapproved arithmetic syntax: '+expr)
    return visit(ast.parse(expr,mode='eval').body)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--archive',type=Path,default=Path('X:/GitHub/scRNA_seq/raw_data/england_continuation_inputs/zenodo_v1.1.zip'))
    ap.add_argument('--reference-root',type=Path,default=REPO)
    ap.add_argument('--output-dir',type=Path,default=HERE)
    args=ap.parse_args();out=args.output_dir.resolve()
    existing=[name for name in OUTPUTS if (out/name).exists()]
    if existing:raise SystemExit('REFUSED: source-accounting outputs already exist; no inputs read or outputs changed: '+','.join(existing))
    assert out==HERE,'This run is confined to the owned A17 source-accounting directory'
    import numpy as np
    import scipy
    from scipy.io import loadmat
    started=datetime.now(timezone.utc).isoformat()
    archive_bytes=args.archive.read_bytes();assert sha_bytes(archive_bytes)==EXPECTED_ARCHIVE
    refs={
        'specification':args.reference_root/'docs/roadmap_runs/2026-09-28-gap-fill/A17_SOURCE_ACCOUNTING_SPEC.md',
        'batch1_summary':args.reference_root/'Research Article/gate2_C2_england_2025/trials/batch1/clones/clone_summary_by_mouse.csv',
        'batch1_schema':args.reference_root/'Research Article/gate2_C2_england_2025/trials/batch1/clones/mouse_schema.csv',
        'batch1_decoder_reference_only':args.reference_root/'Research Article/gate2_C2_england_2025/scripts/run_clone_batch1.py',
        'audited_table_s1_transcription':args.reference_root/'docs/audits/2026-09-28-england-paper-rqs/table_s1_reconciliation.csv',
        'manuscript_parameter_transcription':args.reference_root/'docs/audits/2026-09-28-england-paper-rqs/REPORT.md',
    }
    input_manifest={'archive':{'path':str(args.archive.resolve()),'bytes':len(archive_bytes),'sha256':EXPECTED_ARCHIVE},
       'specification_checkpoint':'7f1aae4244fc3a7aaba39ae0ce1b22d43bb76e72',
       'script':{'path':str(Path(__file__).resolve()),'sha256':sha(Path(__file__))},
       'reference_inputs':{k:{'path':str(p.resolve()),'sha256':sha(p)} for k,p in refs.items()},
       'archive_members':[],'decoder':'scipy.io.loadmat(squeeze_me=False, struct_as_record=True); explicit dataset/mouse/lobe/channel indices',
       'identity_rule':'Mouse IDs are stable source-array coordinates, not recovered animal identifiers. No identities are inferred from clone rows.'}
    matrices={};source={}
    with zipfile.ZipFile(io.BytesIO(archive_bytes)) as archive:
        for stem in ['datasets','time_points','chlbls','clone_sizes_total','clone_sizes_SPC_pos','lobe_area_total']:
            names=[n for n in archive.namelist() if n.endswith('/'+stem+'.mat')];assert len(names)==1
            payload=archive.read(names[0]);matrices[stem]=loadmat(io.BytesIO(payload),squeeze_me=False,struct_as_record=True)[stem]
            input_manifest['archive_members'].append({'member':names[0],'bytes':len(payload),'sha256':sha_bytes(payload),'variable':stem,'shape':list(matrices[stem].shape)})
        for stem in ['sim_two_pop_model.m','data_analysis.m']:
            names=[n for n in archive.namelist() if n.endswith('/'+stem)];assert len(names)==1
            payload=archive.read(names[0]);source[stem]=payload.decode('utf-8')
            input_manifest['archive_members'].append({'member':names[0],'bytes':len(payload),'sha256':sha_bytes(payload)})
    assert sha_bytes(source['sim_two_pop_model.m'].encode())==EXPECTED_SIM
    datasets=[str(v[0]) for v in matrices['datasets'][0,:]]
    channels=[str(v[0]) for v in matrices['chlbls'][0,:]]
    assert channels==['YFP','RFP']
    times=matrices['time_points'][:,0]
    assert len(datasets)==len(times)==matrices['clone_sizes_total'].shape[1]
    # MATLAB source explicitly combines Confetti channels but keeps KRAS channels.
    analysis=source['data_analysis.m']
    assert 'vertcat(clone_sizes_total{ndatas}{nmice}{:,nchannel})' in analysis
    assert 'vertcat(clone_sizes_total{ndatas}{nmice}{:})' in analysis
    manifest=[];vectors={};lobe_counts={};raw_rows=0
    for di,ds in enumerate(datasets):
        mice=matrices['clone_sizes_total'][0,di]
        spc_mice=matrices['clone_sizes_SPC_pos'][0,di]
        area_mice=matrices['lobe_area_total'][0,di]
        assert mice.shape==spc_mice.shape==area_mice.shape and mice.shape[0]==1
        for mi in range(mice.shape[1]):
            cells=mice[0,mi];spc=spc_mice[0,mi];area=np.asarray(area_mice[0,mi]).reshape(-1)
            assert cells.shape==spc.shape and cells.shape[1]==len(channels) and len(area)==cells.shape[0]
            mouse=f'{ds}:m{mi+1}';lobe_counts[mouse]=cells.shape[0]
            for ci,ch in enumerate(channels):
                pieces=[];locators=[]
                for li in range(cells.shape[0]):
                    values=np.asarray(cells[li,ci]);positive=np.asarray(spc[li,ci])
                    assert values.size==positive.size and values.dtype.kind in 'uif'
                    assert values.ndim==2 and (1 in values.shape or values.size==0)
                    flat=values.reshape(-1);pieces.append(flat)
                    locators.append({'matlab_lobe_index':li+1,'mat_shape':list(values.shape),'rows':int(values.size),'raw_array_sha256':sha_bytes(np.asarray(flat,dtype='<f8').tobytes())})
                raw=np.concatenate(pieces);raw_rows+=len(raw)
                valid=np.isfinite(raw)&(raw>=1);sizes=raw[valid]
                assert np.all(sizes==np.floor(sizes))
                sizes=np.asarray(sizes,dtype='<i8');n2=sizes[sizes>=2]
                vectors[(ds,ch,mouse)]=sizes
                manifest.append({'dataset':ds,'source_dataset_index_1based':di+1,'week_as_archived':float(times[di]),
                  'channel':ch,'source_channel_index_1based':ci+1,'mouse_id':mouse,'source_mouse_index_1based':mi+1,
                  'biological_animal_identifier':'not_encoded_in_decoded_size_arrays','lobes':cells.shape[0],
                  'matlab_locator':f'clone_sizes_total{{{di+1}}}{{{mi+1}}}(:,{ci+1})',
                  'raw_clone_rows':len(raw),'invalid_size_rows_excluded':int((~valid).sum()),'valid_clone_rows':len(sizes),
                  'clones_ge2':len(n2),'valid_size_vector_sha256':sha_bytes(sizes.tobytes()),
                  'ge2_size_vector_sha256':sha_bytes(n2.tobytes()),'vector_hash_encoding':'little-endian signed int64; lobe order then source row order',
                  'lobe_source_detail_json':json.dumps(locators,separators=(',',':'))})
    reference=read_csv(refs['batch1_summary']);cross=[]
    for row in reference:
        ds,ch,mouse=row['dataset'],row['channel'],row['mouse_id']
        vv=np.concatenate([vectors[(ds,c,mouse)] for c in channels]) if ch=='combined_YFP_RFP' else vectors[(ds,ch,mouse)]
        current=len(vv[vv>=2]);expected=int(row['proliferative_clones'])
        cross.append({'dataset':ds,'channel':ch,'mouse_id':mouse,'raw_decoded_valid_clones':len(vv),'batch1_valid_clones':int(row['clones']),
                      'raw_decoded_clones_ge2':current,'batch1_clones_ge2':expected,'match':current==expected and len(vv)==int(row['clones'])})
    expected_keys={(ds,'combined_YFP_RFP' if ds.startswith('conf') else ch,m) for ds,ch,m in vectors}
    assert {(r['dataset'],r['channel'],r['mouse_id']) for r in reference}==expected_keys
    assert len(reference)==len(expected_keys) and all(r['match'] for r in cross)
    schema=read_csv(refs['batch1_schema'])
    assert len(schema)==len(lobe_counts) and all(lobe_counts[r['mouse_id']]==int(r['lobes']) for r in schema)

    table=[];discrepancies=[]
    for old in read_csv(refs['audited_table_s1_transcription']):
        ds,ch=old['dataset'],old['channel'];printed=json.loads(old['printed_mouse_counts'])
        selected=sorted((r for r in manifest if (r['dataset'],r['channel'])==(ds,ch)),key=lambda r:r['source_mouse_index_1based'])
        decoded=[r['clones_ge2'] for r in selected]
        assert decoded==json.loads(old['archive_mouse_counts']) and sum(decoded)==int(old['archive_total'])
        assert len(decoded)==int(old['archive_mouse_count']) and sum(printed)==int(old['printed_mouse_sum'])
        issues=[]
        if len(printed)!=len(decoded):issues.append('printed_mouse_list_length_differs_from_archive')
        if any(a!=b for a,b in zip(printed,decoded)):issues.append('printed_mouse_entry_differs_from_archive')
        if sum(printed)!=int(old['printed_total']):issues.append('printed_total_differs_from_printed_mouse_sum')
        if sum(decoded)!=int(old['printed_total']):issues.append('printed_total_differs_from_archive')
        new={'dataset':ds,'channel':ch,'printed_mouse_counts':json.dumps(printed),'printed_mouse_sum':sum(printed),
             'printed_total':int(old['printed_total']),'raw_decoded_mouse_count':len(decoded),
             'raw_decoded_mouse_counts':json.dumps(decoded),'raw_decoded_total':sum(decoded),
             'prior_audit_archive_counts_reproduced':True,'issues':';'.join(issues)}
        table.append(new)
        if issues:discrepancies.append(new)
    primary=[];frequencies=[];primary_datasets=['kras1w','kras2w','kras4w']
    for ds in primary_datasets:
        group=sorted((r for r in manifest if r['dataset']==ds and r['channel']=='RFP'),key=lambda r:r['source_mouse_index_1based'])
        for row in group:
            primary.append({k:row[k] for k in ['dataset','week_as_archived','channel','mouse_id','source_dataset_index_1based','source_mouse_index_1based','source_channel_index_1based','matlab_locator','clones_ge2','ge2_size_vector_sha256']}
               |{'primary_size_min':2,'mouse_evaluation_weight_unnormalized':1,'within_timepoint_normalized_equal_mouse_weight':1/len(group),
                 'exposure':'previously analysed; any future fit is exploratory','animal_id_status':'source mouse index only'})
            vals=vectors[(ds,'RFP',row['mouse_id'])];counts=Counter(int(x) for x in vals if x>=2)
            frequencies.extend({'dataset':ds,'channel':'RFP','mouse_id':row['mouse_id'],'clone_size':size,'clone_count':count} for size,count in sorted(counts.items()))
    assert sum(r['clone_count'] for r in frequencies)==sum(r['clones_ge2'] for r in primary)

    sim=source['sim_two_pop_model.m'];lines=sim.splitlines()
    code=[line.split('%',1)[0].strip() for line in lines]
    start=code.index('elseif chan ==2');end=next(i for i in range(start+1,len(code)) if code[i]=='end')
    env={};assignments=[]
    for i in range(start+1,end):
        if not code[i]:continue
        left,right=code[i].rstrip(';').split('=',1);left,right=left.strip(),right.strip()
        if left=='times':
            assert right=='7*[1,2,4]';value=[7,14,28]
        else:value=arithmetic(right,env)
        env[left]=value;assignments.append({'main_variable':left,'expression':right,'value':value,'source_line_1based':i+1})
    call=next((i,s) for i,s in enumerate(code) if s.startswith('clone_info = function_2_population_model_ageing('))
    signature=next((i,s) for i,s in enumerate(code) if s.startswith('function clone_info = function_2_population_model_ageing('))
    args_call=call[1].split('(',1)[1].split(')',1)[0].split(',')
    args_formal=signature[1].split('(',1)[1].split(')',1)[0].split(',')
    argument_map=[{'position_1based':i+1,'main_argument':a,'formal_parameter':b} for i,(a,b) in enumerate(zip(args_call,args_formal))]
    assert len(args_call)==len(args_formal)==13
    assert [(args_call[i],args_formal[i]) for i in [0,2,5,7,10]]==[('sigma_s','sigma_f'),('sigma_p','sigma_s'),('tausigma_s','tausigma_f'),('tausigma_p','tausigma_s'),('fs','prop_f')]
    required=['params.sigma_s = sigma_s_in;','params.sigma_p = sigma_p_in;','params.fs = fs;',
       'sigma_s = params.sigma_s;','sigma_p = params.sigma_p;','fs =  params.fs;',
       'if t < tau','dt =  - log(1-rand()) / w;','t = t + dt;',
       'elseif ran <= (ws1+ws2+wp2+wp2)/w','if rep <= prop_f*nclones','rep = 0;','nclones = 1000;',
       'sim_clones_size(sim_clones_size <= ignore_clones_of_size) = [];']
    assert all(token in sim for token in required)
    rates=[]
    for phase,fast,slow,r,q in [('early',env['sigmas_s_in'],env['sigmas_p_in'],env['r_in'],env['q_in']),
                               ('late',env['tausigma_s'],env['tausigma_p'],env['taur'],env['tauq'])]:
        for process,sigma,prob in [('fast',fast,r),('slow',slow,q)]:
            rates.append({'phase':phase,'canonical_process':process,'attempt_rate_per_day':sigma,'attempt_rate_per_week':7*sigma,
              'symmetric_renewal_probability':prob,'nominal_birth_rate_per_week':7*sigma*prob,
              'nominal_loss_rate_per_week':7*sigma*(1-prob),'nominal_net_expansion_per_week':7*sigma*(2*prob-1),
              'interpretation':'rates of intended birth-death law; not realised drift of defective event selector'})
    assert np.allclose([r['nominal_net_expansion_per_week'] for r in rates],[3.1,.9,.5,.01])
    nclones=1000;fast_founders=sum(rep<=env['fss_in']*nclones for rep in range(nclones))
    assert fast_founders==81 and env['tau']==14
    parameter_discrepancies=[
      {'item':'fraction','manuscript_table3_symbol':'f_S','manuscript_value':.16,'archive_main_variable':'fss_in / fs','archive_value':env['fss_in'],
       'archive_canonical_allocation':'passed as prop_f, selects fast founders; literal <= boundary gives 81/1000',
       'status':'numerical values differ; manuscript-symbol correspondence unresolved'},
      {'item':'early slow nominal net expansion','manuscript_value_per_week':1.1,'archive_value_per_week':rates[1]['nominal_net_expansion_per_week'],
       'archive_expression':'sigmas_p_in = 0.9/7/(2*q_in-1)','status':'values differ; no silent substitution'},
    ]
    trace={'source_member':'sim_two_pop_model.m','source_sha256':EXPECTED_SIM,'selected_block':'Red2Kras / chan == 2 / RFP',
      'assignments':assignments,'main_to_function_argument_map':argument_map,'call_line_1based':call[0]+1,'function_line_1based':signature[0]+1,
      'canonical_rates':rates,'tau_days':env['tau'],'observation_days':env['times'],
      'schedule':{'early':'event-start t < 14 days','late':'event-start t >= 14 days',
        'literal_boundary_rule':'Propensities are chosen before the waiting-time draw. The old-rate event is applied after t += dt even if it crosses tau; no boundary splitting occurs.',
        'terminal_rule':'The event is applied after advancing time; a crossing event can occur beyond t_max before the next while-condition check.',
        'source_lines_1based':{'while_condition':330,'rate_branch':332,'late_branch':337,'time_draw':346,'time_advance':347,'event_selection':350}},
      'founder_allocation':{'nominal_fs':env['fss_in'],'formal_argument':'prop_f','canonical_process':'fast','nclones':nclones,
        'literal_fast_founders':fast_founders,'literal_fast_fraction':fast_founders/nclones,'basis':'rep starts at 0; rep <= prop_f*nclones; all final nonnegative populations are recorded'},
      'known_source_defect':{'slow_loss_threshold':'(ws1+ws2+wp2+wp2)/w','source_line_1based':356,'status':'preserved; not repaired or simulated in this pass'},
      'manuscript_parameter_differences':parameter_discrepancies,'manuscript_source':'previous visually checked Methods S1 Table 3 transcription in audited REPORT.md; no new PDF transcription',
      'manuscript_symbol_mapping':'unresolved','published_curve_parameter_provenance':'unresolved','fit_or_simulation_executed':False}
    ledger={'table_s1_affected_rows':len(discrepancies),'table_s1_discrepancies':discrepancies,
      'parameter_discrepancies':parameter_discrepancies,
      'scope_limits':['Raw size arrays preserve mouse grouping but do not supply named animal IDs.','No source file, manuscript table, or original output was repaired.',
          'The intended net rates are distinct from the literal defective event-selection process.','No stochastic fit, simulation, likelihood, model comparison, or published-curve attribution was executed.',
          'Future FU_S amendment must freeze source variants, rate-switch handling across the grid, tail diagnostics, unobserved-bin likelihood rules, and common comparator folds/bins/weights.']}
    primary_n=sum(r['clones_ge2'] for r in primary)
    text=f'''# A17 source accounting completed

Fresh decoding of the hash-identified Zenodo v1.1 MAT files reproduces all **{len(cross)} mouse/analysis-channel counts** in batch1. The source contains {len(lobe_counts)} mouse-indexed arrays across {len(datasets)} datasets; both raw channels were decoded separately before matching the original Confetti combination. This closes deterministic input accounting, not published-fit provenance or the future FU_S comparison.

The unchanged primary input is RFP, `kras1w` / `kras2w` / `kras4w`, clone size >=2: **{len(primary)} source-indexed mice and {primary_n:,} clone measurements**. It has four, four and three mice respectively. [Primary manifest](primary_cohort_manifest.csv) retains source coordinates, vector hashes and equal-mouse weights; [size frequencies](primary_clone_size_frequencies.csv) preserve the complete observed size distribution without tail trimming. Stable IDs such as `kras1w:m1` identify nested source entries, not newly recovered animal names. No spatial mouse identity is inferred.

## Table S1 reconciliation

[Fresh reconciliation](table_s1_reconciliation.csv) reproduces all eight prior audit archive-count rows. Five printed table rows remain discrepant:

- At 1 and 2 weeks, both channels print three mouse entries while the archive holds four. The omitted fourth-mouse counts are 1,107 / 851 at 1 week and 4,815 / 2,739 at 2 weeks (YFP / RFP).
- The 2-week YFP third entry prints 1,142; the archive contains 1,152.
- The 4-day RFP entries and archive sum to 922, but the printed total is 10,464.

The transcription and archive values remain separate. The prior visually checked table transcription is a hashed reference; the raw MAT arrays, rather than the prior decoded summary, supply the new counts. [Discrepancy ledger](discrepancy_ledger.json) preserves every affected row and its comparisons.

## Mutant parameter and schedule trace

Positional arguments in the archived RFP call establish **main `sigma_s` -> function `sigma_f` -> fast process** and **main `sigma_p` -> function `sigma_s` -> slow process**. Likewise, `tausigma_s` feeds late fast rates, `tausigma_p` late slow rates, and `fs` feeds `prop_f`. [Machine-readable trace](mutant_parameter_trace.json) includes source line numbers and all units.

| Phase, by event-start time | Fast nominal net expansion | Slow nominal net expansion | Renewal probabilities |
|---|---:|---:|---|
| t < 14 days | 3.1/week | 0.9/week | r=q=0.7 |
| t >= 14 days | 0.5/week | 0.01/week | r=q=0.7 |

These are rates of the intended birth-death law, not the realised drift of the defective event selector. The literal code chooses rates before drawing its waiting time, so an event crossing 14 days retains the old rates. It also applies an event after advancing beyond an observation time before checking the loop again. The repeated slow-loss cumulative term remains documented and unmodified.

The archive's nominal `fs=0.08` allocates fast founders; its zero-based `rep <= prop_f*nclones` boundary gives 81 fast founders per 1,000. Methods S1 Table 3 was previously transcribed as `f_S=0.16` and early slow expansion 1.1/week. Both manuscript values are preserved; manuscript-symbol correspondence and the parameters that produced published curves remain unresolved.

## Executed checks and boundary

[Run record](run_record.json) hashes the archive, consumed MAT/source members, references, executing script and all outputs. Checks passed for nested dimensions, channel order, integer support, lobe pairing, full batch1 count parity, Table S1 archive-count parity, primary frequency totals, argument mapping and arithmetic rate conversion. Completed outputs cannot be overwritten by this script.

No fits, stochastic simulations or model rankings were run. A future exploratory FU_S contract still needs source variants, grid-wide rate switching, tail diagnostics, unobserved-bin likelihood handling and common comparator folds/bins/weights. These exposed data cannot become an independent validation set through this reconciliation.

To reproduce in a new authorized output location, preserve the script and its archive hash and change the explicit output confinement deliberately; the completed audited run is immutable. Runtime: Python {sys.version.split()[0]}, NumPy {np.__version__}, SciPy {scipy.__version__}.
'''
    content={'input_manifest.json':json_text(input_manifest),'mouse_channel_manifest.csv':csv_text(manifest),
      'batch1_count_crosscheck.csv':csv_text(cross),'table_s1_reconciliation.csv':csv_text(table),
      'discrepancy_ledger.json':json_text(ledger),'primary_cohort_manifest.csv':csv_text(primary),
      'primary_clone_size_frequencies.csv':csv_text(frequencies),'mutant_parameter_trace.json':json_text(trace),'REPORT.md':text}
    checks={'archive_hash':True,'all_nested_mice_channels_decoded':True,'integer_support_for_valid_sizes':True,
      'mouse_lobe_spc_shapes_match':True,'batch1_mouse_schema_match':True,'batch1_all_counts_match':True,'table_s1_prior_archive_counts_match':True,
      'primary_frequencies_match_counts':True,'mutant_positional_arguments_match':True,'nominal_rate_arithmetic_match':True,
      'literal_founder_boundary_checked':True,'no_fit_or_simulation':True}
    run={'started_utc':started,'completed_utc':datetime.now(timezone.utc).isoformat(),'specification_checkpoint':input_manifest['specification_checkpoint'],
      'script_sha256':sha(Path(__file__)),'archive_sha256':EXPECTED_ARCHIVE,'input_manifest_sha256':sha_bytes(content['input_manifest.json'].encode()),
      'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'source_mouse_arrays':len(lobe_counts),'source_mouse_channel_rows':len(manifest),
      'raw_clone_measurements':raw_rows,'batch1_reference_rows':len(cross),'primary_mice':len(primary),'primary_clones_ge2':primary_n,
      'table_s1_discrepant_rows':len(discrepancies),'checks':checks,
      'outputs':[{ 'file':name,'sha256':sha_bytes(value.encode('utf-8')),'bytes':len(value.encode('utf-8'))} for name,value in content.items()]}
    content['run_record.json']=json_text(run)
    for name,value in content.items():
        with (out/name).open('x',encoding='utf-8',newline='') as stream:stream.write(value)
    assert all(sha(out/r['file'])==r['sha256'] for r in run['outputs'])
    print(json.dumps({'source_mice':len(lobe_counts),'mouse_channel_rows':len(manifest),'batch1_rows_matching':len(cross),
      'primary_mice':len(primary),'primary_clones_ge2':primary_n,'table_s1_discrepant_rows':len(discrepancies),'fit_or_simulation':False}))

if __name__=='__main__':main()
