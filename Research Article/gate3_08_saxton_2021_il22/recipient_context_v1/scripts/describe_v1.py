"""Two fixed transcripts in saved cells; no contrasts, model, relabeling or network."""
from __future__ import annotations

import argparse
import csv
import importlib.metadata
import json
from collections import Counter
from pathlib import Path

import h5py
import numpy as np
from scipy.sparse import csr_matrix

ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / 'analysis/research/runs/p001_figure1_v1_f001_d56ee41e13cd4327'
GENES = ('Il22ra1', 'Il10rb')
LIBRARIES = ('PBS_AT2_Tomato', 'Day14_AT2_Tomato', 'Day28_AT2_Tomato')
LABELS = ('hAT2', 'cAT2', 'pAT2', 'DATP', 'AT1', 'unassigned',
          'contaminant_ciliated', 'contaminant_club_or_airway',
          'contaminant_endothelium', 'contaminant_immune', 'contaminant_mesenchyme')
AGGREGATES = ('ALL_RETAINED', 'NON_CONTAMINANT')
LIBRARY_METADATA = {'PBS_AT2_Tomato': ('GSM4304609', 'PBS'),
                    'Day14_AT2_Tomato': ('GSM4304611', 'day 14'),
                    'Day28_AT2_Tomato': ('GSM4304613', 'day 28')}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def strings(node):
    if isinstance(node, h5py.Dataset):
        return node.asstr()[:].astype(str)
    encoding = node.attrs.get('encoding-type')
    if encoding == 'nullable-string-array':
        require(not node['mask'][:].any(), 'Missing string metadata')
        return strings(node['values'])
    if encoding == 'categorical':
        codes = node['codes'][:]
        categories = strings(node['categories'])
        require(np.all((codes >= 0) & (codes < len(categories))), 'Invalid categorical code')
        return categories[codes]
    raise ValueError(f'Unsupported string encoding: {encoding}')


def gene_columns(features):
    require(len(set(features)) == len(features), 'Duplicate saved feature identity')
    indices = []
    for gene in GENES:
        hit = np.flatnonzero(features == gene)
        require(len(hit) == 1, f'Missing or ambiguous exact symbol: {gene}')
        indices.append(int(hit[0]))
    return indices


def count_metrics(matrix, columns, saved_totals):
    require(isinstance(matrix, csr_matrix), 'Expected saved CSR count layer')
    matrix.check_format(full_check=True)
    require(matrix.has_canonical_format, 'Duplicate/unsorted sparse coordinates')
    values = matrix.data
    require(np.isfinite(values).all() and (values > 0).all(), 'Invalid stored counts')
    require(np.equal(values, np.floor(values)).all(), 'Non-integer stored counts')
    totals = np.asarray(matrix.sum(axis=1, dtype=np.int64)).ravel()
    require((totals > 0).all(), 'Cell with zero count denominator')
    require(np.array_equal(totals, saved_totals), 'Saved cell totals disagree with count layer')
    selected = matrix[:, columns].toarray().astype(np.int64)
    return selected, totals


def verify_metadata(obs, cell_rows, composition_rows):
    n = len(obs['barcode'])
    require(len(set(obs['barcode'])) == n, 'Duplicate saved cell ID')
    require(len(cell_rows) == n, 'Cell-state row count mismatch')
    require(all(len(v) == n for v in obs.values()), 'Metadata length mismatch')
    for i, row in enumerate(cell_rows):
        for key in obs:
            field = 'sample_prefixed_cell_id' if key == 'barcode' else key
            require(row[field] == obs[key][i], f'Ordered cell-state mismatch: {i}/{key}')
    require(set(obs['library']) == set(LIBRARIES), 'Unexpected/missing library')
    require(set(obs['state']).issubset(LABELS), 'Unexpected literal pipeline label')
    for lib in LIBRARIES:
        mask = obs['library'] == lib
        gsm, time = LIBRARY_METADATA[lib]
        require(set(obs['gsm'][mask]) == {gsm} and set(obs['timepoint'][mask]) == {time},
                'Library/source metadata join mismatch')
    expected = {(r['library'], r['state']): int(r['count']) for r in composition_rows}
    require(len(expected) == len(composition_rows), 'Duplicate composition key')
    require(dict(Counter(zip(obs['library'], obs['state']))) == expected,
            'Saved composition differs from literal label partition')
    for row in composition_rows:
        mask = obs['library'] == row['library']
        excluded = np.char.startswith(obs['state'], 'contaminant_') & mask
        require(int(row['post_doublet_cells']) == int(mask.sum()), 'Retained denominator mismatch')
        require(int(row['contaminant_cells']) == int(excluded.sum()), 'Contaminant denominator mismatch')
        require(int(row['alveolar_including_unassigned']) == int((mask & ~excluded).sum()),
                'Non-contaminant denominator mismatch')


