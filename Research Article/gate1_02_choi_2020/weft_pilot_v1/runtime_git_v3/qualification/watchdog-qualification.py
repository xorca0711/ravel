"""Repeat the unchanged tiny watchdog fixture on the derived image; no science."""
import datetime
import json
import os
import pathlib
import signal
import subprocess
import sys
import time

base = pathlib.Path(__file__).parent
evidence = base / 'evidence/watchdog'
evidence.mkdir(exist_ok=True)
image = (base/'image.id').read_text().strip()
case = base.parent/'source/Research Article/gate1_02_choi_2020/weft_pilot_v1/runtime/watchdog_case.py'
docker = ['docker','--host','unix:///var/run/docker.sock']

if len(sys.argv)>1 and sys.argv[1]=='launcher':
    args = docker+['create','--name','ravel-v3-watchdog','--network=none','--cpus=1',
        '--memory=256m','--memory-swap=256m','--pids-limit=32','--user=1000:1000',
        '--read-only','--cap-drop=ALL','--security-opt=no-new-privileges:true',
        '--mount',f'type=bind,src={case},dst=/case.py,readonly',image,
        'timeout','--signal=TERM','--kill-after=1s','6s','python','-I','-u','/case.py']
    cid=subprocess.check_output(args,text=True).strip()
    subprocess.run(docker+['start',cid],check=True,capture_output=True)
    captured=[]
    for _ in range(40):
        top=subprocess.check_output(docker+['top',cid,'-eo','pid,ppid,pgid,args'],text=True)
        if 'grandchild' in top:break
        time.sleep(.05)
    assert 'grandchild' in top
    for line in top.splitlines()[1:]:
        pid=int(line.split()[0])
        captured.append({'pid':pid,'starttime':pathlib.Path(f'/proc/{pid}/stat').read_text().split()[21]})
    (evidence/'local-process-identities.json').write_text(json.dumps({'cid':cid,'captured':captured,'launcher_pid':os.getpid()}))
    while True:time.sleep(1)

launcher=subprocess.Popen([sys.executable,__file__,'launcher'],stdout=(evidence/'launcher.stdout').open('w'),stderr=(evidence/'launcher.stderr').open('w'))
for _ in range(150):
    if (evidence/'local-process-identities.json').exists():break
    if launcher.poll() is not None:raise RuntimeError('launcher failed')
    time.sleep(.1)
assert (evidence/'local-process-identities.json').exists()
identity=json.loads((evidence/'local-process-identities.json').read_text())
launcher.kill();launcher.wait(timeout=5)
assert launcher.returncode == -signal.SIGKILL
cid=identity['cid']
for _ in range(150):
    info=json.loads(subprocess.check_output(docker+['inspect',cid],text=True))[0]
    if not info['State']['Running']:break
    time.sleep(.1)
assert not info['State']['Running']
logs=subprocess.check_output(docker+['logs',cid],text=True)
roles=[json.loads(line) for line in logs.splitlines() if line.startswith('{')]
assert {x['role'] for x in roles}=={'parent','child','grandchild'}
assert len({x['pgid'] for x in roles})==1
absent=[]
for item in identity['captured']:
    file=pathlib.Path(f"/proc/{item['pid']}/stat")
    current=file.read_text().split()[21] if file.exists() else None
    absent.append(current!=item['starttime'])
assert all(absent)
state=info['State']
assert state['ExitCode']==137 and not state['OOMKilled'] and state['Pid']==0
duration=(datetime.datetime.fromisoformat(state['FinishedAt'].replace('Z','+00:00'))-datetime.datetime.fromisoformat(state['StartedAt'].replace('Z','+00:00'))).total_seconds()
assert 6<=duration<=12
receipt={'status':'PASS','image':info['Image'],'watchdog':'GNU timeout --signal=TERM --kill-after=1s 6s',
    'deadline_seconds':6,'kill_after_seconds':1,'launcher_exit_code':launcher.returncode,
    'launcher_killed_after_all_three_fixture_processes_observed':True,
    'observer_is_separate_process_from_launcher':os.getpid()!=identity['launcher_pid'],
    'fixture_roles':sorted(x['role'] for x in roles),'fixture_processes_share_process_group':True,
    'captured_process_identity_count':len(absent),'all_original_process_identities_absent':all(absent),
    'container_running':state['Running'],'container_exit_code':state['ExitCode'],'container_pid_zero':state['Pid']==0,
    'oom_killed':state['OOMKilled'],'actual_container_seconds':duration,
    'controls':{k:info['HostConfig'][k] for k in ['NetworkMode','NanoCpus','Memory','MemorySwap','PidsLimit','ReadonlyRootfs','CapDrop','SecurityOpt']},
    'host_timeout_used_as_proof':False,
    'limits':['Tiny synthetic process tree only; does not qualify biological workloads, host power loss, or daemon failure.']}
(evidence/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
subprocess.run(docker+['rm',cid],check=True,capture_output=True)
print(json.dumps(receipt),flush=True)
