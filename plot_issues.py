import json
import os

with open('active_milestones.json', 'r') as f:
    data = json.load(f)

milestones = []

for d in data:
    milestones.append(d['data'][0]['url'])

print milestones

# print date - number of open issues - number of closed issues

closed_count_list = []

for dirpath, dirnames, filenames in os.walk('data'):
    for filename in filenames:
        print filename
        with open(os.path.join('data', filename)) as f:
            data = json.load(f)
            open_count = len(filter(lambda x: x['state'] == 'open', data[0]['issues']))
            closed_count = len(filter(lambda x: x['state'] == 'closed', data[0]['issues']))
            closed_count_list.append(closed_count)

print closed_count_list
