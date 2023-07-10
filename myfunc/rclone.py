import subprocess
import json

def link(path):
    return subprocess.run(['rclone', 'link', path], capture_output=True).stdout.decode().strip('\n')

def id(path):
    lsjson = json.loads(subprocess.run(['rclone', 'lsjson', path], capture_output=True).stdout.decode())
    return list({'name': i['Name'], 'id': i['ID']} for i in lsjson)

def copy(source, dest):
    subprocess.run(['rclone', 'copy', source, dest, '--drive-server-side-across-configs', '--no-update-modtime'])
