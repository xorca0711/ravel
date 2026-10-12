"""P001 metadata/input/sparse-loader stage. No biology, no network."""
import argparse,json,pathlib,sys,time,resource
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from common import ROOT,CONFIG,require_reviewed_job,fresh_output,write_json
from sparse_input import load_triplet

def check_feature_order(reference,var):
 current=var.gene_id.tolist()
 if reference is not None and reference!=current:raise ValueError('cross-library feature ID/order mismatch')
 return current if reference is None else reference

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--reviewed-job');args=p.parse_args();job=require_reviewed_job(args.reviewed_job,'metadata')
 out=fresh_output(args.output,'metadata');manifest=json.loads((CONFIG/'inputs.json').read_text());audits=[];gene_order=None;start=time.monotonic()
 for sample in manifest['samples']:
  t=time.monotonic();X,var,bc,audit=load_triplet(ROOT,manifest['files'],sample['gsm']);gene_order=check_feature_order(gene_order,var);audit['cross_library_feature_id_order']='reference' if not audits else 'equal';audit['load_seconds']=time.monotonic()-t;audit['process_peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;audits.append(audit);del X,var,bc
 write_json(out/'input-readiness.json',{'stage':'metadata','job_id':job['job_id'],'libraries':audits,'cross_library_feature_id_order_equal':True,'elapsed_seconds':time.monotonic()-start,'scope':'integrity and sparse loader only; no cell QC or biology','full_data_memory':'observed stage-specific peak, requires reviewer acceptance'})
if __name__=='__main__':main()
