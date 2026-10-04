"""Qualify remaining source boundaries and preserve every failed-run byte."""
import argparse,csv,hashlib,importlib.util,json,re,shutil,zipfile
from pathlib import Path

FAILED=['wg_source_scores_v1','wg_source_scores_v2','wg_bulk_paired_descriptive_v1']
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write_json(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def tsv(p,rows,fields):
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t');w.writeheader();w.writerows(rows)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);out=ap.parse_args().output
    root=Path('raw_data/wagner_closeout_20261004');archives=[]
    for name in FAILED:
        src=Path('analysis/research/runs')/name
        receipt=json.loads((src/'receipt.json').read_text());assert receipt['status']=='execution_failed'
        for p in sorted(src.iterdir()):
            assert p.is_file(),'Unexpected nested failed artifact'
            target=out/f'failed_{name}__{p.name}'
            before=digest(p);shutil.copyfile(p,target);assert digest(target)==before==digest(p)
            archives.append(dict(original_path=p.as_posix(),archive_file=target.name,sha256=before,original_status='execution_failed'))
    write_json(out/'failure_preservation.json',{'status':'byte_preservation_verified','original_git_checkpoint':'30bf90d','files':archives,'limit':'Successful metadata/archive execution does not change any failed scientific status. Originals remain byte-identical locally and in earlier commits. Successful wrapper copies replace unsuccessful registry entries using the existing Nb5 preservation pattern; no validator changes.'})
    acquisition={p.name:json.loads(p.read_text()) for p in sorted(root.glob('*.json'))}
    write_json(out/'acquisition_records.json',acquisition)
    # Pin identity includes the Git object hash, not just an unversioned URL.
    manifest=json.loads((root/'compass_acquisition_v1.json').read_text());rows=[]
    for r in manifest['files']:
        assert 'error' not in r
        p=Path(r['path']);assert digest(p)==r['sha256']
        b=p.read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['git_blob_sha']
        rows.append({k:r[k]for k in ['source_path','path','bytes','sha256','git_blob_sha','url']})
    tsv(out/'compass_source_inventory.tsv',rows,list(rows[0]))
    model=root/'compass_2021/compass/Resources/Recon2_export/recon2_md.zip'
    with zipfile.ZipFile(model) as z:assert z.testzip() is None;members=z.namelist()
    with (root/'compass_2021/compass/Resources/Recon2_export/rxn_md.csv').open(encoding='utf-8-sig',newline='') as f:old=list(csv.DictReader(f))
    with Path('raw_data/wagner_r0_20261004/reaction_metadata.csv').open(encoding='utf-8-sig',newline='') as f:current=list(csv.DictReader(f))
    a={r['rxn_code_nodirection'] for r in old};b={r['reaction_no_direction']for r in current};assert len(a)==len(old) and len(b)==len(current)
    with Path('raw_data/wagner_r0_20261004/linear_gene_expression_matrix.tsv').open(encoding='utf-8-sig') as f:
        reader=csv.reader(f,delimiter='\t');header=next(reader);gene_count=sum(1 for _ in reader)
    write_json(out/'R2_qualification.json',{'historical_candidate_commit':manifest['pin'],'historical_source_files_verified':len(rows),'model_zip_members':members,'undirected_reactions_historical':len(a),'undirected_reactions_example':len(b),'shared_reaction_ids':len(a&b),'historical_only':sorted(a-b),'example_only':sorted(b-a),'expression_features':gene_count,'expression_columns':len(header)-1,'cplex_python_available':importlib.util.find_spec('cplex') is not None,'cplex_on_path':shutil.which('cplex'),'decision':'HOLD historical expression-to-score execution','reasons':['Historical CPLEX Python API/runtime and license are not qualified; no solver smoke or full run performed.','Published-era code commit is a candidate, not proven manuscript execution identity.','Exact preprocessing/ortholog, neighborhood, medium and solver settings remain incompletely reconstructed.'],'observed_historical_defaults':{'model':'RECON2_mat','species':'required argument','lambda_smoothing':0,'paper_typical_sharing_not_default':0.25,'AND_function':'mean','beta':0.95},'limit':'Reaction-ID overlap does not establish equal stoichiometry, bounds, model provenance, numerical penalties or the missing S2 metareaction grouping. No modern-solver substitution.'})
    # Recover ATAC labels directly from raw SOFT and independently compare the R0 table.
    soft=Path('raw_data/wagner_r0_20261004/GSE165088_family.soft').read_text(encoding='utf-8-sig');samples=[]
    for block in soft.split('^SAMPLE = ')[1:]:
        gsm=block.splitlines()[0].strip();title=re.search(r'^!Sample_title = (.+)$',block,re.M).group(1).strip()
        attrs=dict((a.strip(),b.strip())for a,b in re.findall(r'^!Sample_characteristics_ch1 = ([^:]+): (.+)$',block,re.M))
        samples.append({'gsm':gsm,'title':title,'animal_id':attrs['animal_id'],'cell_type':attrs['cell type'],'treatment':'DFMO' if attrs['treatment']=='DFMO' else 'control','genome':'mm10'})
        assert 'Genome_build: mm10' in block
    assert len(samples)==12 and len({r['animal_id']for r in samples})==3
    assert {r['cell_type']for r in samples}=={'Th17n','iTreg'}
    assert len({(r['animal_id'],r['cell_type'],r['treatment'])for r in samples})==12
    with Path('analysis/research/runs/wg_source_qualification_v1/samples.tsv').open(encoding='utf-8',newline='') as f:r0={r['gsm']:r for r in csv.DictReader(f,delimiter='\t')if r['series']=='GSE165088'}
    for r in samples:
        assert (r0[r['gsm']]['title'],r0[r['gsm']]['animal_id'],r0[r['gsm']]['cell_type'])==(r['title'],r['animal_id'],r['cell_type'])
    tsv(out/'R4_source_samples.tsv',samples,list(samples[0]))
    write_json(out/'R4_qualification.json',{'source_records':12,'animal_labels':3,'lineages':['Th17n','iTreg'],'conditions':['control','DFMO'],'genome':'mm10','source_time':'68 h, source figure/GEO design','source_map_independent_join':'12/12 exact to earlier R0 table','count_matrix_available':False,'expected_filename':'GSE165088_Raw_Count_Data.csv.gz','expected_bytes':1128862,'decision':'HOLD peak-level numerical analysis','blocking_conditions':['Exact count matrix and peak interval universe not retrieved after public GEO HTTP, FTP and browser attempts.','S7 values and exact external motif/ChIP annotation universe remain inaccessible.','DESeq2 package-set process returned abnormal exit -1073741569; no real DESeq2 execution.'],'source_contradiction':'STAR Methods mentions an unpublished Th17p ATAC comparison; the deposited series and S7 legend describe only Th17n/iTreg. No Th17p peak or cross-assay physical pairing is invented.','unblocking_evidence':'Valid GSE165088 count matrix with peak coordinates, S7 and annotation definitions; qualified DESeq2 process; new frozen numerical contract.'})
    functional=[
      ('3','Extracellular flux, metabolite abundance, isotope fractions, lipid endpoints','Assay-labelled independent culture/preparation; distinguish fractions and pool sizes','Qualitative source/legend evidence only'),
      ('4','Polyamine-related enzyme and metabolite/label observations','Assay-specific culture/preparation; reaction scores remain cell-level measurements','Qualitative orthogonal evidence; R1 supplies score values only'),
      ('5/S5','Drug/genetic perturbation, cytokines, transcription factors, rescue, viability/proliferation','Mouse/preparation, with wells/cells nested; exact raw replicate map unavailable','Qualitative source evidence; no new function or conversion inference'),
      ('6G/S6','JMJD3-by-DFMO functional readouts','Source mouse/preparation; 120-hour readout is not the 68-hour RNA endpoint','Qualitative only; R3 RNA interaction is a separate endpoint'),
      ('7','EAE longitudinal course, recall and tissue T-cell phenotype','Mouse, repeated time points within mouse','Qualitative disease evidence; no re-estimated treatment effect')]
    tsv(out/'R5_availability.tsv',[{'source_panel':a,'endpoint':b,'required_unit':c,'current_evidence':d,'raw_values':'not recovered from inspected paper/supplement catalogue/GEO/example source','decision':'HOLD numerical reproduction; retain qualitative evidence'}for a,b,c,d in functional],['source_panel','endpoint','required_unit','current_evidence','raw_values','decision'])
    write_json(out/'qualification.json',{'scope':'Remaining-stage source eligibility and byte-preserving failure archive; no new biological contrasts','R2':'historical source/model files qualified; execution held','R4':'12 source labels/mm10 verified; peak numerics held','R5':'bounded panel/source availability audit closed with numerical holds','failure_files_preserved':len(archives),'RQ_derivation':'not started','scientific_acceptance':'not assessed'})
    print(json.dumps({'status':'qualified_with_explicit_holds','failed_files_preserved':len(archives),'ATAC_source_records':len(samples)}))
if __name__=='__main__':main()
