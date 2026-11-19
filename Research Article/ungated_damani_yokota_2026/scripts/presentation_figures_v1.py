"""Four presentation derivatives of reviewed DY1 tables; no biological refits."""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.text import Text
import pandas as pd
from PIL import Image

ARTICLE=Path('Research Article/gate2_DY1_damani_yokota_2026')
PARAMETERS=ARTICLE/'config/presentation_parameters_v1.json'
BLUE='#356b8c';ORANGE='#bd6d35';TEAL='#4c8072';INK='#24313b';GRAY='#77828a'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.titlesize':11,
    'axes.labelsize':10,'xtick.labelsize':9,'ytick.labelsize':9,'axes.spines.top':False,
    'axes.spines.right':False,'axes.linewidth':.7,'svg.fonttype':'none','pdf.fonttype':42,
    'svg.hashsalt':'DY1_presentation_v1','savefig.facecolor':'white','figure.facecolor':'white'})


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def repository_path(path):return Path(path).resolve().relative_to(Path.cwd().resolve()).as_posix()


def unique_row(frame,key):
    selected=frame
    for column,value in key.items():selected=selected[selected[column]==value]
    if len(selected)!=1:raise ValueError('Expected one source row: '+json.dumps(key))
    return selected.iloc[0]


class Audit:
    """Bind every displayed numeric value to source rows, text, and coordinates."""
    def __init__(self,tables,paths):
        self.tables=tables;self.paths=paths;self.values=[];self.labels=[];self.coordinates=[]
    def number(self,table,key,column,factor=1,fmt='.3f'):
        raw=float(unique_row(self.tables[table],key)[column])
        if not math.isfinite(raw):raise ValueError('Undefined displayed source value')
        record=dict(id=f'value_{len(self.values):04d}',source=self.paths[table],key=key,column=column,
            source_value=raw,factor=factor,visual_value=raw*factor,format=fmt,label=format(raw*factor,fmt))
        self.values.append(record);return record
    def text(self,artist,records=()):
        content=artist.get_text()
        for r in records:
            if r['label'] not in content:raise ValueError('Displayed numeric label missing')
        gid=f'label_{len(self.labels):04d}';artist.set_gid(gid)
        self.labels.append(dict(id=gid,text=content,value_ids=[r['id'] for r in records]))
        return artist
    def line(self,artist,records):
        observed=[float(x) for x in artist.get_xdata()]
        expected=[r['visual_value'] for r in records]
        if observed!=expected:raise ValueError('Artist/source coordinate mismatch')
        gid=f'coordinate_{len(self.coordinates):04d}';artist.set_gid(gid)
        self.coordinates.append(dict(id=gid,kind='line_x',value_ids=[r['id'] for r in records],observed=observed))
    def bar(self,artist,record):
        observed=float(artist.get_width())
        if observed!=record['visual_value']:raise ValueError('Artist/source bar mismatch')
        gid=f'coordinate_{len(self.coordinates):04d}';artist.set_gid(gid)
        self.coordinates.append(dict(id=gid,kind='bar_width',value_ids=[record['id']],observed=[observed]))


def frame(title,subtitle):
    fig=plt.figure(figsize=(11.8,8.0),dpi=100)
    fig.text(.055,.955,title,fontsize=16,weight='bold',color=INK,va='top')
    fig.text(.055,.911,subtitle,fontsize=10.5,color=GRAY,va='top')
    return fig


def axes(fig,box,title,xlim,xlabel):
    ax=fig.add_axes(box);ax.set_title(title,loc='left',pad=17,weight='bold',color=INK)
    ax.set_xlim(*xlim);ax.set_xlabel(xlabel,labelpad=10);ax.set_axisbelow(True)
    ax.grid(axis='x',color='#e5e8eb',lw=.7);ax.tick_params(axis='y',length=0,pad=10)
    ax.spines['left'].set_visible(False)
    return ax


def footer(fig,lines):
    if not 2<=len(lines)<=3 or len(' '.join(lines).split())>65:raise ValueError('Caption exceeds compact limit')
    artist=fig.text(.055,.045,'\n'.join(lines),fontsize=9,linespacing=1.5,va='bottom',color=INK)
    artist.set_gid('caption');return artist


