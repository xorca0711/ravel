"""Independent raw-count semantic check and exact v1 preservation audit."""
import argparse
import csv
import gzip
import hashlib
import itertools
import json
from pathlib import Path


def rows(path):
    opener = gzip.open if path.suffix == '.gz' else open
    with opener(path, 'rt', encoding='utf-8', newline='') as handle:
        yield from csv.DictReader(handle, delimiter='\t')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def raw_counts(paths):
    result = {}
    for number in range(2440985, 2441001):
        gsm = 'GSM' + str(number)
        found = [p for p in paths if p.name.startswith(gsm + '_') and p.name.endswith('.tab.gz')]
        assert len(found) == 1, ('raw source identity', gsm)
        counts = {}
        with gzip.open(found[0], 'rt', encoding='utf-8') as handle:
            for fields in csv.reader(handle, delimiter='\t'):
                assert len(fields) == 2 and fields[0] not in counts
                count = int(fields[1])
                assert count >= 0
                counts[fields[0]] = count
        if result:
            assert counts.keys() == next(iter(result.values())).keys(), 'raw gene universe'
        result[gsm] = counts
    return result


def expected_count_fields(counts, gene):
    result = {}
    for stage, phase, start in [('s2', 'D6', 2440985), ('s2', 'D30', 2440989),
                                ('s4', 'B0', 2440989), ('s4', 'W6', 2440993), ('s4', 'W12', 2440997)]:
        zero = [counts['GSM' + str(i)][gene] == 0 for i in range(start, start + 4)]
        prefix = stage + '__' + phase
        result[prefix + '_zero_libraries'] = str(sum(zero))
        result[prefix + '_control_zero'] = str(all(zero[:2]))
        result[prefix + '_exposed_zero'] = str(all(zero[2:]))
        result[prefix + '_all_zero'] = str(all(zero))
    b = [counts['GSM' + str(i)][gene] == 0 for i in range(2440989, 2440993)]
    result['s4b__primary_reference_any_zero'] = str(all(b[:2]) or all(b[2:]))
    result['s4b__c2_h2_reference_any_zero'] = str(b[1] or b[3])
    result['s4b__c1_h1_reference_any_zero'] = str(b[0] or b[2])
    return result


