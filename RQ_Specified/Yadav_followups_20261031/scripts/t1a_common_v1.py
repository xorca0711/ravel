"""Source-preserving XLSX reader and fixed descriptive arithmetic for T1-A."""
import csv
import json
import math
import statistics
import xml.etree.ElementTree as ET
import zipfile
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parents[1]
BOOK = ROOT / 'raw_data/Yadav_followups_T0_20261031/hamanaka_metabolomics_v1.xlsx'
NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}


def columns(first, last):
    def number(value):
        n = 0
        for c in value:
            n = n * 26 + ord(c) - 64
        return n
    def label(n):
        out = ''
        while n:
            n, r = divmod(n - 1, 26)
            out = chr(r + 65) + out
        return out
    return [label(n) for n in range(number(first), number(last) + 1)]


def workbook(allowed_sheets):
    result = {}
    with zipfile.ZipFile(BOOK) as z:
        shared = [''.join(e.itertext()) for e in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('s:si', NS)]
        rels = {e.get('Id'): e.get('Target') for e in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
        book = ET.fromstring(z.read('xl/workbook.xml'))
        for sheet in book.findall('s:sheets/s:sheet', NS):
            if sheet.get('name') not in allowed_sheets:
                continue
            rid = sheet.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
            target = rels[rid]
            target = target.lstrip('/') if target.startswith('/') else 'xl/' + target
            tree = ET.fromstring(z.read(target))
            cells = {}
            for c in tree.findall('.//s:c', NS):
                v, f = c.find('s:v', NS), c.find('s:f', NS)
                raw = '' if v is None else v.text or ''
                kind = c.get('t', 'n')
                text = shared[int(raw)] if kind == 's' else ''.join(c.find('s:is', NS).itertext()) if kind == 'inlineStr' else raw
                cells[c.get('r')] = {'raw': raw, 'text': text, 'kind': kind,
                                     'formula': '' if f is None else f.text or ''}
            result[sheet.get('name')] = cells
    return result


def cell(sheet, address):
    return sheet.get(address, {'raw': '', 'text': '', 'kind': 'missing', 'formula': ''})


def number(c):
    if c['formula']:
        return None, 'formula_cached_value_not_used'
    if c['kind'] not in ('n', '') or c['raw'] == '':
        return None, 'missing' if c['raw'] == '' else 'nonnumeric'
    try:
        value = Decimal(c['raw'])
    except InvalidOperation:
        return None, 'nonnumeric'
    if not value.is_finite():
        return None, 'nonfinite'
    if value < 0:
        return value, 'negative'
    return value, 'valid'


def closure_tolerance(raw_values, scale):
    """64 binary64 ulps of candidate scale per term, never a biological margin.

    This conservatively covers binary64 arithmetic and Excel's 15-significant-
    digit decimal serialization. Short literals such as 0.4 are not assumed to
    mean rounding to one decimal place. No tolerance is fitted to the outcomes.
    """
    return Decimal(str(math.ulp(float(scale)))) * 64 * len(raw_values)


def fraction_candidates(cells):
    parsed = [number(c) for c in cells]
    if any(status != 'valid' for _, status in parsed):
        return {'status': 'invalid_fraction_cell', 'sum': '', 'candidates': [], 'tolerance_1': '', 'tolerance_100': ''}
    total = sum((value for value, _ in parsed), Decimal(0))
    tolerances = {str(s): closure_tolerance([c['raw'] for c in cells], s) for s in [1, 100]}
    candidates = [str(s) for s in [1, 100] if abs(total - s) <= tolerances[str(s)]]
    return {'status': 'scale_candidate' if len(candidates) == 1 else 'closure_ambiguous_or_failed',
            'sum': str(total), 'candidates': candidates,
            'tolerance_1': str(tolerances['1']), 'tolerance_100': str(tolerances['100'])}


def summary(records, require_fraction=False):
    valid = [r for r in records if r['value_status'] == 'valid' and (not require_fraction or r['fraction_status'] == 'qualified')]
    result = {'n_supplied': len(records), 'n_valid': len(valid), 'status': 'qualified' if records and len(valid) == len(records) else 'held',
              'mean': '', 'minimum': '', 'maximum': ''}
    if result['status'] == 'qualified':
        values = [Decimal(r['numeric_value']) for r in records]
        result.update(mean=str(sum(values) / len(values)), minimum=str(min(values)), maximum=str(max(values)))
    return result


def table(path, rows):
    if not rows:
        raise ValueError('No records for ' + str(path))
    with path.open('x', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def dump(path, data):
    with path.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')


def literal_fields(c):
    value, status = number(c)
    return {'source_type': c['kind'], 'source_raw_value': c['raw'], 'source_text': c['text'],
            'source_formula': c['formula'], 'numeric_value': '' if value is None else str(value), 'value_status': status}
