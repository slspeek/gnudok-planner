bin/django graph_models -a > planner.dot
dot -Tsvg planner.dot -o planner.svg