def layout_check(fig,caption):
    fig.canvas.draw();renderer=fig.canvas.get_renderer();width,height=fig.canvas.get_width_height()
    boxes=[]
    for artist in fig.findobj(Text):
        if not artist.get_visible() or not artist.get_text().strip():continue
        box=artist.get_window_extent(renderer)
        if box.width<=0 or box.height<=0:continue
        if min(box.x0,box.y0)<2 or box.x1>width-2 or box.y1>height-2:
            raise ValueError('Text outside canvas: '+artist.get_text())
        boxes.append((artist.get_text(),box))
    overlaps=[]
    for i,(first,a) in enumerate(boxes):
        for second,b in boxes[i+1:]:
            if min(a.x1,b.x1)-max(a.x0,b.x0)>1 and min(a.y1,b.y1)-max(a.y0,b.y0)>1:
                overlaps.append([first,second])
    if overlaps:raise ValueError('Overlapping text: '+repr(overlaps[:4]))
    cap=caption.get_window_extent(renderer);plot_bottom=min(ax.get_tightbbox(renderer).y0 for ax in fig.axes)
    if cap.y1+12>=plot_bottom:raise ValueError('Caption overlaps plot area')
    return dict(text_items=len(boxes),text_inside_canvas=True,text_overlap_pairs=0,
        caption_lines=len(caption.get_text().splitlines()),caption_font_points=9,
        caption_words=len(caption.get_text().split()),caption_clearance_pixels=float(plot_bottom-cap.y1),
        canvas_inches=list(fig.get_size_inches()),caption_bounds_pixels=list(cap.bounds))


def representation(tables,params,audit):
    p=params['plates'][0];fig=frame(p['title'],p['subtitle'])
    left=axes(fig,[.22,.25,.36,.54],'A  Direction agreement',(0,100),'Agreement with RNA direction (%)')
    right=axes(fig,[.69,.25,.27,.54],'B  Mixed ATAC directions',(0,100),'Genes with both ATAC directions (%)')
    labels=[]
    for i,mapping in enumerate(params['mappings']):
        key={k:mapping[k] for k in ['mapping_rule','distance_subset']};y=3-i;labels.append(mapping['label'])
        pair=audit.number('weighting',key,'pair_weighted_same',100,'.3f')
        equal=audit.number('weighting',key,'equal_gene_same',100,'.3f')
        shift=audit.number('weighting',key,'equal_gene_minus_pair_weighted',100,'+.3f')
        for dy,r,color in [(.14,pair,BLUE),(-.14,equal,ORANGE)]:
            patch=left.barh(y+dy,r['visual_value'],height=.20,color=color)[0];audit.bar(patch,r)
            audit.text(left.text(r['visual_value']+1.7,y+dy,r['label'],va='center',fontsize=8.5),[r])
        audit.text(left.text(86,y,shift['label']+' pp',ha='center',va='center',fontsize=8.5,color=INK),[shift])
        frac=audit.number('weighting',key,'mixed_atac_gene_fraction',100,'.2f')
        n=audit.number('weighting',key,'mixed_atac_genes',fmt=',.0f');total=audit.number('weighting',key,'genes',fmt=',.0f')
        patch=right.barh(y,frac['visual_value'],height=.32,color=TEAL)[0];audit.bar(patch,frac)
        audit.text(right.text(2,y+.33,n['label']+' / '+total['label']+' genes',fontsize=8.5,va='center'),[n,total])
        audit.text(right.text(frac['visual_value']+2,y,frac['label']+'%',fontsize=8.5,va='center'),[frac])
    for ax in [left,right]:ax.set_ylim(-.55,3.60);ax.set_yticks([3,2,1,0],labels if ax==left else ['']*4);ax.set_xticks([0,25,50,75,100])
    # Label colors directly; no duplicate legend axes or detached units.
    audit.text(fig.text(.22,.855,'Region weight',color=BLUE,fontsize=9))
    audit.text(fig.text(.335,.855,'Equal gene weight',color=ORANGE,fontsize=9))
    audit.text(fig.text(.49,.855,'Shift (pp)',color=INK,fontsize=9))
    return fig,footer(fig,p['caption'])


def scope_key(scope):return {k:scope[k] for k in ['cohort','population','floor','scope']}


