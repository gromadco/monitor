"""
Script to get all milestones for active projects.
Input file: `active_projects.json`.
Outoput file: `all_milestones.json`.
"""

import json
import requests

INPUT_FILE = 'active_projects.json'
OUTPUT_FILE = 'all_milestones.json'

GITHUB_API_BASE_URL = 'https://api.github.com'
ISSUES_TEMPLATE = '{base_url}/repos/{user}/{repo}/issues'
MILESTONES_TEMPLATE = '{base_url}/repos/{user}/{repo}/milestones'

with open(INPUT_FILE) as f:
    projects = json.load(f)

milestones = []

for p in projects:
    user, repo = p.split('/')
    url = MILESTONES_TEMPLATE.format(
        base_url=GITHUB_API_BASE_URL,
        user=user,
        repo=repo)
    response = requests.get(url)
    data = json.loads(response.content)
    print data
    milestones.append({"project": p, "data": data})

with open(OUTPUT_FILE, 'w') as f:
    json.dump(milestones, f, indent=2, sort_keys=True)
