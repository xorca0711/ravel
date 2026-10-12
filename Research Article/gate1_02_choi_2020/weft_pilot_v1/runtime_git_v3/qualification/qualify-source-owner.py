import datetime
import hashlib
import json
import os
import pathlib
import subprocess

base = pathlib.Path(__file__).parent
source = base.parent / 'source'
image = (base / 'image.id').read_text().strip()
evidence = base / 'evidence/qualification-source-owner'
evidence.mkdir()
docker = ['docker', '--host', 'unix:///var/run/docker.sock']

def run_case(name, command, seconds, cpus='2', memory='1g'):
    out = base / 'outputs-source-owner' / name
    out.mkdir(parents=True)
    out.chmod(0o777)
    container_name = 'ravel-v3-owner-' + name
    args = docker + ['create', '--name', container_name, '--network=none', '--read-only',
        '--cpus', cpus, '--memory', memory, '--memory-swap', memory, '--pids-limit', '128',
        '--user', '1000:1000', '--cap-drop=ALL', '--security-opt=no-new-privileges:true',
        '--env', 'PYTHONDONTWRITEBYTECODE=1', '--env', 'GIT_OPTIONAL_LOCKS=0',
        '--mount', f'type=bind,src={source},dst=/repo,readonly',
        '--mount', f'type=bind,src={out},dst=/tmp', '--workdir', '/repo',
        image, 'timeout', '--signal=TERM', '--kill-after=5s', str(seconds)+'s'] + command
    cid = subprocess.check_output(args, text=True).strip()
    completed = subprocess.run(docker + ['start', '--attach', cid], capture_output=True, text=True, timeout=seconds+30)
    (evidence / (name+'.stdout')).write_text(completed.stdout)
    (evidence / (name+'.stderr')).write_text(completed.stderr)
    info = json.loads(subprocess.check_output(docker+['inspect', cid], text=True))[0]
    receipt = {'case':name, 'image':info['Image'], 'deadline_seconds':seconds, 'kill_after_seconds':5,
        'state':info['State'], 'controls':{k:info['HostConfig'][k] for k in ['NetworkMode','NanoCpus','Memory','MemorySwap','PidsLimit','ReadonlyRootfs','CapDrop','SecurityOpt']},
        'source_mount_readonly':True, 'source_commit':'47a2fe5bd07742ddddbd0c5aa5f3e0a4b21172e6',
        'command':command, 'output_sha256':hashlib.sha256(completed.stdout.encode()).hexdigest()}
    (evidence/(name+'.json')).write_text(json.dumps(receipt,indent=2)+'\n')
    subprocess.run(docker+['rm',cid],check=True,capture_output=True)
    print(json.dumps({'case':name,'exit_code':info['State']['ExitCode'],'oom_killed':info['State']['OOMKilled']}),flush=True)
    assert info['State']['ExitCode']==0 and not info['State']['OOMKilled'], name
    return completed.stdout

run_case('numerical-synthetic', ['python','-I','/synthetic.py'], 300, '4', '3g')
run_case('committed-source', ['python','-I','-c',
    "import pathlib,sys,json;sys.path.insert(0,'/repo/analysis');from lib.research_governance import committed,git;root=pathlib.Path('/repo');assert git(root,'rev-parse','HEAD').decode().strip()=='47a2fe5bd07742ddddbd0c5aa5f3e0a4b21172e6';paths=['analysis/scripts/research_gate.py','analysis/lib/research_governance.py','analysis/tests/test_research_governance.py'];assert all(committed(root,p) for p in paths);print(json.dumps({'status':'PASS','committed_source_checks':paths,'git_commit':git(root,'rev-parse','HEAD').decode().strip()}))"], 30)
run_case('ravel-synthetic-runner', ['python','-B','/repo/analysis/tests/test_research_governance.py','GovernanceTests.test_runner_receipt_overwrite_and_output_integrity'], 60)
