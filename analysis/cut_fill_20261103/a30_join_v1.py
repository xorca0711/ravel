"""Audit the actual saved A30 join keys; never attach by row order."""
import argparse,json
from pathlib import Path
import pandas as pd

def main(out):
    out.mkdir(exist_ok=True)
    state=pd.read_csv('analysis/research/runs/wp_a30_state_decomposition_v3/cell_states.csv.gz')
    identity=pd.read_csv('analysis/research/runs/wp_human_signature_transfer_v3/cell_identity_qc.csv.gz')
    common=sorted(set(state.columns)&set(identity.columns));assert common==['donor','tissue']
    assert not identity.duplicated(['gsm','barcode']).any()
    table=state.groupby(common).agg(state_rows=('state','size'),distinct_states=('state','nunique')).join(identity.groupby(common).size().rename('identity_rows'),how='outer').reset_index()
    table['join_pairs']=table.state_rows*table.identity_rows;table.to_csv(out/'join_cardinality.csv',index=False)
    ambiguous=table[(table.state_rows>1)&(table.identity_rows>1)]
    result={'state_columns':state.columns.tolist(),'identity_columns':identity.columns.tolist(),'common_keys':common,'state_rows':len(state),'identity_rows':len(identity),'many_to_many_groups':len(ambiguous),'groups_with_multiple_states':int((table.distinct_states>1).sum()),'disposition':'HOLD saved-state lineage/doublet and matched-null calculation: available shared keys identify donor/compartment, not individual cells. The provenance export uniquely keys raw cells, but no saved-state key links it. Row order, equal counts or expression similarity are not accepted as identity.','reopening_input':'Original barcode-keyed clustering membership/object or a separately authorized, provenance-preserving deterministic reconstruction with exact input/runtime and membership verification. A new state solution would require its own amendment, not silent relabelling.','limits':'No evidence that existing association is false; this is a traceability failure. No new activation, regulatory function, residency or causal inference.'}
    (out/'qualification.json').write_text(json.dumps(result,indent=2))
    (out/'verification.json').write_text(json.dumps({'passed':True,'unique_raw_identity_keys':True,'row_order_join_not_used':True,'state_count_sum':int(table.state_rows.sum()),'identity_count_sum':int(table.identity_rows.sum())},indent=2))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);main(ap.parse_args().output)
