"""Validate editorial coverage, relocations and newly broken Markdown links.

Run from the repository root. Reads tracked/untracked documents and Git baseline;
does not rerun analyses or rewrite historical evidence. Existing link defects
are reported separately from regressions introduced by this consolidation.
"""
from __future__ import annotations
import argparse, csv, hashlib, io, json, posixpath, re, subprocess
from pathlib import Path
from urllib.parse import unquote

AUDIT='docs/audits/2026-11-08-source-consolidation'
BASE='1d7c814e86cf9c3c1fc70b35ee78f455420adf59'
ACCESSION=re.compile(r'(?<![A-Za-z0-9])(?:GSE\d{4,}|E-MTAB-\d+|PRJ(?:NA|EB|DB)\d+)(?![A-Za-z0-9])')
INLINE=re.compile(r'!?\[[^\]]*\]\((<[^>\n]+>|[^)\n]+)\)')
REF=re.compile(r'(?m)^\s*\[[^\]]+\]:\s*(\S+)')

def git(*args):
    return subprocess.check_output(['git',*args])

def git_blobs(paths):
    """Read baseline documents in one process rather than one per Markdown file."""
    paths=sorted(paths)
    request=''.join(BASE+':'+p+'\n' for p in paths).encode()
    stream=subprocess.run(['git','cat-file','--batch'],input=request,capture_output=True,check=True).stdout
    result={};offset=0
    for p in paths:
        end=stream.index(b'\n',offset)
        size=int(stream[offset:end].split()[-1])
        offset=end+1;result[p]=stream[offset:offset+size];offset+=size+1
    return result

def anchors(text):
    out=set(re.findall(r'<a\s+(?:name|id)=["\']([^"\']+)',text))
    seen={}
    for line in text.splitlines():
        if not re.match(r'^#{1,6}\s',line):continue
        value=line.lstrip('#').strip().lower()
        value=re.sub(r'!?\[([^\]]+)\]\([^)]*\)',r'\1',value)
        value=re.sub(r'<[^>]+>','',value)
        value=re.sub(r'[^\w\- ]','',value).replace(' ','-')
        n=seen.get(value,0);seen[value]=n+1
        out.add(value+('-'+str(n) if n else ''))
    return out

def links(text):
    # Examples inside fenced code are not navigational links.
    text=re.sub(r'(?ms)^```.*?^```[^\n]*','',text)
    return [m[1] for m in INLINE.finditer(text)]+[m[1] for m in REF.finditer(text)]

def resolve(source,url):
    url=url.strip().strip('<>')
    if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',url) or url.startswith('//'):return None
    url=re.sub(r'\s+["\'].*$','',url)
    path,sep,fragment=unquote(url).partition('#')
    if path.startswith('/'):return None
    dest=posixpath.normpath(posixpath.join(posixpath.dirname(source),path)) if path else source
    return dest,fragment

