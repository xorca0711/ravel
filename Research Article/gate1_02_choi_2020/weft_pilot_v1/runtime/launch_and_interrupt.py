import pathlib,subprocess,time,json,os
b=pathlib.Path(__file__).parent
p=subprocess.Popen(['python',str(b/'watchdog_launcher.py')],stdout=(b/'launcher.stdout').open('w'),stderr=(b/'launcher.stderr').open('w'))
for _ in range(2400):
 if (b/'watchdog-identities.json').exists():break
 if p.poll() is not None:raise RuntimeError('launcher failed; inspect stderr')
 time.sleep(.05)
assert (b/'watchdog-identities.json').exists()
p.kill();p.wait();(b/'launcher-interrupted.json').write_text(json.dumps({'pid':p.pid,'exit':p.returncode,'signal':'SIGKILL','time':time.time(),'controller_pid':os.getpid()}))
print('Launcher killed after container/process capture:',p.returncode)
