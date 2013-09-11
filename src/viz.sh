DJANGO_SETTINGS_MODULE=planner.settings ../bin/python modelviz.py area  > area.dot
DJANGO_SETTINGS_MODULE=planner.settings ../bin/python modelviz.py main  > main.dot
DJANGO_SETTINGS_MODULE=planner.settings ../bin/python modelviz.py nlpostalcode  > pc.dot
sed -i -s "s/&quot;.*&quot;/planner/g" area.dot main.dot pc.dot
dot -Tsvg pc.dot -o ../generated/pc.svg
dot -Tsvg area.dot -o ../generated/area.svg
dot -Tsvg main.dot -o ../generated/main.svg
