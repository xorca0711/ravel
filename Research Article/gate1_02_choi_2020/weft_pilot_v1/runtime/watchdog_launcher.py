import pathlib,subprocess,json,time,os
b=pathlib.Path(__file__).parent
D=['env','-u','DOCKER_HOST','-u','DOCKER_CONTEXT','-u','DOCKER_TLS','-u','DOCKER_TLS_VERIFY','-u','DOCKER_CERT_PATH','docker','--host=unix:///var/run/docker.sock']
image='sha256:c9c7fb60b86d4608c2420d662d386bab33dde70b3b4fa9cd01e7ca8bdc9e6902'
name='weft-watchdog-20261011'
a=D+['create','--name',name,'--network','none','--cpus','1','--memory','256m','--memory-swap','256m','--pids-limit','32','--user','65534:65534','--read-only','--cap-drop','ALL','--security-opt','no-new-privileges:true','--mount',f'type=bind,src={b}/watchdog_case.py,dst=/case.py,readonly',image,'timeout','--signal=TERM','--kill-after=1s','6s','python','-I','-u','/case.py']
(b/'watchdog-command.json').write_text(json.dumps(a,indent=2));cid=subprocess.check_output(a,text=True).strip();subprocess.check_call(D+['start',cid],stdout=subprocess.DEVNULL)
for _ in range(20):
 top=subprocess.check_output(D+['top',cid,'-eo','pid,ppid,pgid,args'],text=True)
 if 'grandchild' in top:break
 time.sleep(.05)
pids=[]
for l in top.splitlines()[1:]:
 pid=int(l.split()[0]);pids.append({'host_pid':pid,'starttime':pathlib.Path(f'/proc/{pid}/stat').read_text().split()[21]})
(b/'watchdog-identities.json').write_text(json.dumps({'container':cid,'launcher_pid':os.getpid(),'host_processes':pids,'top':top,'obtained_at':time.time()},indent=2))
while True:time.sleep(1)