def human_contrasts(tables,params,audit):
    p=params['plates'][1];fig=frame(p['title'],p['subtitle'])
    aa=[axes(fig,[x,.24,.285,.57],letter+'  '+name,(-2.3,4.0),'IPF - Control\nMean gene log2(CPM + 1)')
        for x,letter,name in [(.345,'A','FABP4 panel'),(.685,'B','Matrix-associated panel')]]
    labels=[]
    for i,scope in enumerate(params['human_scopes']):
        y=5-i;key=dict(scope_key(scope),kind='contrast',group='IPF-Control',measure='FABP4_panel')
        ni=audit.number('full',key,'n_first',fmt='.0f');nc=audit.number('full',key,'n_second',fmt='.0f')
        labels.append(scope['label']+'\n'+ni['label']+' IPF / '+nc['label']+' Control donors')
        for j,panel in enumerate(['FABP4_panel','matrix_mac_panel']):
            key=dict(scope_key(scope),kind='contrast',group='IPF-Control',measure=panel)
            estimate=audit.number('full',key,'estimate',fmt='+.3f');lo=audit.number('full',key,'original_ci_low',fmt='+.3f');hi=audit.number('full',key,'original_ci_high',fmt='+.3f')
            color=BLUE if scope['cohort']=='GSE136831' else TEAL
            line,=aa[j].plot([lo['visual_value'],hi['visual_value']],[y,y],color=color,lw=2.1);audit.line(line,[lo,hi])
            point,=aa[j].plot([estimate['visual_value']],[y],'o',color=color,ms=5);audit.line(point,[estimate])
            text=estimate['label']+' ['+lo['label']+', '+hi['label']+']'
            audit.text(aa[j].text(.98,y+.30,text,transform=aa[j].get_yaxis_transform(),ha='right',fontsize=8.3),[estimate,lo,hi])
    for j,ax in enumerate(aa):
        ax.set_ylim(-.55,5.65);ax.set_yticks(range(5,-1,-1),labels if j==0 else ['']*6);ax.set_xticks([-2,-1,0,1,2,3,4]);ax.axvline(0,color=GRAY,lw=.9)
    # Bind displayed donor counts and scope labels as complete label objects.
    for text,scope in zip(aa[0].get_yticklabels(),params['human_scopes']):
        key=dict(scope_key(scope),kind='contrast',group='IPF-Control',measure='FABP4_panel')
        audit.text(text,[audit.number('full',key,'n_first',fmt='.0f'),audit.number('full',key,'n_second',fmt='.0f')])
    return fig,footer(fig,p['caption'])


def human_coupling(tables,params,audit):
    p=params['plates'][2];fig=frame(p['title'],p['subtitle'])
    aa=[axes(fig,[x,.29,.217,.49],title,(-1,1),'Within-IPF Spearman correlation') for x,title in
        [(.235,'A  Original 95% interval'),(.49,'B  Component omission range'),(.745,'C  Donor omission range')]]
    labels=[]
    for i,index in enumerate([0,2]):
        scope=params['human_scopes'][index];y=1-i;key=dict(scope_key(scope),kind='association',group='IPF',measure='FABP4_vs_matrix')
        est=audit.number('full',key,'estimate',fmt='+.3f');n=audit.number('full',key,'n_first',fmt='.0f')
        labels.append(scope['coupling_label']+'\n'+scope['cohort']+' | '+n['label']+' IPF donors')
        for j in range(3):
            if j==0:
                low=audit.number('full',key,'original_ci_low',fmt='+.3f');high=audit.number('full',key,'original_ci_high',fmt='+.3f');color=INK
            else:
                skey=dict(key,diagnostic='leave_component_out' if j==1 else 'leave_donor_out')
                low=audit.number('robustness',skey,'minimum',fmt='+.3f');high=audit.number('robustness',skey,'maximum',fmt='+.3f');color=ORANGE if j==1 else BLUE
                ref=audit.number('robustness',skey,'reference',fmt='+.3f')
                if not math.isclose(ref['visual_value'],est['visual_value'],abs_tol=1e-12):raise ValueError('Omission/full reference mismatch')
            line,=aa[j].plot([low['visual_value'],high['visual_value']],[y,y],color=color,lw=3);audit.line(line,[low,high])
            point,=aa[j].plot([est['visual_value']],[y],'o',color='black',ms=5,zorder=3);audit.line(point,[est])
            text=est['label']+' ['+low['label']+', '+high['label']+']'
            audit.text(aa[j].text(.5,y+.24,text,transform=aa[j].get_yaxis_transform(),ha='center',fontsize=8.5),[est,low,high])
    for j,ax in enumerate(aa):
        ax.set_ylim(-.45,1.55);ax.set_yticks([1,0],labels if j==0 else ['','']);ax.set_xticks([-1,-.5,0,.5,1]);ax.axvline(0,color=GRAY,lw=.8)
    for text,index in zip(aa[0].get_yticklabels(),[0,2]):
        key=dict(scope_key(params['human_scopes'][index]),kind='association',group='IPF',measure='FABP4_vs_matrix')
        audit.text(text,[audit.number('full',key,'n_first',fmt='.0f')])
    audit.text(fig.text(.235,.85,'Black points: unchanged full estimate in every panel',fontsize=9,color=INK))
    return fig,footer(fig,p['caption'])


