"""Frozen six-target/six-library reported-count CPM display; no population inference."""
from pathlib import Path
import argparse,csv,gzip,hashlib,io,json,math
from decimal import Decimal,InvalidOperation
ROOT=Path(__file__).resolve().parents[3]
PRE=ROOT/'docs/research_reviews/2026-11-03-tool-assisted-screening-review/prerequisites'
TARGETS=['Stat6','Egr2','Pparg','Rxra','Irf4','Arg1']
SAMPLES=['WT-CTR_1','WT-CTR_2','WT-IL4_24h_1','WT-IL4_24h_2','WT-pIL4_1','WT-pIL4_2']
GSM=['GSM7903557','GSM7903558','GSM7903565','GSM7903566','GSM7903577','GSM7903578']
OUTPUTS=['target_library_values.tsv','target_condition_summary.tsv','source_library_totals.tsv','rna_context_by_library.png','summary.json']
def require(condition,message):
 if not condition:raise ValueError(message)
def parse_counts(text):
 lines=text.splitlines();require(bool(lines),'empty matrix');header=lines[0].split();require(bool(header) and len(set(header))==len(header),'duplicate/empty sample header')
 values={};positions={};totals=[Decimal(0)]*len(header)
 for line_no,line in enumerate(lines[1:],2):
  tokens=line.split();require(len(tokens)==len(header)+1,'row width');gene=tokens[0];require(gene not in values,'duplicate gene')
  try:row=[Decimal(x) for x in tokens[1:]]
  except InvalidOperation as e:raise ValueError('invalid numeric value') from e
  require(all(x.is_finite() and x>=0 for x in row),'nonfinite/negative value');values[gene]=row;positions[gene]=line_no
  totals=[a+b for a,b in zip(totals,row)]
 require(all(x>0 for x in totals),'nonpositive source total')
 return header,values,positions,totals
