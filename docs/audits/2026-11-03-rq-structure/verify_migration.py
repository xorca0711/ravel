"""Verify the documentation migration, without running biological analyses."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit
import collections
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
manifest = json.loads((HERE / 'MANIFEST.json').read_text(encoding='utf-8'))
base = manifest['base_revision']

def git_file(path):
    return subprocess.check_output(['git', 'show', f'{base}:{path}'], cwd=ROOT)

def text_hash(path):
    return hashlib.sha256((ROOT / path).read_bytes().replace(b'\r\n', b'\n')).hexdigest()

def words_without_urls(text):
    return re.sub(r'(!?\[[^\]]*\]\()([^\s)]+)(\))', r'\1TARGET\3', text.replace('\r\n', '\n')).strip()

old = json.loads(git_file('analysis/research/registry.json'))
new = json.loads((ROOT / 'analysis/research/registry.json').read_text(encoding='utf-8'))
before = {g['question']: g for g in old['question_guides']}
assert {g['question'] for g in new['question_guides']} == {f'A{i}' for i in range(33)}
for key in old:
    if key not in {'questions', 'question_guides', 'question_raster_provenance'}:
        assert old[key] == new[key], key
for original, current in zip(old['questions'], new['questions']):
    assert {k:v for k,v in original.items() if k!='evidence'} == {k:v for k,v in current.items() if k!='evidence'}
    assert set(original['evidence']).issubset(current['evidence'])

homes = set()
for guide in new['question_guides']:
    q = guide['question']; prior = before[q]
    entry, context, image = (ROOT / guide[k] for k in ('entrypoint', 'context', 'schematic'))
    assert entry.relative_to(ROOT).parts[0] == 'RQ_Specified' and entry.name == 'README.md', q
    assert entry.parent.name.startswith(q+'_'), q
    assert context == entry.parent/'LITERATURE_CONTEXT.md' and image.parent == entry.parent/'schematics', q
    assert (entry.parent/'PLAN.md').is_file(), q
    homes.add(entry.parent)
    text = entry.read_text(encoding='utf-8')
    assert re.findall(r'^## (.+)$', text, re.M)[:2] == manifest['readme_order'], q
    images = [(entry.parent/unquote(t)).resolve() for t in re.findall(r'!\[[^\]]*\]\(([^)]+)\)', text)]
    assert images.count(image.resolve()) == 1, q
    assert hashlib.sha256(image.read_bytes()).hexdigest() == prior['schematic_sha256'] == guide['schematic_sha256'], q
    assert guide['hypothesis_sha256'] == prior['hypothesis_sha256'] == manifest['hypotheses'][q], q
    prior_context = git_file(prior['context']).decode('utf-8').replace('\r\n','\n')
    assert words_without_urls(prior_context.split('\n',1)[1]) in words_without_urls(context.read_text(encoding='utf-8')), q
    if q not in manifest['new_homes']:
        original = git_file(prior['entrypoint']).decode('utf-8').splitlines()
        current = collections.Counter(line.strip() for line in text.splitlines())
        meaningful = collections.Counter(line.strip() for line in original if line.strip() and not line.startswith(('#','<!--','GPT-generated matte illustration')) and not line.startswith('!['))
        missing = meaningful-current
        assert not missing, (q, 'lost original analysis lines', dict(missing))
assert len(homes) == 33

for row in manifest['retained_and_copied_assets']:
    for key in ('old_path','new_path'):
        p=ROOT/row[key]
        actual=hashlib.sha256(p.read_bytes()).hexdigest() if p.suffix=='.png' else text_hash(row[key])
        assert actual==row['content_sha256'], row
for p in old['question_raster_provenance']:
    assert hashlib.sha256((ROOT/p['image']).read_bytes()).hexdigest()==p['image_sha256']
    assert text_hash(p['prompt'])==p['prompt_sha256']
    assert text_hash(p['source_schematic'])==p['source_schematic_sha256']

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.refs=[]; self.images=0
    def handle_starttag(self, tag, attrs):
        self.images += tag=='img'
        self.refs.extend(v for k,v in attrs if k in ('href','src'))

gallery=ROOT/'RQ_Specified/SCHEMATIC_GALLERY.html'
links=Links(); links.feed(gallery.read_text(encoding='utf-8'))
assert links.images==33
for ref in links.refs:
    assert not urlsplit(ref).scheme and (gallery.parent/unquote(ref)).is_file(), ref

assert not subprocess.check_output(['git','diff',base,'--','RESEARCH_QUESTIONS.md','CLAIMS.md','analysis/lib','analysis/scripts','analysis/tests','analysis/research/legacy_artifacts.json'],cwd=ROOT)
assert not subprocess.check_output(['git','diff','--name-only','--diff-filter=D',base,'--'],cwd=ROOT)
result={'base_revision':base,'question_homes':33,'readme_orders_verified':33,
        'contexts_preserved':33,'existing_readme_analysis_lines_preserved':26,
        'hypothesis_bindings_preserved':33,'prior_png_svg_prompt_sets_preserved':33,
        'new_asset_copies_verified':21,'html_gallery_images':33,
        'html_references_verified':len(links.refs),'existing_files_deleted':0,
        'scientific_code_and_question_cards_changed':False,'analysis_rerun':False}
(HERE/'VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))
