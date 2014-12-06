"""
Creates a csv file with number of issues closed.
"""
import csv
import datetime
import json
from pymongo import MongoClient


db = MongoClient().monitor


def count_active_milestones(date):
    """
    Counts active milestones for a given date
    :param date:
    :return:
    """
    pipeline = [
        {'$match': {'date': date}},
        {'$group': {
            '_id': 'null', 'count': {'$sum': 1}}}]
    return db.data.aggregate(pipeline)['result'][0]['count']


def count_issues(date, project, state=None, max_dates_back=10):
    """
    Counts number of issues with a given state
    for a given project on a given date
    :param date:
    :param project:
    :param state:
    :return:
    """
    pipeline = [
        {'$match': {'date': date, 'project': project}},
        {'$unwind': '$issues'}]
    if state is not None:
        pipeline.append(
            {'$match': {
                'issues.state': state}})
    pipeline.append(
        {'$group': {
            '_id': 'null', 'count': {'$sum': 1}}})
    try:
        return db.data.aggregate(pipeline)['result'][0]['count']
    except IndexError:
        if max_dates_back > 0:
            return count_issues(
                date - datetime.timedelta(1), project, state, max_dates_back=max_dates_back - 1)
        else:
            return 0


def count_closed_delta(date, project):
    """
    Counts difference between issues done for a date and a date before.
    :param date:
    :param project:
    :return:
    """
    return count_issues(date, project, state='closed') - \
        count_issues(date - datetime.timedelta(1), project, state='closed')


def find_min_date():
    return db.data.find().sort([('date', 1)])[0]['date']


def find_max_date():
    return db.data.find().sort([('date', -1)])[0]['date']


with open('active_milestones.json', 'r') as f:
    milestones = json.load(f)

for m in milestones:
    print m['project']

print count_active_milestones(datetime.datetime(2014, 11, 25))
print count_issues(datetime.datetime(2014, 11, 25), milestones[0]['project'])
print count_issues(datetime.datetime(2014, 11, 25), milestones[0]['project'], 'open')
print count_issues(datetime.datetime(2014, 11, 25), milestones[0]['project'], 'closed')
print count_closed_delta(datetime.datetime(2014, 11, 25), milestones[0]['project'])


projects = [m['project'] for m in milestones]

with open('data/issues_closed.csv', 'w') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(['date'] + projects)
    date_from = find_min_date()
    date_to = find_max_date()
    for date in [
            date_from + datetime.timedelta(x + 1)
            for x in xrange((date_to - date_from).days)]:
        print date
        closed_delta = []
        for p in projects:
            print p
            closed_delta.append(count_closed_delta(date, p))
        csv_writer.writerow([date.strftime("%Y-%m-%d")] + closed_delta)