def summarize(obs, selected, totals):
    require(selected.shape == (len(totals), len(GENES)), 'Selected matrix shape mismatch')
    require((selected >= 0).all() and (selected <= totals[:, None]).all(), 'Invalid gene counts')
    require(np.equal(selected, np.floor(selected)).all(), 'Non-integer selected counts')
    rows = []
    for lib in LIBRARIES:
        library_mask = obs['library'] == lib
        for label in LABELS + AGGREGATES:
            mask = library_mask.copy()
            if label == 'NON_CONTAMINANT':
                mask &= ~np.char.startswith(obs['state'], 'contaminant_')
            elif label != 'ALL_RETAINED':
                mask &= obs['state'] == label
            n = int(mask.sum())
            total = int(totals[mask].sum())
            for j, gene in enumerate(GENES):
                v = selected[mask, j]
                detected = int(np.count_nonzero(v)) if n else None
                count_sum = int(v.sum()) if n else None
                rows.append({'library': lib, 'gsm': LIBRARY_METADATA[lib][0],
                             'timepoint': LIBRARY_METADATA[lib][1],
                             'stratum_kind': 'aggregate' if label in AGGREGATES else 'literal_label',
                             'pipeline_label_or_aggregate': label, 'gene': gene,
                             'status': 'observed_cells' if n else 'empty_stratum',
                             'n_cells': n, 'n_detected': detected,
                             'detection_fraction': detected / n if n else None,
                             'gene_count_sum': count_sum,
                             'total_count_sum': total if n else None,
                             'counts_per_million_stratum_counts': count_sum * 1e6 / total if n else None,
                             'n_count_zero': int(np.count_nonzero(v == 0)) if n else None,
                             'n_count_one': int(np.count_nonzero(v == 1)) if n else None,
                             'n_count_ge_two': int(np.count_nonzero(v >= 2)) if n else None})
    return rows


