"""S0 source/matrix/sample qualification; no treatment-effect estimation."""
import argparse
import csv
import gzip
import hashlib
import io
import json
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from pypdf import PdfReader

RAW = Path('raw_data/zhang_2026/source_v1')


def dump(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def table(path, rows):
    with path.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def matrix(text):
    rows = list(csv.reader(io.StringIO(text.lstrip('\ufeff'))))
    assert all(len(row) == len(rows[0]) for row in rows[1:]), 'Ragged matrix'
    genes = [row[0] for row in rows[1:]]
    assert all(genes) and len(genes) == len(set(genes)), 'Empty/duplicate feature identity'
    samples = rows[0][1:]
    assert len(samples) == len(set(samples)), 'Duplicate sample'
    values = np.array([row[1:] for row in rows[1:]], dtype=float)
    assert np.isfinite(values).all() and (values >= 0).all(), 'Invalid abundance'
    return genes, samples, values


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    out = args.output
    records = json.loads((RAW / 'acquisition_v1.json').read_text(encoding='utf-8'))
    records += json.loads((RAW / 'acquisition_extra_v1.json').read_text(encoding='utf-8'))
    tree = {x['path']: x for x in json.loads((RAW / 'author_tree.json').read_text())['tree']}
    manifest = []
    for record in records:
        row = dict(record)
        if 'path' in row:
            data = Path(row['path']).read_bytes()
            assert hashlib.sha256(data).hexdigest() == row['sha256']
            prefix = (RAW / 'author').as_posix() + '/'
            if row['path'].startswith(prefix):
                rel = row['path'][len(prefix):]
                blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
                assert blob == tree[rel]['sha'], rel
                row['git_blob_verified'] = blob
            if row['path'].endswith('.pdf'):
                row['format_verified'] = data.startswith(b'%PDF-')
            elif row['path'].endswith('.xlsx'):
                row['format_verified'] = data.startswith(b'PK')
            elif row['path'].endswith('europepmc_supplements.zip'):
                row['format_verified'] = data.startswith(b'PK')
                row['access_result'] = 'API reports article is not open access; not a ZIP'
            if row.get('format_verified') is False:
                row['qualified_input'] = False
                row.setdefault('access_result', 'HTML challenge response, not the requested scientific file')
        manifest.append(row)
    dump(out / 'source_manifest.json', manifest)

    genes, samples, values = matrix((RAW / 'author/input_files/NK_kallisto_tpm.csv').read_text())
    gg, gs, gv = matrix(gzip.decompress((RAW / 'geo/GSE287581_transposed_kallisto_NK_only.csv.gz').read_bytes()).decode())
    same_identity = genes == gg and samples == gs
    equal_values = bool(same_identity and np.array_equal(values, gv))
    geo_text = gzip.decompress((RAW / 'geo/GSE287581_family.soft.gz').read_bytes()).decode()
    prior_text = gzip.decompress((RAW / 'prior/prior_geo.soft.gz').read_bytes()).decode()
    blocks = re.split(r'(?m)^\^SAMPLE = ', geo_text)[1:]
    geo = {}
    for block in blocks:
        gsm = block.splitlines()[0].strip()
        title = re.search(r'(?m)^!Sample_title = (.+)$', block).group(1).strip()
        rep = 'rep' + re.search(r'rep (\d+)$', title).group(1)
        condition = 'ITDT_aCD4' if 'anti-CD4' in title else ('ITDT' if ', ITDT,' in title else 'PBS')
        key = (condition, rep)
        assert key not in geo, 'Duplicate GEO condition/block'
        geo[key] = {'gsm': gsm, 'geo_title': title}
    with (RAW / 'author/input_files/sample_info_NK.csv').open() as stream:
        metadata = list(csv.DictReader(stream))
    assert [x[''] for x in metadata] == samples, 'Matrix/metadata sample order disagreement'
    assert len(geo) == len(metadata) == 9
    crosswalk = []
    for row in metadata:
        condition, rep, sample = row['condition'], row['replicate'], row['']
        expected = ('NK_ITDTCD4_' if condition == 'ITDT_aCD4' else 'NK_' + condition) + rep[-1]
        assert sample == expected, 'Name-derived cross-check failed'
        crosswalk.append({'sample': sample, **geo[(condition, rep)], 'condition': condition,
                          'block': rep, 'unit': 'sorted pooled NK preparation/library',
                          'mouse_ids': 'unknown', 'pool_size': 'exact unknown; paper 3-4 tumors, methods/GEO 2-4 mice',
                          'cross_assay_animal_reuse': 'unknown', 'pairing': 'experimental block, not repeated mouse'})
    assert len({r['gsm'] for r in crosswalk}) == 9
    table(out / 'sample_crosswalk.csv', crosswalk)
    # Independent balance/rank check: one-hot conditions and sum-to-zero blocks.
    design = []
    for row in crosswalk:
        design.append([int(row['condition'] == c) for c in ['PBS', 'ITDT', 'ITDT_aCD4']] +
                      {'rep1': [1, 0], 'rep2': [0, 1], 'rep3': [-1, -1]}[row['block']])
    rank = int(np.linalg.matrix_rank(design))
    assert rank == 5 and equal_values, 'Source identity or design qualification failed'
    qualification = {
        'genes': len(genes), 'libraries': len(samples), 'matrix_orientation': 'gene_symbol_by_library',
        'duplicate_genes': 0, 'duplicate_samples': 0, 'missing_nonfinite_or_negative_values': 0,
        'column_sums': dict(zip(samples, values.sum(axis=0).tolist())),
        'fractional_values': int(np.count_nonzero(values != np.floor(values))),
        'GEO_GitHub_identity_equal': same_identity, 'GEO_GitHub_values_exactly_equal': equal_values,
        'GEO_SOFT_content_unchanged': geo_text == prior_text,
        'design_rank': rank, 'design_columns': 5, 'residual_df': len(samples) - rank,
        'semantics': 'Released source explicitly uses kallisto TPM; numerical scale consistent with TPM. These are not qualified counts.',
        'unit_limit': 'Nine pooled libraries in three reported blocks; hidden animal membership and cross-assay reuse remain unknown.',
        'count_reanalysis': 'HOLD: qualified gene/transcript counts, transcript annotation and length/aggregation treatment not acquired',
        'S1': 'Qualified released TPM replay; conditional pooled-library description, no animal-level inference',
        'S2': 'Conditional on S1 and verified pinned gene sets/API',
        'S3': 'Conditional on reconciled S1/S2; no count sensitivity without qualified counts',
        'S4_numeric': 'HOLD: four linked supplemental files returned HTML, and Europe PMC API disallows OA retrieval',
        'S4_synthesis': 'Source-grounded endpoint synthesis permitted',
    }
    dump(out / 'qualification.json', qualification)
    pdf = PdfReader(RAW / 'prior/supplied_paper.pdf')
    first = pdf.pages[0].extract_text()
    assert 'adx4411' in first and 'Zhang' in first
    dump(out / 'paper_identity.json', {
        'current_sha256': hashlib.sha256((RAW / 'prior/supplied_paper.pdf').read_bytes()).hexdigest(),
        'planning_sha256': '05e9193c9ff71924063e6bfbadbbb826120c167a635aa7d1750ef1d3f8539273',
        'hash_matches_planning': False, 'current_pdf_pages': len(pdf.pages),
        'identity': 'First page identifies Zhang et al., Science Immunology 11 eadx4411, 10 April 2026.',
        'limit': 'Different supplied file version; byte equivalence to planning PDF is not established. Original remains untouched; no functional values extracted.'})
    r = shutil.which('Rscript')
    packages = ['limma', 'edgeR', 'fgsea', 'msigdbr', 'BiocParallel', 'data.table', 'ggplot2', 'dplyr', 'jsonlite']
    expression = "cat(R.version.string,'\\n');for(p in c(" + ','.join(repr(p) for p in packages) + ")) cat(p,if(requireNamespace(p,quietly=TRUE))as.character(packageVersion(p))else'UNAVAILABLE','\\n')"
    proc = subprocess.run([r, '--vanilla', '-e', expression], capture_output=True, text=True) if r else None
    runtime = {'python': sys.version, 'numpy': np.__version__, 'platform': platform.platform(),
               'R_available': bool(r), 'R_inventory': proc.stdout if proc else '',
               'R_stderr': proc.stderr if proc else '', 'R_exit_code': proc.returncode if proc else None,
               'remote_discovery': 'Only local NGS target; saved cloud environments target weft, with no attached Ravel executor.'}
    dump(out / 'runtime.json', runtime)
    table(out / 'discrepancy_ledger.csv', [
        {'item': 'model', 'source': 'paper log-CPM/voom; released log2(TPM+0.5), limma-trend', 'disposition': 'Released reproduction only; count branch held'},
        {'item': 'blocking', 'source': 'GEO treatment-only text; paper/code experimental replicate', 'disposition': 'Use released rank-5 blocked design'},
        {'item': 'GSEA ranking', 'source': 'paper adjusted P; comments signed -log10(P); executable logFC', 'disposition': 'Replay logFC; signed moderated t is separate sensitivity'},
        {'item': 'figures', 'source': 'code preprint names differ from final panels; TPM heatmaps labelled log2CPM', 'disposition': 'Content crosswalk; label measured TPM transform'},
        {'item': 'Zenodo locator', 'source': 'supplied paper ref89 and PMC manuscript ref95 point to bioRxiv DOI 10.1101/2025.06.26.661417', 'disposition': 'No verified archive accession; GitHub pinned source remains qualified'},
        {'item': 'supplements', 'source': 'PMC lists XLSX tables plus PDF figures, data S1-S17 and MDAR', 'disposition': 'Located, not acquired: challenge HTML; no raw FCS/worksheet qualification'},
        {'item': 'functional labels', 'source': 'supplied Figure5 caption F/G versus axes; Figure6J Tconv FOXP3-positive legend', 'disposition': 'Retain ambiguity; no numeric functional extraction'},
        {'item': 'PDF version', 'source': 'current supplied PDF hash differs; 16 pages versus recorded 15', 'disposition': 'Preserve new version with exact hash; first-page article identity verified'},
    ])
    print(json.dumps({'qualification': 'passed_for_TPM_replay', 'genes': len(genes), 'libraries': len(samples), 'design_rank': rank}))


if __name__ == '__main__':
    main()