def verify(source, output, paths):
    checks = 0
    def same(actual, expected, label):
        nonlocal checks
        checks += 1
        assert actual == expected, (label, actual, expected)

    copied = ['gene_atac.tsv.gz', 'association_results.tsv', 'covariance_identity.tsv',
              'fig01_associations.png', 'fig01_associations.pdf']
    for name in copied:
        same(sha(output / name), sha(source / name), 'byte preservation: ' + name)
    counts = raw_counts(paths)
    flags_by_gene = {}
    summary_counts = {u: {'count': 0, 'range': 0, 'range_only': 0} for u in ['primary', 'all_mapped']}
    removed_false_positives = 0
    old_name, count_name, range_name = 'rna_any_zero_flag', 'rna_any_count_zero_flag', 'rna_any_adjustment_range_includes_zero_flag'
    for old, new in itertools.zip_longest(rows(source / 'gene_join.tsv.gz'), rows(output / 'gene_join.tsv.gz')):
        assert old is not None and new is not None, 'row count mismatch'
        gene = old['gene_id']
        assert gene not in flags_by_gene, 'duplicate gene'
        wanted_source = expected_count_fields(counts, gene)
        for field, expected in wanted_source.items():
            same(old[field], expected, 'source flag versus raw counts: ' + gene + ':' + field)
        count_flag = any(library[gene] == 0 for library in counts.values())
        crossing_values = [old['s4__W6_adjustment_range_includes_zero'], old['s4__W12_adjustment_range_includes_zero']]
        assert set(crossing_values) <= {'True', 'False'}
        crossing_flag = 'True' in crossing_values
        expected = {k: v for k, v in old.items() if k != old_name}
        expected.update({count_name: str(count_flag), range_name: str(crossing_flag)})
        same(set(new), set(expected), 'corrected schema')
        for field, value in expected.items():
            same(new[field], value, 'copied or corrected field: ' + gene + ':' + field)
        same(old[old_name], str(count_flag or crossing_flag), 'bounded v1 defect')
        flags_by_gene[gene] = {count_name: count_flag, range_name: crossing_flag}
        removed_false_positives += old[old_name] == 'True' and not count_flag
        for u, totals in summary_counts.items():
            if old['universe_' + u] == 'True':
                totals['count'] += count_flag
                totals['range'] += crossing_flag
                totals['range_only'] += crossing_flag and not count_flag
    same(set(flags_by_gene), set(next(iter(counts.values()))), 'complete source gene universe')

    for old, new in itertools.zip_longest(rows(source / 'anchor_values.tsv'), rows(output / 'anchor_values.tsv')):
        assert old is not None and new is not None
        expected = {k: v for k, v in old.items() if k != old_name}
        expected.update({k: str(v) for k, v in flags_by_gene[old['gene_id']].items()})
        same(new, expected, 'all anchor values and flags')
    manifest = json.loads((source / 'anchor_manifest.json').read_text())
    for item in manifest:
        if item['source_record_present']:
            del item[old_name]
            item.update(flags_by_gene[item['gene_id']])
    same(json.loads((output / 'anchor_manifest.json').read_text()), manifest, 'anchor manifest')

    old_summary = json.loads((source / 'universe_summary.json').read_text())
    new_summary = json.loads((output / 'universe_summary.json').read_text())
    for u, block in old_summary['universes'].items():
        del block['rna_any_zero_genes']
        block.update(rna_any_count_zero_genes=summary_counts[u]['count'],
                     rna_any_adjustment_range_includes_zero_genes=summary_counts[u]['range'],
                     range_includes_zero_without_count_zero_genes=summary_counts[u]['range_only'])
    old_summary['analysis_id'] = new_summary['analysis_id']
    same(new_summary, old_summary, 'complete summary; no other changes')
    audit = json.loads((output / 'flag_correction_audit.json').read_text())
    same(audit['gene_records'], len(flags_by_gene), 'audit gene count')
    same(audit['v1_true_count_zero_false'], removed_false_positives, 'audit false positives')
    same(audit['v1_false_count_zero_true'], 0, 'audit missed zeros')
    same(set(audit['count_zero_allowlist']), set(wanted_source), 'explicit count allowlist')
    same(audit['range_includes_zero_allowlist'], ['s4__W6_adjustment_range_includes_zero', 's4__W12_adjustment_range_includes_zero'], 'explicit range allowlist')
    same(audit['byte_preserved_files'], copied, 'declared copies')
    same(audit['all_original_source_fields_preserved'], True, 'copy audit status')
    for name, expected_n in [('association_results.tsv', 312), ('covariance_identity.tsv', 96)]:
        # Fixture tables may have fewer rows; byte identity remains mandatory.
        same(sum(1 for _ in rows(output / name)), sum(1 for _ in rows(source / name)), name + ' row count')
    return dict(status='passed', checks=checks, gene_records=len(flags_by_gene), raw_count_libraries=16,
                raw_count_zero_semantics_verified=True, v1_false_positive_count_flags=removed_false_positives,
                byte_preserved_files=copied, all_other_source_fields_and_eligibility_unchanged=True,
                numerical_coefficients_recomputed=False, independent_biological_replication=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--contract', type=Path, required=True)
    parser.add_argument('--run-dir', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    c = json.loads(args.contract.read_text(encoding='utf-8-sig'))
    inputs = [root / x['path'] for x in c['inputs']]
    source = next(p for p in inputs if p.name == 'gene_join.tsv.gz').parent
    result = verify(source, args.run_dir, inputs)
    result['analysis_id'] = c['analysis_id']
    for name, number in [('association_results.tsv', 312), ('covariance_identity.tsv', 96)]:
        assert sum(1 for _ in rows(args.run_dir / name)) == number
    (args.run_dir / 'verification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result), flush=True)
