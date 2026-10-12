import json
import subprocess
for item in json.load(open('/packages.lock.json')):
    actual = subprocess.check_output(['dpkg-query', '-W', '-f=${Version}', item['package']], text=True)
    assert actual == item['version'], (item['package'], actual, item['version'])
print('All downloaded Debian package versions match the verified lock.')