def cofactor(tables,params,audit):
    p=params['plates'][3];fig=frame(p['title'],p['subtitle'])
    aa=[axes(fig,[x,.27,.29,.52],title,(-1,1),'Mapped-row Spearman correlation') for x,title in [(.29,'A  Within source-labelled IL4'),(.67,'B  Within source-labelled CTRL')]]
    labels=[]
    for i,mapping in enumerate(params['mappings']):
        y=3-i;key={k:mapping[k] for k in ['mapping_rule','distance_subset']}
        count=audit.number('mapping',dict(key,condition='IL4'),'pair_rows',fmt=',.0f')
        other=audit.number('mapping',dict(key,condition='CTRL'),'pair_rows',fmt=',.0f')
        if count['source_value']!=other['source_value']:raise ValueError('Unexpected unequal condition support')
        labels.append(mapping['label']+'\n'+count['label']+' mapped rows')
        for j,condition in enumerate(['IL4','CTRL']):
            rho=audit.number('mapping',dict(key,condition=condition),'mapped_row_spearman',fmt='+.5f')
            point,=aa[j].plot([rho['visual_value']],[y],'o',color=BLUE if j==0 else TEAL,ms=6);audit.line(point,[rho])
            audit.text(aa[j].text(.14,y,rho['label'],va='center',fontsize=10),[rho])
    for j,ax in enumerate(aa):
        ax.set_ylim(-.55,3.55);ax.set_yticks([3,2,1,0],labels if j==0 else ['']*4);ax.set_xticks([-1,-.5,0,.5,1]);ax.axvline(0,color=GRAY,lw=.8)
    for text,mapping in zip(aa[0].get_yticklabels(),params['mappings']):
        key={k:mapping[k] for k in ['mapping_rule','distance_subset']}
        audit.text(text,[audit.number('mapping',dict(key,condition='IL4'),'pair_rows',fmt=',.0f')])
    return fig,footer(fig,p['caption'])


BUILDERS=[representation,human_contrasts,human_coupling,cofactor]


def verify_values(audit):
    """Independent CSV row search and scalar formatting, separate from pandas selection."""
    cache={};checks=0
    for r in audit.values:
        if r['source'] not in cache:
            with Path(r['source']).open(encoding='utf-8',newline='') as handle:cache[r['source']]=list(csv.DictReader(handle,delimiter='\t'))
        def matches(row):
            return all(float(row[k])==v if isinstance(v,(int,float)) else row[k]==v for k,v in r['key'].items())
        rows=[row for row in cache[r['source']] if matches(row)]
        if len(rows)!=1:raise ValueError('Independent row selection failed')
        value=float(rows[0][r['column']]);visual=value*r['factor']
        if value!=r['source_value'] or visual!=r['visual_value'] or format(visual,r['format'])!=r['label']:
            # Parsers can differ at the final binary digit; require printed parity too.
            if not (math.isclose(value,r['source_value'],rel_tol=0,abs_tol=1e-14) and math.isclose(visual,r['visual_value'],rel_tol=0,abs_tol=1e-12) and format(visual,r['format'])==r['label']):
                raise ValueError('Independent numeric/label mismatch')
        checks+=3
    return checks