def write_csv(path, rows):
    with path.open('x', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def render(rows, output):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.colors import Normalize

    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9,
                         'svg.fonttype': 'none', 'svg.hashsalt': 'sx22-e1a-v1'})
    labels = LABELS + AGGREGATES
    lookup = {(r['library'], r['pipeline_label_or_aggregate'], r['gene']): r for r in rows}
    denominators = np.array([[lookup[(lib, label, GENES[0])]['n_cells'] for lib in LIBRARIES]
                            for label in labels])
    detection = np.full((len(labels), 6), np.nan)
    abundance = detection.copy()
    for i, label in enumerate(labels):
        for k, lib in enumerate(LIBRARIES):
            for j, gene in enumerate(GENES):
                r = lookup[(lib, label, gene)]
                if r['n_cells']:
                    detection[i, 2*k+j] = r['detection_fraction'] * 100
                    abundance[i, 2*k+j] = r['counts_per_million_stratum_counts']
    fig, axes = plt.subplots(1, 3, figsize=(19, 9), gridspec_kw={'width_ratios': [2, 4.2, 4.2]})
    fig.subplots_adjust(left=.23, right=.98, top=.78, bottom=.27, wspace=.13)
    panel_specs = [(denominators, denominators, 'Greys', Normalize(0, max(1, denominators.max())),
                    'A  Retained cells (n)', ['PBS', 'day 14', 'day 28']),
                   (detection, detection, 'Blues', Normalize(0, 100),
                    'B  Cells with positive count (%)', [f'{lib}\n{gene}' for lib in ('PBS', 'day 14', 'day 28') for gene in GENES]),
                   (abundance, np.log10(1 + abundance), 'YlGnBu',
                    Normalize(0, max(1, np.nanmax(np.log10(1 + abundance)))),
                    'C  Counts per million stratum counts', [f'{lib}\n{gene}' for lib in ('PBS', 'day 14', 'day 28') for gene in GENES])]
    for panel, (ax, spec) in enumerate(zip(axes, panel_specs)):
        raw, color, cmap_name, norm, title, xticks = spec
        cmap = plt.get_cmap(cmap_name).with_extremes(bad='#eeeeee')
        image = ax.imshow(color, aspect='auto', cmap=cmap, norm=norm)
        ax.set_title(title, fontsize=11, pad=13, loc='left')
        ax.set_xticks(range(raw.shape[1]), xticks, fontsize=8)
        ax.xaxis.tick_top(); ax.tick_params(axis='both', length=0)
        ax.set_yticks(range(len(labels)), labels if panel == 0 else [''] * len(labels), fontsize=8.5)
        for i in range(raw.shape[0]):
            for j in range(raw.shape[1]):
                value = raw[i, j]
                text = 'NA' if np.isnan(value) else (f'{int(value):,}' if panel == 0 else f'{value:.1f}')
                ink = 'white' if np.isfinite(color[i, j]) and norm(color[i, j]) > .64 else '#17212b'
                ax.text(j, i, text, ha='center', va='center', fontsize=8, color=ink)
        ax.axhline(len(LABELS)-.5, color='#17212b', linewidth=1.4)
        if panel:
            ax.axvline(1.5, color='white', linewidth=2)
            ax.axvline(3.5, color='white', linewidth=2)
            box = ax.get_position()
            color_axis = fig.add_axes([box.x0, .22, box.width, .02])
            bar = fig.colorbar(image, cax=color_axis, orientation='horizontal')
            bar.set_label('Positive-count cells (%)' if panel == 1 else 'Color = log10(1 + counts per million)', fontsize=8)
            bar.ax.tick_params(labelsize=8)
        for spine in ax.spines.values(): spine.set_visible(False)
    reference = (axes[0].get_position().y0, axes[0].get_position().height)
    require(all(np.allclose((ax.get_position().y0, ax.get_position().height), reference)
                for ax in axes), 'Figure rows are not vertically aligned')
    fig.text(.02, .95, 'Two prespecified transcripts in the saved Choi benchmark', fontsize=19, weight='bold')
    fig.text(.02, .905, 'Observed cells within each library and literal pipeline label. No condition contrasts or population inference.', fontsize=11)
    fig.text(.02, .865, 'PBS: GSM4304609 / PBS_AT2_Tomato     day 14: GSM4304611 / Day14_AT2_Tomato     day 28: GSM4304613 / Day28_AT2_Tomato', fontsize=9)
    fig.text(.02, .145, 'Each library pools two mice; one library per condition. Library, time and processing cannot be separated.', fontsize=10)
    fig.text(.02, .105, 'NA = no retained cells in that label. Zero detection in a populated stratum does not establish biological absence. Labels are not validated cell identities.', fontsize=9)
    fig.text(.02, .065, 'Abundance = 1,000,000 x summed gene counts / summed counts across all saved features in the same stratum. Aggregates overlap the label rows.', fontsize=9)
    fig.text(.02, .025, 'Counts do not measure receptor protein, signaling, responsiveness, memory, lineage or repair. Non-contaminant uses the original label-prefix rule.', fontsize=9)
    for suffix in ('png', 'svg'):
        path = output / f'recipient_transcripts.{suffix}'
        require(not path.exists(), 'Figure already exists')
        fig.savefig(path, dpi=180, metadata={'Date': None} if suffix == 'svg' else {})
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--output', required=True)
    args = parser.parse_args(); output = Path(args.output).resolve()
    require(output.parent == ROOT / 'analysis/research/runs', 'Output outside runner directory')
    require(output.is_dir(), 'Runner must create fresh output directory')
    require(all(p.name in {'receipt.json', 'stdout.log', 'stderr.log'} for p in output.iterdir()), 'Existing output artifacts')
    with h5py.File(SOURCE / 'figure1_descriptive.h5ad', 'r') as source:
        features = strings(source['var/feature']); columns = gene_columns(features)
        obs = {k: strings(source['obs'][k]) for k in ('barcode', 'library', 'gsm', 'timepoint', 'state')}
        cells = list(csv.DictReader((SOURCE / 'cell_states.csv').open(newline='', encoding='utf-8')))
        composition = list(csv.DictReader((SOURCE / 'composition.csv').open(newline='', encoding='utf-8')))
        verify_metadata(obs, cells, composition)
        layer = source['layers/counts']
        require(layer.attrs.get('encoding-type') == 'csr_matrix', 'Changed count encoding')
        shape = tuple(int(x) for x in layer.attrs['shape'])
        require(shape == (len(obs['barcode']), len(features)) == (11683, 27998), 'Changed matrix dimensions')
        matrix = csr_matrix((layer['data'][:], layer['indices'][:], layer['indptr'][:]), shape=shape)
        selected, totals = count_metrics(matrix, columns, source['obs/total_counts'][:])
    rows = summarize(obs, selected, totals)
    write_csv(output / 'strata.csv', rows)
    cell_rows = [dict(sample_prefixed_cell_id=obs['barcode'][i], library=obs['library'][i],
                      pipeline_label=obs['state'][i], total_counts=int(totals[i]),
                      **{g: int(selected[i, j]) for j, g in enumerate(GENES)}) for i in range(len(totals))]
    write_csv(output / 'cell_counts.csv', cell_rows)
    summary = {'scope': 'Observed-cell transcript description only; shared-source reanalysis',
               'genes': list(GENES), 'gene_columns_zero_based': dict(zip(GENES, columns)),
               'cells': len(totals), 'features': len(features), 'stratum_gene_rows': len(rows),
               'empty_stratum_gene_rows': sum(r['status'] == 'empty_stratum' for r in rows),
               'count_layer': 'layers/counts', 'abundance_scale': '1e6 * sum(gene counts) / sum(all saved feature counts in the same stratum)',
               'weighting': 'Ratio of sums, not mean of per-cell normalized values; deeper cells contribute more counts',
               'denominator_rule': 'All labels retained; NON_CONTAMINANT excludes only labels beginning contaminant_',
               'checks': ['Original ordered metadata join', 'Saved composition and all denominators',
                          'Canonical sparse positive integer entries', 'Every saved cell total equals count-row sum'],
               'runtime': {m: importlib.metadata.version(m) for m in ('h5py', 'numpy', 'scipy', 'matplotlib')},
               'scientific_acceptance': 'not_assessed'}
    with (output / 'summary.json').open('x', encoding='utf-8') as stream:
        json.dump(summary, stream, indent=2, allow_nan=False); stream.write('\n')
    render(rows, output)
    print(json.dumps({'cells': len(totals), 'stratum_gene_rows': len(rows), 'status': 'descriptive_execution_complete'}))


if __name__ == '__main__':
    main()
