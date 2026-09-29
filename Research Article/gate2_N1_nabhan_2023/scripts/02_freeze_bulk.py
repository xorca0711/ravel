"""Freeze the adapted bulk analysis after schema QC, before fitting endpoints."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(2**20), b''):
            h.update(b)
    return h.hexdigest()


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--gmt-root', type=Path, required=True)
    args = p.parse_args()
    out = ROOT / 'trials/bulk_v1'
    out.mkdir(parents=True, exist_ok=True)
    assert not (out/'contract.json').exists(), 'Do not overwrite a frozen run'
    config = json.loads((ROOT/'config/pipeline.json').read_text())
    labels = dict(zip(config['primary_deposit']['conditions'], ['Wnt','withdraw48','withdraw24','CHIR','Fzd6','Fzd5']))
    contrasts = {labels[a]+'_vs_'+labels[b]: [labels[a],labels[b]] for a,b in config['primary_contrasts']+config['secondary_contrasts']}
    paths = ['raw/bulk_counts.csv.gz','raw/gene_mapping.tsv','metadata/samples.tsv',
             'metadata/source_panel_membership.tsv','scripts/03_bulk.R']
    resources = [args.gmt_root/n for n in ['mh.all.v2024.1.Mm.symbols.gmt','m5.go.bp.v2024.1.Mm.symbols.gmt']]
    contract = dict(namespace='Nb2',run='bulk_v1',frozen_utc=datetime.now(timezone.utc).isoformat(),
        exposure='Paper, owner notes, prior repository results and schema QC already inspected; new count contrasts not fitted',
        condition_labels=labels,contrasts=contrasts,
        primary_contrasts=list(contrasts)[:3],
        input_hashes={n:sha(ROOT/n) for n in paths},
        gene_set_resources=[dict(name=p.name,path=str(p),sha256=sha(p)) for p in resources],
        filter='raw count >=10 in >=3 of18 libraries; retain all gene IDs for schema record',
        normalization='edgeR TMM on filtered assigned counts; limma voom; source internal normalization not recovered',
        model='unpaired ~0+condition, rank6; residual12; eBayes nonrobust',
        unit='deposited library; authors report independent animals OR cultures; independence/pairing not independently verified',
        inference='Conditional model diagnostic only; no confirmed donor-level inference, equivalence, or causal fate interpretation',
        gene_testing='BH per contrast and pooled across10 contrasts; effect/conditional95%CI retained for every tested ID',
        source_thresholds='Report abs log2FC>1 and>2 separately atFDR<.05; caption rawP<.001 andFDR<.001 separately; no target-total fitting',
        panels='Five original Fig4D panels;19/20 mapped; Crim2 unresolved; three-gene Hippo is adapted and cannot stand for complete source panel',
        panel_endpoint='Per-library mean log2CPM; descriptive mean contrast and range of9 cross-arm library differences; genes not independent replicates',
        panel_display='Gene-wise z-score across18 libraries, then mean by panel for display only',
        wnt_sensitivity='Original4 genes and prespecified3gene panel without Birc5',
        enrichment='CAMERA against all expressed unique-symbol genes; GO BP+Hallmark sets15..500; correlation.01; BH per/all contrasts; Hallmark estimated-correlation sensitivity',
        practical_effect='No validated biological importance/equivalence margin; source thresholds descriptive, no equivalence test',
        qc='Top2000variance genes PCA; no outcome-driven sample deletion',
        scripts_sha256={Path(__file__).name:sha(__file__)})
    (out/'contract.json').write_text(json.dumps(contract,indent=2)+'\n')
    print('Frozen bulk_v1; contract SHA256',sha(out/'contract.json'))


if __name__=='__main__':
    main()
