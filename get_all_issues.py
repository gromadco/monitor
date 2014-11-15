"""
Script to get all issues for active milestones.
Input file: `active_milestones.json`.
Output file: `data/yyyy-mm-dd/data.json`.
"""

import datetime
import logging
import os

import json
import requests

INPUT_FILE = 'active_milestones.json'

GITHUB_API_BASE_URL = 'https://api.github.com'
ISSUES_TEMPLATE = '{base_url}/repos/{user}/{repo}/issues?' + \
    'state=all&milestone={milestone}'


def get_data_filename():
    return os.path.join(
        'data/',
        datetime.datetime.now().strftime("%Y-%m-%d.json"))

logging.basicConfig(
    filename=os.path.join(
        os.path.expanduser('~'),
        'logs/gromadco-monitor.log'),
    level=logging.DEBUG,
    format='%(asctime)s %(message)s')
logging.info('started get_all_issues.py')

with open(INPUT_FILE) as f:
    milestones = json.load(f)

for m in milestones:
    user, repo = m['project'].split('/')
    milestone = m['data'][0]['number']
    print user, repo, milestone
    url = ISSUES_TEMPLATE.format(
        base_url=GITHUB_API_BASE_URL,
        user=user,
        repo=repo,
        milestone=milestone)
    response = requests.get(url)
    m['issues'] = json.loads(response.content)

filename = get_data_filename()
with open(filename, 'w') as f:
    json.dump(milestones, f, indent=2, sort_keys=True)
