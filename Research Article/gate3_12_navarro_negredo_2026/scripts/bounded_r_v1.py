"""Run a hash-bound R stage with memory/time limits; invoked only by Ravel's runner."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

p=argparse.ArgumentParser()
p.add_argument('--script',required=True)
p.add_argument('--config',required=True)
p.add_argument('--output',required=True)
a=p.parse_args()
out=Path(a.output)
env=dict(os.environ,R_MAX_VSIZE='11G',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
rscript=shutil.which('Rscript')
if not rscript: raise RuntimeError('Rscript is unavailable')
start=time.monotonic()
proc=subprocess.Popen([rscript,'--vanilla',a.script,a.config,str(out)],env=env)
peak_rss=peak_cgroup=0
reason=None
while proc.poll() is None:
    try:
        rows=Path(f'/proc/{proc.pid}/status').read_text().splitlines()
        rss=next(int(s.split()[1])*1024 for s in rows if s.startswith('VmRSS:'))
        cgroup=int(Path('/sys/fs/cgroup/memory.current').read_text())
        peak_rss=max(peak_rss,rss);peak_cgroup=max(peak_cgroup,cgroup)
        if rss>12*1024**3: reason='RSS exceeded 12 GiB'
        if cgroup>15*1024**3: reason='cgroup memory exceeded 15 GiB'
        if time.monotonic()-start>1800: reason='wall time exceeded 1800 seconds'
        if reason:
            proc.terminate()
            try: proc.wait(timeout=10)
            except subprocess.TimeoutExpired: proc.kill();proc.wait()
            break
    except (FileNotFoundError,StopIteration): pass
    time.sleep(0.5)
result={'R_exit_code':proc.wait(),'elapsed_seconds':round(time.monotonic()-start,3),
        'peak_R_RSS_bytes':peak_rss,'peak_cgroup_bytes':peak_cgroup,
        'R_MAX_VSIZE':'11G','RSS_stop_bytes':12*1024**3,'cgroup_stop_bytes':15*1024**3,
        'stop_reason':reason,'source_input_modified':False}
(out/'resource_usage.json').write_text(json.dumps(result,indent=2)+'\n')
if result['R_exit_code'] or reason: sys.exit(1)
