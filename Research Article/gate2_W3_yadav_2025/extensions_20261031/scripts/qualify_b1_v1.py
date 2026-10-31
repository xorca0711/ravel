"""B1: author-code/state provenance and explicit resource/retention hold."""
import argparse,json,re
from common_v1 import ROOT,EXT,RUNS,read_csv,save_csv,save_json,sha
CACHE=ROOT/'raw_data/Yd1_checkpoint_b_20261031'
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args()
    out=ROOT/a.output;out.mkdir(exist_ok=True,parents=True)
    spec=json.loads((EXT/'config/checkpoint_b_spec_v1.json').read_text())
    code=(ROOT/spec['X3_code']).read_text();lines=code.splitlines()
    match=re.search(r'annotation\s*<-\s*c\((.*?)\)',code,re.S);assert match
    labels=re.findall(r'"([^"]+)"',match.group(1));assert set(spec['nominated_states'])<=set(labels)
    assert 'names(annotation) <- levels(MG)' in code and 'MG <- RenameIdents(MG, annotation)' in code
    start=code[:match.start()].count('\n')+1
    rows=[dict(annotation_position=i+1,label=label,source_line=start,cluster_binding='levels(MG) at code execution; actual saved-object levels not inspected',nominated=int(label in spec['nominated_states']),provenance='author code, not verified saved-object annotation') for i,label in enumerate(labels)]
    save_csv(out/'author_code_annotation_vector.csv',rows)
    patterns=['write.table(meta','saveRDS(MG','MG@meta.data$sample','@meta.data$Day','@meta.data$treatment','subset(MG, idents','FindClusters(MG','names(annotation)','RenameIdents']
    locators=[dict(line=i+1,text=line) for i,line in enumerate(lines) if any(s in line for s in patterns)]
    save_csv(out/'author_code_locators.csv',locators)
    tree=json.loads((ROOT/spec['X3_repository_tree']).read_text());paths=[r['path'] for r in tree['tree']]
    assert tree['truncated'] is False
    samples=read_csv(RUNS/'Yd1_extension_x0_v1/x3_sample_coverage.csv')
    assert len(samples)==12
    proposed=[]
    for sample in samples:
        for state in spec['nominated_states']:
            proposed.append(dict(sample=sample['sample'],day=sample['day'],proposed_author_label=state,pre_filter_barcodes=sample['pre_filter_barcodes'],author_retained_barcodes='',author_state_cells='',demultiplex_ambiguity='',support_status='unknown; deposited object not accessed',zero_cell_status='not determined; blank is not zero'))
    save_csv(out/'requested_state_support_grid.csv',proposed)
    resource=json.loads((CACHE/'resource_assessment_v1.json').read_text())
    save_json(out/'metadata_hold.json',dict(author_code_reference=tree['sha'],code_sha256=sha(ROOT/spec['X3_code']),repository_files=paths,author_export='meta.txt is written by code lines103-106 but absent from inspected repository tree and GEO listings',small_export_in_tree=any(p.endswith('meta.txt') for p in paths),named_labels_from_code=sorted(set(labels)),nominated_mapping={s:dict(author_code_label=s,saved_object_field=None,verified=False) for s in spec['nominated_states']},retention='unknown; code exclusions cannot establish deposited-object retained barcodes',resource_assessment=resource,expression_bearing_container_accessed=False,RDS_acquired=False,expression_extracted=False,occupancy_estimated=False,decision='Hold actual author-state/retention recovery pending a small exported meta.txt or qualified metadata-only runtime/memory for the specifically authorized object',unchanged_conditional_design=spec['retained_X3_design'],scientific_acceptance='not_assessed'))
    print('B1 author annotation provenance recovered; object-state/retention/support remains explicitly held')
if __name__=='__main__':main()
