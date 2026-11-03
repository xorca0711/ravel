"""Frozen single-source ERBB RNA description; no state annotation or inference."""
from __future__ import annotations
import argparse
import csv
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
CONFIG = ROOT / 'RQ_Specified/A12_recipient_context/config/erbb_sorted_spec_v1.json'


def write_csv(path, rows):
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def qc_mask(total, detected, mitochondrial, cfg):
    # Integer arithmetic includes the exact 10% boundary without rounding.
    return ((total > 0) & (detected >= cfg['minimum_detected_features']) &
            (detected <= cfg['maximum_detected_features']) &
            (100 * mitochondrial <= cfg['maximum_mitochondrial_percent'] * total))


def read_source(base, cfg):
    prefix = cfg['sample_prefix']
    with gzip.open(base / (prefix + '_genes.tsv.gz'), 'rt') as f:
        genes = [x.rstrip('\n').split('\t') for x in f]
    with gzip.open(base / (prefix + '_barcodes.tsv.gz'), 'rt') as f:
        barcodes = [x.strip() for x in f]
    assert len(set(barcodes)) == len(barcodes), 'Duplicate barcodes'
    assert all(len(g) == 2 for g in genes), 'Unexpected feature table schema'
    assert len({g[0] for g in genes}) == len(genes), 'Duplicate feature identifiers'
    target_rows = {}
    for symbol, ensembl in cfg['targets'].items():
        hits = [i for i, g in enumerate(genes) if g[1] == symbol]
        assert len(hits) == 1 and genes[hits[0]][0] == ensembl, 'Ambiguous target'
        target_rows[hits[0]] = symbol
    mt = np.array([g[1].startswith('MT-') for g in genes])
    assert mt.any(), 'No mitochondrial identifiers'
    n = len(barcodes)
    total = np.zeros(n, dtype=np.int64)
    detected = np.zeros(n, dtype=np.int64)
    mitochondrial = np.zeros(n, dtype=np.int64)
    panel = {g: np.zeros(n, dtype=np.int64) for g in cfg['targets']}
    with gzip.open(base / (prefix + '_matrix.mtx.gz'), 'rt') as f:
        assert f.readline().strip() == '%%MatrixMarket matrix coordinate integer general'
        line = next(f)
        while line.startswith('%'):
            line = next(f)
        nr, nc, nnz = map(int, line.split())
        assert (nr, nc) == (len(genes), n), 'Dimension mismatch'
        previous_row = np.full(n, -1, dtype=np.int64)
        observed = 0
        for line in f:
            r, c, count = map(int, line.split())
            r -= 1
            c -= 1
            assert 0 <= r < nr and 0 <= c < nc and count > 0, 'Invalid count/index'
            # CellRanger export is ordered by feature within each barcode.
            # Failing this invariant stops rather than double-counting features.
            assert r > previous_row[c], 'Duplicate or unordered feature coordinate'
            previous_row[c] = r
            total[c] += count
            detected[c] += 1
            if mt[r]:
                mitochondrial[c] += count
            if r in target_rows:
                panel[target_rows[r]][c] += count
            observed += 1
        assert observed == nnz, 'Nonzero-count mismatch'
    return genes, barcodes, total, detected, mitochondrial, panel, nnz


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    cfg = json.loads(CONFIG.read_text(encoding='utf-8'))
    base = ROOT / cfg['source_directory']
    inventory = []
    for sample in cfg['source_samples']:
        fields = {}
        for line in (base / (sample['sample'] + '.soft')).read_text().splitlines():
            if ' = ' in line:
                k, v = line.split(' = ', 1)
                fields.setdefault(k, []).append(v)
        inventory.append(dict(series=sample['series'], sample=sample['sample'],
            title=' | '.join(fields.get('!Sample_title', [])),
            source_name=' | '.join(fields.get('!Sample_source_name_ch1', [])),
            source_characteristics=' | '.join(fields.get('!Sample_characteristics_ch1', [])),
            source_library_scope=sample['scope'], donor_identity='unresolved',
            author_barcode_state_map='not_recovered', state_comparison='unestimated',
            numerical_route='sorted_preparation_only' if sample['sample'] == cfg['sample'] else 'not_run'))
    write_csv(output / 'source_inventory.csv', inventory)
    genes, barcodes, total, detected, mito, panel, nnz = read_source(base, cfg)
    keep = qc_mask(total, detected, mito, cfg['qc'])
    cells = []
    for i, barcode in enumerate(barcodes):
        failures = []
        if total[i] == 0: failures.append('zero_depth')
        if detected[i] < 200: failures.append('below_200_features')
        if detected[i] > 6000: failures.append('above_6000_features')
        if 100 * mito[i] > 10 * total[i]: failures.append('above_10pct_mitochondrial')
        cells.append(dict(sample=cfg['sample'], barcode=barcode,
            full_rna_umi=int(total[i]), detected_features=int(detected[i]), mitochondrial_umi=int(mito[i]),
            mitochondrial_percent=float(100 * mito[i] / total[i]) if total[i] else '',
            ERBB4_umi=int(panel['ERBB4'][i]), ERBB2_umi=int(panel['ERBB2'][i]),
            operational_qc=int(keep[i]), qc_exclusion_reasons=';'.join(failures),
            epithelial_state='unknown', donor_id='unknown'))
    write_csv(output / 'cell_measurements.csv', cells)
    summary = []
    both = (panel['ERBB4'] > 0) & (panel['ERBB2'] > 0)
    for subset, mask in [('deposited', np.ones(len(barcodes), dtype=bool)), ('operational_qc', keep)]:
        n, full = int(mask.sum()), int(total[mask].sum())
        for gene, values in panel.items():
            umi, positive = int(values[mask].sum()), int((values[mask] > 0).sum())
            summary.append(dict(sample=cfg['sample'], subset=subset, gene=gene,
                ensembl=cfg['targets'][gene], n_barcodes=n, n_positive_depth=int((total[mask] > 0).sum()),
                gene_umi=umi, full_rna_umi=full, full_rna_cpm=1e6 * umi / full if full else '',
                detected_barcodes=positive, detection_percent=100 * positive / n if n else '',
                codetected_barcodes=int(both[mask].sum()),
                codetection_percent=100 * int(both[mask].sum()) / n if n else ''))
    write_csv(output / 'receptor_summary.csv', summary)
    qc = dict(sample=cfg['sample'], deposited_barcodes=len(barcodes),
        full_feature_count=len(genes), matrix_nonzero_coordinates=nnz,
        retained_barcodes=int(keep.sum()), excluded_barcodes=int((~keep).sum()),
        zero_depth_barcodes=int((total == 0).sum()),
        below_200_features=int((detected < 200).sum()), above_6000_features=int((detected > 6000).sum()),
        above_10pct_mitochondrial=int((100 * mito > 10 * total).sum()),
        exclusion_counts_overlap=True, cell_state_unknown=len(barcodes), donor_identity='unresolved',
        mitochondrial_features=[dict(ensembl=g[0], symbol=g[1]) for g in genes if g[1].startswith('MT-')],
        qc_definition=cfg['qc'], identity='source-defined HTII-280-sorted preparation; no state assignment')
    (output / 'qc_summary.json').write_text(json.dumps(qc, indent=2) + '\n')
    rscript = 'RQ_Specified/A12_recipient_context/scripts/verify_erbb_sorted_v1.R'
    with tempfile.TemporaryDirectory(prefix='a12_erbb_verify_') as tmp:
        check_path = Path(tmp) / 'independent.csv'
        r = subprocess.run(['Rscript', str(ROOT / rscript), str(base), str(check_path)],
                           check=True, capture_output=True, text=True)
        with check_path.open(newline='') as f:
            independent = list(csv.DictReader(f))
        assert len(independent) == len(cells), 'Independent cell count differs'
        for row, expected in zip(independent, cells):
            assert row['barcode'] == expected['barcode'], 'Independent barcode order differs'
            for field in ['full_rna_umi', 'detected_features', 'mitochondrial_umi',
                          'ERBB4_umi', 'ERBB2_umi', 'operational_qc']:
                assert int(row[field]) == expected[field], f'Independent mismatch: {field}'
        for row in summary:
            selected = independent if row['subset'] == 'deposited' else [x for x in independent if int(x['operational_qc'])]
            n = len(selected)
            raw = sum(int(x[row['gene'] + '_umi']) for x in selected)
            denominator = sum(int(x['full_rna_umi']) for x in selected)
            positive = sum(int(x[row['gene'] + '_umi']) > 0 for x in selected)
            co = sum(int(x['ERBB4_umi']) > 0 and int(x['ERBB2_umi']) > 0 for x in selected)
            assert (n, raw, denominator, positive, co) == (row['n_barcodes'], row['gene_umi'], row['full_rna_umi'], row['detected_barcodes'], row['codetected_barcodes'])
            if denominator:
                assert abs(row['full_rna_cpm'] - 1e6 * raw / denominator) < 1e-10
        verification = dict(status='passed', independent_method='R Matrix::readMM -> CsparseMatrix -> sparse colSums and exact target rows; Python streaming is independent',
            checked_barcodes=len(cells), checked_integer_fields_per_barcode=6,
            checked_summary_rows=len(summary), barcode_order='exact', runtime=r.stdout.strip(),
            r_stderr=r.stderr.strip(), scope='arithmetic and identifiers only; not independent biological validation')
        (output / 'independent_verification.json').write_text(json.dumps(verification, indent=2) + '\n')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 4.2), layout='constrained')
    colors = ['#747f8c', '#287e8f']
    for j, (subset, label) in enumerate([('deposited', 'Deposited'), ('operational_qc', 'Operational QC')]):
        rows = [x for x in summary if x['subset'] == subset]
        xx = np.arange(2) + (j - 0.5) * 0.3
        for ax, key, ylabel in [(axes[0], 'detection_percent', 'Barcodes with >=1 UMI (%)'),
                                 (axes[1], 'full_rna_cpm', 'UMI per million full RNA UMIs')]:
            values = [x[key] if x[key] != '' else np.nan for x in rows]
            ax.bar(xx, values, width=0.28, color=colors[j], label=f"{label} (n={rows[0]['n_barcodes']:,})")
            ax.set_xticks([0, 1], ['ERBB4', 'ERBB2'])
            ax.set_ylabel(ylabel)
            ax.spines[['top', 'right']].set_visible(False)
            ax.set_ylim(bottom=0)
    axes[0].legend(frameon=False, fontsize=8)
    fig.suptitle('ERBB RNA in one fresh HTII-280-sorted preparation', fontsize=12)
    fig.supxlabel('GSM4522986; no assigned epithelial state, donor inference or receptor activity', fontsize=9)
    fig.savefig(output / 'erbb_sorted_rna.png', dpi=180)
    plt.close(fig)
    print(json.dumps(dict(status='completed', barcodes=len(cells), qc_barcodes=int(keep.sum()), summary_rows=len(summary))))


if __name__ == '__main__':
    main()
