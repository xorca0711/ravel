"""Supplementary A23 figure resolving the published-versus-filtered cell mismatch."""
import csv,json,hashlib
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[3];RQ=ROOT/'RQ_Specified/A23_slc34a2_transition_homeostasis';RUN='published_cell_audit_v1'
def table(path):
 with path.open(encoding='utf-8') as f:return list(csv.DictReader(f,delimiter='\t'))
def main():
 out=RQ/'figures'/RUN
 if out.exists():raise FileExistsError(out)
 out.mkdir(parents=True)
 plt.rcParams.update({'font.family':'Arial','font.size':9,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'svg.fonttype':'none','savefig.dpi':300})
 old=table(RQ/'tables/external_pilot_v2/annotation_coverage.tsv');new=table(RQ/'tables'/RUN/'marker_differences.tsv')
 fig,axes=plt.subplots(1,2,figsize=(8.6,3.7),layout='constrained')
 a=axes[0];x=np.arange(3);matched=[int(r['matched']) for r in old];missing=[int(r['published_not_filtered']) for r in old]
 a.bar(x,matched,color='#2166AC',label='In filtered matrices');a.bar(x,missing,bottom=matched,color='#B35806',label='Recovered from raw')
 for xx,base,extra in zip(x,matched,missing):
  a.text(xx,base+extra+70,str(base+extra),ha='center',fontsize=8)
  if extra:a.text(xx,base+extra/2,str(extra),ha='center',va='center',color='white',fontsize=8)
 a.set_xticks(x,['PAM CD45−','PAM CD45+','Control'],rotation=15);a.set_ylabel('Published cell barcodes');a.set_ylim(0,7200);a.legend(frameon=False,fontsize=7,loc='upper right');a.set_title('A  Published cell set recovered',loc='left')
 b=axes[1];genes=['KRT8','SPRR1A','CLU','SLC34A2']
 for k,(group,color,marker,label) in enumerate([('published_AT2_all','#2166AC','o','Published AT2'),('published_AT2_primary','#B35806','s','Primary QC'),('published_AT2_strict','#7B3294','^','Strict QC')]):
  xx=[float(next(r['mean_log1p_difference'] for r in new if r['group']==group and r['gene']==g)) for g in genes]
  b.scatter(xx,np.arange(4)+(k-1)*.16,s=24,color=color,marker=marker,label=label)
 b.axvline(0,color='.5',lw=.8);b.set_yticks(np.arange(4),genes);b.set_ylim(3.5,-.7);b.set_xlabel('PAM − control: mean log-normalized RNA');b.legend(frameon=False,fontsize=7,loc='upper left');b.set_title('B  Complete published AT2 comparison',loc='left')
 for ext in ['png','pdf','svg']:fig.savefig(out/('S1_published_cells.'+ext),bbox_inches='tight',facecolor='white')
 plt.close(fig)
 record={'source_receipt_sha256':hashlib.sha256((RQ/'metadata'/RUN/'run_record.json').read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'outputs':[dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(out.iterdir())]}
 (RQ/'metadata'/RUN/'figure_record.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
 print('Saved supplementary source-completeness figure.')
if __name__=='__main__':main()
