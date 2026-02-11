#!/usr/bin/env python3
"""Check health of Spark1 and Spark2 nodes.
Attempts a simple ping; if that fails, tries an SSH command.
Outputs JSON with keys 'spark1' and 'spark2' each containing
status: 'ok' or 'unreachable' and optional 'error' message.
"""
import json
import subprocess
import sys

NODES = ['spark1', 'spark2']

def ping(host):
    try:
        subprocess.check_output(['ping', '-c', '1', '-W', '2', host], stderr=subprocess.STDOUT)
        return True, None
    except subprocess.CalledProcessError as e:
        return False, e.output.decode()

def ssh_check(host):
    # Simple SSH command; assumes keyless SSH works.
    try:
        subprocess.check_output(['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=5', f'{host}', 'echo ok'], stderr=subprocess.STDOUT)
        return True, None
    except Exception as e:
        return False, str(e)

def check_node(host):
    ok, err = ping(host)
    if ok:
        return {'status': 'ok'}
    # try ssh as fallback
    ok2, err2 = ssh_check(host)
    if ok2:
        return {'status': 'ok'}
    return {'status': 'unreachable', 'error': err or err2}

def main():
    results = {}
    for node in NODES:
        results[node] = check_node(node)
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()
