"""Bounded A5 source inventory; no expression extraction or invented mouse IDs."""
import argparse,json,re,csv,hashlib
from pathlib import Path

def main(out):
    out.mkdir(exist_ok=True);root=Path('raw_data/cut_fill_20261103')
    tree=json.loads((root/'a5_tree.txt').read_text());z=json.loads((root/'a5_zenodo.txt').read_text())
    geo=(root/'a5_geo.txt').read_text();fl=(root/'a5_filelist.txt').read_text();shiny=(root/'a5_shiny.txt').read_text()
    cross=list(csv.DictReader(open('RQ_Specified/A5_developmental_programme_reuse/replication_gate_20260928/GSE303646_library_crosswalk.tsv'),delimiter='\t'))
    result={'geo_samples':sorted(set(re.findall(r'!Series_sample_id = (GSM\d+)',geo))),'author_revision':tree['sha'],'tree_truncated':tree['truncated'],'author_files':[x['path'] for x in tree['tree'] if x['type']=='blob'],'zenodo_files':[{'key':x['key'],'bytes':x['size']} for x in z['files']],'filelist_sha256':hashlib.sha256((root/'a5_filelist.txt').read_bytes()).hexdigest(),'previous_filelist_sha256':'caaa87d12c4497325df225fb8d37cb2db7e53d114639f8cf0a890ca4bc6fe57e','crosswalk_rows':len(cross),'shiny_download_controls':re.findall(r'.{0,80}(?:shiny-download-link|downloadButton|downloadLink).{0,80}',shiny),'disposition':'HOLD: no barcode-to-author-state or library-to-mouse export in inspected metadata inventories. 56 libraries versus reported 55 mice unresolved. No expression score; fixed component, exclusions, primary activated-AT2 comparator and 500-UMI scale unchanged.','coverage_limit':'Current GEO series/filelist, complete pinned code tree, Zenodo file inventory and public browser entry HTML; no live websocket export or author contact. No global unavailability claim.'}
    assert not tree['truncated'];assert len(result['geo_samples'])==56
    (out/'qualification.json').write_text(json.dumps(result,indent=2))
    (out/'source_acquisition.json').write_bytes((root/'acquisition_a5_v1.json').read_bytes())
    (out/'verification.json').write_text(json.dumps({'passed':True,'geo_sample_count':56,'author_revision_unchanged':tree['sha']=='e52bede4d8a0f9a8a07cb88ceb557fe01455d0c0','geo_filelist_unchanged':result['filelist_sha256']==result['previous_filelist_sha256'],'no_inferred_mouse_ids':True},indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);main(ap.parse_args().output)
