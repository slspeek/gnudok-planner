https://github.com/lanyrd/mysql-postgresql-converter

```
mysqldump --compatible=postgresql --default-character-set=utf8 \
-r planner.mysql -u root -p djangoplanner
```

```
python db_converter.py planner.mysql planner.psql
```

```
psql -f planner.psql
```