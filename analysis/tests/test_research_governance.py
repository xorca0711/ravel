"""Adversarial contract/runner tests using synthetic files, never biological data."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from lib.research_governance import (ResearchError, DOSSIER_SECTIONS, check_registry,
    contract_errors, execute, receipt_errors, sha256, within)

REPO=Path(__file__).resolve().parents[2]


class GovernanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        def write(path,text):
            p=self.root/path; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(text,encoding='utf-8')
        self.write=write
        write('analysis/research/contract.schema.json',(REPO/'analysis/research/contract.schema.json').read_text())
        write('RESEARCH_QUESTIONS.md','### A1. A synthetic question\n')
        write('dossier.md','\n'.join('## '+s+'\nSynthetic test content describing a bounded scientific decision.\n' for s in DOSSIER_SECTIONS))
        write('evidence.md','Synthetic source context only.\n')
        write('input.txt','synthetic input\n')
        write('analysis/run.py','import pathlib,sys\npathlib.Path(sys.argv[1], "result.json").write_text("{}")\n')
        self.index={'questions':[{'id':'A1','card':'RESEARCH_QUESTIONS.md#a1','dossier':'dossier.md','evidence':['evidence.md']}],
                    'article_candidates':[],'contracts':[],'receipts':[],'infrastructure_paths':[]}
        self.save_index()
        write('analysis/research/legacy_artifacts.json','{"artifacts": []}')
        template=json.loads((REPO/'analysis/research/contract.template.json').read_text())
        for key,value in template.items():
            if isinstance(value,str) and value.startswith('REPLACE:'):
                template[key]='Synthetic declared design with a meaningful decision and explicit limitation.'
        self.c=template
        self.c.update(analysis_id='A1.synthetic_v1',owner='A1',status='frozen',analysis_type='exploratory',
            biological_unit='Independent donor',unit_status='verified',precision_status='unknown',
            prior_outcome_exposure='exposed',evidence_refs=['evidence.md'],entrypoint='analysis/run.py',
            code=[{'path':'analysis/run.py','sha256':sha256(self.root/'analysis/run.py')}],
            inputs=[{'path':'input.txt','sha256':sha256(self.root/'input.txt'),'study_id':'synthetic-study',
                     'unit_ids':['synthetic-study/donor-1'],'role':'context','independence':'verified','exposure':'exposed'}],
            arguments=['{run_dir}'],expected_outputs=['result.json'])
    def save_index(self): self.write('analysis/research/registry.json',json.dumps(self.index))
    def freeze(self):
        if 'contract.json' not in self.index['contracts']:
            self.index['contracts'].append('contract.json')
            self.save_index()
        self.write('contract.json',json.dumps(self.c))
        subprocess.run(['git','init','-q',str(self.root)],check=True,capture_output=True)
        subprocess.run(['git','-C',str(self.root),'add','.'],check=True,capture_output=True)
        subprocess.run(['git','-C',str(self.root),'-c','user.name=Synthetic Test','-c','user.email=test@example.invalid','commit','-qm','fixture'],check=True,capture_output=True)
    def test_valid_exposed_exploration(self):
        self.assertEqual(contract_errors(self.root,self.c,check_inputs=True),[])
    def test_unknown_and_missing_fields_rejected(self):
        self.c['unexpected']='silently ignored?'; del self.c['strongest_rival']
        errors=contract_errors(self.root,self.c)
        self.assertTrue(any('unknown field' in e for e in errors))
        self.assertTrue(any('missing strongest_rival' in e for e in errors))
    def test_exposed_confirmation_rejected(self):
        self.c.update(analysis_type='confirmatory',precision_status='justified')
        self.assertTrue(any('unexposed' in e for e in contract_errors(self.root,self.c)))
    def test_unsupported_units_block_population_inference(self):
        self.c.update(unit_status='unknown',inference_scope='association')
        self.assertTrue(any('biological units' in e for e in contract_errors(self.root,self.c)))
    def test_external_validation_reuse_rejected(self):
        self.c['inputs'][0]['role']='discovery'
        other=copy.deepcopy(self.c['inputs'][0]); other.update(path='other.txt',role='validation')
        self.c['inputs'].append(other); self.c['validation_scope']='external'
        self.assertTrue(any('overlap' in e for e in contract_errors(self.root,self.c)))
    def test_external_subject_overlap_across_study_labels_rejected(self):
        self.c['inputs'][0]['role']='discovery'
        other=copy.deepcopy(self.c['inputs'][0]); other.update(path='other.txt',study_id='renamed-study',sha256='a'*64,role='validation')
        self.c['inputs'].append(other); self.c['validation_scope']='external'
        self.assertTrue(any('overlap' in e for e in contract_errors(self.root,self.c)))
    def test_causal_design_required(self):
        self.c.update(inference_scope='causal',design_identifiability='unknown')
        self.assertTrue(any('identification' in e for e in contract_errors(self.root,self.c)))
    def test_input_and_code_tampering_detected(self):
        self.write('input.txt','different input'); self.write('analysis/run.py','changed code')
        self.assertEqual(sum('Hash mismatch' in e for e in contract_errors(self.root,self.c,check_inputs=True)),2)
    def test_traversal_rejected(self):
        for path in ('../outside','/absolute','C:/absolute','a\\b'):
            with self.assertRaises(ResearchError): within(self.root,path,exists=False)
    def test_unavailable_input_still_requires_safe_path(self):
        self.c['inputs'][0]['path']='../private-input'
        self.assertTrue(any('Unsafe path' in e for e in contract_errors(self.root,self.c)))
    def test_output_routing_required(self):
        self.c['arguments']=[]
        self.assertTrue(any('route outputs' in e for e in contract_errors(self.root,self.c)))
    def test_malformed_contract_fails_before_execution(self):
        self.c['code']='not an asset list'
        self.write('contract.json',json.dumps(self.c))
        with self.assertRaisesRegex(ResearchError,'expected array'): execute(self.root,'contract.json','bad')
    def test_amendment_must_have_distinct_id(self):
        self.write('predecessor.json',json.dumps(self.c)); self.c['amendment_of']='predecessor.json'
        self.assertTrue(any('new analysis ID' in e for e in contract_errors(self.root,self.c)))
    def test_draft_cannot_run(self):
        self.c['status']='draft'; self.freeze()
        with self.assertRaisesRegex(ResearchError,'frozen'): execute(self.root,'contract.json','draft')
    def test_uncommitted_contract_cannot_run(self):
        self.freeze(); self.c['decision']='A changed decision after the prior freeze must be committed.'
        self.write('contract.json',json.dumps(self.c))
        with self.assertRaisesRegex(ResearchError,'Freeze'): execute(self.root,'contract.json','changed')
    def test_unregistered_contract_cannot_run(self):
        self.freeze(); self.index['contracts']=[]; self.save_index()
        with self.assertRaisesRegex(ResearchError,'registered'): execute(self.root,'contract.json','unregistered')
    def test_frozen_contract_amendment_requires_new_path(self):
        self.freeze(); self.c['decision']='A different decision after exposure must use a versioned amendment.'
        self.write('contract.json',json.dumps(self.c))
        self.assertTrue(any('Frozen contracts changed' in e for e in check_registry(self.root,base='HEAD')))
    def test_prior_contract_cannot_be_deregistered(self):
        self.freeze(); self.index['contracts']=[]; self.save_index()
        self.assertTrue(any('cannot be removed' in e for e in check_registry(self.root,base='HEAD')))
    def test_runner_receipt_overwrite_and_output_integrity(self):
        self.freeze(); receipt=execute(self.root,'contract.json','synthetic-v1')
        rel=receipt.relative_to(self.root).as_posix()
        self.assertEqual(receipt_errors(self.root,rel),[])
        self.assertEqual(json.loads(receipt.read_text())['scientific_acceptance'],'not_assessed')
        with self.assertRaisesRegex(ResearchError,'already exists'): execute(self.root,'contract.json','synthetic-v1')
        (receipt.parent/'result.json').write_text('changed')
        self.assertTrue(any('hash mismatch' in e for e in receipt_errors(self.root,rel)))
    def test_receipt_records_portable_command_without_local_paths(self):
        self.freeze(); receipt=execute(self.root,'contract.json','portable-v1')
        record=json.loads(receipt.read_text())
        self.assertEqual(record['argv_format'],'repository_relative')
        self.assertEqual(record['argv'], ['python','analysis/run.py',
            'analysis/research/runs/portable-v1'])
        self.assertNotIn(str(self.root),json.dumps(record))
        self.assertNotIn(sys.executable,json.dumps(record))
        self.assertEqual(receipt_errors(self.root,receipt.relative_to(self.root).as_posix()),[])
    def test_missing_expected_output_leaves_failed_receipt(self):
        self.c['expected_outputs']=['missing.json']; self.freeze()
        with self.assertRaises(ResearchError): execute(self.root,'contract.json','missing')
        record=json.loads((self.root/'analysis/research/runs/missing/receipt.json').read_text())
        self.assertEqual(record['status'],'execution_failed')
    def test_nonzero_process_leaves_failed_receipt(self):
        self.write('analysis/run.py','raise SystemExit(3)\n')
        self.c['code'][0]['sha256']=sha256(self.root/'analysis/run.py'); self.freeze()
        with self.assertRaises(ResearchError): execute(self.root,'contract.json','failed')
        record=json.loads((self.root/'analysis/research/runs/failed/receipt.json').read_text())
        self.assertEqual(record['exit_code'],3)
    def test_registry_does_not_accept_empty_dossier(self):
        self.write('dossier.md','## Biological problem\nTBD\n')
        self.assertTrue(any('dossier section' in e for e in check_registry(self.root)))
    def test_duplicate_question_id_rejected(self):
        self.index['questions'].append(copy.deepcopy(self.index['questions'][0])); self.save_index()
        self.assertTrue(any('duplicates' in e for e in check_registry(self.root)))
    def test_new_scientific_code_requires_registration(self):
        self.freeze(); self.write('analysis/unregistered.py','print(1)\n')
        self.assertTrue(any('Unregistered scientific asset' in e for e in check_registry(self.root,base='HEAD')))
    def test_historical_artifact_change_detected(self):
        self.write('analysis/research/legacy_artifacts.json',json.dumps({'artifacts':[{'path':'input.txt','sha256':sha256(self.root/'input.txt')}]}))
        self.write('input.txt','modified')
        self.assertTrue(any('Historical artifact changed' in e for e in check_registry(self.root)))


if __name__=='__main__': unittest.main()
