sudo -u postgres createuser --pwprompt --superuser planner
sudo -u postgres createdb -E UNICODE -O planner planner
sudo -u postgres createdb -E UNICODE -O planner test_planner
