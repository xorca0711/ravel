"""Checkpoint C source/sample/feature metadata only; never opens expression files."""
import argparse,csv,gzip,hashlib,json,re,xml.etree.ElementTree as ET
from common_v1 import ROOT,EXT,save_csv,save_json,sha
CACHE=ROOT/'raw_data/Yd1_checkpoint_c_20261031'

def fields(path,prefix):
    d={}
    for line in path.read_text(encoding='utf-8').splitlines():
        if line.startswith(prefix) and ' = ' in line:
            key,val=line.split(' = ',1);d.setdefault(key[len(prefix):],[]).append(val)
    return d
def one(d,k):return '; '.join(d.get(k,[]))
def attributes(values):
    return {k.strip().lower():v.strip() for k,v in (x.split(':',1) for x in values if ':' in x)}
def csvread(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args()
    out=ROOT/a.output;out.mkdir(parents=True,exist_ok=True)
    spec=json.loads((EXT/'config/checkpoint_c_spec_v1.json').read_text())
    assert not any(p.suffix in {'.h5','.h5ad','.rds','.tar'} or '_matrix.' in p.name for p in CACHE.iterdir())
    parent=fields(CACHE/'GSE145231.txt','!Series_')
    assert 'SuperSeries of: GSE145230' in parent['relation']
    series_rows=[];samples=[];attrs=[];runs=[];files=[];support=[];coverage=[]
    for source in spec['sources']:
        gse=source['series'];s=fields(CACHE/(gse+'.txt'),'!Series_')
        assert s['geo_accession']==[gse]
        if source['parent']:assert 'SubSeries of: '+source['parent'] in s['relation']
        series_rows.append(dict(study=source['study'],series=gse,parent=source['parent'],last_update=one(s,'last_update_date'),public_status=one(s,'status'),pubmed=one(s,'pubmed_id'),reported_sample_records=len(s['sample_id']),relations=one(s,'relation'),source_record=gse+'.txt'))
        bios={b.get('accession'):b for b in ET.parse(CACHE/(gse+'_biosamples.xml')).findall('.//BioSample')}
        runrows=csvread(CACHE/(gse+'_runinfo.csv'))
        for gsm in s['sample_id']:
            m=fields(CACHE/(gsm+'.txt'),'!Sample_')
            ch=attributes(m.get('characteristics_ch1',[]))
            bs=re.search(r'biosample/(SAMN\d+)',one(m,'relation')).group(1)
            sx=re.search(r'term=(SRX\d+)',one(m,'relation')).group(1)
            assert bs in bios
            bam={x.get('attribute_name').lower():x.text or '' for x in bios[bs].findall('.//Attribute')}
            for key,val in bam.items():attrs.append(dict(study=source['study'],GSM=gsm,BioSample=bs,attribute=key,value=val))
            for key,val in ch.items():
                assert key in bam and val.casefold()==bam[key].casefold(),(gsm,key,val,bam.get(key))
            rr=[r for r in runrows if r['Experiment']==sx]
            assert rr and all(r['BioSample']==bs for r in rr)
            title=one(m,'title');token=re.search(r'(?:Gran|Neut|WB)_([o]?[FM]\d+)',title)
            sample=dict(study=source['study'],series=gse,GSM=gsm,title=title,BioSample=bs,SRA_experiment=sx,SRA_runs=';'.join(r['Run'] for r in rr),source=one(m,'source_name_ch1'),sex=ch.get('gender',ch.get('sex','')),age=ch.get('age',''),cells=ch.get('cells',ch.get('tissue','')),purification=ch.get('purification','RBC depletion; GEO extraction protocol'),library_protocol=one(m,'extract_protocol_ch1'),processing=one(m,'data_processing'),instrument=one(m,'instrument_model'),sample_last_update=one(m,'last_update_date'),experimental_id=ch.get('description for exp id',''),lab_data_id=ch.get('lab  data id',''),title_token_unverified=token.group(1) if token else '',donor_id='',donor_join_status='no explicit participant crosswalk; title token is not a verified donor join',fresh_frozen='not explicitly supplied in inspected sample/BioSample fields',collection_or_processing_time='not supplied; embedded lab-ID dates and SRA load/release dates are not collection times')
            samples.append(sample)
            for r in rr:
                runs.append({k:r.get(k,'') for k in ['Run','Experiment','BioSample','Sample','SampleName','LibraryName','LibraryStrategy','LibrarySelection','LibrarySource','LibraryLayout','Platform','Model','SRAStudy','BioProject','Subject_ID','Sex','ReleaseDate','LoadDate']}|dict(study=source['study'],GSM=gsm))
            labels=source['state_labels'] if source['study']=='Gupta2020' or ch.get('cells')=='purified neutrophils' else []
            coverage.append(dict(study=source['study'],GSM=gsm,source_context=sample['cells'],published_label_candidates=';'.join(labels),label_context=source['state_context'] if labels else 'Published purified-cell state labels not transferred to this preparation',author_retained_barcodes='',author_state_field='',author_state_assignments='',complete_target_zero_denominator='',cell_calls_and_state_join='unavailable; no matrix downloaded or classifier run'))
            feature_names=[u.rsplit('/',1)[-1] for k,v in m.items() if k.startswith('supplementary_file') for u in v if u.endswith('_genes.tsv.gz')]
            for gene in spec['targets']:
                if feature_names:
                    assert len(feature_names)==1
                    fp=CACHE/feature_names[0]
                    with gzip.open(fp,'rt',encoding='utf-8') as f:fr=list(csv.reader(f,delimiter='\t'))
                    matches=[(i+1,r) for i,r in enumerate(fr) if len(r)>1 and r[1]==gene]
                    support.append(dict(study=source['study'],GSM=gsm,target=gene,feature_file=fp.name,feature_sha256=sha(fp),feature_rows=len(fr),matched_rows=len(matches),row_1based=';'.join(str(i) for i,r in matches),feature_ids=';'.join(r[0] for i,r in matches),feature_types=';'.join(sorted(set(r[2] for i,r in matches if len(r)>2))),measurement_support='listed in original feature reference; not evidence of detected transcript' if len(matches)==1 else 'held: missing or ambiguous feature identity',expression_read=False))
                else:
                    support.append(dict(study=source['study'],GSM=gsm,target=gene,feature_file='',feature_sha256='',feature_rows='',matched_rows='',row_1based='',feature_ids='',feature_types='',measurement_support='unverified; features embedded in expression H5, no small feature export in inspected listing',expression_read=False))
        with (CACHE/(gse+'_filelist.txt')).open(encoding='utf-8') as f:
            for r in csv.DictReader(f,delimiter='\t'):
                p=CACHE/r['Name'];acquired=p.exists()
                if acquired:assert p.stat().st_size==int(r['Size'])
                files.append(dict(study=source['study'],series=gse,kind=r['#Archive/File'],filename=r['Name'],listed_modified=r['Time'],listed_bytes=int(r['Size']),format=r['Type'],acquired=acquired,acquired_sha256=sha(p) if acquired else '',decision='feature-only metadata acquired' if acquired else 'not acquired; no expression/H5/archive or large raw-barcode list authorized for this pass'))
        assert set(r['Experiment'] for r in runrows)=={r['SRA_experiment'] for r in samples if r['series']==gse}
    save_csv(out/'series_relations.csv',series_rows)
    save_csv(out/'sample_library_map.csv',samples)
    save_csv(out/'biosample_attributes.csv',attrs)
    save_csv(out/'sequencing_run_map.csv',runs)
    save_csv(out/'file_inventory.csv',files)
    save_csv(out/'target_feature_support.csv',support)
    save_csv(out/'state_denominator_coverage.csv',coverage)
    overlap={}
    for key in ['BioSample','SRA_experiment']:
        groups=[{r[key] for r in samples if r['study']==s['study']} for s in spec['sources']]
        overlap[key]=sorted(groups[0]&groups[1])
    rgroups=[{r['Run'] for r in runs if r['study']==s['study']} for s in spec['sources']]
    overlap['SRA_Run']=sorted(rgroups[0]&rgroups[1])
    save_json(out/'source_decision.json',dict(series_sample_records={r['series']:r['reported_sample_records'] for r in series_rows},sequencing_run_records=len(runs),listed_files=len(files),metadata_feature_files_acquired=sum(r['acquired'] for r in files),cross_study_accession_intersections=overlap,participant_overlap='unresolved; distinct accessions, common authors or matching title tokens cannot prove donor independence or reuse',scahn_context='Both studies already contribute to SCAHN; SCAHN-retained cells and exact 18-of-19 Wigerblad inclusion join unresolved',Gupta='preferred conditional source; original feature coverage recovered but retained neutrophil/state/target-zero and donor joins held',Wigerblad='sole fallback checked; mixed preparation libraries and missing small feature/retained-state exports prevent execution',proposed_description=spec['proposed_description'],expression_container_accessed=False,target_expression_calculated=False,new_classifier=False,scientific_acceptance='not_assessed'))
    print('C metadata mapped; two source eligibility holds retained, no expression accessed')
if __name__=='__main__':main()
