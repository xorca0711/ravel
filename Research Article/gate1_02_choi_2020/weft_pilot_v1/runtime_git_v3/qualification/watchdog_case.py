import os,sys,time,signal,subprocess,json
signal.signal(signal.SIGTERM,signal.SIG_IGN)
role=sys.argv[1] if len(sys.argv)>1 else 'parent'
if role=='parent':subprocess.Popen([sys.executable,__file__,'child'])
elif role=='child':subprocess.Popen([sys.executable,__file__,'grandchild'])
print(json.dumps({'role':role,'namespace_pid':os.getpid(),'ppid':os.getppid(),'pgid':os.getpgrp(),'starttime':open('/proc/self/stat').read().split()[21]}),flush=True)
time.sleep(60)