def export_check(path,stem,labels,expected_pages=1):
    svg=ET.parse(path/(stem+'.svg')).getroot();namespace={'s':'http://www.w3.org/2000/svg'}
    if svg.findall('.//s:image',namespace):raise ValueError('Raster embedded in SVG')
    svg_text='\n'.join(''.join(x.itertext()) for x in svg.findall('.//s:text',namespace))
    for record in labels:
        for line in record['text'].splitlines():
            if line not in svg_text:raise ValueError('Label missing from vector SVG: '+line)
    data=(path/(stem+'.pdf')).read_bytes()
    if re.search(rb'/Subtype\s*/Image\b',data):raise ValueError('Raster embedded in PDF')
    if len(re.findall(rb'/Type\s*/Page\b',data))!=expected_pages:raise ValueError('Unexpected PDF page count')
    with Image.open(path/(stem+'.png')) as im:
        if any(abs(v-300)>.1 for v in im.info.get('dpi',(0,0))):raise ValueError('PNG DPI mismatch')
        if im.size!=(3540,2400):raise ValueError('PNG canvas mismatch')
    return dict(vector_svg=True,svg_label_parity=True,vector_pdf=True,pdf_pages=1,png_dpi=300,png_pixels=[3540,2400])


def main(out):
    out.mkdir(parents=True,exist_ok=True);params=json.loads(PARAMETERS.read_text())
    paths=params['sources'];tables={k:pd.read_csv(v,sep='\t') for k,v in paths.items()}
    audit=Audit(tables,paths);records=[];inventory=[];checks=0
    date=datetime(2026,10,30,tzinfo=timezone.utc)
    metadata={'Title':'DY1 reviewed presentation derivatives','Author':'Ravel','CreationDate':date,'ModDate':date}
    with PdfPages(out/'DY1_presentation_plates_v1.pdf',metadata=metadata) as bundle:
        for builder,p in zip(BUILDERS,params['plates']):
            first=len(audit.labels);fig,caption=builder(tables,params,audit);qa=layout_check(fig,caption)
            stem=p['stem']
            fig.savefig(out/(stem+'.png'),dpi=300)
            fig.savefig(out/(stem+'.svg'),metadata={'Date':'2026-10-30','Creator':'Ravel'})
            fig.savefig(out/(stem+'.pdf'),metadata=metadata);bundle.savefig(fig)
            export=export_check(out,stem,audit.labels[first:]);plt.close(fig)
            records.append(dict(stem=stem,title=p['title'],caption=p['caption'],layout=qa,exports=export,
                source_tables=p['source_tables'],presentation_supersedes=p.get('presentation_supersedes','')))
            for extension in ['png','svg','pdf']:
                file=out/(stem+'.'+extension);inventory.append(dict(plate=stem,format=extension,path=repository_path(file),sha256=sha(file)))
    if len(re.findall(rb'/Type\s*/Page\b',(out/'DY1_presentation_plates_v1.pdf').read_bytes()))!=4:raise ValueError('Bundle page count mismatch')
    inventory.append(dict(plate='four_plate_bundle',format='pdf',path=repository_path(out/'DY1_presentation_plates_v1.pdf'),sha256=sha(out/'DY1_presentation_plates_v1.pdf')))
    checks=verify_values(audit)
    for file in [Path(__file__),PARAMETERS,ARTICLE/'tests/test_presentation_figures_v1.py']:
        inventory.append(dict(plate='render_code',format=file.suffix,path=repository_path(file),sha256=sha(file)))
    record=dict(analysis_id='DY1-P02.presentation_figures_v1',source_inputs=[dict(path=v,sha256=sha(v)) for v in paths.values()],
        code=[dict(path=x['path'],sha256=x['sha256']) for x in inventory if x['plate']=='render_code'],
        figures=records,bundle='DY1_presentation_plates_v1.pdf',bundle_pages=4,
        scope='Exposed presentation derivatives only; copied intervals and deterministic omission ranges remain distinct; no biological refit, inferential statistics or scientific acceptance.')
    (out/'render_record.json').write_text(json.dumps(record,indent=2)+'\n',newline='\n')
    (out/'data_label_verification.json').write_text(json.dumps(dict(status='passed',independent_value_checks=checks,values=audit.values,labels=audit.labels,coordinates=audit.coordinates),indent=2)+'\n',newline='\n')
    pd.DataFrame(inventory).to_csv(out/'render_inventory.tsv',sep='\t',index=False,lineterminator='\n')
    print(json.dumps(dict(plates=4,formats=['PNG300','SVG','PDF'],bundle_pages=4,value_checks=checks)))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);main(parser.parse_args().output)
