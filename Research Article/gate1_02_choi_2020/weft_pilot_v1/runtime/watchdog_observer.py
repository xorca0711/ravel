import pathlib,subprocess,json,time,os
b=pathlib.Path(__file__).parent;identity=json.loads((b/'watchdog-identities.json').read_text());interruption=json.loads((b/'launcher-interrupted.json').read_text())
D=['env','-u','DOCKER_HOST','-u','DOCKER_CONTEXT','-u','DOCKER_TLS','-u','DOCKER_TLS_VERIFY','-u','DOCKER_CERT_PATH','docker','--host=unix:///var/run/docker.sock'];cid=identity['container']
for _ in range(120):
 i=json.loads(subprocess.check_output(D+['inspect',cid],text=True))[0]
 if not i['State']['Running']:break
 time.sleep(.1)
assert not i['State']['Running']
logs=subprocess.run(D+['logs',cid],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True).stdout;(b/'watchdog.log').write_text(logs)
checks=[]
for v in identity['host_processes']:
 p=pathlib.Path(f"/proc/{v['host_pid']}/stat")
 current=p.read_text().split()[21] if p.exists() else None
 checks.append({**v,'current_starttime':current,'original_identity_absent':current!=v['starttime']})
ns=[json.loads(l) for l in logs.splitlines() if l.startswith('{')]
assert {x['role'] for x in ns}=={'parent','child','grandchild'} and len({x['pgid'] for x in ns})==1
assert all(c['original_identity_absent'] for c in checks) and i['State']['ExitCode']==137 and not i['State']['OOMKilled']
receipt={'status':'PASS','image':i['Image'],'watchdog':'official GNU timeout --signal=TERM --kill-after=1s 6s','deadline_seconds':6,'kill_after_seconds':1,'host_launcher_interrupted':interruption,'observer_pid':os.getpid(),'observer_is_new_process':os.getpid()!=interruption['pid'],'namespace_processes':ns,'host_identity_checks':checks,'container_state':i['State'],'terminal_container_pid':i['State']['Pid'],'actual_container_seconds':( __import__('datetime').datetime.fromisoformat(i['State']['FinishedAt'].replace('Z','+00:00'))-__import__('datetime').datetime.fromisoformat(i['State']['StartedAt'].replace('Z','+00:00'))).total_seconds(),'controls':{k:i['HostConfig'][k] for k in ['NetworkMode','NanoCpus','Memory','MemorySwap','PidsLimit','ReadonlyRootfs','CapDrop','SecurityOpt']},'user':i['Config']['User'],'host_timeout_used_as_proof':False,'failures':[]}
(b/'watchdog-receipt.json').write_text(json.dumps(receipt,indent=2));print(json.dumps({'status':receipt['status'],'exit':i['State']['ExitCode'],'duration':receipt['actual_container_seconds'],'captured_host_processes':len(checks),'all_absent':True}))
subprocess.check_call(D+['rm',cid],stdout=subprocess.DEVNULL)
