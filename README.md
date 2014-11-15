List all active projects in `active_projects.json`. Format:

```json
[
  "user/project", 
  ...
]
```

Run `get_all_milestones.py` that saves data to `all_milestones.json`.
Edit this JSON file leaving only active milestones.

Get data about all tickets for these milestones with `get_all_issues.py`.
Data is saved to `data/yyyy-mm-dd.json`.

Cron to repeat. For example

```crontab
00 11,16,21 * * * cd path/to/script && path/to/python get_all_issues.py
```
