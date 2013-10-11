#!/bin/bash
. ~/venv/bin/activate
~/venv/gnudok-planner/bin/django runfcgi host=127.0.0.1 port=8080

