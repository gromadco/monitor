populate_mongo:
	python populate_mongo.py

get_all_issues: 
	python get_all_issues.py

issues_closed: populate_mongo
	python create_issues_csv.py