def defects(texts,files):
    all_anchors={p:anchors(t) for p,t in texts.items()}
    dirs={'.'}
    for p in files:
        parent=posixpath.dirname(p)
        while parent:
            dirs.add(parent);parent=posixpath.dirname(parent)
    result=set();count=0
    for p,text in texts.items():
        for url in links(text):
            target=resolve(p,url)
            if not target:continue
            count+=1;dest,frag=target
            if dest not in files and dest not in dirs:
                result.add((p,dest,frag,'missing path'))
            elif frag and dest in texts and frag not in all_anchors[dest]:
                result.add((p,dest,frag,'missing fragment'))
    return result,count

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);args=parser.parse_args()
    failures=[];checks=0
    def check(ok,message):
        nonlocal checks
        checks+=1
        if not ok:failures.append(message)
    manifest=json.loads(Path(AUDIT,'document_moves.json').read_text())
    moved={r['from']:r['to'] for r in manifest['moves']}
    baseline_files=set(git('ls-tree','-r','--name-only',BASE).decode().splitlines())
    files=set(git('ls-files','--cached','--others','--exclude-standard').decode().splitlines())
    files={p for p in files if Path(p).is_file()}
    baseline_blobs=git_blobs({p for p in baseline_files if p.endswith('.md') or p.startswith('docs/audits/2026-11-07-public-data-inventory/snapshot_')}|{'Research Article/ROADMAP.json','analysis/research/registry.json'})
    baseline_texts={p:b.decode('utf-8-sig',errors='replace') for p,b in baseline_blobs.items() if p.endswith('.md')}
    texts={p:Path(p).read_text(encoding='utf-8-sig',errors='replace') for p in files if p.endswith('.md')}
    old_defects,_=defects(baseline_texts,baseline_files)
    new_defects,link_count=defects(texts,files)
    # Normalize existing defects to moved locations so historical defects do not
    # become alleged regressions merely because their document moved.
    normalized={(moved.get(p,p),moved.get(d,d),f,k) for p,d,f,k in old_defects}
    regressions=sorted(new_defects-normalized)
    for p,d,f,k in regressions:check(False,f'{k}: {p} -> {d}#{f}')
    check(not regressions,'No new broken local links or fragments')
    master=texts['docs/DATASETS.md']
    census=list(csv.DictReader(io.StringIO(Path('docs/audits/2026-11-07-public-data-inventory/snapshot_v2/accession_references.csv').read_text())))
    for r in census:check(r['accession'] in ACCESSION.findall(master),'Missing source '+r['accession'])
    for source in ['docs/DATASETS.md','docs/DATASET_UPDATES_2026-11-07.md']:
        for a in set(ACCESSION.findall(baseline_texts[source])):check(a in master,'Lost original source '+a)
    for source,delimiter in [('analysis/research/runs/sx10_coinput_qualification_v2/source_candidates.csv',','),('analysis/research/runs/sx22_priming_qualification_v2/source_candidates.csv',','),('analysis/research/runs/wp_e5_external_screen_v1/candidates.csv',','),('docs/audits/2026-09-27-register-gate-audit/candidates.tsv','\t'),('Research Article/gate1_01_niethamer_2025/trials/g0_gsea_feasibility/g0_deposits.csv',',')]:
        for r in csv.DictReader(Path(source).open(encoding='utf-8-sig'),delimiter=delimiter):
            check(r['accession'] in master,'Lost screen source '+r['accession'])
    check('DATASET_UPDATES_' not in texts['README.md'],'Root README must have one source-list route')
    check('docs/DATASETS.md' in texts['README.md'],'Root source register link')
    for move in manifest['moves']:
        check(move['to'] in files,'Missing moved document '+move['to'])
        old=baseline_blobs[move['from']]
        check(hashlib.sha256(old).hexdigest()==move['original_sha256'],'Original document hash '+move['from'])
        if move['compatibility_consumers']:check(move['from'] in files,'Missing compatibility locator '+move['from'])
        # Remove only the archival banner and link destinations. Non-link prose
        # must survive the move, including original limits and unfavorable results.
        new=texts[move['to']]
        new=re.sub(r'\n\n> Historical record, archived 8 November 2026\..*?> for active sources and navigation\.\n','\n',new,count=1,flags=re.S)
        mask=lambda t: re.sub(r'(?<=\]\()[^)\n]+(?=\))','DEST',t).replace('\r\n','\n')
        check(mask(old.decode('utf-8-sig')).strip()==mask(new).strip(),'Changed non-link prose '+move['to'])
    protected=json.loads(Path(AUDIT,'protected_markdown.json').read_text())
    for p in protected:
        if p in baseline_files:check(Path(p).read_bytes()==baseline_blobs[p],'Changed hash-bound Markdown '+p)
    for p in baseline_files:
        if p.startswith('docs/audits/2026-11-07-public-data-inventory/snapshot_'):
            check(Path(p).read_bytes()==baseline_blobs[p],'Changed historical snapshot '+p)
    for p in ['CLAIMS.md','docs/CLAIM_SUMMARY.md','docs/NEGATIVE_RESULTS.md','docs/PIPELINE_AS_RUN.md','docs/ANALYSIS_RATIONALE.md','Research Article/ROADMAP.json','analysis/research/registry.json']:
        check(Path(p).read_bytes()==baseline_blobs[p],'Changed preserved authority/evidence '+p)
    # The root measured-method gallery must retain all image embeds.
    embeds=lambda s:re.findall(r'!\[[^\]]*\]\([^)]+\)',s)
    check(embeds(texts['README.md'])==embeds(baseline_texts['README.md']),'Root measured gallery changed')
    result={'base':BASE,'checks':checks,'local_links_checked':link_count,'source_identifiers':len(set(ACCESSION.findall(master))),'census_coverage':len(census),'moved_documents':len(moved),'compatibility_locators':sum(bool(r['compatibility_consumers']) for r in manifest['moves']),'preexisting_link_defects':len(old_defects),'new_link_defects':regressions,'failures':failures,'passed':not failures}
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['new_link_defects']}))
    return 0 if not failures else 1

if __name__=='__main__':raise SystemExit(main())