def cpm(value,total):return float(value*Decimal(1000000)/total)
def log_cpm(value):return math.log2(value+1.0)
def target_rows(header,values,positions,totals,targets,samples,gsms):
 require(len(set(samples))==len(samples) and len(samples)==len(gsms),'sample roster')
 require(all(s in header for s in samples),'missing sample');require(all(g in values for g in targets),'missing target')
 result=[]
 for order,g in enumerate(targets,1):
  for j,(s,gsm) in enumerate(zip(samples,gsms)):
   idx=header.index(s);v=values[g][idx];x=cpm(v,totals[idx]);condition=['control','initial_IL4_24h','post_IL4'][j//2]
   result.append({'fixed_gene_order':order,'gene':g,'role':'separate_effector' if g=='Arg1' else 'regulator_RNA_context','source_row_1based':positions[g],'GSM':gsm,'source_column':s,'source_column_1based':idx+1,'condition':condition,'library_suffix':s.rsplit('_',1)[1],'reported_gene_value':str(v),'source_gene_total':str(totals[idx]),'reported_count_CPM':x,'log2_CPM_plus1':log_cpm(x),'presence':'observed'})
 return result
def condition_rows(rows,targets):
 result=[]
 for g in targets:
  for condition in ['control','initial_IL4_24h','post_IL4']:
   selected=[r['reported_count_CPM'] for r in rows if r['gene']==g and r['condition']==condition];require(len(selected)==2,'two libraries per condition')
   result.append({'gene':g,'condition':condition,'n_measured_libraries':2,'mean_reported_count_CPM':math.fsum(selected)/2,'min_reported_count_CPM':min(selected),'max_reported_count_CPM':max(selected)})
 return result
def write_tsv(path,rows):
 with path.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
def draw(rows,path):
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 fig,axes=plt.subplots(3,2,figsize=(12,9.7))
 for gene,ax in zip(TARGETS,axes.flat):
  vals=[r for r in rows if r['gene']==gene]
  for j,r in enumerate(vals):ax.scatter(j//2+(-.08 if j%2==0 else .08),r['log2_CPM_plus1'],s=52,color='#ba642c' if gene=='Arg1' else '#245c86',edgecolor='white',linewidth=.5,zorder=3)
  maximum=max(r['log2_CPM_plus1'] for r in vals);ax.set_ylim(0,max(1,maximum*1.16));ax.set_xlim(-.4,2.4)
  ax.set_xticks([0,1,2],['Control','Initial IL-4\n24-hour exposure','Post-IL4\nafter washout/rest']);ax.set_title(gene+(' | separate effector RNA' if gene=='Arg1' else ' | regulator RNA context'),loc='left',fontsize=11)
  ax.grid(axis='y',alpha=.2);ax.spines[['top','right']].set_visible(False)
 fig.suptitle('A3 | Six fixed targets in six source libraries',fontsize=17,x=.07,ha='left')
 fig.supylabel('log2(reported-count CPM + 1)',x=.015)
 fig.subplots_adjust(left=.08,right=.98,bottom=.20,top=.91,hspace=.55,wspace=.20)
 fig.text(.08,.125,'Each point is a measured library; left/right offsets show source suffix _1/_2, with no inferred pairing.\nEach gene has its own y-axis maximum. No gene ranking, mean glyph or trajectory is implied.',fontsize=9)
 fig.text(.08,.055,'CPM denominator: summed deposited gene counts/estimates. Composition, length and unknown batch can affect values.\nControl harvest alignment and preparation sharing are unresolved; RNA abundance is not regulator activity,\nwithdrawal effect, chromatin memory or repair function. Source reports two biological replicates per condition.',fontsize=9)
 fig.savefig(path,dpi=180,facecolor='white');plt.close(fig)
def self_test():
 h,v,p,t=parse_counts('a b\nStat6 0 1.5\nArg1 1.5 0\nBackground 1.5 1.5\n');require(t==[Decimal('3.0'),Decimal('3.0')],'fractional denominator');require(cpm(v['Stat6'][0],t[0])==0,'zero');require(cpm(v['Stat6'][1],t[1])==500000,'all-gene denominator');require(v['Stat6'][1]==Decimal('1.5'),'fraction retained');require(log_cpm(0)==0 and abs(log_cpm(3)-2)<1e-15,'transform')
 failures=['a a\nx 1 2','a b\nx 1','a\nx 1\nx 2','a\nx -1','a\nx NaN','a\nx Infinity','a\nx 0']
 for text in failures:
  try:parse_counts(text)
  except ValueError:pass
  else:raise AssertionError('invalid input accepted')
 for targets,samples in [(['Missing'],['a','b']),(['Stat6'],['a','Missing'])]:
  try:target_rows(h,v,p,t,targets,samples,['x','y'])
  except ValueError:pass
  else:raise AssertionError('missing input accepted')
 hh,vv,pp,tt=parse_counts('c_1 c_2 i_1 i_2 p_1 p_2\nStat6 0 1 2 3 4 5\nBackground 6 5 4 3 2 1\n');rr=target_rows(hh,vv,pp,tt,['Stat6'],hh,['g0','g1','g2','g3','g4','g5']);ss=condition_rows(rr,['Stat6']);require(len(ss)==3 and math.isclose(ss[0]['mean_reported_count_CPM'],1000000/12) and ss[0]['min_reported_count_CPM']==0 and math.isclose(ss[2]['max_reported_count_CPM'],5000000/6),'actual raw-CPM summary');require([r['source_column'] for r in rr]==hh,'fixed order')
 print('PASS: parsing, fractional/zero values, all-gene denominator, transform and seven invalid-input/missing cases')
def main():
 a=argparse.ArgumentParser();a.add_argument('--self-test',action='store_true');a.add_argument('--output',type=Path);args=a.parse_args()
 if args.self_test:self_test();return
 require(args.output is not None,'output required');out=args.output;out.mkdir(parents=True,exist_ok=True);require(not any((out/n).exists() for n in OUTPUTS),'refuse output overwrite')
 manifest=json.loads((PRE/'A3_FULL_SOURCE_SEMANTICS_V1.json').read_text());source=ROOT/'raw_data/source_intake_20261104/A3/GSE247943_rna.counts.tsv.gz';compressed=source.read_bytes();require(hashlib.sha256(compressed).hexdigest()==manifest['compressed_sha256'],'compressed hash');raw=gzip.decompress(compressed);require(hashlib.sha256(raw).hexdigest()==manifest['decompressed_sha256'],'decompressed hash')
 h,v,p,t=parse_counts(raw.decode());require(h==manifest['sample_columns'] and len(v)==24411,'source dimensions/order');require(manifest['target_order']==TARGETS and manifest['selected_columns_in_display_order']==SAMPLES and manifest['selected_GSMs']==GSM,'frozen roster')
 join=list(csv.DictReader((PRE/'A3_GSE247943_HEADER_JOIN_V1.tsv').open(),delimiter='\t'));mapping={r['count_column']:r for r in join};require(len(join)==len(mapping)==52 and set(mapping)==set(h),'full sample join')
 for i,s in enumerate(h):require(int(mapping[s]['column_index_1based'])==i+1,'source column mapping')
 for s,gsm in zip(SAMPLES,GSM):require(mapping[s]['GSM']==gsm,'GSM mapping')
 target_map=list(csv.DictReader((PRE/'A3_FIXED_TARGET_MAP_V1.tsv').open(),delimiter='\t'));require([r['gene'] for r in target_map]==TARGETS,'gene roster')
 for r in target_map:require(int(r['source_row_1based_including_header'])==p[r['gene']] and int(r['exact_matches'])==1,'gene row identity')
 totals=list(csv.DictReader((PRE/'A3_SOURCE_LIBRARY_TOTALS_V1.tsv').open(),delimiter='\t'));require(len(totals)==52,'total rows')
 for i,r in enumerate(totals):require(r['count_column']==h[i] and r['GSM']==mapping[h[i]]['GSM'] and Decimal(r['reported_gene_count_total'])==t[i],'source totals parity')
 rows=target_rows(h,v,p,t,TARGETS,SAMPLES,GSM);summaries=condition_rows(rows,TARGETS);require(len(rows)==36 and len(summaries)==18,'output shape')
 write_tsv(out/OUTPUTS[0],rows);write_tsv(out/OUTPUTS[1],summaries);(out/OUTPUTS[2]).write_bytes((PRE/'A3_SOURCE_LIBRARY_TOTALS_V1.tsv').read_bytes());draw(rows,out/OUTPUTS[3])
 summary={'analysis_id':'A3.rna_context_display_v1','measured_libraries':6,'fixed_targets':6,'library_target_rows':36,'condition_summary_rows':18,'source_gene_rows':24411,'source_libraries':52,'compressed_sha256':manifest['compressed_sha256'],'decompressed_sha256':manifest['decompressed_sha256'],'source_totals_exact_parity':True,'gene_order':TARGETS,'sample_order':SAMPLES,'scope':'Exposed descriptive reported-count CPM in six libraries; preparation/batch and control-duration unknown; no population or withdrawal-effect inference','figure':'Library points only; separate y maxima, zero baseline; raw-CPM means/ranges in table only'}
 (out/OUTPUTS[4]).write_bytes((json.dumps(summary,indent=2)+'\n').encode());print(json.dumps({k:summary[k] for k in ['library_target_rows','condition_summary_rows','source_totals_exact_parity']}))
if __name__=='__main__':main()
