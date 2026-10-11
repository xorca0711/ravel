"""P001 metadata/input/sparse-loader stage. No biology, no network."""
import argparse,json,pathlib,sys,time,resource
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from common import ROOT,CONFIG,require_reviewed_job,fresh_output,write_json
from sparse_input import load_triplet

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--reviewed-job');args=p.parse_args();job=require_reviewed_job(args.reviewed_job,'metadata')
 out=fresh_output(args.output,'metadata');manifest=json.loads((CONFIG/'inputs.json').read_text());audits=[];start=time.monotonic()
 for sample in manifest['samples']:
  t=time.monotonic();X,var,bc,audit=load_triplet(ROOT,manifest['files'],sample['gsm']);audit['load_seconds']=time.monotonic()-t;audit['process_peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss;audits.append(audit);del X,var,bc
 write_json(out/'input-readiness.json',{'stage':'metadata','job_id':job['job_id'],'libraries':audits,'elapsed_seconds':time.monotonic()-start,'scope':'integrity and sparse loader only; no cell QC or biology','full_data_memory':'observed stage-specific peak, requires reviewer acceptance'})
if __name__=='__main__':main()
